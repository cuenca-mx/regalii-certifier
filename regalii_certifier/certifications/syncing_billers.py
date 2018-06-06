from regalii_certifier import db
from regalii_certifier.client import client
from regalii_certifier.models import Biller


def etl_billers():
    resp = client.biller.credentials()
    for biller_dict in resp.data()['billers']:
        biller = Biller.transform(biller_dict)
        db.Session.add(biller)
    db.Session.commit()
