from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    from .config import Config 
    app.config.from_object(Config)
    
    # Deshabilitar redirección automática de trailing slash
    app.url_map.strict_slashes = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # ✅ Configuración de CORS simplificada y más permisiva
    CORS(app, 
         origins=["http://localhost:3000", "http://127.0.0.1:3000"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )
    
    ma.init_app(app)

    # ✅ Registrar blueprints SIN duplicar url_prefix
    from app.api.auth import bp_auth
    app.register_blueprint(bp_auth)
    
    from app.api.club import bp_club
    app.register_blueprint(bp_club)
    
    from app.api.cancha import bp_cancha
    app.register_blueprint(bp_cancha)
    
    from app.api.reserva import bp_reserva
    app.register_blueprint(bp_reserva)
    
    from app.api.user import bp_user
    app.register_blueprint(bp_user)
    
    from app.api.timeslot import bp_timeslot
    app.register_blueprint(bp_timeslot)
    
    return app