from app.models.equipo import Equipo
from app import ma

class EquipoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Equipo
        include_relationships = True
        load_instance = True
        fields = (
            "id", 
            "nombre", 
            "representante", 
            "telefono", 
            "email", 
            "torneo",
            "created_at", 
            "updated_at"
        )
    
    torneo = ma.Nested('TorneoSchema', exclude=('equipos', 'partidos'))

equipo_schema = EquipoSchema()
equipos_schema = EquipoSchema(many=True)