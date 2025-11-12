from app.models.torneo import Equipo
from app import ma
from app.schemas.torneos.torneo_schema import TorneoSchema

class EquipoSchema(ma.SQLAlchemyAutoSchema):
    torneo = ma.Nested(TorneoSchema)
    
    class Meta:
        model = Equipo
        include_relationships = True
        load_instance = True
        fields = (
            "id", 
            "torneo", 
            "nombre", 
            "representante", 
            "telefono", 
            "email", 
            "created_at", 
            "updated_at"
        )
    
equipo_schema = EquipoSchema()
equipos_schema = EquipoSchema(many=True)