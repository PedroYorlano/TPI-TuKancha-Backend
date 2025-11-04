from app.models.direccion import Direccion
from app import db

class DireccionRepository:
    def __init__(self):
        pass
    
    def get_all(self):
        return Direccion.query.all()
    
    def get_by_id(self, id):
        return Direccion.query.get(id)
    
    def create(self, direccion):
        self.db.session.add(direccion)
        self.db.session.commit()
        return direccion
    
    def update(self, direccion):
        self.db.session.commit()
        return direccion
    
    def delete(self, direccion):
        self.db.session.delete(direccion)
        self.db.session.commit()
