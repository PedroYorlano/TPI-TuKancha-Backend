from app.repositories.torneos.partido_repo import PartidoRepository
from app.models.partido import Partido
from app import db
from datetime import datetime

class PartidoService:
    """
    Servicio para la gestión de partidos en torneos
    """
    
    def __init__(self, db):
        """
        Inicializa el servicio con la sesión de base de datos
        """
        self.db = db
        self.partido_repo = PartidoRepository()
    
    def get_all(self):
        """
        Obtiene todos los partidos
        """
        return self.partido_repo.get_all()
    
    def get_by_id(self, partido_id):
        """
        Obtiene un partido por su ID
        """
        return self.partido_repo.get_by_id(partido_id)
    
    def get_by_torneo(self, torneo_id):
        """
        Obtiene todos los partidos de un torneo específico
        """
        return self.partido_repo.get_by_torneo(torneo_id)
    
    def create(self, partido_data):
        """
        Crea un nuevo partido
        """
        required_fields = ['torneo_id', 'equipo1_id', 'equipo2_id']
        for field in required_fields:
            if field not in partido_data or not partido_data[field]:
                raise ValueError(f"El campo '{field}' es requerido")
        
        if partido_data['equipo1_id'] == partido_data['equipo2_id']:
            raise ValueError("Un equipo no puede jugar contra sí mismo")
        
        try:
            partido = Partido(
                torneo_id=partido_data['torneo_id'],
                equipo1_id=partido_data['equipo1_id'],
                equipo2_id=partido_data['equipo2_id'],
                goles_equipo1=None,
                goles_equipo2=None,
                ganador_id=None
            )
            
            partido = self.partido_repo.create(partido)
            self.db.session.commit()
            return partido
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al crear el partido: {str(e)}")
    
    def update(self, partido_id, partido_data):
        """
        Actualiza un partido existente
        """
        partido = self.partido_repo.get_by_id(partido_id)
        if not partido:
            raise ValueError("Partido no encontrado")
        
        if 'equipo1_id' in partido_data and 'equipo2_id' in partido_data:
            if partido_data['equipo1_id'] == partido_data['equipo2_id']:
                raise ValueError("Un equipo no puede jugar contra sí mismo")
        
        try:
            partido_actualizado = self.partido_repo.update(partido, partido_data)
            self.db.session.commit()
            return partido_actualizado
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al actualizar el partido: {str(e)}")
    
    def registrar_resultado(self, partido_id, data):
        """
        Registra o actualiza el resultado de un partido
        """
        partido = self.partido_repo.get_by_id(partido_id)

        if not partido:
            raise ValueError("Partido no encontrado")

        if 'goles_equipo1' not in data or 'goles_equipo2' not in data:
            raise ValueError("Se requieren los goles de ambos equipos")

        goles_equipo1 = data['goles_equipo1']
        goles_equipo2 = data['goles_equipo2']
        
        if not isinstance(goles_equipo1, int) or not isinstance(goles_equipo2, int):
            raise ValueError("Los goles deben ser números enteros")
        
        if goles_equipo1 < 0 or goles_equipo2 < 0:
            raise ValueError("Los goles no pueden ser negativos")
        
        try:
            partido.goles_equipo1 = goles_equipo1
            partido.goles_equipo2 = goles_equipo2
        
            if goles_equipo1 > goles_equipo2:
                partido.ganador_id = partido.equipo1_id
            elif goles_equipo2 > goles_equipo1:
                partido.ganador_id = partido.equipo2_id
            else:
                partido.ganador_id = None
            
            self.db.session.commit()
            return partido
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al registrar el resultado: {str(e)}")
    
    def delete(self, partido_id):
        """
        Elimina un partido
        """
        partido = self.partido_repo.get_by_id(partido_id)
        if not partido:
            raise ValueError("Partido no encontrado")
        
        try:
            self.partido_repo.delete(partido)
            self.db.session.commit()
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al eliminar el partido: {str(e)}")