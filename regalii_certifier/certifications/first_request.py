from regalii_certifier.client import client


def get_account_balance():
    resp = client.account.info()
    assert resp.response.status_code == 200
    account_balance = float(resp.data()['balance'])
    return account_balance
