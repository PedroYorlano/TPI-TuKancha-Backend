from app.repositories.cancha_repo import CanchaRepository
from app.repositories.club_repo import ClubRepository
from app.models.cancha import Cancha
from datetime import date, time, timedelta


class CanchaService:
    def __init__(self, db):
        self.db = db
        self.cancha_repo = CanchaRepository()
        self.club_repo = ClubRepository()

    def get_all(self):
        return self.cancha_repo.get_all()

    def get_by_predio(self, predio_id):
        return self.cancha_repo.get_by_predio(predio_id)

    def get_by_id(self, cancha_id):
        return self.cancha_repo.get_by_id(cancha_id)

    def create(self, data):
        # Campos requeridos según el modelo Cancha
        required_fields = ['nombre', 'deporte', 'superficie', 'techado', 'iluminacion', 'precio_hora', 'club_id']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"El campo '{field}' es requerido")
        
        try:
            # Verificar que el club existe
            club = self.club_repo.get_by_id(data['club_id'])
            if not club:
                raise ValueError(f"Club con ID {data['club_id']} no encontrado")
            
            # ✅ VALIDACIÓN: Verificar que el club tenga horarios definidos
            horarios_club = [h for h in club.horarios if h.activo]
            if not horarios_club:
                raise ValueError(
                    f"El club '{club.nombre}' no tiene horarios definidos. "
                    f"Debe configurar los horarios del club antes de crear canchas."
                )
            
            # Crear instancia de Cancha
            nueva_cancha = Cancha(
                nombre=data['nombre'],
                deporte=data['deporte'],
                superficie=data['superficie'],
                techado=data['techado'],
                iluminacion=data['iluminacion'],
                precio_hora=data['precio_hora'],
                club_id=data['club_id'],
                activa=data.get('activa', True)  # Por defecto True si no se especifica
            )
            
            self.cancha_repo.create(nueva_cancha)
            self.db.session.flush()  # Para obtener el ID de la cancha antes del commit
            
            # Generar timeslots automáticamente para los próximos 3 meses
            self._generar_timeslots_automaticos(nueva_cancha, club)
            
            self.db.session.commit()
            return nueva_cancha
            
        except ValueError as e:
            self.db.session.rollback()
            raise e
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al crear la cancha: {e}")
    
    def _generar_timeslots_automaticos(self, cancha, club):
        """
        Genera timeslots automáticamente para una cancha nueva.
        Usa los horarios del club para determinar apertura y cierre.
        Configuración fija: turnos de 60 minutos sin solapamiento.
        """
        from app.services.timeslot_service import TimeslotService
        
        # Definir rango de fechas: hoy hasta 3 meses
        fecha_desde = date.today()
        fecha_hasta = fecha_desde + timedelta(days=90)
        
        # Obtener horarios del club (ya validados en create())
        horarios_club = [h for h in club.horarios if h.activo]
        
        # Usar el horario más temprano de apertura y más tardío de cierre
        horario_apertura = min(h.abre for h in horarios_club)
        horario_cierre = max(h.cierra for h in horarios_club)
        
        print(f"📅 Generando timeslots para '{cancha.nombre}'")
        print(f"   Horario: {horario_apertura.strftime('%H:%M')} - {horario_cierre.strftime('%H:%M')}")
        print(f"   Período: {fecha_desde} a {fecha_hasta}")
        
        # Generar timeslots usando el servicio
        timeslot_service = TimeslotService(self.db)
        
        try:
            resultado = timeslot_service.generar_timeslots_para_cancha(
                cancha=cancha,
                fecha_desde=fecha_desde,
                fecha_hasta=fecha_hasta,
                horario_apertura=horario_apertura,
                horario_cierre=horario_cierre,
                auto_commit=False  # No hacer commit aquí, se hará en el create()
            )
            print(f"✅ {resultado['mensaje']}")
        except Exception as e:
            # Si falla la generación de timeslots, rollback completo
            print(f"❌ ERROR al generar timeslots automáticos: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Error al generar timeslots: {e}")

    def update(self, cancha_id, data):
        cancha = self.cancha_repo.get_by_id(cancha_id)
        
        if not cancha:
            raise ValueError("Cancha no encontrada")
        
        try:
            # Actualizar solo los campos que vienen en data
            if 'nombre' in data:
                cancha.nombre = data['nombre']
            if 'deporte' in data:
                cancha.deporte = data['deporte']
            if 'superficie' in data:
                cancha.superficie = data['superficie']
            if 'techado' in data:
                cancha.techado = data['techado']
            if 'iluminacion' in data:
                cancha.iluminacion = data['iluminacion']
            if 'precio_hora' in data:
                cancha.precio_hora = data['precio_hora']
            if 'activa' in data:
                cancha.activa = data['activa']
            if 'club_id' in data:
                cancha.club_id = data['club_id']
            
            self.cancha_repo.update(cancha, data)
            self.db.session.commit()
            return cancha
            
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al actualizar la cancha: {e}")

    def delete(self, cancha_id):
        cancha = self.cancha_repo.get_by_id(cancha_id)
        
        if not cancha:
            raise ValueError("Cancha no encontrada")
        
        try:
            self.cancha_repo.delete(cancha)
            self.db.session.commit()
            return cancha
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error al eliminar la cancha: {e}")