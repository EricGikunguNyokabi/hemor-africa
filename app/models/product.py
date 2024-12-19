from app import db

class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    category_description = db.Column(db.Text, nullable=True)  # Optional category description
    category_image_path = db.Column(db.String(255), nullable=True)  # Path for category image
    updated_by = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)  # FK to Employee

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # One-to-Many relationship with Product
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.category_name}>"

class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)  # FK to Category
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=True)  # FK to Supplier
    product_name = db.Column(db.String(255), nullable=False)
    product_description = db.Column(db.Text, nullable=True)
    cost_price = db.Column(db.Float, nullable=False)  # Price purchased from supplier
    selling_price = db.Column(db.Float, nullable=False)  # Price sold to customer
    discount = db.Column(db.Float, default=0.0)  # Any discount on the product
    product_image_path = db.Column(db.String(255), nullable=True)  # Image path

    stock_quantity = db.Column(db.Integer, default=0)
    stock_threshold = db.Column(db.Integer, default=10)  # Alert threshold for low stock

    # Tracking fields
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)  # FK to Employee

    def __repr__(self):
        return f"<Product {self.product_name}, Updated by Employee ID {self.updated_by}>"

    def is_below_threshold(self):
        return self.stock_quantity < self.stock_threshold



    

class ProductImage(db.Model):
    __tablename__ = "product_images"
    image_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<ProductImage {self.image_path}>"



class ProductVariant(db.Model):
    __tablename__ = "product_variants"
    variant_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    variant_name = db.Column(db.String(100), nullable=False)  # e.g., "Size", "Color"
    variant_value = db.Column(db.String(100), nullable=False)  # e.g., "Large", "Red"
    stock_quantity = db.Column(db.Integer, default=0)
    additional_cost = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<ProductVariant {self.variant_name}: {self.variant_value}>"
