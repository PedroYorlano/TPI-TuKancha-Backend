from app.models.equipo import Equipo
from app import ma

class EquipoSchema(ma.SQLAlchemyAutoSchema):
    torneo = ma.Nested('TorneoSchema', exclude=('equipos',), many=False)
    
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

from app.schemas.torneos.torneo_schema import TorneoSchema