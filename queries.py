from models import GroupModel, StudentModel, CourseModel
from sqlalchemy import select, MetaData, Table, func


def get_groups_with_less_or_equal_student_count(count, session):
    result = session.query(GroupModel). \
        outerjoin(GroupModel.students). \
        group_by(GroupModel.id). \
        having(func.count(StudentModel.id) <= count). \
        all()
    return result


def get_students_assigned_on_course_by_given_name(course, session):
    course = session.query(CourseModel).group_by(CourseModel.id).where(CourseModel.name == course).all()
    result = course.students

    return result


def add_new_student(name, lastname, session):
    session = session

    new_student = StudentModel(name=name, lastname=lastname)

    session.add(new_student)
    session.commit()


def delete_student_by_id(id, session):
    session = session
    record = session.query(StudentModel).get(id)
    session.delete(record)


def add_student_to_course(student_id, list_of_courses, session):
    session = session
    for course_id in list_of_courses:
        course = session.query(CourseModel).where(CourseModel.id == course_id).one()
        student = session.query(StudentModel).where(StudentModel.id == student_id).one()
        student.courses.append(course)

    session.commit()


def remove_student_from_course(student_id, course_id, session):
    course = session.query(CourseModel).where(CourseModel.id == course_id).one()
    student = session.query(StudentModel).where(StudentModel.id == student_id).one()
    student.courses.remove(course)
    session.commit()
