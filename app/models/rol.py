from . import db


class Rol(db.Model):
    __tablename__ = "rol"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(40), nullable=False)

    usuarios = db.relationship("User", backref="rol")

    def __repr__(self):
        return f"<Rol {self.nombre}>"
