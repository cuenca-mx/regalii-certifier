import pytest

from regalii_certifier.client import (
    cancel_transaction, create_bill, pay_bill, RegaliiException)


def test_failure_wrong_account_number():
    with pytest.raises(RegaliiException) as excinfo:
        create_bill(40, '501000000004')
    err = excinfo.value
    assert err.code == 'R2'
    assert err.message == 'Invalid Account Number'


def test_unexpected_error():
    with pytest.raises(RegaliiException) as excinfo:
        create_bill(6900, '1111362009')
    err = excinfo.value
    assert err.code == 'R9'
    assert err.message.startswith('Unexpected error')


def test_cancel_bill():
    _, bill = create_bill(35, '123456851236')
    _, transaction = pay_bill(bill)
    resp, cancellation = cancel_transaction(transaction['id'])
    assert resp.response.status_code == 200
    assert cancellation['code'] == 'R0'
    assert cancellation['message'] == 'Transaction successful'
