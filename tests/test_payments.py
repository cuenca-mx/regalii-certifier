"""
Payments
https://www.arcusfi.com/api/v3/#payments-optional
"""
from regalii_certifier.client import client, create_bill


def test_payments():
    resp, bill = create_bill(40, '501000000007')
    assert resp.response.status_code == 200
    assert bill['id']
    assert bill['status'] == 'linked'

    params = dict(amount=bill['balance'], currency=bill['balance_currency'])
    resp = client.bill.pay(bill['id'], params=params)
    assert resp.response.status_code == 201
    transaction = resp.data()
    assert transaction['id']
    assert transaction['status'] == 'fulfilled'
