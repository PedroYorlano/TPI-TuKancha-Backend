from app import ma
from app.models.club import Club
from app.schemas.direccion_schema import DireccionSchema 

class ClubSchema(ma.SQLAlchemyAutoSchema):
    direccion = ma.Nested(DireccionSchema) 

    class Meta:
        model = Club
        fields = ("id", "nombre", "cuit", "telefono", "direccion") 
        load_instance = True 
        include_relationships = True 

club_schema = ClubSchema()
clubes_schema = ClubSchema(many=True)