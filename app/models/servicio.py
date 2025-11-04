from . import db


servicios_por_reserva = db.Table(
    "servicios_por_reserva",
    db.Column("id_servicio", db.Integer, db.ForeignKey("servicio.id"), nullable=False),
    db.Column("id_reserva", db.Integer, db.ForeignKey("reserva.id"), nullable=False),
    db.PrimaryKeyConstraint("id_servicio", "id_reserva", name="pk_servicios_por_reserva")
)


class Servicio(db.Model):
    __tablename__ = "servicio"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), nullable=False)

    reservas = db.relationship("Reserva", secondary=servicios_por_reserva, backref="servicios")

    def __repr__(self):
        return f"<Servicio {self.nombre}>"
