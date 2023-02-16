from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, create_engine, select, Integer, Table, Column
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import random
from random_data_creating import create_random_group, create_random_students


class Base(DeclarativeBase):

    pass


student_course_association = Table('student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('course_id', Integer, ForeignKey('course.id'))
)


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
    courses = relationship("CourseModel", secondary=student_course_association, back_populates="students")


class CourseModel(Base):
    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    students = relationship("StudentModel", secondary=student_course_association, back_populates="courses")