from app.repositories.user_repo import UserRepository
from app.repositories.rol_repo import RolRepository
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash

class UserService:
    def __init__(self, db):
        self.db = db
        self.user_repo = UserRepository()
        self.rol_repo = RolRepository()
    
    def get_all(self):
        return self.user_repo.get_all()
    
    def get_by_id(self, id):
        return self.user_repo.get_by_id(id)
    
    def get_by_club(self, club_id):
        return self.user_repo.get_by_club(club_id)
    
    def create(self, data):
        required_fields = ['email', 'rol_id', 'nombre', 'password', 'club_id']

        for field in required_fields:
            if field not in data:
                raise ValueError(f"El campo '{field}' es requerido")

        if self.user_repo.get_by_email(data['email']):
            raise ValueError("El email ya está en uso")

        rol_id_recibido = data['rol_id']
        rol_en_db = self.rol_repo.get_by_id(rol_id_recibido)
        
        if not rol_en_db:
            raise ValueError(f"El rol_id '{rol_id_recibido}' no es válido o no existe.")

        password_plano = data['password']
        hash_pass = generate_password_hash(password_plano)
        
        try:
            nuevo_usuario = User(
                nombre=data['nombre'],
                email=data['email'],
                hash_password=hash_pass,
                rol_id=data['rol_id'],
                club_id=data['club_id'],
                telefono=data.get('telefono')  # Campo opcional
            )
            self.user_repo.create(nuevo_usuario)
            self.db.session.commit()
            return nuevo_usuario
        except ValueError as ve:
            self.db.session.rollback()
            raise ve
        except Exception as e:
            self.db.session.rollback()
            import traceback
            print("Error en user_service.create:")
            traceback.print_exc()
            # Capturar errores de integridad de la BD
            if 'UNIQUE constraint failed' in str(e) or 'Duplicate entry' in str(e):
                raise ValueError("El email ya está en uso")
            if 'FOREIGN KEY constraint failed' in str(e):
                raise ValueError(f"El club_id o rol_id no son válidos")
            raise Exception(f"Error al crear usuario: {str(e)}")
        
    
    def update(self, user_id, data):
        if not data:
            raise ValueError("No se proporcionaron datos para actualizar")
        
        usuario = self.user_repo.get_by_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        try:
            # Verificar email único si se está actualizando
            if 'email' in data and data['email'] != usuario.email:
                email_existente = self.user_repo.get_by_email(data['email'])
                if email_existente:
                    raise ValueError("El email ya está en uso por otro usuario")
            
            # Verificar rol_id si se está actualizando
            if 'rol_id' in data:
                rol_en_db = self.rol_repo.get_by_id(data['rol_id'])
                if not rol_en_db:
                    raise ValueError(f"El rol_id '{data['rol_id']}' no es válido o no existe.")

            if 'password' in data:
                password_plano = data.pop('password')
                usuario.hash_password = generate_password_hash(password_plano)
            
            for key, value in data.items():
                if hasattr(usuario, key) and key != 'id':
                    setattr(usuario, key, value)
            
            self.user_repo.update(usuario, data)
            self.db.session.commit()
            return usuario
        except ValueError as ve:
            self.db.session.rollback()
            raise ve
        except Exception as e:
            self.db.session.rollback()
            import traceback
            print("Error en user_service.update:")
            traceback.print_exc()
            raise Exception(f"Error al actualizar usuario: {str(e)}")
    
    def delete(self, user_id):
        usuario = self.user_repo.get_by_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        try:
            self.user_repo.delete(usuario)
            self.db.session.commit()
            return usuario
        except ValueError as ve:
            self.db.session.rollback()
            raise ve
        except Exception as e:
            self.db.session.rollback()
            import traceback
            print("Error en user_service.delete:")
            traceback.print_exc()
            raise Exception(f"Error al eliminar usuario: {str(e)}")