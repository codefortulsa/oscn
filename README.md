# OSCN utilities

A python library for scraping case information from the [Oklahoma State Courts Network](https://www.oscn.net/dockets/).

## Contents

oscn > Python package source to provide an api for retrieving and parsing case records.

scripts > Python scripts showing use of the oscn package
- example.py: demostrates use of the request Case and Caselist
- retrieve-counts.py: saves a list of all counts for a list of counties and years
- find-counts.py: saves a list of counts passing a test for a list of counties and years
- soup_test.py: a stub for testing parsing attempts using BeautifulSoup
- parse_test.py: a stub for developing using saved examples


## OSCN package

### oscn

- counties: Returns a list of counties.


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
- parties: returns a list of objects that look like this: {'name': 'Some Name', 'type': 'Description'}
- docket: returns a list of rows in a docket
- events: returns a list of rows in the event table
- attorneys: returns a list of strings found in the attorney table
- issues: returns a list of dicts with issue information.  Includes a 'dispositions' key with a list of dicts with disposition details.

### oscn.find (experimental)
These functions use parse results to determine additional properties.
- pleas: returns a list of docket minutes containing pleas
- sentence: returns a list of docket minutes containing sentences


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

- `python scripts/{file.py}`

## Deployment steps

1. `python3 setup.py sdist bdist_wheel`
1. `twine upload dist/*`
