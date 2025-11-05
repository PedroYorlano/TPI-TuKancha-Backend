from app.models.timeslot_definicion import TimeslotDefinicion 
from app import db

class TimeslotDefinicionRepository: 
    def __init__(self): 
        self.db = db

    def get_activa_por_club(self, club_id: int): 
        return TimeslotDefinicion.query.filter_by(club_id=club_id, activo=True).first()
