from regalii_certifier import db
from regalii_certifier.client import client
from regalii_certifier.models import Biller


ENDPOINT = '/billers/credentials'


def _get_page(page):
    endpoint = f'{ENDPOINT}?page={page}'
    return client.biller.request(endpoint).get()


def etl_billers():
    billers = _get_page(1).data()
    for biller_dict in billers['billers']:
        biller = Biller.transform(biller_dict)
        db.Session.add(biller)
    db.Session.commit()
