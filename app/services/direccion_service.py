from app.repositories.direccion_repo import DireccionRepository
from app.models.direccion import Direccion

class DireccionService:
    def __init__(self, db):
        self.db = db
        self.direccion_repo = DireccionRepository()

    def find_or_create_direccion(self, direccion_data):
        # Buscar por todos los campos relevantes
        direccion = Direccion.query.filter_by(
            calle=direccion_data['calle'],
            numero=direccion_data['numero'],
            ciudad=direccion_data.get('ciudad'),
            provincia=direccion_data.get('provincia'),
            codigo_postal=direccion_data.get('codigo_postal')
        ).first()
    
        # Si no existe, la creamos
        if not direccion:
            direccion = Direccion(**direccion_data)
            self.db.session.add(direccion)
            self.db.session.commit()
    
        return direccion
