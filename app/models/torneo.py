from . import db
from datetime import datetime
from .enums import TorneoEstado

class Torneo(db.Model):
    __tablename__ = "torneo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(80))
    estado = db.Column(db.Enum(TorneoEstado, name="torneo_estado", native_enum=False), 
                      nullable=False, default=TorneoEstado.CREADO)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    reglamento = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    partidos = db.relationship("Partido", back_populates="torneo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Torneo {self.nombre} ({self.estado.value})>"