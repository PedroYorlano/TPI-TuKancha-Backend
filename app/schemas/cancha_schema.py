from app import ma
from app.models.cancha import Cancha

class CanchaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cancha
        exclude = ("reservas", "timeslots")  # Excluir relaciones que causan loops
        load_instance = True
        include_fk = True

cancha_schema = CanchaSchema()
canchas_schema = CanchaSchema(many=True)