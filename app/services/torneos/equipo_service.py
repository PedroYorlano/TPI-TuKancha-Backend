from app.repositories.torneos.equipo_repo import EquipoRepository
from app.models.equipo import Equipo
from app import db
from datetime import datetime

class EquipoService:
    """
    Servicio para la gestión de equipos en torneos
    """
    
    def __init__(self, db_session):
        """
        Inicializa el servicio con la sesión de base de datos
        """
        self.db = db_session
        self.equipo_repo = EquipoRepository()
    
    def get_all(self):
        """
        Obtiene todos los equipos
        
        Returns:
            list[Equipo]: Lista de todos los equipos
        """
        return self.equipo_repo.get_all()
    
    def get_by_id(self, equipo_id):
        """
        Obtiene un equipo por su ID
        
        Args:
            equipo_id (int): ID del equipo a buscar
            
        Returns:
            Equipo: El equipo encontrado o None
        """
        return self.equipo_repo.get_by_id(equipo_id)
    
    def get_by_torneo(self, torneo_id):
        """
        Obtiene todos los equipos de un torneo específico
        
        Args:
            torneo_id (int): ID del torneo
            
        Returns:
            list[Equipo]: Lista de equipos del torneo
        """
        return self.equipo_repo.get_by_torneo(torneo_id)
    
    def create(self, equipo_data):
        """
        Crea un nuevo equipo
        
        Args:
            equipo_data (dict): Datos del equipo a crear
            
        Returns:
            Equipo: El equipo creado
            
        Raises:
            ValueError: Si faltan campos requeridos o el equipo ya existe
        """
        # Validar campos requeridos
        required_fields = ['nombre', 'torneo_id']
        for field in required_fields:
            if field not in equipo_data or not equipo_data[field]:
                raise ValueError(f"El campo '{field}' es requerido")
        
        # Verificar si ya existe un equipo con el mismo nombre en el torneo
        if self.equipo_repo.existe_equipo_en_torneo(equipo_data['nombre'], equipo_data['torneo_id']):
            raise ValueError("Ya existe un equipo con este nombre en el torneo")
        
        try:
            # Crear una instancia de Equipo con los datos
            equipo = Equipo(
                nombre=equipo_data['nombre'],
                torneo_id=equipo_data['torneo_id'],
                representante=equipo_data.get('representante'),
                telefono=equipo_data.get('telefono'),
                email=equipo_data.get('email')
            )
            
            # Guardar el equipo en la base de datos
            equipo = self.equipo_repo.create(equipo)
            self.db.session.commit()
            return equipo
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al crear el equipo: {str(e)}")
    
    def update(self, equipo_id, equipo_data):
        """
        Actualiza un equipo existente
        
        Args:
            equipo_id (int): ID del equipo a actualizar
            equipo_data (dict): Datos a actualizar
            
        Returns:
            Equipo: El equipo actualizado
            
        Raises:
            ValueError: Si el equipo no existe o hay datos inválidos
        """
        equipo = self.equipo_repo.get_by_id(equipo_id)
        if not equipo:
            raise ValueError("Equipo no encontrado")
        
        # Verificar si se está intentando cambiar el nombre y ya existe otro con el mismo nombre
        if 'nombre' in equipo_data and equipo_data['nombre'] != equipo.nombre:
            if self.equipo_repo.existe_equipo_en_torneo(
                equipo_data['nombre'], 
                equipo.torneo_id, 
                exclude_id=equipo_id
            ):
                raise ValueError("Ya existe otro equipo con este nombre en el torneo")
        
        try:
            # Actualizar el equipo
            equipo_actualizado = self.equipo_repo.update(equipo, equipo_data)
            self.db.session.commit()
            return equipo_actualizado
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al actualizar el equipo: {str(e)}")
    
    def delete(self, equipo_id):
        """
        Elimina un equipo
        
        Args:
            equipo_id (int): ID del equipo a eliminar
            
        Raises:
            ValueError: Si el equipo no existe
        """
        equipo = self.equipo_repo.get_by_id(equipo_id)
        if not equipo:
            raise ValueError("Equipo no encontrado")
        
        try:
            self.equipo_repo.delete(equipo)
            self.db.session.commit()
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al eliminar el equipo: {str(e)}")
