from app.models.torneo import Torneo
from app import ma
from app.schemas.club_schema import ClubSchema

class TorneoSchema(ma.SQLAlchemyAutoSchema):
    club = ma.Nested(ClubSchema)
    equipos = ma.Nested('EquipoSchema', exclude=('torneo',), many=True)
    
    class Meta:
        model = Torneo
        include_relationships = True
        load_instance = True
        fields = (
            "id", 
            "club", 
            "equipos", 
            "nombre", 
            "categoria", 
            "estado", 
            "fecha_inicio", 
            "fecha_fin", 
            "reglamento", 
            "created_at", 
            "updated_at"
        )
        
torneo_schema = TorneoSchema()
torneos_schema = TorneoSchema(many=True)

from app.schemas.torneos.equipo_schema import EquipoSchema