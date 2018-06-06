from regalii_certifier.client import client


def test_create_with_credentials():
    """https://www.arcusfi.com/api/v3/#linking-bill-credentials"""
    params = dict(biller_id=6500, login='user', password='letmein')
    resp = client.bill.create(params=params)
    assert resp.response.status_code == 200
    bill = resp.data()
    assert bill['id']
    assert bill['status'] == 'linked'


def test_create_by_account_number():
    """https://www.arcusfi.com/api/v3/#linking-bill-creation"""
    params = dict(biller_id=8925, login='user', account_number='1234567')
    resp = client.bill.create(params=params)
    assert resp.response.status_code == 200
    bill = resp.data()
    assert bill['id']
    assert bill['status'] == 'linked'


def test_create_bill_and_wait():
    """https://www.arcusfi.com/api/v3/#linking-bill-slow"""
    params = dict(biller_id=6500, login='slow', password='slow')
    resp = client.bill.create(params=params)
    assert resp.response.status_code == 202
    bill = resp.data()
    assert bill['status'] == 'fetching'
    while bill['status'] == 'fetching':
        resp = client.bill.show(bill['id'])
        bill = resp.data()
    assert resp.response.status_code == 200
    assert bill['status'] == 'linked'


def test_create_with_mfa_question():
    """https://www.arcusfi.com/api/v3/?ruby#linking-bill-mfa-question"""
    params = dict(biller_id=6500, login='user', password='challengeme')
    resp = client.bill.create(params=params)
    assert resp.response.status_code == 201
    bill = resp.data()
    assert bill['status'] == 'mfa'

    mfa_challenge = bill['mfa_challenges'][0]
    mfa_response = dict(
        id=mfa_challenge['id'],
        type=mfa_challenge['type'],
        response='8')
    resp = client.bill.update(
        bill['id'], params=dict(mfa_challenges=[mfa_response]))
    assert resp.response.status_code == 200
    bill = resp.data()
    assert bill['status'] == 'linked'


def test_create_with_mfa_code():
    """https://www.arcusfi.com/api/v3/?ruby#linking-bill-mfa-code"""
    params = dict(biller_id=6500, login='user', password='codeme')
    resp = client.bill.create(params=params)
    assert resp.response.status_code == 201
    bill = resp.data()
    assert bill['status'] == 'mfa'

    mfa_challenge = bill['mfa_challenges'][0]
    mfa_response = dict(
        id=mfa_challenge['id'],
        type=mfa_challenge['type'],
        response='4')
    resp = client.bill.update(
        bill['id'], params=dict(mfa_challenges=[mfa_response]))
    assert resp.response.status_code == 200
    bill = resp.data()
    assert bill['status'] == 'linked'


def test_invalid_credentials():
    """https://www.arcusfi.com/api/v3/?ruby#linking-bill-invalid-credentials"""
    params = dict(biller_id=6500, login='credentials', password='credentials')
    resp = client.bill.create(params=params)
    assert resp.response.status_code == 422


def test_refreshing_a_bill():
    """https://www.arcusfi.com/api/v3/?ruby#refreshing-a-bill"""
    params = dict(biller_id=6500, login='user', password='letmein')
    resp = client.bill.create(params=params)
    bill = resp.data()

    resp = client.bill.refresh(bill['id'])
    assert resp.response.status_code == 200
    refreshed_bill = resp.data()
    assert bill['balance'] != refreshed_bill['balance']


def test_getting_xdata():
    """https://www.arcusfi.com/api/v3/?ruby#getting-xdata"""
    params = dict(biller_id=6500, login='user_xdata', password='letmein')
    resp = client.bill.create(params=params)
    assert resp.response.status_code == 200
