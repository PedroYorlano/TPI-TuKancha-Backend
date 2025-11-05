from app import ma
from app.models.reserva import Reserva

class ReservaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        fields = (
            "id", 
            "fecha", 
            "hora", 
            "club_id", 
            "cancha_id", 
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

reserva_schema = ReservaSchema()
reservas_schema = ReservaSchema(many=True)
