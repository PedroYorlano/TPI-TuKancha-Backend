from app import ma
from app.models.cancha import Cancha
from app.schemas.club_schema import ClubSchema

class CanchaSchema(ma.SQLAlchemyAutoSchema):
    club = ma.Nested(ClubSchema)

    class Meta:
        model = Cancha
        fields = (
            "id", 
            "club", 
            "nombre", 
            "deporte", 
            "superficie", 
            "techado", 
            "iluminacion", 
            "precio_hora", 
            "activa"
        )
        load_instance = True
        include_relationships = True

cancha_schema = CanchaSchema()
canchas_schema = CanchaSchema(many=True)