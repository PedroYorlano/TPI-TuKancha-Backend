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
            "partidos_local",
            "partidos_visitante",
            "partidos_ganador",
            "created_at", 
            "updated_at"
        )
    
    torneo = ma.Nested('TorneoSchema', exclude=('equipos', 'partidos'))
    partidos_local = ma.Nested('PartidoSchema', exclude=('equipo1', 'equipo2', 'torneo', 'ganador'), many=True)
    partidos_visitante = ma.Nested('PartidoSchema', exclude=('equipo1', 'equipo2', 'torneo', 'ganador'), many=True)
    partidos_ganador = ma.Nested('PartidoSchema', exclude=('equipo1', 'equipo2', 'torneo', 'ganador'), many=True)

equipo_schema = EquipoSchema()
equipos_schema = EquipoSchema(many=True)