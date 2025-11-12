from app.models.torneo import Torneo
from app import db
from datetime import datetime

class TorneoRepository:
    def get_all(self):
        """Obtiene todos los torneos."""
        return Torneo.query.all()
    
    def get_by_id(self, torneo_id):
        """Obtiene un torneo por su ID.
        
        Args:
            torneo_id (int): ID del torneo a buscar
            
        Returns:
            Torneo: El torneo encontrado o None si no existe
        """
        return Torneo.query.get(torneo_id)
    
    def get_by_club_id(self, club_id):
        """Obtiene todos los torneos de un club específico.
        
        Args:
            club_id (int): ID del club
            
        Returns:
            list[Torneo]: Lista de torneos del club
        """
        return Torneo.query.filter_by(club_id=club_id).all()
    
    def get_by_estado(self, estado):
        """Obtiene torneos por estado.
        
        Args:
            estado (str): Estado del torneo (CREADO, ACTIVO, FINALIZADO, CANCELADO)
            
        Returns:
            list[Torneo]: Lista de torneos con el estado especificado
        """
        return Torneo.query.filter_by(estado=estado).all()
    
    def create(self, torneo_data):
        """Crea un nuevo torneo.
        
        Args:
            torneo_data (dict): Datos del torneo a crear
            
        Returns:
            Torneo: El torneo creado
        """
        torneo = Torneo(**torneo_data)
        db.session.add(torneo)
        return torneo
    
    def update(self, torneo, torneo_data):
        """Actualiza los datos de un torneo existente.
        
        Args:
            torneo (Torneo): Instancia del torneo a actualizar
            torneo_data (dict): Datos a actualizar
            
        Returns:
            Torneo: El torneo actualizado
        """
        for key, value in torneo_data.items():
            if hasattr(torneo, key) and key != 'id':
                setattr(torneo, key, value)
        torneo.updated_at = datetime.utcnow()
        db.session.add(torneo)
        return torneo
    
    def delete(self, torneo):
        """Elimina un torneo.
        
        Args:
            torneo (Torneo): Instancia del torneo a eliminar
        """
        db.session.delete(torneo)
    
    def cambiar_estado(self, torneo, nuevo_estado):
        """Cambia el estado de un torneo.
        
        Args:
            torneo (Torneo): Instancia del torneo
            nuevo_estado (str): Nuevo estado del torneo
            
        Returns:
            Torneo: El torneo actualizado
        """
        torneo.estado = nuevo_estado
        torneo.updated_at = datetime.utcnow()
        db.session.add(torneo)
        return torneo
    
    def get_torneos_activos(self):
        """Obtiene todos los torneos activos.
        
        Returns:
            list[Torneo]: Lista de torneos activos
        """
        return Torneo.query.filter_by(estado='ACTIVO').all()
    
    def get_torneos_por_fecha(self, fecha_inicio, fecha_fin=None):
        """Obtiene torneos por rango de fechas.
        
        Args:
            fecha_inicio (date): Fecha de inicio del rango
            fecha_fin (date, optional): Fecha de fin del rango. Si no se especifica, 
                                      se busca solo por fecha_inicio.
                                      
        Returns:
            list[Torneo]: Lista de torneos en el rango de fechas
        """
        query = Torneo.query.filter(Torneo.fecha_inicio >= fecha_inicio)
        
        if fecha_fin:
            query = query.filter(Torneo.fecha_inicio <= fecha_fin)
            
        return query.order_by(Torneo.fecha_inicio).all()