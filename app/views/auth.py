from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.employee import Employee
from app.models.user import User  
from app import db
import random
import string
from app.forms.auth import UserRegistrationForm,LoginForm





# Define Blueprint
auth = Blueprint("auth", __name__)

# Helper function to generate OTP
def generate_otp(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

# Route: Registration
@auth.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegistrationForm
    if request.method == "POST":
        email = form.get.email
        mobile_no = form.get.mobile_no
        password = form.get.password

        # Check if user already exists
        if  User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return render_template("auth/register.html", form=form)
        if User.query.filter_by(mobile_no=mobile_no).first():
            flash("Mobile Number already exists","error")
            return render_template("auth/register.html",form=form)

        hashed_password = generate_password_hash(password, method="sha256")
        new_user = User(
            email=email,
            mobile_no=mobile_no,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!","success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email_or_mobile = form.email_or_mobile.data
        password = form.password.data

        # Normalize the email_or_mobile
        if email_or_mobile.startswith("+"):  
            email_or_mobile = email_or_mobile[1:]  
        if email_or_mobile.startswith("0"):  
            email_or_mobile = "254" + email_or_mobile[1:]  

        user = Employee.query.filter(
            (Employee.email == email_or_mobile) | (Employee.mobile_no == email_or_mobile)
        ).first() or User.query.filter(
            (User .email == email_or_mobile) | (User .mobile_no == email_or_mobile)
        ).first()

        if user:
            print(f"User  found: {user.email} or {user.mobile_no}")
            if check_password_hash(user.password, password):
                print("Password is correct.")
                login_user(user)
                print(f"Current user after login: {current_user}")
                user.login_count += 1
                user.last_login = db.func.current_timestamp()
                db.session.commit()
                flash(f"{user.__class__.__name__} logged in successfully!", category="success")
                return redirect(url_for("main.dashboard"))
            else:
                flash("Invalid credentials.", category="danger")
        else:
            flash("Invalid credentials.", category="danger")
        
        return redirect(url_for("auth.login"))
    
    return render_template("auth/login.html", form=form)




# Route: Request OTP
@auth.route("/request-otp", methods=["GET", "POST"])
def request_otp():
    if request.method == "POST":
        email_or_mobile = request.form.get("email_or_mobile")

        # Find user by email or mobile number
        user = Employee.query.filter((Employee.email == email_or_mobile) | (Employee.mobile_no == email_or_mobile)).first()
        if not user:
            flash("No user found with the provided email or mobile number.", category="danger")
            return redirect(url_for("auth.request_otp"))

        # Generate and save OTP
        otp = generate_otp()
        user.otp = otp
        user.otp_created_at = db.func.current_timestamp()
        db.session.commit()

        flash(f"OTP sent to {email_or_mobile}", category="info")
        # Here, you'd integrate an email or SMS sending service to deliver the OTP
        print(f"Generated OTP: {otp}")  # Debugging purposes

        return redirect(url_for("auth.verify_otp"))

    return render_template("auth/request_otp.html")

# Route: Verify OTP
@auth.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        email_or_mobile = request.form.get("email_or_mobile")
        otp = request.form.get("otp")

        # Find user by email or mobile number
        user = Employee.query.filter((Employee.email == email_or_mobile) | (Employee.mobile_no == email_or_mobile)).first()
        if not user or user.otp != otp:
            flash("Invalid OTP.", category="danger")
            return redirect(url_for("auth.verify_otp"))

        flash("OTP verified successfully!", category="success")
        return redirect(url_for("auth.reset_password", email_or_mobile=email_or_mobile))

    return render_template("auth/verify_otp.html")

# Route: Reset Password
@auth.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    email_or_mobile = request.args.get("email_or_mobile")
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.", category="danger")
            return redirect(url_for("auth.reset_password", email_or_mobile=email_or_mobile))

        # Find user and update password
        user = Employee.query.filter((Employee.email == email_or_mobile) | (Employee.mobile_no == email_or_mobile)).first()
        if not user:
            flash("Invalid request.", category="danger")
            return redirect(url_for("auth.request_otp"))

        user.password = generate_password_hash(password, method="sha256")
        user.otp = None  # Clear OTP after successful reset
        db.session.commit()

        flash("Password reset successfully!", category="success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")



from flask_login import logout_user

@auth.route("/logout")
def logout():
    # Log out the current user
    logout_user()
    flash("You have successfully logged out.", category="info")  # flash message on logout

    
    # Redirect to the homepage or login page
    return redirect(url_for('main.home'))  # or use 'auth.login' if you want to go back to the login page
