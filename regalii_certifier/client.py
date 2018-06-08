import os

from regalii.configuration import Configuration
from regalii.regaliator import Regaliator


API_KEY = os.environ['REGALII_API_KEY']
SECRET_KEY = os.environ['REGALII_SECRET_KEY']
HOST = 'api.casiregalii.com'
VERSION = '3.1'

config = Configuration(API_KEY, SECRET_KEY, HOST, version=VERSION)
client = Regaliator(config)


class RegaliiException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message


def create_bill(biller_id, account_number):
    params = dict(biller_id=biller_id, account_number=account_number)
    resp = client.bill.create(params=params)
    if resp.fail():
        data = resp.data()
        raise RegaliiException(data['code'], data['message'])
    bill = resp.data()
    return resp, bill


def pay_bill(bill_id, amount, currency):
    params = dict(amount=amount, currency=currency)
    resp = client.bill.pay(bill_id, params=params)
    if resp.fail():
        data = resp.data()
        raise RegaliiException(data['code'], data['message'])
    transaction = resp.data()
    return resp, transaction


def show_transaction(transaction_id):
    resp = client.transaction.request(
        f'/transactions?q[id_eq]={transaction_id}').get()
    transaction = resp.data()['transactions'][0]
    return resp, transaction


def cancel_transaction(transaction_id):
    req = client.transaction.request(
        '/transaction/cancel', params=dict(id=transaction_id))
    resp = req.post()
    cancellation = resp.data()
    return resp, cancellation
