from app.models.timeslot_definicion import TimeslotDefinicion 
from app import db

class TimeslotDefinicionRepository: 
    def __init__(self): 
        self.db = db

    def get_activa_por_club(self, club_id: int): 
        return TimeslotDefinicion.query.filter_by(club_id=club_id, activo=True).first()

    def create(self, timeslot_definicion): 
        db.session.add(timeslot_definicion)
        return timeslot_definicion

    def update(self, timeslot_definicion, data):
        for key, value in data.items():
            setattr(timeslot_definicion, key, value)
        return timeslot_definicion

    def delete(self, timeslot_definicion):
        db.session.delete(timeslot_definicion)
