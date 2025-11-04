from . import db
from datetime import datetime


class CanchaBloqueo(db.Model):
    __tablename__ = "cancha_bloqueo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cancha_id = db.Column(db.Integer, db.ForeignKey("canchas.id"), nullable=False)
    inicio = db.Column(db.DateTime, nullable=False)
    fin = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(160))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    cancha = db.relationship("Cancha", backref="bloqueos")

    def __repr__(self):
        return f"<CanchaBloqueo cancha={self.cancha_id} {self.inicio}->{self.fin}>"
