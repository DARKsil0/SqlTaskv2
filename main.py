
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import CourseModel, StudentModel, GroupModel, Base
from service import set_engine, start_session



def insert_data_in_db():
    with Session(engine) as session:
        random_student = StudentModel(name='Dmytro', id=123, group_id=1, last_name = 'Katrych')
        random_course = CourseModel( id=456, name='Applied Math', description='Best way to suicide')
        random_group = GroupModel(id=987, name='Group 987', )
        session.add_all([random_group, random_course, random_student])
        session.commit()


if __name__ == '__main__':
    engine = set_engine()
    Base.metadata.create_all(engine)
    insert_data_in_db()
    session = start_session(engine)
    stmt = select(StudentModel).where(StudentModel.name == "Dmytro")
    with engine.connect() as conn:
        result = conn.execute(stmt)
        rows = result.fetchall()
        print(rows)
    engine.dispose()






