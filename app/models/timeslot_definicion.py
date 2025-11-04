from . import db
from datetime import datetime


class TimeslotDefinicion(db.Model):
    __tablename__ = "timeslot_definicion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=False)
    duracion_minutos = db.Column(db.Integer, nullable=False)
    paso_minutos = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    club = db.relationship("Club", backref="ts_defs")

    def __repr__(self):
        return f"<TimeslotDef club={self.club_id} dur={self.duracion_minutos} paso={self.paso_minutos}>"
