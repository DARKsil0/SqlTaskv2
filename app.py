from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from flask_restful import Resource, Api, reqparse
from queries import get_students_assigned_on_course_by_given_name, get_groups_with_less_or_equal_student_count, add_new_student, delete_student_by_id\
    , add_student_to_course, remove_student_from_course
from service import set_engine, get_session


app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
engine = set_engine()


add_new_student_parser = reqparse.RequestParser()
add_new_student_parser.add_argument('name', type=str, help='Name of the student is required', required=True)
add_new_student_parser.add_argument('last_name', type=str, help='Last name of the student is required', required=True)

assign_student_on_courses_parser = reqparse.RequestParser()
assign_student_on_courses_parser.add_argument('courses', type=list, required=True, location='json')


specs_dict_get_courses = {
    "summary": "Get students assigned to a course",
    "description": "Returns a dictionary of students assigned to a course by given name.",
    "parameters": [
        {
            "name": "course_name",
            "description": "The name of the course to get the students assigned to.",
            "in": "path",
            "type": "string",
            "required": True
        }
    ],
    "responses": {
        200: {
            "description": "A dictionary of students assigned to the course by given name.",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "last name": {"type": "string"},
                            "group": {"type": "integer"}
                        }
                    }
                }
            }
        },
        404: {
            "description": "The course was not found."
        }
    }
}


specs_dict_get_groups_with_students = {
    'tags': ['Groups'],
    'description': 'Returns all groups with less or equal count of students than the specified number',
    'parameters': [
        {
            'name': 'count',
            'description': 'The maximum number of students allowed in each group',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'A dictionary containing group information',
            'schema': {
                'type': 'object',
                'properties': {
                    'group_id': {
                        'type': 'object',
                        'properties': {
                            'group name': {'type': 'string'},
                            'group id': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
}


specs_dict_post_add_new_student = {
    'tags': ['students'],
    'description': 'Add a new student to the database using a dictionary payload',
    'parameters': [
        {
            'name': 'student_data',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'The name of the student'},
                    'last_name': {'type': 'string', 'description': 'The last name of the student'}
                },
                'required': ['name', 'last_name']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'The student was successfully added to the database',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
}

specs_dict_delete_student_by_id = {
    "tags": ["students"],
    "description": "Deletes a student with the given ID.",
    "parameters": [
        {
            "name": "student_id",
            "description": "ID of the student to delete.",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "Student deleted successfully."
        },
        "404": {
            "description": "Student not found."
        },
        "500": {
            "description": "Internal server error occurred."
        }
    }
}


specs_dict_assign_student_on_courses = {
    'tags': ['Courses'],
    'description': 'Assigns courses to a student',
    'parameters': [
        {
            'name': 'student_id',
            'description': 'The ID of the student to assign courses to',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'course_ids',
            'description': 'A comma-separated list of course IDs to assign to the student',
            'in': 'formData',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'The courses were successfully assigned to the student',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
}

specs_dict_remove_student_from_course = {
    'tags': ['Courses'],
    'description': 'Remove a student from a course by student and course IDs.',
    'parameters': [
        {
            'name': 'student_id',
            'description': 'ID of the student to remove from the course.',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'course_id',
            'description': 'ID of the course from which to remove the student.',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Course successfully removed',
            'content': {
                'application/json': {
                    'example': {'message': 'Course with id 1 was successfully removed.'}
                }
            }
        }
    }
}



class GetStudentsCourses(Resource):

    @swag_from(specs_dict_get_courses )
    def get(self, course_name):
        session = get_session(engine)
        result = get_students_assigned_on_course_by_given_name(course_name, session)
        result_dict = {}
        for student in result:
            result_dict[student.id] = {'name': student.name,'last name': student.last_name,'id':student.id, 'group': student.group_id}

        session.close()

        return result_dict, 201


class GetGroupWithGivenNumbersStudents(Resource):

    @swag_from(specs_dict_get_groups_with_students)
    def get(self, count):
        session = get_session(engine)
        result = get_groups_with_less_or_equal_student_count(count,session)
        result_dict = {}
        for group in result:
            result_dict[group.id]={'group name': group.name, ' group id': group.id}

        session.close()
        return result_dict, 201


class AddNewStudent(Resource):
    @swag_from(specs_dict_post_add_new_student)
    def post(self):
        session = get_session(engine)

        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            last_name = data.get('last_name')
        else:
            args = add_new_student_parser.parse_args()
            name = args['name']
            last_name = args['last_name']

        add_new_student(name=name, last_name=last_name, session=session)

        session.commit()
        session.close()

        return {'message': 'The student was successfully added to the database'}, 201


class DeleteStudentById(Resource):

    @swag_from(specs_dict_delete_student_by_id)
    def delete(self, student_id):

        session = get_session(engine)
        delete_student_by_id(student_id, session)

        session.close()

        return {'message': f'Student with ID {student_id} deleted successfully.'}


class AssignedStudentOnCourses(Resource):

    @swag_from(specs_dict_assign_student_on_courses)
    def put(self, student_id):

        sesion = get_session(engine)
        args = assign_student_on_courses_parser.parse_args()
        add_student_to_course(student_id, args, sesion)


        sesion.close()

        return {'message': f'Courses added to student with ID {student_id} successfully.'}


class RemoveStudentFromCourse(Resource):

    @swag_from(specs_dict_remove_student_from_course)
    def delete(self, student_id, course_id):
        session = get_session(engine)
        remove_student_from_course(student_id, course_id, session)
        session.close()

        return {'message': f'Course with id {course_id} was successfully removed.'}


api.add_resource(GetStudentsCourses, '/courses/<string:course_name>/students')

api.add_resource(GetGroupWithGivenNumbersStudents, '/groups/<int:count>')

api.add_resource(AddNewStudent, '/students')

api.add_resource(DeleteStudentById, '/students/<int:student_id>')

api.add_resource(AssignedStudentOnCourses, '/students/<int:student_id>/courses')

api.add_resource(RemoveStudentFromCourse, '/students/<int:student_id>/courses/<int:course_id>')

if __name__ == '__main__':
    app.run(debug=True)