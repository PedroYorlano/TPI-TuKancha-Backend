from . import db
from datetime import datetime
from .enums import ReservaEstado, FuenteReserva


class Reserva(db.Model):
    __tablename__ = "reserva"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cancha_id = db.Column(db.Integer, db.ForeignKey("cancha.id"), nullable=False)
    cliente_nombre = db.Column(db.String(120), nullable=False)
    cliente_telefono = db.Column(db.String(30))
    cliente_email = db.Column(db.String(120), nullable=False)
    estado = db.Column(db.Enum(ReservaEstado, name="reserva_estado", native_enum=False), nullable=False, default=ReservaEstado.PENDIENTE)
    fuente = db.Column(db.Enum(FuenteReserva, name="fuente_reserva", native_enum=False), nullable=False)
    servicios = db.Column(db.String(255))  # Lista de servicios separados por coma
    precio_total = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    cancha = db.relationship("Cancha", backref="reservas")
    timeslots = db.relationship("ReservaTimeslot", backref="reserva", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Reserva {self.id} {self.estado.value}>"
