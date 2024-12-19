from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class SupplierForm(FlaskForm):
    supplier_name = StringField("Supplier Name", validators=[DataRequired(message="Supplier name is required.")])
    contact_person = StringField("Contact Person")
    email = StringField("Email", validators=[DataRequired(message="Email is required."), Email(message="Invalid email format.")])
    phone_number = StringField("Phone Number")
    address = StringField("Address")
    country = StringField("Country")
    submit = SubmitField("Register Supplier")
