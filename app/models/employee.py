from app import db
from flask_login import UserMixin

class Employee(db.Model, UserMixin):
    __tablename__ = "employee"

    employee_id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String(50), default="employee")
    employee_status = db.Column(db.String(50), default="active")
    first_name = db.Column(db.String(255), nullable=False) 
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=False) 
    mobile_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    otp = db.Column(db.String(6), nullable=True)  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    otp_created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    employee_ratings = db.Column(db.Float, default=0.0)
    department = db.Column(db.String(100), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    employment_type = db.Column(db.String(50), default="full-time")
    login_count = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    shift_start = db.Column(db.Time, nullable=True)
    shift_end = db.Column(db.Time, nullable=True)

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"

    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    def get_id(self):
        return str(self.employee_id)  # Make sure this corresponds to the primary key

    # This method will map 'active' status to the 'is_active' functionality for Flask-Login
    @property
    def is_active(self):
        return self.employee_status == 'active'  # Define your own logic based on employee_status
    
    @property
    def is_authenticated(self):
        return True  # Always return True for authenticated users

    @property
    def is_anonymous(self):
        return False  # Always return False for authenticated users
