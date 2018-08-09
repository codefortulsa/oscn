OSCN_URL = "https://www.oscn.net/dockets/GetCaseInformation.aspx"
DOCKET_FORM_URL = "https://www.oscn.net/dockets/"
INVALID_CASE_MESSAGES = [
    "Case Number is Invalid",
    ]
UNUSED_CASE_MESSAGES = [
    "Something went wrong",
    'THIS CASE NUMBER WAS NOT USED',
    "is formatted incorrectly or is not found within",
    ]

# How many empty cases in a row to decide we're at the end of the case list?
MAX_EMPTY_CASES = 10
