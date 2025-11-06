from app.repositories.cancha_repo import CanchaRepository

class CanchaService:
    def __init__(self, db):
        self.db = db
        self.cancha_repo = CanchaRepository()

    def get_all(self):
        return self.cancha_repo.get_all()

    def get_by_predio(self, predio_id):
        return self.cancha_repo.get_by_predio(predio_id)

    def get_by_id(self, cancha_id):
        return self.cancha_repo.get_by_id(cancha_id)

    def create(self, data):
        required_fields = ['nombre', 'tipo', 'precio', 'predio_id']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"El campo '{field}' es requerido")
        try:
            self.cancha_repo.create(data)
            self.db.session.commit()
            return data
        except Exception as e:
            self.db.session.rollback()
            raise e

    def update(self, cancha, data):
        required_fields = ['nombre', 'tipo', 'precio', 'predio_id']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"El campo '{field}' es requerido")
        try:
            self.cancha_repo.update(cancha, data)
            self.db.session.commit()
            return data
        except Exception as e:
            self.db.session.rollback()
            raise e

    def delete(self, cancha):
        try:
            self.cancha_repo.delete(cancha)
            self.db.session.commit()
            return cancha
        except Exception as e:
            self.db.session.rollback()
            raise e