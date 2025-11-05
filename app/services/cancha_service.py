from app.repositories.cancha_repo import CanchaRepository

class CanchaService:
    def __init__(self, db):
        self.db = db

    def get_by_predio(self, predio_id):
        return CanchaRepository.get_by_predio(predio_id)

    def get_by_id(self, cancha_id):
        return CanchaRepository.get_by_id(cancha_id)

    def create(self, data):
        return CanchaRepository.create(data)

    def update(self, cancha, data):
        return CanchaRepository.update(cancha, data)

    def delete(self, cancha):
        return CanchaRepository.delete(cancha)