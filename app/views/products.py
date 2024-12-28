import os
from flask import Blueprint, render_template, request, flash, current_app, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from app.models.product import Product, Category
from app.forms.product import ProductForm
from app.forms.supplier import SupplierForm
from app.models.user import User, Employee
from app.models.supplier import Supplier
from app import db

products = Blueprint("products", __name__,url_prefix="/hemor-afriqa/product/")



@products.route("/products")
def all_products():
    products = Product.query.all()  # Fetch all products
    categories = Category.query.all()  # Fetch all categories for name mapping
    form = ProductForm()  # Create an instance of the form
    return render_template('pos/product-management/all_products.html', products=products, categories=categories, form=form)


@products.route("/add-product", methods=["POST", "GET"])
def add_product():
    form = ProductForm()
    categories = Category.query.all()
    form.product_category.choices = [(category.category_id, category.category_name) for category in categories]

    # Fetch suppliers and add the default supplier as the first choice
    suppliers = Supplier.query.all()
    form.supplier.choices = [(1, "Kibe (Default)")] + [
        (supplier.supplier_id, supplier.supplier_name) for supplier in suppliers
    ]

    if form.validate_on_submit():
        try:
            # Retrieve form data
            product_category = form.product_category.data
            product_name = form.product_name.data
            product_description = form.product_description.data
            product_cost = form.cost_price.data
            product_selling_price = form.selling_price.data
            product_discount = form.discount.data
            product_stock_quantity = form.stock_quantity.data
            stock_threshold = form.stock_threshold.data
            product_image = form.product_image.data

    

            # Secure file upload or handle default image
            if product_image:
                image_filename = secure_filename(product_image.filename)
                upload_folder = current_app.config["ECOMMERCE_PRODUCT_UPLOAD_FOLDER"]
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join(upload_folder, image_filename)
                product_image.save(image_path)
                image_path_db = f"app/static/images/ecommerce/products/{image_filename}"
            else:
                image_path_db = "images/ecommerce/products/default.jpg"

            # Retrieve selected category
            # map category according to selection
            product_category_id = form.product_category.data
            category = Category.query.get(product_category_id)
            if not category:
                flash("Invalid product category selected.", "danger")
                return render_template("pos/product-management/add_product.html", form=form, categories=categories)

            # Assign supplier or fallback to default supplier
            product_supplier_id = form.supplier.data or 1  # Fallback to default supplier ID
            supplier = Supplier.query.get(product_supplier_id)
            if not supplier:
                flash("Default supplier is not properly configured in the database.", "danger")
                return render_template("pos/product-management/add_product.html", form=form, categories=categories)

            # Ensure unique product name
            if Product.query.filter_by(product_name=product_name).first():
                flash(f"Product with name '{product_name}' already exists.", "danger")
                return render_template("pos/product-management/add_product.html", form=form, categories=categories)

            # Create new product
            new_product = Product(
                product_category_id=product_category_id,
                product_category=category,
                supplier=supplier,
                product_name=product_name,
                product_description=product_description,
                cost_price=product_cost,
                selling_price=product_selling_price,
                discount=product_discount,
                stock_quantity=product_stock_quantity,
                stock_threshold=stock_threshold,
                product_image_path=image_path_db
                
            )

            db.session.add(new_product)
            db.session.commit()

            flash(f"Product '{product_name}' added successfully!", "success")
            return redirect(url_for('products.all_products'))

        except Exception as e:
            db.session.rollback()
            import logging
            logging.error(f"An error occurred while adding a product: {str(e)}")
            flash("An unexpected error occurred. Please try again later.", "danger")

    return render_template("pos/product-management/add_product.html", form=form, categories=categories, suppliers=suppliers)



# EDIT CATEGORY
@products.route("/edit/<int:product_id>", methods=["POST", "GET"])
def edit_product(product_id):
    # Get the product from the database
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()  # Fetch all categories for the dropdown
    suppliers = Supplier.query.all()  # Fetch all suppliers for the dropdown
    form = ProductForm(obj=product)  # Populate the form with current product data

    # Set the choices for categories and suppliers
    form.product_category.choices = [(category.category_id, category.category_name) for category in categories]
    form.supplier.choices = [(supplier.supplier_id, supplier.supplier_name) for supplier in suppliers]

    if form.validate_on_submit():
        try:
            # Update the product details
            product.product_name = form.product_name.data
            product.product_description = form.product_description.data
            product.cost_price = form.cost_price.data
            product.selling_price = form.selling_price.data
            product.discount = form.discount.data
            product.stock_quantity = form.stock_quantity.data
            product.stock_threshold = form.stock_threshold.data
            product.product_category_id = form.product_category.data
            product.supplier_id = form.supplier.data

            # Handle image upload if a new image is provided
            if form.product_image.data:
                product_image = form.product_image.data
                image_filename = secure_filename(product_image.filename)
                upload_folder = current_app.config["ECOMMERCE_PRODUCT_UPLOAD_FOLDER"]
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join(upload_folder, image_filename)
                product_image.save(image_path)

                # Update the image path in the database
                product.product_image_path = f"app/static/images/ecommerce/products/{image_filename}"

            # Commit the changes to the database
            db.session.commit()

            flash(f"Product '{product.product_name}' updated successfully!", "success")
            return redirect(url_for("products.all_products"))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating the product: {str(e)}", "danger")

    return render_template("pos/product-management/edit_product.html", form=form, product=product, categories=categories, suppliers=suppliers)



@products.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product or return 404

    try:
        # Delete the image file if it exists
        image_path = os.path.join(current_app.root_path, product.product_image_path)
        if os.path.exists(image_path):
            os.remove(image_path)

        db.session.delete(product)
        db.session.commit()  # Save deletion to the database
        flash(f"Category '{product.product_name}' deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash(f'Error deleting product: {e}', 'danger')

    return redirect(url_for("products.all_products"))  # Redirect to the all products page



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