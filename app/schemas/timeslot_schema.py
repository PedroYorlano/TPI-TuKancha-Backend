from app import ma
from app.models.timeslot import Timeslot
from app.schemas.cancha_schema import cancha_schema

class TimeslotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Timeslot
        fields = (
            "id",
            "cancha",
            "inicio",
            "fin",
            "estado",
            "precio",
            "created_at",
            "updated_at")
        load_instance = True
    
    cancha = ma.Nested(cancha_schema, exclude=("timeslots",))
    
timeslot_schema = TimeslotSchema()
timeslots_schema = TimeslotSchema(many=True)

