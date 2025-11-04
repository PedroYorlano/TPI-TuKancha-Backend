from . import db
from datetime import datetime

class Cancha(db.Model):
    __tablename__ = 'canchas'
    
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    deporte = db.Column(db.String(50), nullable=False)
    superficie = db.Column(db.Float, nullable=False)
    techado = db.Column(db.Boolean, nullable=False)
    iluminacion = db.Column(db.Boolean, nullable=False)
    precio_hora = db.Column(db.Float, nullable=False)
    activa = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

