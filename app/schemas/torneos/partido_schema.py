from app.models.partido import Partido
from app import ma

class PartidoSchema(ma.SQLAlchemyAutoSchema):
    equipo1 = ma.Nested('EquipoSchema', exclude=('partidos',), many=False)
    equipo2 = ma.Nested('EquipoSchema', exclude=('partidos',), many=False)
    torneo = ma.Nested('TorneoSchema', exclude=('partidos',), many=False)
    cancha = ma.Nested('CanchaSchema', exclude=('partidos',), many=False)
    
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
            "cancha",
            "created_at",
            "updated_at"
        )
    
partido_schema = PartidoSchema()
partidos_schema = PartidoSchema(many=True)

# Importaciones al final para evitar referencias circulares
from app.schemas.torneos.equipo_schema import EquipoSchema
from app.schemas.torneos.torneo_schema import TorneoSchema
from app.schemas.cancha_schema import CanchaSchema
