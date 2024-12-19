from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.models.employee import Employee
from app import db
from app.forms.auth import EmployeeRegistrationForm  # Import the registration form

employee = Blueprint("employee", __name__)

@employee.route("/emp/register", methods=["GET", "POST"])
def register():
    form = EmployeeRegistrationForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        mobile_no = form.mobile_no.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Process mobile number formatting
        if mobile_no.startswith("0"):
            mobile_no = "254" + mobile_no[1:]  # Remove leading zero and prepend '254'

        # Check if email or mobile number already exists
        existing_user = Employee.query.filter((Employee.email == email) | (Employee.mobile_no == mobile_no)).first()
        if existing_user:
            flash("Email or Mobile number already in use.", category="danger")
            return redirect(url_for("employee.register"))  # Redirect back to the registration page

        # Hash the password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Create the new employee record
        new_employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_no=mobile_no,
            password=hashed_password
        )
        db.session.add(new_employee)
        db.session.commit()

        # Flash success message
        flash("Account created successfully!", category="success")
        return redirect(url_for("auth.login"))  # Redirect to login page

    return render_template("auth/employee/register.html", form=form)
