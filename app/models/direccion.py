from . import db
from datetime import datetime


class Direccion(db.Model):
    __tablename__ = "direccion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    calle = db.Column(db.String(120))
    numero = db.Column(db.String(20))
    piso = db.Column(db.String(10))
    depto = db.Column(db.String(10))
    ciudad = db.Column(db.String(80))
    provincia = db.Column(db.String(80))
    pais = db.Column(db.String(80), default="Argentina")
    cp = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One direccion puede aplicarse a varios clubes en algunos modelos
    clubes = db.relationship("Club", back_populates="direccion")

    def __repr__(self):
        return f"<Direccion {self.calle} {self.numero}>"
