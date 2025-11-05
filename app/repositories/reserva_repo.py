from app.models.reserva import Reserva
from app import db

class ReservaRepository:
    def __init__(self):
        pass
    
    def get_by_id(self, id):
        return Reserva.query.get(id)
    
    def get_all(self):
        return Reserva.query.all()
    
    def create(self, reserva):
        db.session.add(reserva)
        return reserva
    
    def update(self, reserva):
        db.session.add(reserva)
        return reserva
    
    def delete(self, reserva):
        db.session.delete(reserva)
