from app.repositories.timeslot_repo import TimeslotRepository
from app.models.timeslot import Timeslot
from app import db
from app.repositories.club_repo import ClubRepository
from app.repositories.timeslot_definicion_repo import TimeslotDefinicionRepository
from datetime import datetime, timedelta
from app.models.timeslot import Timeslot

class TimeslotService:
    def __init__(self, db):
        self.db = db
        self.timeslot_repo = TimeslotRepository(db)
        self.club_repo = ClubRepository(db)
        self.definicion_repo = TimeslotDefinicionRepository(db)

    def get_all(self):
        """Retorna todos los timeslots."""
        return self.timeslot_repo.get_all()

    def get_by_id(self, id):
        """Retorna un timeslot por su ID."""
        return self.timeslot_repo.get_by_id(id)

    def generar_timeslots_para_club(self, club_id: int, fecha_desde: date, fecha_hasta: date, horario_apertura: time, horario_cierre: time):
        """
        Genera timeslots para todas las canchas de un club en un rango de fechas.
        
        Args:
            club_id: ID del club
            fecha_desde: Fecha de inicio (inclusive)
            fecha_hasta: Fecha de fin (inclusive)
            horario_apertura: Hora de apertura diaria
            horario_cierre: Hora de cierre diaria
            
        Returns:
            Dict con un mensaje y la cantidad de timeslots generados
            
        Raises:
            ValueError: Si el club no existe, no tiene canchas o no tiene una definición activa
        """
        if fecha_desde > fecha_hasta:
            raise ValueError("La fecha desde debe ser anterior a la fecha hasta")
        
        club = self.club_repo.get_by_id(club_id)
        if not club:
            raise ValueError("Club no encontrado")

        definicion = self.definicion_repo.get_activa_por_club(club_id)
        if not definicion:
            raise ValueError("No hay una definición de timeslot activa para este club.")

        canchas = club.canchas
        if not canchas:
            raise ValueError("El club no tiene canchas.")

        dias_a_generar = [fecha_desde + timedelta(days=d) for d in range((fecha_hasta - fecha_desde).days + 1)]
        nuevos_timeslots_totales = []

        for dia in dias_a_generar:
            for cancha in canchas:
                if not self.timeslot_repo.existen_en_fecha(cancha.id, dia):
                    nuevos = self._calcular_timeslots_para_dia(cancha, dia, definicion, horario_apertura, horario_cierre)
                    nuevos_timeslots_totales.extend(nuevos)
    
        if not nuevos_timeslots_totales:
            raise ValueError("No se generaron nuevos timeslots (probablemente ya existían).")

        self.timeslot_repo.guardar_bulk(nuevos_timeslots_totales)
        return {"mensaje": f"Se generaron y guardaron {len(nuevos_timeslots_totales)} nuevos timeslots."}

    def _calcular_timeslots_para_dia(self, cancha, dia, definicion, apertura, cierre) -> list:
        """
        Calcula los timeslots para un día y cancha específicos.
        
        Args:
            cancha: Instancia de Cancha
            dia: Fecha para la que se generarán los timeslots
            definicion: Instancia de TimeslotDefinicion con la configuración
            apertura: Hora de apertura
            cierre: Hora de cierre
            
        Returns:
            Lista de objetos Timeslot generados
        """
        timeslots_del_dia = []
        hora_actual = datetime.combine(dia, apertura)
        hora_fin_jornada = datetime.combine(dia, cierre)
    
        duracion = timedelta(minutes=definicion.duracion_minutos)
        paso = timedelta(minutes=definicion.paso_minutos)

        while hora_actual < hora_fin_jornada:
            hora_fin_timeslot = hora_actual + duracion
            if hora_fin_timeslot > hora_fin_jornada:
                break

            ts = Timeslot(
                cancha_id=cancha.id,
                inicio=hora_actual,
                fin=hora_fin_timeslot,
                precio=definicion.precio
            )
            timeslots_del_dia.append(ts)
            hora_actual += paso
        
        return timeslots_del_dia

    def update(self, id, data):
        """Actualiza un timeslot por su ID."""
        return self.timeslot_repo.update(id, data)

    def delete(self, id):
        """Elimina un timeslot por su ID."""
        return self.timeslot_repo.delete(id)
