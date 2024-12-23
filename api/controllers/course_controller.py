from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import db, Course
from api.utils import role_required

course_bp = Blueprint('course', __name__)

# Create a new course
@course_bp.route('/create', methods=['POST'], endpoint='create_course')
@role_required('instructor')
def create_course():
    """
    Create a new course. Endpoint: POST /courses/create (Instructor only)
    Expects JSON:
    {
        "name": "Course Name",
        "description": "Course Description"
    }
    Response:
    {
        "message": "Course created successfully!"
    }
    """
    data = request.json
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({"message": "Invalid data provided"}), 400

    instructor_id = get_jwt_identity().get('id')
    course = Course(
        name=data['name'],
        description=data['description'],
        instructor_id=instructor_id
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({"message": "Course created successfully!"}), 201

# Get all courses
@course_bp.route('/list', methods=['GET'], endpoint='get_all_courses')
@jwt_required()
def get_courses():
    """
    Get all courses. Endpoint: GET /courses/list
    Response:
    [
        {
            "id": int,
            "name": "Course Name",
            "description": "Course Description"
        },
        ...
    ]
    """
    courses = Course.query.all()
    return jsonify([{
        "id": course.id,
        "name": course.name,
        "description": course.description
    } for course in courses]), 200

# Update a course
@course_bp.route('/update/<int:course_id>', methods=['PUT'], endpoint='update_course')
@role_required('instructor')
def update_course(course_id):
    """
    Update a course. Endpoint: PUT /courses/update/<course_id> (Instructor only)
    Expects JSON:
    {
        "name": "Updated Course Name",
        "description": "Updated Course Description"
    }
    Response:
    {
        "message": "Course updated successfully!"
    }
    """
    data = request.json
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    course.name = data.get('name', course.name)
    course.description = data.get('description', course.description)
    db.session.commit()
    return jsonify({"message": "Course updated successfully!"}), 200