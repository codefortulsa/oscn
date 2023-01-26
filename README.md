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
- judges: Returns a list of objects formated as {'name': 'Bond, James', 'number': '007'}
- types: returns a dict of case type codes and descriptons
- type: function to return case type description. Usage:
  ```
  >>> oscn.type("AO")
  'CIVIL ADMINISTRATIVE'
  ```

### oscn.request

- Case: Returns a single case. Case can be saved as files using Case.save() and retrieved using Case.open().

- CaseList: Returns an iterator for retrieving cases for a county and year. CaseLists can be filtered using .find(). See scripts/example.py for details

- Party: Returns information on parties available on OSCN.

- Docket: Returns docket of cases for specific judges and date

### oscn.parse

Parsers accept the html of an OSCN page and return python objects.

#### Case Page Parsers

- filed: returns a string of the filing date (e.g. 12/25/2017)
- closed: returns a string of the date the case was closed. Return None if not closed.
- counts: returns of list of count dicts found in a case. Keys include 'description'
  of the count. If available 'violation' and 'disposed' are added.
- judge: returns a string of the judge's name
- parties: returns a list of dicts with these keys: id, name, type
- docket: returns a list of rows in a docket
- events: returns a list of dicts with these keys: event, party, docket, reporter, date, description. The keys date and description are cleaner versions of the event text. The event key will be deprecated some day so use date and description if you are starting a project.
- attorneys: returns a list of dicts with these keys: name, address, and representing
- issues: returns a list of dicts with issue information. Each issues includes a list of dicts for each party

#### Party Page Parsers

- name: returns 'Requested Party'
- alias: returns 'Alias or Alternate Names'
- profile: returns dict of values in 'Personal Profile'
- birth_month: returns string of 'Birth Month and Year'
- addresses: returns a list of dicts for each address

#### Docket Page Parsers

- cases: returns a list of case indexes
- tables: returns the html table for each case in the docket

### oscn.find

- CaseIndexes: returns an iterator of case indexes (e.g. tulsa-CF-2019-12).

#### Usage

Create a CaseIndexes list using these key word arguments:

- county: defaults to all,
- last_name: use this for company or organization names
- first_name: optional
- middle_name: optional
- filed_after: More readable than FiledDateL
- filed_before: More readable than FiledDateH
- closed_after: More readable than ClosedDateL
- closed_before: More readable than ClosedDateH

#### Notes

- The % wild card is added to all words in name, first and middle
- Date arguments use MM/DD/YYY strings.

#### OSCN search parameters

If you are familar with the OSCN search parameters you can initialize CaseIndexes using these as key word arguments: db, number, lname, fname, mname, DoBMin, DoBMax, partytype, apct, dcct, FiledDate, FiledDateH, ClosedDateL, ClosedDateH, iLC, iLCType, iYear, iNumber, and citation

Using this will override init keyword values such as first or filed_after.

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

or use case index notation:

`oscn.request.Case('love-CF-2019-25')`

To request a list of cases to iterate:

`oscn.request.CaseList(county='adair', year='2016')`

## Run test scripts

- `pytest tests/`

or with ipdb:

    - `pytest -s tests/`

specify a test:

- `pytest -s tests/test_parse.py -k 'test_events'`

## Deployment steps

1. `python3 setup.py sdist bdist_wheel`
1. `twine upload dist/*`

## User Agent

In some cases a custom user agent is required in the header of requests.
Setting an environmental varialbe called OSCN_USER_AGENT will override the default.
