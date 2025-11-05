from app.models.direccion import Direccion
from app import db

class DireccionRepository:
    def __init__(self):
        pass
    
    def get(self, calle, numero, ciudad, provincia):
        return Direccion.query.filter_by(calle=calle, numero=numero, ciudad=ciudad, provincia=provincia).first()
    
    def delete(self, direccion):
        db.session.delete(direccion)

    def find_or_create_direccion(self, direccion_data):
        direccion = self.get(direccion_data['calle'], direccion_data['numero'], direccion_data['ciudad'], direccion_data['provincia'])
        if not direccion:
            direccion = Direccion(**direccion_data)
            db.session.add(direccion)
        return direccion