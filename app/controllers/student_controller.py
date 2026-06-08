import re
from datetime import datetime
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