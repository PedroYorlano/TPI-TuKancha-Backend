from app.models.timeslot import Timeslot 
from app import db
from datetime import date, datetime

class TimeslotRepository: 
    def __init__(self, db): 
        self.db = db
    
    def existen_en_fecha(self, cancha_id: int, fecha: date) -> bool: 
        """Verifica si ya existen timeslots para una cancha en una fecha dada.""" 
        return self.db.session.query(
            self.db.session.query(Timeslot).filter( 
                Timeslot.cancha_id == cancha_id, 
                db.func.date(Timeslot.inicio) == fecha 
            ).exists() 
        ).scalar()
    
    def existe_timeslot_exacto(self, cancha_id: int, inicio: datetime, fin: datetime) -> bool:
        """
        Verifica si ya existe un timeslot con exactamente el mismo horario.
        Esto previene duplicados exactos que serían un error grave.
        """
        return self.db.session.query(
            self.db.session.query(Timeslot).filter(
                Timeslot.cancha_id == cancha_id,
                Timeslot.inicio == inicio,
                Timeslot.fin == fin
            ).exists()
        ).scalar()
    
    def get_by_club_and_fecha(self, club_id: int, fecha: date):
        """
        Obtiene todos los timeslots de un club para una fecha específica.
        Incluye la relación con cancha para acceder a sus datos.
        """
        return (
            self.db.session.query(Timeslot)
            .join(Timeslot.cancha)
            .filter(
                Timeslot.cancha.has(club_id=club_id),
                db.func.date(Timeslot.inicio) == fecha
            )
            .order_by(Timeslot.inicio)
            .all()
        )

    def guardar_bulk(self, timeslots: list):
        """Guarda una lista de timeslots en la base de datos."""
        if not timeslots:
            return
        
        self.db.session.add_all(timeslots)