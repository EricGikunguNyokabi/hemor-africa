from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional


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
    # Category Dropdown for selecting product category
    product_category = SelectField(
        "Product Category", 
        coerce=int,  # coerce values to integers
        validators=[DataRequired(message="Product category is required.")]
    )

    product_name = StringField("Product Name", 
        validators=[DataRequired(message="Product name is required.")]
    )
    product_description = TextAreaField("Description", 
        validators=[Length(max=1000, message="Description cannot exceed 1000 characters.")]
    )
    cost_price = FloatField("Cost Price", default=0,
        validators=[DataRequired(message="Cost price is required.")]
    )
    selling_price = FloatField("Selling Price", default=0,
        validators=[DataRequired(message="Selling price is required.")]
    )
    # discount = FloatField("Discount")
    discount = FloatField("Discount", default=0)
    stock_quantity = IntegerField("Stock Quantity", 
        validators=[DataRequired(message="Stock quantity is required.")]
    )
    product_image = FileField("Upload Product Image")

    
    submit = SubmitField("Register Product")





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
