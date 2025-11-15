from . import db
from datetime import datetime

class Club(db.Model):
    __tablename__ = 'club'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cuit = db.Column(db.String(13), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion_id = db.Column(db.Integer, db.ForeignKey('direccion.id'), nullable=False)
    direccion = db.relationship("Direccion", back_populates="clubes", lazy=True)
    canchas = db.relationship("Cancha", backref="club", lazy=True, cascade="all, delete-orphan")
    torneos = db.relationship("Torneo", backref="club", lazy=True, cascade="all, delete-orphan")
    horarios = db.relationship('ClubHorario', back_populates='club', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    usuarios = db.relationship(
        "User", 
        back_populates="club", 
        lazy=True, 
        cascade="all, delete-orphan"
    )
