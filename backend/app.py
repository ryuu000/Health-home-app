from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///dev.db'),
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET', 'change_me'),
    )

    db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
CORS(app)

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app

