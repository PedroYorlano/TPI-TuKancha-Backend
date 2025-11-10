from app.models.rol import Rol
from app import db

class RolRepository:
    def get_all(self):
        return Rol.query.all()
    
    def get_by_id(self, id):
        return db.session.get(Rol, id)

    def get_by_name(self, name):
        return Rol.query.filter_by(nombre=name).first()
    
    def create(self, rol):
        db.session.add(rol)
        return rol
    
    def update(self, rol):
        for key, value in rol.items():
            setattr(rol, key, value)
        db.session.add(rol)
        return rol
    
    def delete(self, rol):
        db.session.delete(rol)

