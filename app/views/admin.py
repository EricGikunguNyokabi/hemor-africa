from flask import Blueprint, render_template

from app.models.user import User, Employee

admin = Blueprint("admin", __name__,url_prefix="/hemor-afriqa/adm")

@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")
