
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text


def set_engine():
    #engine = create_engine('postgresql://username:password@host:5000/database')
    engine = create_engine('postgresql://postgres:4756Figur@localhost:5432/postgres')


    with engine.connect() as conn:


        conn.execute(text("CREATE USER newuser WITH PASSWORD '123456'"))
        conn.execute(text("GRANT ALL PRIVILEGES ON DATABASE postgres TO newuser"))
        result = conn.execute(text("SELECT usename FROM pg_user;"))
        users = [row[0] for row in result]
        if 'newuser' in users:
            print('User created successfully')

        # Check if the user has the expected privileges
        result = conn.execute(text(
            "SELECT usename, datname, has_database_privilege(usename, datname, 'CREATE') AS can_create_database, has_database_privilege(usename, datname, 'CONNECT') AS can_connect FROM pg_user, pg_database;"))
        for row in result:
            if row[0] == 'newuser' and row[1] == 'postgres' and row[2] and row[3]:
                print('User has all privileges')
    return engine


def start_session(engine):
    session = Session(engine)
    return session
