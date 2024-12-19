from app import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(255), nullable=True)  # Optional field for a specific representative
    email = db.Column(db.String(255), unique=True, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Integer, default=5)  # Rating based on performance

    # One-to-Many relationship with Product
    products = db.relationship('Product', backref='supplier', lazy=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<Supplier {self.supplier_name}>"
#