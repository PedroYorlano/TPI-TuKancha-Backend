from app import ma
from app.models.reserva import Reserva
from app.schemas.cancha_schema import CanchaSchema

class ReservaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        fields = (
            "id",
            "cancha", 
            "cliente_nombre", 
            "cliente_telefono", 
            "cliente_email", 
            "estado", 
            "fuente", 
            "servicios", 
            "precio_total", 
            "created_at", 
            "updated_at")
        load_instance = True
        include_relationships = True

    cancha = ma.Nested("CanchaSchema", exclude=("reservas",))

reserva_schema = ReservaSchema()
reservas_schema = ReservaSchema(many=True)
