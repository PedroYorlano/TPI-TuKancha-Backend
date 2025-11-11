from app import ma
from app.models.club import Club
from app.schemas.direccion_schema import DireccionSchema
from app.schemas.club_horario_schema import ClubHorarioSchema


class ClubSchema(ma.SQLAlchemyAutoSchema):
    direccion = ma.Nested(DireccionSchema)
    horarios = ma.Nested(ClubHorarioSchema, many=True)  # Incluir horarios

    class Meta:
        model = Club
        fields = ("id", "nombre", "cuit", "telefono", "direccion", "horarios")
        load_instance = True 
        include_relationships = True 

club_schema = ClubSchema()
clubes_schema = ClubSchema(many=True)