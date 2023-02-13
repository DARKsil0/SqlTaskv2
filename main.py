from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class GroupModel(Base):
    __tablename__ = 'group'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))



class StudentModel(Base):
    __tablename__ = 'student'

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int]
    name: Mapped[str]
    last_name: Mapped[str]


class CourseModel(Base):
    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]


def set_engine():
    engine= create_engine("sqlite://")
    return engine


def insert_data_in_db():
    with Session(engine) as session:
        random_student = StudentModel(name='Dmytro', id=123, group_id = 1, last_name = 'Katrych')
        random_course = CourseModel( id=456, name='Applied Math', description='Best way to suicide')
        random_group = GroupModel(id=987, name='Group 987', )
        session.add_all([random_group, random_course, random_student])
        session.commit()


if __name__ == '__main__':
    engine = set_engine()
    Base.metadata.create_all(engine)
    insert_data_in_db()
    session = Session(engine)
    stmt = select(StudentModel).where(StudentModel.name == "Dmytro")
    with engine.connect() as conn:
        result = conn.execute(stmt)
        rows = result.fetchall()
        print(rows)





