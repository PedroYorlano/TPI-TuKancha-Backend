from app.repositories.club_repo import ClubRepository
from app.models.club import Club
from app.repositories.direccion_repo import DireccionRepository
from app.repositories.club_horario_repo import ClubHorarioRepository
from app.models.club_horario import ClubHorario
from app.repositories.user_repo import UserRepository
from app.repositories.rol_repo import RolRepository
from app.models.user import User
from app.models.torneo import Torneo
from app.models.timeslot import Timeslot
from app.models.cancha import Cancha
from app.models.enums import DiaSemana, TorneoEstado, TimeslotEstado
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db

from app.errors import AppError, ConflictError, NotFoundError, ValidationError

class ClubService:
    """
    Servicio para la gestión de clubes deportivos.
    
    Este servicio maneja la lógica de negocio relacionada con los clubes,
    incluyendo su creación, actualización, eliminación y consulta,
    así como la gestión de sus relaciones con direcciones, horarios y usuarios.
    """
    
    # Mapeo de días en español a enum DiaSemana
    DIA_MAPPING = {
        'lunes': DiaSemana.LUN,
        'martes': DiaSemana.MAR,
        'miércoles': DiaSemana.MIE,
        'miercoles': DiaSemana.MIE,  # Sin acento
        'jueves': DiaSemana.JUE,
        'viernes': DiaSemana.VIE,
        'sábado': DiaSemana.SAB,
        'sabado': DiaSemana.SAB,  # Sin acento
        'domingo': DiaSemana.DOM
    }
    
    def __init__(self, db):
        """
        Inicializa el servicio de clubes con los repositorios necesarios.
        
        Args:
            db: Instancia de la base de datos SQLAlchemy
        """
        self.db = db
        self.club_repo = ClubRepository()
        self.direccion_repo = DireccionRepository()
        self.club_horario_repo = ClubHorarioRepository()
        self.user_repo = UserRepository()
        self.rol_repo = RolRepository()

    def get_all(self):
        """
        Obtiene todos los clubes registrados en el sistema.
        
        Returns:
            list[Club]: Lista de todos los clubes
        """
        clubes = self.club_repo.get_all()
        if not clubes:
            raise NotFoundError("No se encontraron clubes")
        return clubes

    def get_by_id(self, id):
        """
        Obtiene un club por su ID.
        
        Args:
            id (int): ID del club a buscar
            
        Returns:
            Club: El club encontrado o None si no existe
            
        Raises:
            ValueError: Si el ID no es válido
        """
        club = self.club_repo.get_by_id(id)
        if not club:
            raise NotFoundError("Club no encontrado")
        return club

    def create(self, data):
        """
        Crea un nuevo club con toda su información asociada.
        
        Este método realiza una transacción atómica que incluye:
        1. Creación de la dirección del club
        2. Creación del club
        3. Creación de los horarios del club (si se proporcionan)
        4. Creación del usuario administrador del club
        
        Args:
            data (dict): Datos del club a crear. Debe incluir:
                - nombre (str): Nombre del club
                - cuit (str): CUIT del club
                - telefono (str): Teléfono de contacto
                - direccion (dict): Datos de la dirección
                - usuario (dict): Datos del usuario administrador
                - horarios (list[dict], opcional): Lista de horarios del club
                
        Returns:
            Club: El club recién creado
            
        Raises:
            ValueError: Si faltan campos requeridos o los datos son inválidos
            Exception: Si ocurre un error durante la creación
        """
        required_fields = ['nombre', 'cuit', 'telefono', 'direccion', 'usuario']
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"El campo '{field}' es requerido")

        # Validar campos requeridos de dirección
        required_direccion_fields = ['calle', 'numero', 'ciudad', 'provincia']
        for field in required_direccion_fields:
            if field not in data['direccion'] or not data['direccion'][field]:
                raise ValidationError(f"El campo 'direccion.{field}' es requerido")

        # Validar campos requeridos de usuario
        required_usuario_fields = ['nombre', 'email', 'password', 'rol']
        for field in required_usuario_fields:
            if field not in data['usuario'] or not data['usuario'][field]:
                raise ValidationError(f"El campo 'usuario.{field}' es requerido")

        # Validar que el email no esté en uso
        if self.user_repo.get_by_email(data['usuario']['email']):
            raise ConflictError("El email ya está en uso")

        try:
            # PASO 1: Crear la dirección
            direccion_data = data.pop('direccion')
            direccion = self.direccion_repo.find_or_create_direccion(direccion_data)

            # PASO 2: Crear el club
            nuevo_club = Club(
                nombre=data['nombre'],
                cuit=data['cuit'],
                telefono=data['telefono'],
                direccion=direccion 
            )
            self.club_repo.create(nuevo_club)
            self.db.session.flush()  # Para obtener el ID del club

            # PASO 3: Crear los horarios del club (si se proporcionan)
            if 'horarios' in data and data['horarios']:
                for horario_data in data['horarios']:
                    # Validar campos requeridos
                    if 'dia' not in horario_data or 'abre' not in horario_data or 'cierra' not in horario_data:
                        raise ValidationError("Cada horario debe tener 'dia', 'abre' y 'cierra'")
                    
                    # Convertir el día de español a enum
                    dia_str = horario_data['dia'].lower()
                    dia_enum = self.DIA_MAPPING.get(dia_str)
                    if not dia_enum:
                        raise ValidationError(f"Día inválido: {horario_data['dia']}. Debe ser uno de: {', '.join(self.DIA_MAPPING.keys())}")
                    
                    # Convertir strings de hora a objetos time
                    try:
                        abre = datetime.strptime(horario_data['abre'], '%H:%M').time()
                        cierra = datetime.strptime(horario_data['cierra'], '%H:%M').time()
                    except ValueError as e:
                        raise ValidationError(f"Formato de hora inválido. Use HH:MM (ej: 09:00)")
                    
                    # Validar que abre sea antes que cierra
                    if abre >= cierra:
                        raise ValidationError(f"La hora de apertura debe ser anterior a la de cierre para {horario_data['dia']}")
                    
                    # Crear el horario
                    nuevo_horario = ClubHorario(
                        club_id=nuevo_club.id,
                        dia=dia_enum,
                        abre=abre,
                        cierra=cierra
                    )
                    self.club_horario_repo.create(nuevo_horario)

            # PASO 4: Crear el usuario administrador del club
            usuario_data = data.pop('usuario')
            
            # Obtener el rol por nombre
            rol_nombre = usuario_data['rol'].lower()
            rol = self.rol_repo.get_by_name(rol_nombre)
            if not rol:
                raise ValidationError(f"El rol '{usuario_data['rol']}' no existe en el sistema")
            
            # Hash de la contraseña
            hash_password = generate_password_hash(usuario_data['password'])
            
            # Crear el usuario
            nuevo_usuario = User(
                nombre=usuario_data['nombre'],
                email=usuario_data['email'],
                hash_password=hash_password,
                rol_id=rol.id,
                club_id=nuevo_club.id,
                telefono=usuario_data.get('telefono')  # Opcional
            )
            self.user_repo.create(nuevo_usuario)

            # Commit de toda la transacción
            self.db.session.commit()    

            return nuevo_club
        
        except ValidationError as e:
            self.db.session.rollback()
            raise e
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al crear el club: {str(e)}")
        
    def update(self, club_id, data):
        """
        Actualiza los datos de un club existente.
        
        Permite actualizar los datos básicos del club y su dirección.
        
        Args:
            club_id (int): ID del club a actualizar
            data (dict): Datos a actualizar. Puede incluir:
                - nombre (str, opcional): Nuevo nombre del club
                - cuit (str, opcional): Nuevo CUIT
                - telefono (str, opcional): Nuevo teléfono
                - direccion (dict, opcional): Nueva dirección
                
        Returns:
            Club: El club actualizado
            
        Raises:
            ValueError: Si el club no existe
            Exception: Si ocurre un error durante la actualización
        """
        # Obtener el club existente
        club = self.club_repo.get_by_id(club_id)
        if not club:
            raise NotFoundError("Club no encontrado")
        
        # Manejar la actualización de dirección si se proporciona
        try:
            if 'direccion' in data:
                direccion_data = data.pop('direccion')
                direccion = self.direccion_repo.find_or_create_direccion(direccion_data)
                club.direccion_id = direccion.id
        except Exception as e:
            raise AppError(f"Error al actualizar dirección: {e}")

        for key, value in data.items():
            if hasattr(club, key):
                setattr(club, key, value)
        
        try:
            self.club_repo.update(club, data)
            self.db.session.commit()
            return club
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al actualizar: {e}")

    def delete(self, club_id):
        club = self.get_by_id(club_id)
        
        try:
            # VALIDACIONES DE LÓGICA DE NEGOCIO
            
            torneos_activos = db.session.query(Torneo).filter_by(
                club_id=club_id, 
                estado=TorneoEstado.ACTIVO
            ).first()
            if torneos_activos:
                raise ConflictError(f"No se puede eliminar el club. Tiene torneos activos ('{torneos_activos.nombre}').")

            reservas_futuras = db.session.query(Timeslot)\
                .join(Cancha, Timeslot.cancha_id == Cancha.id)\
                .filter(
                    Cancha.club_id == club_id,
                    Timeslot.estado.in_([TimeslotEstado.RESERVADO, TimeslotEstado.PAGADO]),
                    Timeslot.inicio >= datetime.utcnow()
                ).first()
            
            if reservas_futuras:
                raise ConflictError("No se puede eliminar el club. Tiene reservas futuras activas.")

            # Ejecutar el borrado
            self.club_repo.delete(club)            
            self.db.session.commit()
            return club 
            
        except (NotFoundError, ConflictError) as e:
            self.db.session.rollback()
            raise e
        except Exception as e:
            # Si es un error inesperado (ej: fallo de DB)
            self.db.session.rollback()
            raise AppError(f"Error al eliminar el club: {str(e)}")

