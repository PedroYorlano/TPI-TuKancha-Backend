from app.repositories.timeslot_repo import TimeslotRepository
from app.models.timeslot import Timeslot, TimeslotEstado
from app import db
from app.repositories.club_repo import ClubRepository
from datetime import datetime, timedelta, date, time
from collections import defaultdict

# Configuración fija de timeslots para MVP
DURACION_TIMESLOT_MINUTOS = 60  # Turnos de 1 hora
PASO_TIMESLOT_MINUTOS = 60      # Sin solapamiento

class TimeslotService:
    def __init__(self, db):
        self.db = db
        self.timeslot_repo = TimeslotRepository(db)
        self.club_repo = ClubRepository()

    def get_all(self):
        """Retorna todos los timeslots."""
        return self.timeslot_repo.get_all()

    def get_by_id(self, id):
        """Retorna un timeslot por su ID."""
        return self.timeslot_repo.get_by_id(id)
    
    def get_disponibilidad_por_club_y_fecha(self, club_id: int, fecha: date):
        """
        Obtiene la disponibilidad de canchas agrupada por horario para un club y fecha.
        
        Returns:
            dict: {
                "club_id": int,
                "fecha": str,
                "horarios": [
                    {
                        "hora": "HH:MM",
                        "canchas_disponibles": [...]
                    }
                ]
            }
        """
        # Verificar que el club existe
        club = self.club_repo.get_by_id(club_id)
        if not club:
            raise ValueError("Club no encontrado")
        
        # Obtener todos los timeslots del club para esa fecha
        timeslots = self.timeslot_repo.get_by_club_and_fecha(club_id, fecha)
        
        if not timeslots:
            raise ValueError("No hay timeslots disponibles para esta fecha. Puede que necesites generarlos primero.")
        
        # Agrupar timeslots por hora de inicio
        timeslots_por_hora = defaultdict(list)
        for ts in timeslots:
            hora_str = ts.inicio.strftime('%H:%M')
            timeslots_por_hora[hora_str].append(ts)
        
        # Construir respuesta
        horarios = []
        for hora in sorted(timeslots_por_hora.keys()):
            canchas_disponibles = []
            
            for ts in timeslots_por_hora[hora]:
                # Solo incluir canchas con timeslot disponible
                if ts.estado == TimeslotEstado.DISPONIBLE:
                    cancha_info = {
                        "timeslot_id": ts.id,
                        "cancha_id": ts.cancha.id,
                        "nombre": ts.cancha.nombre,
                        "deporte": ts.cancha.deporte,
                        "techado": ts.cancha.techado,
                        "iluminacion": ts.cancha.iluminacion,
                        "superficie": float(ts.cancha.superficie),
                        "precio": float(ts.precio) if ts.precio else float(ts.cancha.precio_hora),
                        "hora_inicio": ts.inicio.strftime('%H:%M'),
                        "hora_fin": ts.fin.strftime('%H:%M')
                    }
                    canchas_disponibles.append(cancha_info)
            
            # Incluir el horario incluso si no hay canchas disponibles
            horarios.append({
                "hora": hora,
                "canchas_disponibles": canchas_disponibles,
                "total_disponibles": len(canchas_disponibles)
            })
        
        return {
            "club_id": club_id,
            "fecha": fecha.isoformat(),
            "total_horarios": len(horarios),
            "horarios": horarios
        }

    def generar_timeslots_para_cancha(self, cancha, fecha_desde: date, fecha_hasta: date, horario_apertura: time, horario_cierre: time, auto_commit: bool = True):
        """
        Genera timeslots para una cancha específica en un rango de fechas.
        Usa configuración fija: turnos de 60 minutos sin solapamiento.
        
        Args:
            cancha: Instancia de Cancha
            fecha_desde: Fecha de inicio (inclusive)
            fecha_hasta: Fecha de fin (inclusive)
            horario_apertura: Hora de apertura diaria
            horario_cierre: Hora de cierre diaria
            auto_commit: Si debe hacer commit automático (False cuando se llama desde creación de cancha)
            
        Returns:
            Dict con un mensaje y la cantidad de timeslots generados
        """
        if fecha_desde > fecha_hasta:
            raise ValueError("La fecha desde debe ser anterior a la fecha hasta")
        
        dias_a_generar = [fecha_desde + timedelta(days=d) for d in range((fecha_hasta - fecha_desde).days + 1)]
        nuevos_timeslots = []
        
        for dia in dias_a_generar:
            # Verificar que no existan timeslots para esta cancha en esta fecha
            if not self.timeslot_repo.existen_en_fecha(cancha.id, dia):
                timeslots_dia = self._calcular_timeslots_para_dia(cancha, dia, horario_apertura, horario_cierre)
                nuevos_timeslots.extend(timeslots_dia)
        
        if nuevos_timeslots:
            self.timeslot_repo.guardar_bulk(nuevos_timeslots)
            if auto_commit:
                db.session.commit()
        
        return {
            "mensaje": f"Se generaron {len(nuevos_timeslots)} timeslots para la cancha '{cancha.nombre}'",
            "cantidad": len(nuevos_timeslots)
        }

    def generar_timeslots_para_club(self, club_id: int, fecha_desde: date, fecha_hasta: date, horario_apertura: time, horario_cierre: time):
        """
        Genera timeslots para todas las canchas de un club en un rango de fechas.
        Usa configuración fija: turnos de 60 minutos sin solapamiento.
        
        Args:
            club_id: ID del club
            fecha_desde: Fecha de inicio (inclusive)
            fecha_hasta: Fecha de fin (inclusive)
            horario_apertura: Hora de apertura diaria
            horario_cierre: Hora de cierre diaria
            
        Returns:
            Dict con un mensaje y la cantidad de timeslots generados
            
        Raises:
            ValueError: Si el club no existe o no tiene canchas
        """
        if fecha_desde > fecha_hasta:
            raise ValueError("La fecha desde debe ser anterior a la fecha hasta")
        
        club = self.club_repo.get_by_id(club_id)
        if not club:
            raise ValueError("Club no encontrado")

        canchas = club.canchas
        if not canchas:
            raise ValueError("El club no tiene canchas.")

        dias_a_generar = [fecha_desde + timedelta(days=d) for d in range((fecha_hasta - fecha_desde).days + 1)]
        nuevos_timeslots_totales = []

        for dia in dias_a_generar:
            for cancha in canchas:
                if not self.timeslot_repo.existen_en_fecha(cancha.id, dia):
                    nuevos = self._calcular_timeslots_para_dia(cancha, dia, horario_apertura, horario_cierre)
                    nuevos_timeslots_totales.extend(nuevos)
    
        if not nuevos_timeslots_totales:
            raise ValueError("No se generaron nuevos timeslots (probablemente ya existían).")

        self.timeslot_repo.guardar_bulk(nuevos_timeslots_totales)
        db.session.commit()
        return {"mensaje": f"Se generaron y guardaron {len(nuevos_timeslots_totales)} nuevos timeslots."}

    def _calcular_timeslots_para_dia(self, cancha, dia, apertura, cierre) -> list:
        """
        Calcula los timeslots para un día y cancha específicos.
        Verifica duplicados exactos antes de crear cada timeslot.
        Configuración fija: turnos de 60 minutos sin solapamiento.
        
        Args:
            cancha: Instancia de Cancha
            dia: Fecha para la que se generarán los timeslots
            apertura: Hora de apertura
            cierre: Hora de cierre
            
        Returns:
            Lista de objetos Timeslot generados (sin duplicados)
        """
        timeslots_del_dia = []
        hora_actual = datetime.combine(dia, apertura)
        hora_fin_jornada = datetime.combine(dia, cierre)
    
        duracion = timedelta(minutes=DURACION_TIMESLOT_MINUTOS)
        paso = timedelta(minutes=PASO_TIMESLOT_MINUTOS)

        while hora_actual < hora_fin_jornada:
            hora_fin_timeslot = hora_actual + duracion
            if hora_fin_timeslot > hora_fin_jornada:
                break

            # VALIDACIÓN CRÍTICA: Verificar que no exista un timeslot exacto
            if not self.timeslot_repo.existe_timeslot_exacto(cancha.id, hora_actual, hora_fin_timeslot):
                ts = Timeslot(
                    cancha_id=cancha.id,
                    inicio=hora_actual,
                    fin=hora_fin_timeslot,
                    precio=cancha.precio_hora  # Usar el precio de la cancha por defecto
                )
                timeslots_del_dia.append(ts)
            else:
                print(f"⚠️  DUPLICADO DETECTADO: Timeslot ya existe para cancha {cancha.id} en {hora_actual} - {hora_fin_timeslot}")
            
            hora_actual += paso
        
        return timeslots_del_dia

    def update(self, id, data):
        """Actualiza un timeslot por su ID."""
        return self.timeslot_repo.update(id, data)

    def delete(self, id):
        """Elimina un timeslot por su ID."""
        return self.timeslot_repo.delete(id)
