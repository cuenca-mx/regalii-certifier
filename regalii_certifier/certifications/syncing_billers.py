import json

from regalii_certifier import db
from regalii_certifier.client import client
from regalii_certifier.models import Biller


ENDPOINTS = ['utilities', 'topups', 'credentials']


def etl_from_endpoint(endpoint, page=1):
    resp = client.biller.request(f'/billers/{endpoint}?page={page}').get()
    for biller_dict in resp.data()['billers']:
        biller = Biller.transform(biller_dict)
        db.Session.add(biller)
    db.Session.commit()
    next_page = json.loads(resp.pagination())['next_page']
    if next_page:
        etl_from_endpoint(endpoint, next_page)


def etl_billers():
    for endpoint in ENDPOINTS:
        etl_from_endpoint(endpoint)


def verify_biller_count():
    total_entries = 0
    for endpoint in ENDPOINTS:
        resp = client.biller.request(f'/billers/{endpoint}').get()
        total_entries += json.loads(resp.pagination())['total_entries']
    local_count = Biller.query.count()
    assert local_count == total_entries
