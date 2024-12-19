import os
from flask import Blueprint, render_template, request, flash, current_app, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from app.models.product import Product
from app.forms.product import ProductForm
from app import db

products = Blueprint("products", __name__)

@products.route('/')
def home():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('home.html', products=products)

@products.route('/products')
def all_products():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('product/all_products.html', products=products)


@products.route("/product/add-product", methods=["POST", "GET"])
def add_product_details():
    form = ProductForm()  # Create an instance of the form
    if form.validate_on_submit():  # Check if the form is submitted and valid
        try:
            # Retrieve form data
            product_name = form.product_name.data
            product_description = form.product_description.data
            product_cost = form.cost_price.data
            product_selling_price = form.selling_price.data
            product_discount = form.discount.data
            product_stock_quantity = form.stock_quantity.data
            product_image = form.product_image.data  # Access the uploaded file

            # Secure file upload
            image_filename = secure_filename(product_image.filename)
            upload_folder = current_app.config["ECOMMERCE_PRODUCT_UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            product_image.save(image_path)

            # Save product to the database using SQLAlchemy
            new_product = Product(
                product_name=product_name,
                product_description=product_description,
                cost_price=product_cost,
                selling_price=product_selling_price,
                discount=product_discount,
                stock_quantity=product_stock_quantity,
                product_image_path=f"images/ecommerce/products/{image_filename}"  # Relative path for the database
            )
            db.session.add(new_product)
            db.session.commit()

            flash(f"Product '{product_name}' added successfully!", "success")
            return redirect(url_for('products.all_products'))  # Redirect to the products list

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("pos/product-management/add_product.html", form=form)

    return render_template("pos/product-management/add_product.html", form=form)


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