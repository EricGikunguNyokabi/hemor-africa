import os
from flask import Blueprint, redirect, render_template, request, flash, current_app, session, url_for
from flask_login import current_user, login_required
from app import db
# file uploads
from werkzeug.utils import secure_filename
# Utils
from app.utils.date import format_date
from app.utils.email import send_email
from app.utils.otp import generate_otp
from app.utils.token import generate_token
# Models
from app.models.product import Category,Product
from app.models.user import User, Employee
# Forms
from app.forms.auth import LoginForm
from app.forms.product import CategoryForm, ProductForm, ProductImageForm,ProductVariantForm
from app.forms.supplier import SupplierForm



category = Blueprint("category", __name__)


@category.route("/categories", methods=["GET"])
def all_categories():
    categories = Category.query.all()
    print(f"category {categories}")
    return render_template("pos/category/categories.html", categories=categories)


# @category.route("/category/new", methods=["POST", "GET"])
# def new_category():
#     form = CategoryForm()

#     if form.validate_on_submit():  # Use form validation
#         try:
#             # Retrieve form data using the form object
#             category_name = form.category_name.data
#             category_description = form.category_description.data
#             category_image = form.category_image.data  # Correct field name

#             # Secure file upload
#             image_filename = secure_filename(category_image.filename)
#             upload_folder = current_app.config.get("ECOMMERCE_CATEGORY_UPLOAD_FOLDER", "static/uploads/categories")
#             os.makedirs(upload_folder, exist_ok=True)
#             image_path = os.path.join(upload_folder, image_filename)
#             category_image.save(image_path)

#             # Save category to the database using SQLAlchemy
#             new_category = Category(
#                 category_name=category_name,
#                 category_description=category_description,  # Save description if needed
#                 category_image_path=f"app/static/images/category/{image_filename}"  # Relative path for the database
#             )
#             db.session.add(new_category)
#             db.session.commit()

#             flash(f"Category '{category_name}' added successfully!", "success")
#             return redirect(url_for('admin.add_category_details'))  # Redirect after successful submission

#         except Exception as e:
#             db.session.rollback()
#             flash(f"An error occurred: {str(e)}", "danger")
#             return render_template("pos/category/new_category.html", form=form)

#     return render_template("pos/category/new_category.html", form=form)


@category.route("/category/new", methods=["POST", "GET"])
def new_category():
    form = CategoryForm()

    if form.validate_on_submit():  # Use form validation
        try:
            # Retrieve form data using the form object
            category_name = form.category_name.data
            category_description = form.category_description.data
            category_image = form.category_image.data  # Correct field name

            # Secure file upload
            image_filename = secure_filename(category_image.filename)
            upload_folder = current_app.config.get("ECOMMERCE_CATEGORY_UPLOAD_FOLDER", "static/uploads/categories")
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            category_image.save(image_path)

            # Save category to the database using SQLAlchemy
            new_category = Category(
                category_name=category_name,
                category_description=category_description,  # Save description if needed
                category_image_path=f"app/static/images/ecommerce/category/{image_filename}"  # Relative path for the database
            )
            db.session.add(new_category)
            db.session.commit()

            flash(f"Category '{category_name}' added successfully!", "success")
            return redirect(url_for('category.new_category'))  # Redirect after successful submission

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while adding the category: {str(e)}", "danger")
            return render_template("pos/category/new_category.html", form=form)

    return render_template("pos/category/new_category.html", form=form)     







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
