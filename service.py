from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text


@lru_cache()
def set_engine():
    engine = create_engine('postgresql://dmytro:qwerty@localhost:5432/postgres')

    return engine


@lru_cache()
def get_session(engine):
    session = Session(engine)

    return session
