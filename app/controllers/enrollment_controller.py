from datetime import datetime

from flask import jsonify, request

from app.extensions import db
from app.models.enrollment_model import Enrollment, VALID_STATUSES
from app.models.student_model import Student
from app.models.course_model import Course


def _validate(data, enrollment_id=None):
    errors = []

    if not data:
        return ["Request body is required."]

    enrollment_id_value = data.get("enrollment_id")
    if enrollment_id_value:
        q = Enrollment.query.filter(
            Enrollment.enrollment_id == enrollment_id_value
        )

        if enrollment_id:
            q = q.filter(
                Enrollment.enrollment_id != enrollment_id
            )

        if q.first():
            errors.append("Enrollment ID already exists.")

    student_id = data.get("student_id")
    if not student_id or not Student.query.get(student_id):
        errors.append("Invalid student selected.")

    course_id = data.get("course_id")
    if not course_id or not Course.query.get(course_id):
        errors.append("Invalid course selected.")

    enrollment_date = data.get("enrollment_date")
    if not enrollment_date:
        errors.append("Enrollment date is required.")
    else:
        try:
            datetime.strptime(enrollment_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Enrollment date is required.")

    status = data.get("status")
    if status not in ["active", "completed", "dropped"]:
        errors.append("Invalid enrollment status.")

    return errors