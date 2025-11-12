from . import db
from datetime import datetime

class Partido(db.Model):
    __tablename__ = "partido"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    torneo_id = db.Column(db.Integer, db.ForeignKey("torneo.id"), nullable=False)
    equipo1_id = db.Column(db.Integer, db.ForeignKey("equipo.id"), nullable=False)
    equipo2_id = db.Column(db.Integer, db.ForeignKey("equipo.id"), nullable=False)
    goles_equipo1 = db.Column(db.Integer, nullable=False, default=0)
    goles_equipo2 = db.Column(db.Integer, nullable=False, default=0)
    cancha_id = db.Column(db.Integer, db.ForeignKey("cancha.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    equipo1 = db.relationship("Equipo", foreign_keys=[equipo1_id])
    equipo2 = db.relationship("Equipo", foreign_keys=[equipo2_id])
    torneo = db.relationship("Torneo", back_populates="partidos")
    cancha = db.relationship("Cancha", back_populates="partidos")

    def __repr__(self):
        return f"<Partido {self.equipo1.nombre} {self.goles_equipo1}-{self.goles_equipo2} {self.equipo2.nombre}>"