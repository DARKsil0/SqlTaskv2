import random
from sqlalchemy import select, MetaData, Table, func
from sqlalchemy.sql import text
import os
from models import CourseModel, StudentModel, GroupModel, Base, student_course_association
from service import set_engine, get_session
from random_data_creating import create_random_group, create_random_students, create_random_courses
from cli import cli
from queries import get_groups_with_less_or_equal_student_count, add_student_to_course, remove_student_from_course


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
        session.add(new_group)
    session.commit()


def add_random_students_to_db():
    session = get_session(engine)

    groups = session.query(GroupModel).all()

    for name, lastname in create_random_students():
        group = random.choice(groups)
        new_student = StudentModel(group=group, group_id=group.id, name=name, last_name=lastname)
        session.add(new_student)

    session.commit()


def add_courses_to_db():
    session = get_session(engine)
    for course in create_random_courses():
        new_course = CourseModel(name=course['name'], description=course['description'])
        session.add(new_course)
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


def main():
    session = get_session(engine)
    if os.environ.get("TERM") is not None:
        args = cli()
        if args.random:
            add_randomgroups_to_db()
            add_random_students_to_db()
            add_courses_to_db()
            assign_students_to_courses()
        if args.find:
            if args.find == 'student':
                if args.id:
                    student = session.query(StudentModel).filter_by(id=args.id).first()
                    print(student.name, student.id, student.group)
                    return student
                elif args.name:
                    student = session.query(StudentModel).filter_by(name=args.name).first()
                    print(student.name, student.id, student.group)
                    return student

            elif args.find == 'group':
                if args.id:
                    group = session.query(GroupModel).filter_by(id=args.id).first()
                    print(group.name, group.id)
                    return group
                elif args.name:
                    group = session.query(GroupModel).filter_by(name=args.name).first()
                    print(group.name, group.id)
                    return group

            if args.find == 'course':
                if args.id:
                    course = session.query(CourseModel).filter_by(id=args.id).first()
                    print(course.name, course.id, course.description)
                    return course
                elif args.name:
                    course  = session.query(CourseModel).filter_by(name=args.name).first()
                    print(course.name, course.id, course.description)
                    return course

        elif args.delete:
            if args.delete == 'student':
                if args.id:
                    record = session.query(StudentModel).get(args.id)
                    session.delete(record)

                elif args.name:
                    record = session.query(StudentModel).get(args.name)
                    session.delete(record)
            elif args.delete == 'group':
                if args.id:
                    record = session.query(GroupModel).get(args.id)
                    session.delete(record)
                elif args.name:
                    record = session.query(GroupModel).get(args.name)
                    session.delete(record)
            if args.delete == 'course':
                if args.id:
                    record = session.query(CourseModel).get(args.id)
                    session.delete(record)
                elif args.name:
                    record = session.query(CourseModel).get(args.name)
                    session.delete(record)
        session.commit()
    else:
        print('Functionality is developing')


if __name__ == '__main__':
    engine = set_engine()
    Base.metadata.create_all(engine)
    main()
    session = get_session(engine)


    engine.dispose()



