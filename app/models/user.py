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
    otp = db.Column(db.String(6), nullable=True)  
    otp_created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
    account_status = db.Column(db.String(20), default="active")

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.email})>"

    def full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()

    def add_points(self, points):
        self.points += points

    def update_total_purchases(self, amount):
        self.total_purchases += amount

    # Flask-Login compatibility
    def get_id(self):
        return str(self.user_id)

    @property
    def is_active(self):
        return self.account_status == 'active'  # Custom logic for active status

    @property
    def is_authenticated(self):
        return True  # For simplicity, all users are considered authenticated (depends on logic)

    @property
    def is_anonymous(self):
        return False  # For simplicity, all users are considered authenticated
