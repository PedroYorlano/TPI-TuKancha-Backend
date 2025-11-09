from app.models.cancha import Cancha
from app import db

class CanchaRepository:
    def get_all(self):
        return Cancha.query.all()
    
    def get_by_predio(self, predio_id):
        return Cancha.query.filter_by(predio_id=predio_id).all()

    def get_by_id(self, cancha_id):
        return Cancha.query.get(cancha_id)

    def create(self, cancha):
        db.session.add(cancha)
        return cancha

    def update(self, cancha, data):
        for key, value in data.items():
            setattr(cancha, key, value)
        return cancha

    def delete(self, cancha):
        db.session.delete(cancha)