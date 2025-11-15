from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask import jsonify

from app.errors import AppError, NotFoundError, ValidationError, AuthError, ConflictError
from werkzeug.exceptions import NotFound, MethodNotAllowed, InternalServerError

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

    @app.errorhandler(AppError)
    def handle_app_error(error):
        """Manejador genérico para nuestros errores personalizados."""
        response = error.to_dict()
        app.logger.warning(f"Error de aplicación: {error.message}") # Log interno
        return jsonify(response), error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Manejador para errores de validación (400)."""
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        """Manejador para errores de 'no encontrado' (404)."""
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(ConflictError)
    def handle_conflict_error(error):
        """Manejador para errores de conflicto (409)."""
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        """Manejador para errores de autenticación (401)."""
        return jsonify(error.to_dict()), error.status_code
    
    # --- Manejadores para errores nativos de Flask/Werkzeug ---
    
    @app.errorhandler(NotFound) # Error 404 de Flask (ruta no encontrada)
    def handle_flask_not_found(error):
        return jsonify({"error": "Ruta no encontrada."}), 404

    @app.errorhandler(MethodNotAllowed) # Error 405 de Flask
    def handle_method_not_allowed(error):
        return jsonify({"error": "Método HTTP no permitido para esta ruta."}), 405

    @app.errorhandler(InternalServerError) # Error 500 genérico
    @app.errorhandler(Exception) # Atrapa-todo para cualquier error no manejado
    def handle_generic_exception(error):
        """Manejador para errores 500 y excepciones no controladas."""
        app.logger.error(f"Error interno no capturado: {error}", exc_info=True)
        return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

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

    from app.api.torneos.torneo import bp_torneo
    app.register_blueprint(bp_torneo)
    
    from app.api.torneos.equipo import bp_equipo
    app.register_blueprint(bp_equipo)

    from app.api.torneos.partido import bp_partido
    app.register_blueprint(bp_partido)
    
    return app