from app.repositories.cancha_repo import CanchaRepository
from app.repositories.club_repo import ClubRepository
from app.models.cancha import Cancha
from datetime import date, time, timedelta


class CanchaService:
    def __init__(self, db):
        """
        Inicializa el servicio de canchas con los repositorios necesarios.
        
        Args:
            db: Instancia de la base de datos SQLAlchemy
        """
        self.db = db
        self.cancha_repo = CanchaRepository()
        self.club_repo = ClubRepository()

    def get_all(self):
        """
        Obtiene todas las canchas.
        
        Returns:
            list[Cancha]: Lista de todas las canchas
        """
        return self.cancha_repo.get_all()

    def get_by_predio(self, predio_id):
        """
        Obtiene las canchas de un predio específico.
        
        Args:
            predio_id (int): ID del predio
            
        Returns:
            list[Cancha]: Lista de canchas del predio
        """
        return self.cancha_repo.get_by_predio(predio_id)

    def get_by_id(self, cancha_id):
        """
        Obtiene una cancha por su ID.
        
        Args:
            cancha_id (int): ID de la cancha a buscar
            
        Returns:
            Cancha: La cancha encontrada o None si no existe
        """
        return self.cancha_repo.get_by_id(cancha_id)

    def create(self, data):
        """
        Crea una nueva cancha.
        
        Args:
            data (dict): Datos de la cancha a crear. Debe incluir:
                - nombre (str): Nombre de la cancha
                - deporte (str): Deporte que se practica en la cancha
                - superficie (str): Tipo de superficie de la cancha
                - techado (bool): Indica si la cancha está techada
                - iluminacion (bool): Indica si la cancha tiene iluminación
                - precio_hora (float): Precio por hora de uso
                - club_id (int): ID del club al que pertenece la cancha
                
        Returns:
            Cancha: La cancha creada
            
        Raises:
            ValueError: Si faltan campos requeridos o los datos son inválidos
        """
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
        
        Args:
            cancha (Cancha): Instancia de la cancha para la que se generarán los timeslots
            club (Club): Instancia del club al que pertenece la cancha
            
        Note:
            Este método es de uso interno y no debe ser llamado directamente.
            Se ejecuta automáticamente al crear una nueva cancha.
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
        """
        Actualiza los datos de una cancha existente.
        
        Args:
            cancha_id (int): ID de la cancha a actualizar
            data (dict): Datos a actualizar. Puede incluir:
                - nombre (str, opcional): Nuevo nombre de la cancha
                - deporte (str, opcional): Nuevo deporte
                - superficie (str, opcional): Nueva superficie
                - techado (bool, opcional): Indica si está techada
                - iluminacion (bool, opcional): Indica si tiene iluminación
                - precio_hora (float, opcional): Nuevo precio por hora
                - activa (bool, opcional): Estado de la cancha
                
        Returns:
            Cancha: La cancha actualizada
            
        Raises:
            ValueError: Si la cancha no existe o los datos son inválidos
        """
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
        """
        Elimina una cancha del sistema.
        
        Args:
            cancha_id (int): ID de la cancha a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa
            
        Raises:
            ValueError: Si la cancha no existe o no se puede eliminar
        """
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