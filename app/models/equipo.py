from . import db
from datetime import datetime


class Equipo(db.Model):
    __tablename__ = "equipo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    torneo_id = db.Column(db.Integer, db.ForeignKey("torneo.id"), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    representante = db.Column(db.String(120))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Equipo {self.nombre}>"
