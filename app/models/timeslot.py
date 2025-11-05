from . import db
from datetime import datetime
from .enums import TimeslotEstado


class Timeslot(db.Model):
    __tablename__ = "timeslot"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cancha_id = db.Column(db.Integer, db.ForeignKey("cancha.id"), nullable=False)
    inicio = db.Column(db.DateTime, nullable=False)
    fin = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Enum(TimeslotEstado, name="timeslot_estado", native_enum=False), nullable=False, default=TimeslotEstado.DISPONIBLE)
    precio = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    reserva = db.relationship("ReservaTimeslot", backref="timeslot", uselist=False)

    def __repr__(self):
        return f"<Timeslot cancha={self.cancha_id} {self.inicio}-{self.fin} {self.estado.value}>"
