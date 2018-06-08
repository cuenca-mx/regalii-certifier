import pytest

from regalii_certifier.client import create_bill, RegaliiException


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
