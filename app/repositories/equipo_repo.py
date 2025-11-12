from app.models.equipo import Equipo
from app import db
from datetime import datetime

class EquipoRepository:
    """
    Repositorio para manejar operaciones de base de datos para equipos
    """
    
    def get_all(self):
        """Obtiene todos los equipos"""
        return Equipo.query.all()
    
    def get_by_id(self, equipo_id):
        """Obtiene un equipo por su ID"""
        return Equipo.query.get(equipo_id)
    
    def get_by_torneo(self, torneo_id):
        """Obtiene todos los equipos de un torneo específico"""
        return Equipo.query.filter_by(torneo_id=torneo_id).all()
    
    def create(self, equipo):
        """Crea un nuevo equipo"""
        db.session.add(equipo)
        return equipo
    
    def update(self, equipo, data):
        """Actualiza los datos de un equipo existente"""
        for key, value in data.items():
            if hasattr(equipo, key) and key != 'id':
                setattr(equipo, key, value)
        equipo.updated_at = datetime.now()
        db.session.add(equipo)
        return equipo
    
    def delete(self, equipo):
        """Elimina un equipo"""
        db.session.delete(equipo)
    
    def existe_equipo_en_torneo(self, nombre, torneo_id, exclude_id=None):
        """Verifica si ya existe un equipo con el mismo nombre en el torneo"""
        query = Equipo.query.filter(
            Equipo.nombre == nombre,
            Equipo.torneo_id == torneo_id
        )
        
        if exclude_id:
            query = query.filter(Equipo.id != exclude_id)
            
        return query.first() is not None
