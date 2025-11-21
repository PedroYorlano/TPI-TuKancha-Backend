from app.repositories.rol_repo import RolRepository
from app.models.rol import Rol
from app import db

from app.errors import ValidationError, NotFoundError, AppError, ConflictError

class RolService:
    def __init__(self, db):
        self.db = db
        self.rol_repo = RolRepository()
    
    def get_all(self):
        return self.rol_repo.get_all()
    
    def get_by_id(self, id):
        rol = self.rol_repo.get_by_id(id)
        if not rol:
            raise NotFoundError("No se encontraron roles")
        return rol

    def get_by_name(self, name):
        rol = self.rol_repo.get_by_name(name)
        if not rol:
            raise NotFoundError("No se encontraron roles")
        return rol
    
    def create(self, rol):
        required_fields = ['nombre']
        for field in required_fields:
            if field not in rol:
                raise ValidationError(f"El campo '{field}' es requerido")
        
        if self.rol_repo.get_by_name(rol['nombre']):
            raise ConflictError("El nombre ya está en uso")

        try:
            nuevo_rol = Rol(
                nombre=rol['nombre']
            )
            self.rol_repo.create(nuevo_rol)
            self.db.session.commit()
            return nuevo_rol
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al crear: {e}")

    
    def update(self, rol):
        required_fields = ['nombre']
        for field in required_fields:
            if field not in rol:
                raise ValidationError(f"El campo '{field}' es requerido")
        
        try:
            rol_actualizado = self.rol_repo.update(rol)
            self.db.session.commit()
            return rol_actualizado
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al actualizar: {e}")
    
    def delete(self, rol):
        required_fields = ['id']
        for field in required_fields:
            if field not in rol:
                raise ValidationError(f"El campo '{field}' es requerido")
            
        try:
            rol_actualizado = self.rol_repo.delete(rol)
            self.db.session.commit()
            return rol_actualizado
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al eliminar: {e}")
