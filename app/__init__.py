from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    from .config import Config 
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    ma.init_app(app)

    from app.api.club import bp_club
    app.register_blueprint(bp_club, url_prefix='/api/v1/clubes')
    from app.api.cancha import bp_cancha
    app.register_blueprint(bp_cancha, url_prefix='/api/v1/canchas')
    from app.api.reserva import bp_reserva
    app.register_blueprint(bp_reserva, url_prefix='/api/v1/reservas')
    from app.api.user import bp_user
    app.register_blueprint(bp_user, url_prefix='/api/v1/users')
    
    return app