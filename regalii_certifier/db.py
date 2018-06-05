import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


Session = scoped_session(sessionmaker())
engine = create_engine(os.environ['DATABASE_URI'])
metadata = MetaData(bind=engine)
