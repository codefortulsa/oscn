# OSCN utilities

A python library for scraping case information from the [Oklahoma State Courts Network](https://www.oscn.net/dockets/).

## Contents

oscn > Python package source to provide an api for retrieving and parsing case records.

scripts > Python scripts showing use of the oscn package
- example.py: demonstrates use of the request Case and Caselist
- retrieve-counts.py: saves a list of all counts for a list of counties and years
- find-counts.py: saves a list of counts passing a test for a list of counties and years
- soup_test.py: a stub for testing parsing attempts using BeautifulSoup
- parse_test.py: a stub for developing using saved examples


## OSCN package

### oscn

- counties: Returns a list of counties.
- courts: Same as counties but more a accurate description.


### oscn.request

- Case: Returns a single case.  Case can be saved as files using Case.save() and retrieved using Case.open().

- CaseList: Returns an iterator for retrieving cases for a county and year.

 CaseLists can be filtered using .find().  See scripts/example.py for details


### oscn.parse
Parsers accept the html of an OSCN case page and return python objects.
- filed: returns a string of the filing date (e.g. 12/25/2017)
- closed: returns a string of the date the case was closed.  Return None if not closed.
- counts: returns of list of count dicts found in a case.  Keys include 'description'
of the count. If available 'violation' and 'disposed' are added.
- judge: returns a string of the judge's name
- parties: returns a list of dicts with these keys: name, type
- docket: returns a list of rows in a docket
- events: returns a list of dicts with these keys: event, party, docket, reporter, date, description.  The keys date and description are cleaner versions of the event text.  The event key will be deprecation some day so use date and description if you are starting a project.
- attorneys: returns a list of dicts with these keys: name, address, and representing
- issues: returns a list of dicts with issue information. Each issues includes a list of dicts for each party 

### oscn.find (experimental)
Calls to the OSCN search application.

## Development Install

1. Create and activate a Python 3.6 virtual env
1. `git clone git@github.com:codefortulsa/oscn.git`
1. `cd oscn`
1. `pip install -e .`

## Usage

Install with `pip install oscn`

Script example:

`import oscn`

Request a single case:

`oscn.request.Case(county='tulsa', year='2018', number=84)`

or request a list of cases to iterate:

`oscn.request.CaseList(county='adair', year='2016')`

## Run test scripts

- `pytest tests/`

or with ipdb:

    - `py.test -s tests/`

## Deployment steps

1. `python3 setup.py sdist bdist_wheel`
1. `twine upload dist/*`
