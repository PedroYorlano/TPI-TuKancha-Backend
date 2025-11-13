from app.models.torneo import Torneo
from app import ma

class TorneoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Torneo
        include_relationships = True
        load_instance = True
        fields = (
            "id",
            "club",
            "nombre",
            "categoria",
            "estado",
            "fecha_inicio",
            "fecha_fin",
            "reglamento",
            "equipos",
            "partidos",
            "created_at",
            "updated_at"
        )
    
    club = ma.Nested('ClubSchema', exclude=('torneos',))
    equipos = ma.Nested('EquipoSchema', exclude=('torneo',), many=True)
    partidos = ma.Nested('PartidoSchema', exclude=('torneo',), many=True)

torneo_schema = TorneoSchema()
torneos_schema = TorneoSchema(many=True)