"""
Payments
https://www.arcusfi.com/api/v3/#payments-optional
"""
from regalii_certifier.client import client


def test_payments():
    params = dict(biller_id=6500, login='user', password='letmein')
    resp = client.bill.create(params=params)
    assert resp.response.status_code == 200
    bill = resp.data()
    assert bill['id']
    assert bill['status'] == 'linked'

    params = dict(amount=bill['balance'], currency=bill['balance_currency'])
    resp = client.bill.pay(bill['id'], params=params)
    assert resp.response.status_code == 201
    transaction = resp.data()
    assert transaction['id']
    assert transaction['status'] == 'sent'
