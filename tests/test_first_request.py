"""
Authentication + First Request
https://www.arcusfi.com/api/v3/#authentication--first-request
"""
from regalii_certifier.certifications import first_request


def test_first_request():
    balance = first_request.get_account_balance()
    assert type(balance) is float
