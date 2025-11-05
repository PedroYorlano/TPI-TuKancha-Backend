from app.models.cancha import Cancha
from app import db

class CanchaRepository:
    def get_by_predio(predio_id):
        return Cancha.query.filter_by(predio_id=predio_id).all()

    def get_by_id(cancha_id):
        return Cancha.query.get(cancha_id)

    def create(cancha_data):
        cancha = Cancha(**cancha_data)
        db.session.add(cancha)
        return cancha

    def update(cancha, cancha_data):
        for key, value in cancha_data.items():
            setattr(cancha, key, value)
        return cancha

    def delete(cancha):
        db.session.delete(cancha)