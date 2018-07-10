# OSCN Query utilities

This is a collection of python utilities to scrape case information from the [Oklahoma Supreme Court Network](https://www.oscn.net/dockets/).

## Contents

oscn > This is python package to provide an api for retrieving and parsing case records.

examples > Source HTML files for testing

scripts > Python scripts showing use of the oscn package
- retrieve-counts.py: saves a list of all counts for a list of counties and years
- find-counts.py: saves a list of counts passing a test for a list of counties and years
- soup_test.py: a stub for testing parsing attempts
using BeautifulSoup

## OSCN package

### oscn.request

- Case: Returns a single case.
- CaseList: Returns an iterator for retrieving cases for a county and year.

### oscn.parse

- counts: Returns of list of counts found in a case

## Install

1. Create a Python 3.7 virtual env
1. `git clone git@github.com:codefortulsa/oscn-query.git`
1. `cd oscn-query`
1. `pip install -r requirements.txt`
