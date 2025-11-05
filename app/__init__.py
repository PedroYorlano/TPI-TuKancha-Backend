from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///tukancha.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    ma.init_app(app)

    # Register blueprints
    from app.api.club import bp_club
    app.register_blueprint(bp_club, url_prefix='/api/v1/clubes')
    from app.api.cancha import bp_cancha
    app.register_blueprint(bp_cancha, url_prefix='/api/v1/canchas')
    from app.api.reserva import bp_reserva
    app.register_blueprint(bp_reserva, url_prefix='/api/v1/reservas')
    

    return app