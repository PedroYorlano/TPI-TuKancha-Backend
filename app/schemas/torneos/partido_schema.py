from app.models.partido import Partido
from app import ma

class PartidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Partido
        include_relationships = True
        load_instance = True
        fields = (
            "id",
            "torneo",
            "equipo1",
            "equipo2",
            "goles_equipo1",
            "goles_equipo2",
            "created_at",
            "updated_at"
        )
    
    torneo = ma.Nested('TorneoSchema', exclude=('partidos', 'equipos'))
    equipo1 = ma.Nested('EquipoSchema', exclude=('partidos_local', 'partidos_visitante', 'torneo'))
    equipo2 = ma.Nested('EquipoSchema', exclude=('partidos_local', 'partidos_visitante', 'torneo'))

partido_schema = PartidoSchema()
partidos_schema = PartidoSchema(many=True)