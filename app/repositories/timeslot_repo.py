from app.models.timeslot import Timeslot 
from app import db
from datetime import date

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

    def guardar_bulk(self, timeslots: list):
        """Guarda una lista de timeslots en la base de datos."""
        if not timeslots:
            return
        
        try:
            self.db.session.add_all(timeslots)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al guardar los timeslots en lote: {e}")