"""
Syncing Billers
https://www.arcusfi.com/api/v3/#syncing-billers
"""
import json

from regalii_certifier.client import client
from regalii_certifier.models import Biller
from regalii_certifier.models.base import Base
from regalii_certifier.certifications import syncing_billers


def get_total_billers():
    total_entries = 0
    for endpoint in syncing_billers.ENDPOINTS:
        resp = client.biller.request(f'/billers/{endpoint}').get()
        total_entries += json.loads(resp.pagination())['total_entries']
    return total_entries


def test_syncing_billers():
    Base.metadata.drop_all()
    Base.metadata.create_all()
    syncing_billers.etl_billers()
    assert get_total_billers() == Biller.query.count()
