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


def create_lecturer():
    data = request.get_json() or {}
    errors = _validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    lecturer = Lecturer(
        first_name=str(data.get("first_name")).strip(),
        last_name=str(data.get("last_name")).strip(),
        email=str(data.get("email")).strip(),
        department=str(data.get("department")).strip(),
    )

    db.session.add(lecturer)
    db.session.commit()
    return jsonify(lecturer.to_dict()), 201


def get_lecturers():
    lecturers = Lecturer.query.all()
    return jsonify([lecturer.to_dict() for lecturer in lecturers])


def get_lecturer(lecturer_id):
    lecturer = Lecturer.query.get(lecturer_id)
    if not lecturer:
        return jsonify({"error": "Lecturer not found."}), 404
    return jsonify(lecturer.to_dict())


def update_lecturer(lecturer_id):
    lecturer = Lecturer.query.get(lecturer_id)
    if not lecturer:
        return jsonify({"error": "Lecturer not found."}), 404

    data = request.get_json() or {}
    errors = _validate(data, lecturer_id=lecturer_id)
    if errors:
        return jsonify({"errors": errors}), 400

    lecturer.first_name = str(data.get("first_name")).strip()
    lecturer.last_name = str(data.get("last_name")).strip()
    lecturer.email = str(data.get("email")).strip()
    lecturer.department = str(data.get("department")).strip()

    db.session.commit()
    return jsonify(lecturer.to_dict())


def delete_lecturer(lecturer_id):
    lecturer = Lecturer.query.get(lecturer_id)
    if not lecturer:
        return jsonify({"error": "Lecturer not found."}), 404

    db.session.delete(lecturer)
    db.session.commit()
    return jsonify({"message": "Lecturer deleted successfully."})