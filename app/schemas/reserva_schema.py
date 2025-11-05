from app import ma
from app.models.reserva import Reserva
from app.schemas.club_schema import ClubSchema
from app.schemas.cancha_schema import CanchaSchema

class ReservaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        fields = (
            "id",
            "club", 
            "cancha", 
            "cliente_nombre", 
            "cliente_telefono", 
            "cliente_email", 
            "estado", 
            "fuente", 
            "observaciones", 
            "precio_total", 
            "senia_monto", 
            "senia_pagada", 
            "created_at", 
            "updated_at")
        load_instance = True
        include_relationships = True

    club = ma.Nested("ClubSchema", exclude=("reservas",))
    cancha = ma.Nested("CanchaSchema", exclude=("reservas",))

reserva_schema = ReservaSchema()
reservas_schema = ReservaSchema(many=True)
