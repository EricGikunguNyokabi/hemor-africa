from sqlalchemy.orm import joinedload
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String(50), default="customer")
    first_name = db.Column(db.String(255), nullable=True)
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    mobile_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    account_status = db.Column(db.String(20), default="active")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    otp = db.Column(db.String(6), nullable=True)  
    otp_created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    total_purchases = db.Column(db.Float, default=0.0)
    points = db.Column(db.Integer, default=0)
    loyalty_tier = db.Column(db.String(50), default="Bronze")

    shipping_address = db.Column(db.String(255), nullable=True)
    billing_address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)

    subscription_status = db.Column(db.Boolean, default=False)
    notify_promotions = db.Column(db.Boolean, default=True)

    last_login = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, nullable=True)
    
    # Relationship with Employee
    employee = db.relationship("Employee", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.mobile_no}>"

    def full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()

    def get_id(self):
        return str(self.user_id)

    @property
    def is_active(self):
        return self.account_status == "active"

class Employee(db.Model):
    __tablename__ = "employee"
    employee_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = db.relationship("User", back_populates="employee")
    employee_status = db.Column(db.String(50), default="active")
    department = db.Column(db.String(100), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    shift_start = db.Column(db.Time, nullable=True)
    shift_end = db.Column(db.Time, nullable=True)

    def __repr__(self):
        if self.user:
            return f"<Employee {self.user.first_name} {self.user.last_name}>"
        else:
            return "<Employee No User Associated>"




