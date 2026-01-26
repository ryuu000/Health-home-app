from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# Extension objects (create once, initialize with app inside create_app)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    """Application factory for the Flask app."""
    app = Flask(__name__)

    # Basic configuration from environment with sensible defaults
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///dev.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET', 'change_me'),
    )

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)  # In production, restrict origins: CORS(app, origins=['https://yourdomain.com'])

    # Example health route
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok'}, 200

    # Register your blueprints / routes here, e.g.:
    # from .routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

# Convenience: run app for local development
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
