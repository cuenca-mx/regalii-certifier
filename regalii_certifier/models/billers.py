from sqlalchemy import Boolean, Column, Integer, JSON, String

from .base import Base


class Biller(Base):
    __tablename__ = 'billers'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    country = Column(String)
    currency = Column(String)
    biller_type = Column(String)
    bill_type = Column(String)
    required_parameters = Column(JSON)
    returned_parameters = Column(JSON)
    can_migrate = Column(Boolean)
    has_xdata = Column(Boolean)

    @classmethod
    def transform(cls, biller_dict):
        cols = set(cls.__table__.c.keys())
        biller = cls(**{col: biller_dict.get(col) for col in cols})
        return biller
