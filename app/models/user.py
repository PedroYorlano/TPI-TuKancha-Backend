from . import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=True)
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(30))
    hash_password = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    club = db.relationship("Club", backref="usuarios")

    def __repr__(self):
        return f"<User {self.email}>"
