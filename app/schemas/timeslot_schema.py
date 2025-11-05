from app import ma
from app.models.timeslot import Timeslot

class TimeslotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Timeslot
        fields = (
            "id", 
            "cancha_id", 
            "inicio", 
            "fin", 
            "estado", 
            "precio", 
            "created_at", 
            "updated_at")
        load_instance = True
    
    
timeslot_schema = TimeslotSchema()
timeslots_schema = TimeslotSchema(many=True)

