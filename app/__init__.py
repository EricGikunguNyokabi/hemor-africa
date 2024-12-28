from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # type: ignore
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS  # type: ignore # Import CORS :Enabling supports_credentials in CORS is excellent for applications handling authenticated requests (e.g., cookies for sessions).

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()  # Enable CSRF protection for the entire app



def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Session Configuration
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_FILENAME"] = "filesystem"
    app.config["SESSION_COOKIE_SECURE"] = not app.debug
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # CORS Setup
    CORS(app, supports_credentials=True, origins=["http://localhost:5000"])  # Update for production

    # Context Processor
    @app.context_processor
    def inject_globals():
        return {
            "company_name": app.config["COMPANY_NAME"],
            "mobile_number_1": app.config["MOBILE_NUMBER_1"],
            "mobile_number_2": app.config["MOBILE_NUMBER_2"],
            "company_mail": app.config["COMPANY_MAIL"],
            "company_url": app.config["COMPANY_URL"],
        }

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)



    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        from app.models.user import Employee
        user = User.query.get(int(user_id))
        return user or Employee.query.get(int(user_id))

    # Register Blueprints
    from app.views import main as main_blueprint
    from app.views.admin import admin as admin_blueprint
    from app.views.auth import auth as auth_blueprint
    from app.views.employees import employee as employee_blueprint
    from app.views.categories import category as category_blueprint
    from app.views.products import products as products_blueprint
    from app.views.suppliers import supplier as supplier_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(employee_blueprint, url_prefix="/employee")
    app.register_blueprint(category_blueprint, url_prefix="/category")
    app.register_blueprint(products_blueprint, url_prefix="/products")
    app.register_blueprint(supplier_blueprint, url_prefix="/supplier")

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("500.html"), 500

    return app
