"""
Authentication + First Request
https://www.arcusfi.com/api/v3/#authentication--first-request
"""
from regalii_certifier.client import client


def test_first_request():
    resp = client.account.info()
    assert resp.response.status_code == 200
    account_balance = float(resp.data()['balance'])
    assert type(account_balance) is float
