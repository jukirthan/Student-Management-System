from app.extensions import db
from app.utils import utc_now


class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
   

    

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_of_birth": self.date_of_birth
        }
