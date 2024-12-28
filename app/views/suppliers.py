import os
from flask import Blueprint, render_template, request, flash, current_app
from werkzeug.utils import secure_filename
from app.models.supplier import Supplier
from app import db
from app.models.user import User, Employee

supplier = Blueprint("supplier",__name__)