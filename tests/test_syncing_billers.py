"""
Syncing Billers
https://www.arcusfi.com/api/v3/#syncing-billers
"""

from regalii_certifier.models.base import Base
from regalii_certifier.certifications import syncing_billers


def create_tables():
    Base.metadata.create_all()


def drop_tables():
    Base.metadata.drop_all()


def test_syncing_billers():
    Base.metadata.create_all()
    syncing_billers.etl_billers()
    Base.metadata.drop_all()
