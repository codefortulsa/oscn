OSCN_URL = "https://www.oscn.net/dockets/GetCaseInformation.aspx"
DOCKET_FORM_URL = "https://www.oscn.net/dockets/"
INVALID_CASE_MESSAGES = [
    "Case Number is Invalid",
    "Something went wrong",
    "is formatted incorrectly or is not found within"
    ]
UNUSED_CASE_MESSAGES = ['THIS CASE NUMBER WAS NOT USED',]

# How many empty cases in a row to decide we're at the end of the case list?
MAX_EMPTY_CASES = 10
