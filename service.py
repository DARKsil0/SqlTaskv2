
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def set_engine():
    #engine = create_engine('postgresql://username:password@host:5000/database')
    engine = create_engine('sqlite://')

    # with engine.connect() as conn:
    #     conn.execute("CREATE USER newuser WITH PASSWORD 'newpassword'")
    #     conn.execute("GRANT ALL PRIVILEGES ON DATABASE database TO newuser")
    return engine


def start_session(engine):
    session = Session(engine)
    return session
