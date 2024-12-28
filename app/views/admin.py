from flask import Blueprint, render_template

from app.models.user import User, Employee

admin = Blueprint("admin", __name__,url_prefix="/adm/hemor-afriqa")

@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")
