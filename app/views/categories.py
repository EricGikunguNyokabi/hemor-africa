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

# Blueprint initializtion
category = Blueprint("category", __name__,url_prefix="/admin/category")

# ALL CATEGORY AVAILABLE 
@category.route("/categories", methods=["GET"])
def all_categories():
    categories = Category.query.all()
    form = CategoryForm()  # Create an instance of the form
    return render_template("pos/category/all_categories.html", categories=categories, form=form)

# ADD NEW CATEGORY
@category.route("/new", methods=["POST", "GET"])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():  # Use form validation
        try:
            # Retrieve form data using the form object
            category_name = form.category_name.data
            category_description = form.category_description.data
            category_image = form.category_image.data  

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


# EDIT CATEGORY
# @category.route("/edit/<int:category_id>", methods=["POST", "GET"])
# def edit_category(category_id):
#     category = Category.query.get_or_404(category_id)  # Fetch category by ID or return 404
#     form = CategoryForm(obj=category)  # Pre-fill form with current category values :obj=category: Automatically pre-fills the form with the category's current data using Flask-WTF's obj parameter.
    
#     if form.validate_on_submit():
#         try:
#             # Update category with new data from the form
#             category.category_name = form.category_name.data
#             category.category_description = form.category_description.data
            
#             # Handle image upload if a new file is provided
#             if form.category_image.data:
#                 category_image = form.category_image.data
#                 image_filename = secure_filename(category_image.filename)
#                 upload_folder = current_app.config.get("ECOMMERCE_CATEGORY_UPLOAD_FOLDER", "static/uploads/categories")
#                 os.makedirs(upload_folder, exist_ok=True)
#                 image_path = os.path.join(upload_folder, image_filename)
#                 category_image.save(image_path)
#                 category.category_image_path = f"app/static/images/ecommerce/category/{image_filename}"

#             # Save changes to the database
#             db.session.commit()
#             flash(f"Category '{category.category_name}' updated successfully!", "success")
#             return redirect(url_for("category.all_categories"))  # Redirect to category list

#         except Exception as e:
#             db.session.rollback()
#             flash(f"An error occurred while updating the category: {str(e)}", "danger")
#             return render_template("pos/category/edit_category.html", form=form, category=category)

#     return render_template("pos/category/edit_category.html", form=form, category=category)
@category.route("/admin/category/edit/<int:category_id>", methods=["POST", "GET"])
def edit_category(category_id):
    # Get category from database
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)  # Populate the form with current category data

    if form.validate_on_submit():
        try:
            # Update the category details
            category.category_name = form.category_name.data
            category.category_description = form.category_description.data

            # Handle image upload if a new image is provided
            if form.category_image.data:
                category_image = form.category_image.data
                image_filename = secure_filename(category_image.filename)
                upload_folder = current_app.config.get(
                    "ECOMMERCE_CATEGORY_UPLOAD_FOLDER", "static/uploads/categories"
                )
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join(upload_folder, image_filename)
                category_image.save(image_path)

                # Update the image path in the database
                category.category_image_path = f"app/static/images/ecommerce/category/{image_filename}"

            # Commit the changes to the database
            db.session.commit()

            flash(f"Category '{category.category_name}' updated successfully!", "success")
            return redirect(url_for("category.all_categories"))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating the category: {str(e)}", "danger")

    return render_template("pos/category/edit_category.html", form=form, category=category)


# DELETE CATEGORY
@category.route("/admin/category/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)  # Fetch category or 404 if not found
    try:
        # Delete the image file if it exists
        image_path = os.path.join(current_app.root_path, category.category_image_path)
        if os.path.exists(image_path):
            os.remove(image_path)

        # Delete the category from the database
        db.session.delete(category)
        db.session.commit()
        flash(f"Category '{category.category_name}' deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the category: {str(e)}", "danger")

    return redirect(url_for("category.all_categories"))  # This ensures that after the deletion, the user is redirected to the appropriate page, maintaining a smooth user experience. Overall, your implementation is effective and follows best practices for handling category management in a Flask application. If you have any further questions or need additional features, feel free to ask!



# Route to display products by category
@category.route("/<int:category_id>")
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
