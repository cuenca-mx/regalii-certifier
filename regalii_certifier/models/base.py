from sqlalchemy.ext.declarative import declarative_base

from regalii_certifier.db import metadata, Session


Base = declarative_base(metadata=metadata)
Base.query = Session.query_property()
