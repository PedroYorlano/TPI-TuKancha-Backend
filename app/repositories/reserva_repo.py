from app.models.reserva import Reserva
from app.models.cancha import Cancha
from app import db

class ReservaRepository:
    def __init__(self):
        pass
    
    def get_by_id(self, id):
        return db.session.get(Reserva, id)
    
    def get_all(self):
        return Reserva.query.all()
    
    def get_by_club_id(self, club_id):
        """
        Obtiene todas las reservas de un club específico.
        """
        reservas = Reserva.query.join(Cancha).filter(Cancha.club_id == club_id).all()
        return reservas
    
    def create(self, reserva):
        db.session.add(reserva)
        return reserva
    
    def update(self, reserva, data):
        for key, value in data.items():
            setattr(reserva, key, value)
        db.session.add(reserva)
        return reserva
    
    def delete(self, reserva):
        db.session.delete(reserva)
