import json
import threading

from regalii_certifier import db
from regalii_certifier.client import client
from regalii_certifier.models import Biller


ENDPOINT = '/billers/credentials'


def get_page(page):
    endpoint = f'{ENDPOINT}?page={page}'
    return client.biller.request(endpoint).get()


def etl_biller_page(page):
    resp = get_page(page)
    for biller_dict in resp.data()['billers']:
        biller = Biller.transform(biller_dict)
        db.Session.add(biller)
    db.Session.commit()


def etl_billers():
    resp = client.biller.credentials()
    pages = json.loads(resp.pagination())['total_pages']
    threads = []
    for page in range(pages):
        thread = threading.Thread(target=etl_biller_page, args=(page,))
        thread.start()
        threads.append(thread)
