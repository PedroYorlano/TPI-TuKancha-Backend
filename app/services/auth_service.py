from werkzeug.security import check_password_hash
from app.repositories.user_repo import UserRepository
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


class AuthService:
    def __init__(self):
        """Inicializa el servicio de autenticación con un repositorio de usuarios."""
        self.user_repo = UserRepository()
    
    def login(self, email, password):
        """
        Autentica un usuario y genera tokens JWT.
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña en texto plano
            
        Returns:
            dict: Diccionario con:
                - access_token (str): Token JWT para autenticación
                - refresh_token (str): Token para renovar el access token
                - user (dict): Datos básicos del usuario
                
        Raises:
            ValueError: Si las credenciales son inválidas o el usuario está inactivo
        """
        # Buscar usuario por email
        user = self.user_repo.get_by_email(email)
        
        if not user:
            raise ValueError("Credenciales inválidas")
        
        # Verificar que el usuario esté activo
        if not user.activo:
            raise ValueError("Usuario inactivo")
        
        # Verificar contraseña
        if not check_password_hash(user.hash_password, password):
            raise ValueError("Credenciales inválidas")
        
        # Crear payload del JWT con información del usuario
        additional_claims = {
            "rol": user.rol.nombre,  # Nombre del rol (admin, encargado, etc.)
            "club_id": user.club_id,
            "club_nombre": user.club.nombre if user.club else None,
            "nombre": user.nombre,
            "email": user.email
        }
        
        # Generar tokens
        # Access token (corta duración - 1 hora)
        access_token = create_access_token(
            identity=str(user.id),  # Convertir a string
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=1)
        )
        
        # Refresh token (larga duración - 30 días)
        refresh_token = create_refresh_token(
            identity=str(user.id),  # Convertir a string
            expires_delta=timedelta(days=30)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "nombre": user.nombre,
                "email": user.email,
                "rol": user.rol.nombre,
                "club_id": user.club_id,
                "club_nombre": user.club.nombre if user.club else None
            }
        }
    
    def refresh_access_token(self, current_user_id):
        """
        Genera un nuevo access token usando el refresh token.
        
        Args:
            current_user_id (str): ID del usuario actual como string
            
        Returns:
            dict: Diccionario con el nuevo access_token y datos del usuario:
                - access_token (str): Nuevo token JWT de acceso
                - user (dict): Datos básicos del usuario
                
        Raises:
            ValueError: Si el usuario no existe o está inactivo
        """
        # Convertir string a int para buscar en BD
        user = self.user_repo.get_by_id(int(current_user_id))
        
        if not user or not user.activo:
            raise ValueError("Usuario no encontrado o inactivo")
        
        additional_claims = {
            "rol": user.rol.nombre,
            "club_id": user.club_id,
            "nombre": user.nombre,
            "email": user.email
        }
        
        access_token = create_access_token(
            identity=str(user.id),  # Convertir a string
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=1)
        )
        
        return {"access_token": access_token}
