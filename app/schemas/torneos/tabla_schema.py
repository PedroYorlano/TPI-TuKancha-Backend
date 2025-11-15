from app import ma
from marshmallow import fields

class TablaPosicionesSchema(ma.Schema):
    """
    Schema para formatear la salida de la tabla de posiciones.
    No está ligado a un modelo de SQLAlchemy.
    """
    id = fields.Int()
    nombre = fields.Str()
    PJ = fields.Int() # Partidos Jugados
    PG = fields.Int() # Partidos Ganados
    PE = fields.Int() # Partidos Empatados
    PP = fields.Int() # Partidos Perdidos
    GF = fields.Int() # Goles a Favor
    GC = fields.Int() # Goles en Contra
    Puntos = fields.Int()

# Instancia para serializar una lista de equipos
tabla_posiciones_schema = TablaPosicionesSchema(many=True)