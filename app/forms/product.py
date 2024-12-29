from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, FileField, SubmitField, SelectField, FieldList
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed

class CategoryForm(FlaskForm):
    category_name = StringField("Category Name",
        validators=[
            DataRequired(message="Category name is required."),
            Length(max=255, message="Category name cannot exceed 255 characters.")
        ]
    )
    category_description = TextAreaField("Category Description",
        validators=[
            Optional(),
            Length(max=1000, message="Description cannot exceed 1000 characters.")
        ]
    )
    category_image = FileField(
        "Upload Category Image",
        validators=[
            Optional()
        ]
    )
    submit = SubmitField("Save Category")

   







class ProductForm(FlaskForm):
    product_category = SelectField(
        "Product Category",
        coerce=int,  # FK field as integer
        validators=[DataRequired(message="Product category is required.")]
    )
    supplier = SelectField(
        "Supplier",
        coerce=int,
        validators=[Optional()]  # FK field as nullable
    )
    product_name = StringField(
        "Product Name",
        validators=[
            DataRequired(message="Product name is required."),
            Length(min=3, max=100, message="Product name must be between 3 and 100 characters.")
        ]
    )
    product_description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=1000, message="Description cannot exceed 1000 characters.")]
    )
    cost_price = FloatField(
        "Cost Price",
        default=0.0, 
        validators=[
            NumberRange(min=0, message="Cost price must be non-negative.")
        ]
    )
    selling_price = FloatField(
        "Selling Price",
        default=0.0,
        validators=[
            NumberRange(min=0, message="Selling price must be non-negative.")
        ]
    )
    discount = FloatField(
        "Discount",
        default=0,
        validators=[
            NumberRange(min=0, max=100, message="Discount must be between 0 and 100.")
        ]
    )
    stock_quantity = IntegerField(
        "Stock Quantity",
        default=1.0,
        validators=[
            DataRequired(message="Stock quantity is required."),
            NumberRange(min=0, message="Stock quantity must be non-negative.")
        ]
    )
    stock_threshold = IntegerField(
        "Stock Threshold",
        default=10,
        validators=[
            DataRequired(message="Stock threshold is required."),
            NumberRange(min=1, message="Stock threshold must be at least 1.")
        ]
    )

    product_images = FieldList(FileField("Upload Product Images (multiple)",
        validators=[
            Optional()        ]
    ), min_entries=1, max_entries=50)  # Adjust min and max as needed

    status = SelectField(
        "Product Status",
        choices=[("active", "Active"), ("inactive", "Inactive")],
        default="active",  # Set a default value if needed
        validators=[DataRequired(message="Product status is required.")]
    )

    submit = SubmitField("Add Product")







class ProductVariantForm(FlaskForm):
    variant_name = StringField("Variant Name", 
        validators=[DataRequired(message="Variant name is required.")]
        )
    variant_value = StringField("Variant Value", 
        validators=[DataRequired(message="Variant value is required.")]
        )
    stock_quantity = IntegerField("Stock Quantity", 
        validators=[DataRequired(message="Stock quantity is required.")]
        )
    additional_cost = FloatField("Additional Cost", 
        validators=[DataRequired(message="Additional cost is required.")]
        )

    submit = SubmitField("Add Variant")



class ProductImageForm(FlaskForm):
    image = FileField("Upload Product Image", 
        validators=[Optional()]
        )
    
    submit = SubmitField("Upload Image")
