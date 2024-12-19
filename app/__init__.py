from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # type: ignore
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # type: ignore # Import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object("app.config.Config")  # Load configuration from Config class

#     app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production if using HTTPS
#     app.config['SESSION_COOKIE_HTTPONLY'] = True
#     app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
#     app.config['SECRET_KEY'] = 'your-secret-key'  # Ensure your secret key is set for sessions

#     # Initialize CORS for cross-origin requests with cookie support
#     CORS(app, supports_credentials=True)

#     # Context Processor to make company name and mobile numbers globally available in templates
#     @app.context_processor
#     def inject_globals():
#         return {
#             'company_name': app.config['COMPANY_NAME'],
#             'mobile_number_1': app.config['MOBILE_NUMBER_1'],
#             'mobile_number_2': app.config['MOBILE_NUMBER_2'],
#             'company_mail': app.config['COMPANY_MAIL'],
#             'company_url': app.config['COMPANY_URL']
#         }

#     # Initialize extensions with the app
#     db.init_app(app)
#     migrate.init_app(app, db)
#     login_manager.init_app(app)
#     @login_manager.user_loader
#     def load_user(user_id):
#         from app.models.user import User
#         from app.models.employee import Employee
#         user = User.query.get(int(user_id))
#         if user:
#             return user
#         return Employee.query.get(int(user_id))  # Check Employee if User not found


#     bcrypt.init_app(app)

#     # Set the login view for Flask-Login
#     login_manager.login_view = "auth.login"  # Adjust this based on your blueprint

#     @login_manager.user_loader
#     def load_user(user_id):
#         from app.models.user import User
#         return User.query.get(int(user_id))  # Load user by ID

#     # Register blueprints
#     from app.views import main as main_blueprint
#     from app.views.auth import auth as authentification_blueprint
#     from app.views.employees import employee as employee_blueprint
#     from app.views.categories import category as category_blueprint
#     from app.views.products import products as products_blueprint
#     from app.views.suppliers import supplier as supplier_blueprint

#     app.register_blueprint(main_blueprint)
#     app.register_blueprint(authentification_blueprint)
#     app.register_blueprint(employee_blueprint)
#     app.register_blueprint(category_blueprint)
#     app.register_blueprint(products_blueprint)
#     app.register_blueprint(supplier_blueprint)

#     return app
def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Load configuration from Config class

    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production if using HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SECRET_KEY'] = 'your-secret-key'  # Ensure your secret key is set for sessions

    # Initialize CORS for cross-origin requests with cookie support
    CORS(app, supports_credentials=True)

    # Context Processor to make company name and mobile numbers globally available in templates
    @app.context_processor
    def inject_globals():
        return {
            'company_name': app.config['COMPANY_NAME'],
            'mobile_number_1': app.config['MOBILE_NUMBER_1'],
            'mobile_number_2': app.config['MOBILE_NUMBER_2'],
            'company_mail': app.config['COMPANY_MAIL'],
            'company_url': app.config['COMPANY_URL']
        }

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Set the login view for Flask-Login
    login_manager.login_view = "auth.login"  # Adjust this based on your blueprint

    @login_manager.user_loader
    def load_user(user_id):
        from app.models .user import User
        from app.models.employee import Employee
        user = User.query.get(int(user_id))
        if user:
            return user
        return Employee.query.get(int(user_id))  # Check Employee if User not found

    # Register blueprints
    from app.views import main as main_blueprint
    from app.views.auth import auth as authentification_blueprint
    from app.views.employees import employee as employee_blueprint
    from app.views.categories import category as category_blueprint
    from app.views.products import products as products_blueprint
    from app.views.suppliers import supplier as supplier_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(authentification_blueprint)
    app.register_blueprint(employee_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(supplier_blueprint)

    return app