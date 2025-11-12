from app.models.partido import Partido
from app import db
from datetime import datetime

class PartidoRepository:
    """
    Repositorio para manejar operaciones de base de datos para partidos
    """
    
    def get_all(self):
        """Obtiene todos los partidos"""
        return Partido.query.all()
    
    def get_by_id(self, partido_id):
        """Obtiene un partido por su ID"""
        return Partido.query.get(partido_id)
    
    def get_by_torneo(self, torneo_id):
        """Obtiene todos los partidos de un torneo específico"""
        return Partido.query.filter_by(torneo_id=torneo_id).all()
    
    def create(self, partido):
        """Crea un nuevo partido"""
        db.session.add(partido)
        return partido

    def update(self, partido, data):
        for key, value in data.items():
            if hasattr(partido, key) and key != 'id':
                setattr(partido, key, value)
        partido.updated_at = datetime.now()
        db.session.add(partido)
        return partido
    
    def delete(self, partido):
        """Elimina un partido"""
        db.session.delete(partido)
