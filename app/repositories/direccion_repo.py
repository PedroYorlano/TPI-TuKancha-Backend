from app.models.direccion import Direccion
from app import db

class DireccionRepository:
    def __init__(self, db):
        self.db = db
    
    def get(self, calle, numero, ciudad, provincia):
        return Direccion.query.filter_by(calle=calle, numero=numero, ciudad=ciudad, provincia=provincia).first()
    
    def delete(self, direccion):
        self.db.session.delete(direccion)
        self.db.session.commit()

    def find_or_create_direccion(self, direccion_data):
        direccion = self.get(direccion_data['calle'], direccion_data['numero'], direccion_data['ciudad'], direccion_data['provincia'])
        if not direccion:
            direccion = Direccion(**direccion_data)
            self.db.session.add(direccion)
            self.db.session.commit()
        return direccion