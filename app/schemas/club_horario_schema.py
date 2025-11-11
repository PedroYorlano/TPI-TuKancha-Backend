from app import ma
from app.models.club_horario import ClubHorario
from marshmallow import fields


class ClubHorarioSchema(ma.SQLAlchemyAutoSchema):
    # Convertir el enum DiaSemana a string para la salida
    dia = fields.Method("get_dia_nombre")
    # Convertir time a string en formato HH:MM
    abre = fields.Method("get_abre_str")
    cierra = fields.Method("get_cierra_str")
    
    class Meta:
        model = ClubHorario
        fields = ("id", "dia", "abre", "cierra", "activo")
        load_instance = True
    
    def get_dia_nombre(self, obj):
        """Convierte el enum a nombre completo en español"""
        dia_map = {
            'LUN': 'Lunes',
            'MAR': 'Martes',
            'MIE': 'Miércoles',
            'JUE': 'Jueves',
            'VIE': 'Viernes',
            'SAB': 'Sábado',
            'DOM': 'Domingo'
        }
        return dia_map.get(obj.dia.value, obj.dia.value)
    
    def get_abre_str(self, obj):
        """Convierte time a string HH:MM"""
        return obj.abre.strftime('%H:%M') if obj.abre else None
    
    def get_cierra_str(self, obj):
        """Convierte time a string HH:MM"""
        return obj.cierra.strftime('%H:%M') if obj.cierra else None


club_horario_schema = ClubHorarioSchema()
club_horarios_schema = ClubHorarioSchema(many=True)
