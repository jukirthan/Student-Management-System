from flask import jsonify, request

from app.extensions import db
from app.models.lecturer_model import Lecturer


def _validate(data, lecturer_id=None):
    errors = []

    if not data:
        return ["Request body is required."]


    lecturer_id_value = data.get("lecturer_id")
    if lecturer_id_value:
        q = Lecturer.query.filter(
            Lecturer.lecturer_id == lecturer_id_value
        )

        if lecturer_id:
            q = q.filter(Lecturer.lecturer_id != lecturer_id)

        if q.first():
            errors.append("Lecturer ID already exists.")


    first_name = data.get("first_name", "")
    if not str(first_name).strip().isalpha():
        errors.append("Lecturer first name is required.")


    last_name = data.get("last_name", "")
    if not str(last_name).strip().isalpha():
        errors.append("Lecturer last name is required.")


    email = data.get("email", "")

    if not email or "@" not in str(email):
        errors.append("Invalid lecturer email address.")
    else:
        q = Lecturer.query.filter(
            Lecturer.email == str(email).strip()
        )

        if lecturer_id:
            q = q.filter(Lecturer.lecturer_id != lecturer_id)

        if q.first():
            errors.append("Invalid lecturer email address.")

    department = data.get("department", "")
    if not str(department).strip():
        errors.append("Department is required.")

    return errors