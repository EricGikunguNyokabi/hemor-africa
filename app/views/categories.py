import os
from flask import Blueprint, redirect, render_template, request, flash, current_app, session, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
# Utils
from app.utils.date import format_date
from app.utils.email import send_email
from app.utils.otp import generate_otp
from app.utils.token import generate_token
# Models
from app.models.product import Category,Product
from app.models.employee import Employee 
# Forms
from app.forms.auth import LoginForm
from app.forms.product import ProductsCategoryForm, ProductForm, ProductImageForm,ProductVariantForm
from app.forms.supplier import SupplierForm



category = Blueprint("category", __name__)



@category.route("/categories/new", methods=["GET", "POST"])
@login_required  # Ensure the user is logged in
def new_category():
    form = ProductsCategoryForm
    # Get the current user and employee
    user = current_user
    employee = None
    if user.is_authenticated:
        # Assuming current_user is an instance of Employee
        employee = Employee.query.filter_by(employee_id=user.employee_id).first()  # Adjust based on your Employee model

    if form.validate_on_submit():
        # Check if the user is logged in
        if user.is_authenticated:
            employee_id = employee.employee_id  # Use employee_id from the Employee model
        else:
            flash("You must be logged in to create a category.", "danger")
            return redirect(url_for("auth.login"))  # Adjust based on your login route

        # Process form data and save the category
        category = Category(
            category_name=form.category_name.data.strip(),
            category_description=form.category_description.data.strip(),
            updated_by=employee_id  # Set to the logged-in user's ID
        )

        # Handle file upload if a file is provided
        if form.category_image.data:
            image_filename = secure_filename(form.category_image.data.filename)
            upload_folder = current_app.config.get("ECOMMERCE_CATEGORY_UPLOAD_FOLDER", "static/uploads/categories")
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            form.category_image.data.save(image_path)
            category.category_image_path = image_path

        # Save the category to the database
        db.session.add(category)
        db.session.commit()

        flash(f"Category '{form.category_name.data}' created successfully!", "success")
        return redirect(url_for("category.view_categories"))

    # Render template with form and employee information
    return render_template("pos/category/product_category.html", form=form, user=user, employee=employee)



@category.route("/categories", methods=["GET"])
def view_categories():
    categories = Category.query.all()
    print(f"category {categories}")
    return render_template("pos/category/categories.html", categories=categories)



# Route to display products by category
@category.route("/category/<int:category_id>")
def category_products(category_id):
    # Query category details
    category = Category.query.filter_by(category_id=category_id).first_or_404()
    
    # Query products associated with this category
    products = Product.query.filter_by(product_category_id=category_id).all()

    return render_template(
        "product/category_products.html",
        category=category,
        products=products
    )
