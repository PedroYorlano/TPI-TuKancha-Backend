from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .config import Config
from .api.club import bp as club_bp
from .api.cancha import bp_canchas

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()

app.config.from_object("config.Config")

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(club_bp)
    app.register_blueprint(bp_canchas)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)