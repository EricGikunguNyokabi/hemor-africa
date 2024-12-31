# views provide HTTP requests and providing responses. Routing and interaction with templates or APIs

from flask import Blueprint, render_template,request,jsonify
from flask_login import current_user, login_required
from app.models.product import Product,Category, ProductImage
from app.models.user import User, Employee

main = Blueprint('main', __name__)

# Home route: Display all products
@main.route("/")
def home():
    # Fetch the specified product by product_id
    product = Product.query.all()
    if not product:
        return "<h1>Product Not Found</h1>", 404

    # Fetch the product's images
    # images = ProductImage.query.filter_by(product_id=product.product_id).all()
    
    # Fetch the product's associated category
    # category = Category.query.filter_by(category_id=product.product_category_id).first()

    return render_template(
        "home.html",
        product=product
        # images=images,
        # category=category
    )



# MAIN E-COMMERCE PAGE ==============================================================================================================
# @main.route("/products", defaults={'product_id': None})
# @main.route("/e-commerce")
# @main.route("/e-commerce/<int:product_id>")
# def display_products(product_id):
#     if product_id is not None:
#         # Fetch the specified product by product_id
#         product = Product.query.filter_by(product_id=product_id).first()
#         if not product:
#             return "<h1>Product Not Found</h1>", 404

#         # Fetch the product's images
#         images = ProductImage.query.filter_by(product_id=product.product_id).all()
        
#         # Fetch the product's associated category
#         category = Category.query.filter_by(category_id=product.product_category_id).first()

#         return render_template(
#             "ecommerce.html",
#             product=product,
#             images=images,
#             category=category,
#             is_single_product=True  # Flag to indicate single product view
#         )
#     else:
#         # Fetch all products if no product_id is provided
#         products = Product.query.all()  # Fetch all products
#         categories = Category.query.all()  # Fetch all categories for name mapping
#         return render_template("ecommerce.html", products=products, categories=categories, is_single_product=False)  # Flag for all products view
@main.route("/products", defaults={'product_id': None})
@main.route("/e-commerce")
@main.route("/e-commerce/<int:product_id>")
def display_products(product_id):
    if product_id is not None:
        # Fetch the specified product by product_id
        product = Product.query.filter_by(product_id=product_id).first()
        if not product:
            return "<h1>Product Not Found</h1>", 404

        # Fetch the product's images, limiting to 4 images
        images = ProductImage.query.filter_by(product_id=product.product_id).limit(4).all()
        
        # Fetch the product's associated category
        category = Category.query.filter_by(category_id=product.product_category_id).first()

        return render_template(
            "ecommerce.html",
            product=product,
            images=images,
            category=category,
            is_single_product=True  # Flag to indicate single product view
        )
    else:
        # Fetch all products if no product_id is provided
        products = Product.query.all()  # Fetch all products
        categories = Category.query.all()  # Fetch all categories for name mapping
        return render_template("ecommerce.html", products=products, categories=categories, is_single_product=False)  # Flag for all products view
    


# Profile route: View or update user profile
@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user  # Automatically fetched by Flask-Login

    if request.method == "POST":
        # Update profile logic
        data = request.form  # Fetch submitted data from the form
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.mobile_no = data.get('mobile_no')
        user.address = data.get('address')
        user.city = data.get('city')
        user.postal_code = data.get('postal_code')
        user.country = data.get('country')

        # Save the updated information to the database
        user.save()
        return jsonify({"message": "Profile updated successfully!"}), 200
    # Render the profile template
    return render_template("user/profile.html", user=user)


@main.route("/api/profile", methods=["POST"])
@login_required
def api_update_profile():
    user = current_user
    data = request.json  # Expecting a JSON body

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.mobile_no = data.get('mobile_no', user.mobile_no)
    user.address = data.get('address', user.address)
    user.city = data.get('city', user.city)
    user.postal_code = data.get('postal_code', user.postal_code)
    user.country = data.get('country', user.country)

    user.save()
    
    return jsonify({"message": "Profile updated successfully!", "user": {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile_no": user.mobile_no,
        "address": user.address,
        "city": user.city,
        "postal_code": user.postal_code,
        "country": user.country
    }}), 200



# Dashboard route: Fetch and display user and employee data
@main.route("/dashboard")
@login_required
def dashboard():
    user = current_user  # Automatically fetched by Flask-Login

    # Fetch employee data
    employee = None
    if isinstance(user, Employee):
        # If the current user is an employee, assign them directly
        employee = user
    else:
        # Otherwise, fetch all employees (optional based on use-case)
        employee = Employee.query.all()
        print(f"\n\nemployee: {employee}")

    return render_template(
        "user/dashboard.html", 
        user=user, 
        employee=employee
    )

