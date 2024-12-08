# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # type: ignore
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Load configuration from Config class


    # Context Processor to make company name and mobile numbers globally available in templates
    @app.context_processor
    def inject_globals():
        return {
            'company_name': app.config['COMPANY_NAME'],
            'mobile_number_1': app.config['MOBILE_NUMBER_1'],
            'mobile_number_2': app.config['MOBILE_NUMBER_2'],
            'company_mail': app.config['COMPANY_MAIL']
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
        from app.models.user import User
        return User.query.get(int(user_id))  # Load user by ID

    # Register blueprints
    from app.views import main as main_blueprint
    from app.views.auth import auth as auth_blueprint
    from app.views.ecommerce import ecommerce as ecommerce_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(ecommerce_blueprint)

    return app

# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade

# flask db current
# flask db downgrade

# flask db history