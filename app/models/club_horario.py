from . import db
from datetime import time, datetime
from .enums import DiaSemana


class ClubHorario(db.Model):
    __tablename__ = "club_horario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=False)
    dia = db.Column(db.Enum(DiaSemana, name="dia_semana", native_enum=False), nullable=False)
    abre = db.Column(db.Time, nullable=False)
    cierra = db.Column(db.Time, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    club = db.relationship("Club", backref="horarios")

    def __repr__(self):
        return f"<ClubHorario {self.dia.value} {self.abre}-{self.cierra}>"
