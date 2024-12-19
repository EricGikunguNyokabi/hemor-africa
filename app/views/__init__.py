# views provide HTTP requests and providing responses. Routing and interaction with templates or APIs

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models.product import Product
from app.models.user import User
from app.models.employee import Employee

main = Blueprint('main', __name__)

# Home route: Display all products
@main.route("/")
def home():
    products = Product.query.all()  # Fetch all products from the database
    return render_template("home.html", products=products)

# Dashboard route: Fetch and display user and employee data along with products
@main.route("/dashboard")
# @login_required
def dashboard():
    # Since @login_required ensures the user is authenticated, we can directly use current_user
    user = current_user
    employee = None

    # Check if the current user is an employee
    if isinstance(user, Employee):
        employee = user
    else:
        # If the user is of type User, you might want to fetch the corresponding employee
        employee = Employee.query.filter_by(user_id=user.id).first()  # Adjust based on your Employee model

    products = Product.query.all()
    print(f"\nUser  in dashboard: {user}")
    print(f"\nEmployee in dashboard: {employee}")

    return render_template("home.html", products=products, user=user, employee=employee)