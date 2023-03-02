import random
from sqlalchemy import select, MetaData, Table
from sqlalchemy.sql import text

from models import CourseModel, StudentModel, GroupModel, Base, student_course_association
from service import set_engine, get_session
from random_data_creating import create_random_group, create_random_students, create_random_courses


def insert_data_in_db():
    session = get_session(engine)
    random_student = StudentModel(name='Dmytro', id=12, group_id=1, last_name = 'Katrych')
    random_course = CourseModel( id=45, name='Applied Math', description='Best way to suicide')
    random_group = GroupModel(id=97, name='Group 987' )
    session.add_all([random_group, random_course, random_student])
    session.commit()


def add_randomgroups_to_db():
    session = get_session(engine)
    for group in create_random_group():
        new_group = GroupModel(name=group)
        session.add_all([new_group])
    session.commit()


def add_random_students_to_db():
    session = get_session(engine)

    # Retrieve existing groups from the database
    groups = session.query(GroupModel).all()

    # Assign each student to a randomly selected group
    for name, lastname in create_random_students():
        group = random.choice(groups)
        new_student = StudentModel(groups=group, name=name, last_name=lastname)
        session.add(new_student)

    session.commit()


def add_courses_to_db():
    session = get_session(engine)
    for course in create_random_courses():
        new_course = CourseModel(name=course['name'], description=course['description'])
        session.add_all([new_course])
    session.commit()


def assign_students_to_courses():
    session = get_session(engine)
    students = session.query(StudentModel).all()
    courses = session.query(CourseModel).all()
    for student in students:
        num_courses = random.randint(1, 3)
        for i in range(num_courses):
            course = random.choice(courses)
            student.courses.append(course)
    session.commit()


def get_courses_with_students():
    session = get_session(engine)
    courses = session.query(CourseModel).all()
    course_student_list = []
    for course in courses:
        student_list = [student.name for student in course.students]
        course_student_list.append([course.name] + student_list)
    return course_student_list


if __name__ == '__main__':
    engine = set_engine()
    Base.metadata.create_all(engine)
    # GroupModel.__table__.drop(engine)
    # StudentModel.__table__.drop(engine)
    #
    # Base.metadata.create_all(engine)
    #insert_data_in_db()
    add_randomgroups_to_db()
    add_random_students_to_db()
    add_courses_to_db()
    assign_students_to_courses()
    session = get_session(engine)
    students_with_groups = session.query(StudentModel, GroupModel) \
        .join(GroupModel, StudentModel.group_id == GroupModel.id) \
        .all()
    for student, group in students_with_groups:
        print(f"{student.name} {student.last_name} is in group {group.name}")
    print(get_courses_with_students())





    # with engine.connect() as conn:
    #
    #     conn.execute(text("CREATE USER dmytro WITH PASSWORD 'qwerty'"))
    #     conn.execute(text("GRANT ALL PRIVILEGES ON DATABASE postgres TO dmytro"))
    # with engine.connect() as conn:
    #     result = conn.execute(stmt)
    #     rows = result.fetchall()
    #     print(rows)
    #



    engine.dispose()



