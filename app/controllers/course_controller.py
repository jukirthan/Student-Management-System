from flask import jsonify, request

from app.extensions import db
from app.models.course_model import Course
from app.models.lecturer_model import Lecturer

def _validate(data, course_id=None):
    errors = []

    if not data:
        return ["Request body is required."]


    course_id_value = data.get("course_id")
    if course_id_value:
        q = Course.query.filter(Course.course_id == course_id_value)
        if course_id:
            q = q.filter(Course.course_id != course_id)

        if q.first():
            errors.append("Course ID already exists.")


    course_code = data.get("course_code")
    if course_code:
        q = Course.query.filter(
            Course.course_code == str(course_code).strip()
        )

        if course_id:
            q = q.filter(Course.course_id != course_id)

        if q.first():
            errors.append("Course code already exists.")


    course_name = data.get("course_name", "")
    if len(str(course_name).strip()) < 3:
        errors.append("Course name is required.")


    credits = data.get("credits")
    try:
        credits = int(credits)
        if credits < 1 or credits > 6:
            errors.append("Credits must be between 1 and 6.")
    except (TypeError, ValueError):
        errors.append("Credits must be between 1 and 6.")


    lecturer_id = data.get("lecturer_id")
    try:
        lecturer = Lecturer.query.get(int(lecturer_id))
        if not lecturer:
            errors.append("Invalid lecturer selected.")
    except (TypeError, ValueError):
        errors.append("Invalid lecturer selected.")

    return errors