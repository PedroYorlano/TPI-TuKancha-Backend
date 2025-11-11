from app.repositories.cancha_repo import CanchaRepository
from app.models.cancha import Cancha


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
        # Campos requeridos según el modelo Cancha
        required_fields = ['nombre', 'deporte', 'superficie', 'techado', 'iluminacion', 'precio_hora', 'club_id']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"El campo '{field}' es requerido")
        
        try:
            # Crear instancia de Cancha
            nueva_cancha = Cancha(
                nombre=data['nombre'],
                deporte=data['deporte'],
                superficie=data['superficie'],
                techado=data['techado'],
                iluminacion=data['iluminacion'],
                precio_hora=data['precio_hora'],
                club_id=data['club_id'],
                activa=data.get('activa', True)  # Por defecto True si no se especifica
            )
            
            self.cancha_repo.create(nueva_cancha)
            self.db.session.commit()
            return nueva_cancha
            
        except ValueError as e:
            self.db.session.rollback()
            raise e
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al crear la cancha: {e}")

    def update(self, cancha_id, data):
        cancha = self.cancha_repo.get_by_id(cancha_id)
        
        if not cancha:
            raise ValueError("Cancha no encontrada")
        
        try:
            # Actualizar solo los campos que vienen en data
            if 'nombre' in data:
                cancha.nombre = data['nombre']
            if 'deporte' in data:
                cancha.deporte = data['deporte']
            if 'superficie' in data:
                cancha.superficie = data['superficie']
            if 'techado' in data:
                cancha.techado = data['techado']
            if 'iluminacion' in data:
                cancha.iluminacion = data['iluminacion']
            if 'precio_hora' in data:
                cancha.precio_hora = data['precio_hora']
            if 'activa' in data:
                cancha.activa = data['activa']
            if 'club_id' in data:
                cancha.club_id = data['club_id']
            
            self.cancha_repo.update(cancha, data)
            self.db.session.commit()
            return cancha
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al actualizar la cancha: {e}")

    def delete(self, cancha_id):
        cancha = self.cancha_repo.get_by_id(cancha_id)
        
        if not cancha:
            raise ValueError("Cancha no encontrada")
        
        try:
            self.cancha_repo.delete(cancha)
            self.db.session.commit()
            return cancha
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al eliminar la cancha: {e}")