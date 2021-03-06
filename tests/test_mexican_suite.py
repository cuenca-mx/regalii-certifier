import pytest

from regalii_certifier.client import (
    cancel_transaction, create_bill, pay_bill, show_transaction,
    RegaliiException)


def test_create_bill():
    resp, bill = create_bill(40, '501000000007')
    assert resp.response.status_code == 200
    assert bill['id']
    assert bill['status'] == 'linked'


def test_failure_wrong_account_number():
    with pytest.raises(RegaliiException) as excinfo:
        create_bill(40, '501000000004')
    err = excinfo.value
    assert err.code == 'R2'
    assert err.message == 'Invalid Account Number'


def test_successful_payment():
    _, bill = create_bill(40, '501000000007')
    resp, transaction = pay_bill(
        bill['id'], bill['balance'], bill['balance_currency'])
    assert resp.response.status_code == 201
    assert transaction['id']
    assert transaction['status'] == 'fulfilled'


def test_unexpected_error():
    with pytest.raises(RegaliiException) as excinfo:
        create_bill(6900, '1111362009')
    err = excinfo.value
    assert err.code == 'R9'
    assert err.message.startswith('Unexpected error')


def test_cancel_bill():
    _, bill = create_bill(35, '123456851236')
    _, transaction = pay_bill(
        bill['id'], bill['balance'], bill['balance_currency'])
    resp, cancellation = cancel_transaction(transaction['id'])
    assert resp.response.status_code == 200
    assert cancellation['code'] == 'R0'
    assert cancellation['message'] == 'Transaction successful'

    resp, updated_transaction = show_transaction(transaction['id'])
    assert resp.response.status_code == 200
    assert updated_transaction['id'] == transaction['id']
    assert updated_transaction['status'] == 'refunded'


def test_consult_error():
    """Similar to unexpected error"""
    with pytest.raises(RegaliiException) as excinfo:
        create_bill(2901, '1111322016')
    err = excinfo.value
    assert err.code == 'R16'
    assert err.message == 'Failed to make the consult, please try again later'


def test_biller_maintenance():
    with pytest.raises(RegaliiException) as excinfo:
        create_bill(1821, '1111992022')
    err = excinfo.value
    assert err.code == 'R22'
    assert err.message == (
        'Biller maintenance in progress, please try again later')


def test_timeout_on_payment():
    _, bill = create_bill(37, '2424240024')
    with pytest.raises(RegaliiException) as excinfo:
        pay_bill(bill['id'], bill['balance'], bill['balance_currency'])
    err = excinfo.value
    assert err.code == 'R24'
    assert err.message == 'Timeout from biller'
