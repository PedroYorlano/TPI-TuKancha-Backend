from flask import Flask
from app.db import db
from app.api.club import bp as club_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    app.register_blueprint(club_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)