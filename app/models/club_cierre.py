from . import db
from datetime import date, datetime


class ClubCierre(db.Model):
    __tablename__ = "club_cierre"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    abre = db.Column(db.Time)
    cierra = db.Column(db.Time)
    cerrado = db.Column(db.Boolean, default=False)
    motivo = db.Column(db.String(160))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    club = db.relationship("Club", backref="cierres")

    def __repr__(self):
        return f"<ClubCierre {self.fecha} cerrado={self.cerrado}>"
