from . import db
from datetime import datetime


class ReservaTimeslot(db.Model):
    __tablename__ = "reserva_timeslot"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reserva_id = db.Column(db.Integer, db.ForeignKey("reserva.id"), nullable=False, index=True)
    timeslot_id = db.Column(db.Integer, db.ForeignKey("timeslot.id"), nullable=False, unique=True)

    # backrefs created on Reserva and Timeslot

    def __repr__(self):
        return f"<ReservaTimeslot reserva={self.reserva_id} ts={self.timeslot_id}>"
