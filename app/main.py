from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .config import Config
from .api.club import bp_club
from .api.cancha import bp_cancha
from .api.reserva import bp_reserva

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(bp_club)
    app.register_blueprint(bp_cancha)
    app.register_blueprint(bp_reserva)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)