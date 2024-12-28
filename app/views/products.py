import os
from flask import Blueprint, render_template, request, flash, current_app, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from app.models.product import Product, Category
from app.forms.product import ProductForm
from app.models.user import User, Employee
from app import db

products = Blueprint("products", __name__)



@products.route('/products')
def all_products():
    products = Product.query.all()  # Fetch all products
    categories = Category.query.all()  # Fetch all categories for name mapping
    return render_template('pos/product-management/all_products.html', products=products, categories=categories)


@products.route("/product/add-product", methods=["POST", "GET"])
def add_product():
    form = ProductForm()  # Create an instance of the form
    categories = Category.query.all()  # Get all categories for the dropdown

    # Populate the SelectField with category choices (category_name as the label, category_id as the value)
    form.product_category.choices = [(category.category_id, category.category_name) for category in categories]

    if form.validate_on_submit():
        try:
            # Retrieve form data
            product_name = form.product_name.data
            product_description = form.product_description.data
            product_cost = form.cost_price.data
            product_selling_price = form.selling_price.data
            product_discount = form.discount.data
            product_stock_quantity = form.stock_quantity.data
            product_image = form.product_image.data

            # Secure file upload
            image_filename = secure_filename(product_image.filename)
            upload_folder = current_app.config["ECOMMERCE_PRODUCT_UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            product_image.save(image_path)

            # Retrieve the selected category based on the category_id from the form
            product_category_id = form.product_category.data
            category = Category.query.get(product_category_id)  # Get category by ID

            # Create and save the new product with the selected category
            new_product = Product(
                product_name=product_name,
                product_description=product_description,
                cost_price=product_cost,
                selling_price=product_selling_price,
                discount=product_discount,
                stock_quantity=product_stock_quantity,
                product_image_path=f"images/ecommerce/products/{image_filename}",
                product_category=category
            )

            db.session.add(new_product)
            db.session.commit()

            flash(f"Product '{product_name}' added successfully!", "success")
            return redirect(url_for('products.all_products'))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("pos/product-management/add_product.html", form=form, categories=categories)

    return render_template("pos/product-management/add_product.html", form=form, categories=categories)



@products.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product or return 404 if not found

    if request.method == 'POST':
        # Update product fields from the form submission
        product.name = request.form.get('product_name')
        product.category_id = request.form.get('product_category')
        product.description = request.form.get('product_description')
        product.cost_price = request.form.get('cost_price', type=float)
        product.selling_price = request.form.get('selling_price', type=float)
        product.discount = request.form.get('discount', type=float)
        product.stock_quantity = request.form.get('stock_quantity', type=int)

        # Check for image update
        if 'product_image' in request.files:
            image_file = request.files['product_image']
            if image_file.filename:  # Check if a new image is uploaded
                # (Save image logic: upload to a server, cloud storage, etc.)
                product.image_url = f"/static/images/{image_file.filename}"
                image_file.save(f"static/images/{image_file.filename}")

        db.session.commit()  # Save updates to the database
        flash('Product updated successfully!', 'success')
        return redirect(url_for('all_products'))  # Redirect to the all products page

    # Pre-fill the edit form with product data
    categories = Category.query.all()  # Assuming you have a Category model for the dropdown
    return render_template("pos/product-management/edit_product.html", product=product, categories=categories)



@products.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product or return 404

    try:
        db.session.delete(product)
        db.session.commit()  # Save deletion to the database
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash(f'Error deleting product: {e}', 'danger')

    return redirect(url_for('all_products'))  # Redirect to the all products page



# @products.route("/product/add-product", methods=["POST", "GET"])
# def add_product_details():
#     form = ProductForm()  # Create an instance of the form
#     categories = Category.query.all()
#     if form.validate_on_submit():  # Check if the form is submitted and valid
#         try:
#             # Retrieve form data
#             product_name = form.product_name.data
#             product_description = form.product_description.data
#             product_cost = form.cost_price.data
#             product_selling_price = form.selling_price.data
#             product_discount = form.discount.data
#             product_stock_quantity = form.stock_quantity.data
#             product_image = form.product_image.data  # Access the uploaded file

#             # Secure file upload
#             image_filename = secure_filename(product_image.filename)
#             upload_folder = current_app.config["ECOMMERCE_PRODUCT_UPLOAD_FOLDER"]
#             os.makedirs(upload_folder, exist_ok=True)
#             image_path = os.path.join(upload_folder, image_filename)
#             product_image.save(image_path)

#             # Save product to the database using SQLAlchemy
#             new_product = Product(
#                 product_name=product_name,
#                 product_description=product_description,
#                 cost_price=product_cost,
#                 selling_price=product_selling_price,
#                 discount=product_discount,
#                 stock_quantity=product_stock_quantity,
#                 product_image_path=f"images/ecommerce/products/{image_filename}"  # Relative path for the database
#             )
#             db.session.add(new_product)
#             db.session.commit()

#             flash(f"Product '{product_name}' added successfully!", "success")
#             return redirect(url_for('products.all_products'))  # Redirect to the products list

#         except Exception as e:
#             db.session.rollback()
#             flash(f"An error occurred: {str(e)}", "danger")
#             return render_template("pos/product-management/add_product.html", form=form, categories=categories)

#     return render_template("pos/product-management/add_product.html", form=form, categories=categories)


# SINGLE ITEM VIEW
@products.route('/product/<int:product_id>')
def single_product_detail(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID
    return render_template('product/single_product.html', product=product)

@products.route('/update-product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    from flask import request  # Ensure request is imported
    product = Product.query.get_or_404(product_id)
    user = current_user
    current_employee_id = Employee.query.filter_by(employee_id=user.employee_id).first()  # Adjust based on your Employee model

    # Update product details
    product.product_name = request.json.get('product_name', product.product_name)
    product.selling_price = request.json.get('selling_price', product.selling_price)
    product.stock_quantity = request.json.get('stock_quantity', product.stock_quantity)
    product.updated_by = current_employee_id  # Track who made the change

    db.session.commit()

    return jsonify({"message": f"Product {product.product_name} updated successfully by Employee ID {current_employee_id}"})