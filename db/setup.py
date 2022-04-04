import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def init():
    conn = f'postgresql+psycopg2://{os.getenv("PS_NAME")}:{os.getenv("PS_PASS")}' \
           f'@{os.getenv("PS_HOST")}/{os.getenv("PS_DB")}'
    engine = create_engine(
        conn,
        pool_pre_ping=True)
    Base.metadata.create_all(engine, checkfirst=True)
    return engine
