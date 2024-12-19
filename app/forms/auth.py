# form/auth.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


# EMPLOYEE & ADMIN REISTRATION FORM
class EmployeeRegistrationForm(FlaskForm):
    first_name = StringField("First Name",
        validators=[DataRequired(message="First Name is required")],
        render_kw={"placeholder": "Enter your first name"}
    )
    middle_name = StringField("Middle Name",
        validators=[Optional()]
    )
    last_name = StringField("Last Name",
        validators=[DataRequired(message="Last Name is required")]
    )
    email = StringField("Email", 
        validators=[DataRequired(message="Email is required"), Email()]
        )
    mobile_no = StringField("Mobile Number", 
        validators=[
            DataRequired(message="Mobile number is required."),
            Length(min=10,max=13,message="Mobile number must be between 10 and 13 characters.")]
        )
    password = PasswordField("Password", 
        validators=[
            DataRequired(message="Password is required."),
            Length(min=4,max=64, message="Password must be at least 4 characters long.")]
        )
    confirm_password = PasswordField("Confirm Password", 
        validators=[
            DataRequired(message="Please confirm your password."), 
            EqualTo("password", message="Passwords must match.")]
            )
    submit = SubmitField("Register")




# USER REGISTRATION FORM 
class UserRegistrationForm(FlaskForm):
    first_name = StringField("First Name",
        validators=[Optional()]
    )
    middle_name = StringField("Middle Name",
        validators=[Optional()]
    )
    last_name = StringField("Last Name",
        validators=[Optional()]
    )
    email = StringField("Email", 
        validators=[Optional(), Email()]
        )
    mobile_no = StringField("Mobile Number", 
        validators=[
            DataRequired(message="Mobile number is required."),
            Length(min=10,max=13,message="Mobile number must be between 10 and 13 characters.")]
        )
    password = PasswordField("Password", 
        validators=[
            DataRequired(message="Password is required."),
            Length(min=4,max=64, message="Password must be at least 4 characters long.")]
        )
    confirm_password = PasswordField("Confirm Password", 
        validators=[
            DataRequired(message="Please confirm your password."), 
            EqualTo("password", message="Passwords must match.")]
            )
    submit = SubmitField("Register")



# LOGIN
class LoginForm(FlaskForm):
    email_or_mobile = StringField("Email or Mobile", 
        validators=[
            DataRequired(message="Please enter your email or mobile number")]
            )
    password = PasswordField("Password", 
        validators=[
            DataRequired(message="Password is required."), 
            Length(min=4, message="Password must be at least 4 characters long.")]
            )
    submit = SubmitField("Login")

    class Meta:
        csrf = False  # Disable CSRF protection if needed