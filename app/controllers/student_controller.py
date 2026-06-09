import re
from datetime import datetime
from flask import jsonify, request
from app.extensions import db
from app.models.student_model import Student


def validate_student(data):
    errors = []

    first_name = data.get("first_name", "").strip()
    if not first_name:
        errors.append("First name is required.")
    elif not re.fullmatch(r"[A-Za-z]{2,50}", first_name):
        errors.append("First name must contain only letters.")


    last_name = data.get("last_name", "").strip()
    if not last_name:
        errors.append("Last name is required.")
    elif not re.fullmatch(r"[A-Za-z]{2,50}", last_name):
        errors.append("Last name must contain only letters.")

    email = data.get("email")

    if not email:
        errors.append("Email is required")
    elif "@" not in email or "." not in email:
        errors.append("Please enter a valid email address")


  
    dob = data.get("date_of_birth")

    if not dob:
        errors.append("Date of birth is required")
    else:
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()

            if dob_date >= datetime.today().date():
                errors.append("Date of birth cannot be a future date")

        except:
            errors.append("Invalid date format. Use YYYY-MM-DD")

    return errors


def create_student():
    data = request.get_json() or {}
    errors = validate_student(data)
    if errors:
        return jsonify({"errors": errors}), 400

    student = Student(
        full_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        date_of_birth=datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d").date(),
    )

    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])


def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    return jsonify(student.to_dict())


def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404

    data = request.get_json() or {}
    errors = validate_student(data)
    if errors:
        return jsonify({"errors": errors}), 400

    student.full_name = data.get("first_name")
    student.last_name = data.get("last_name")
    student.email = data.get("email")
    student.date_of_birth = datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d").date()

    db.session.commit()
    return jsonify(student.to_dict())


def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully."})