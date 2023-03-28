from queries import get_groups_with_less_or_equal_student_count, get_students_assigned_on_course_by_given_name, add_student_to_course, add_new_student, delete_student_by_id, remove_student_from_course
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import Session
from models import CourseModel, StudentModel, GroupModel, Base, student_course_association
import pytest


engine = create_engine('postgresql://dmytro:qwerty@localhost:5432/test_db')

Base.metadata.create_all(engine)


def test_1():
    session = Session(engine)
    student_1 = StudentModel(name='Dmytro', last_name='Katrych')
    student_2 = StudentModel(name='Oleksandr', last_name='Katrych')
    student_3 = StudentModel(name='Albert', last_name='Katrych')
    student_4 = StudentModel(name='Mykyta', last_name='Katrych')
    course = CourseModel(name='math', description='Learn the fundamentals of mathematics and problem-solving skills.')
    session.add_all([student_1, student_4, student_3, student_2, course])

    try:


        students = session.query(StudentModel).all()
        course = session.query(CourseModel).one()
        for student in students:
            student.courses.append(course)

        result = get_students_assigned_on_course_by_given_name('math', session)
        assert len(result) == 4

    finally:

        session.rollback()
        print('Finish')




if __name__ == '__main__':

    pytest.main()