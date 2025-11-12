from app.repositories.torneos.torneo_repo import TorneoRepository
from app.models.torneo import Torneo
from app import db
from datetime import datetime, date
from app.models.enums import TorneoEstado

class TorneoService:
    def __init__(self, db):
        self.db = db
        self.torneo_repo = TorneoRepository()
    
    def get_all(self):
        """Obtiene todos los torneos."""
        return self.torneo_repo.get_all()
    
    def get_by_id(self, torneo_id):
        """
        Obtiene un torneo por su ID.
        
        Args:
            torneo_id (int): ID del torneo a buscar
            
        Returns:
            Torneo: El torneo encontrado o None si no existe
        """
        return self.torneo_repo.get_by_id(torneo_id)
    
    def get_by_club_id(self, club_id):
        """
        Obtiene todos los torneos de un club específico.
        
        Args:
            club_id (int): ID del club
            
        Returns:
            list[Torneo]: Lista de torneos del club
        """
        return self.torneo_repo.get_by_club_id(club_id)
    
    def get_torneos_activos(self):
        """
        Obtiene todos los torneos activos.
        
        Returns:
            list[Torneo]: Lista de torneos activos
        """
        return self.torneo_repo.get_torneos_activos()
    
    def get_torneos_por_fecha(self, fecha_inicio, fecha_fin=None):
        """
        Obtiene torneos por rango de fechas.
        
        Args:
            fecha_inicio (date): Fecha de inicio del rango
            fecha_fin (date, optional): Fecha de fin del rango. Si no se especifica, 
                                      se busca solo por fecha_inicio.
                                      
        Returns:
            list[Torneo]: Lista de torneos en el rango de fechas
        """
        return self.torneo_repo.get_torneos_por_fecha(fecha_inicio, fecha_fin)
    
    def create(self, torneo_data):
        """
        Crea un nuevo torneo.
        
        Args:
            torneo_data (dict): Datos del torneo a crear. Debe incluir:
                - nombre (str): Nombre del torneo
                - club_id (int): ID del club organizador
                - categoria (str, opcional): Categoría del torneo
                - estado (str, opcional): Estado inicial (default: CREADO)
                - fecha_inicio (str, opcional): Fecha de inicio en formato YYYY-MM-DD
                - fecha_fin (str, opcional): Fecha de fin en formato YYYY-MM-DD
                - reglamento (str, opcional): Reglamento del torneo
                
        Returns:
            Torneo: El torneo creado
            
        Raises:
            ValueError: Si faltan campos requeridos o los datos son inválidos
        """
        required_fields = ['nombre', 'club_id']
        for field in required_fields:
            if field not in torneo_data or not torneo_data[field]:
                raise ValueError(f"El campo '{field}' es requerido")
        
        try:
            # La validación de formato de fecha ya se hace en la API.
            # Aquí solo validamos la lógica de negocio.
            if ('fecha_inicio' in torneo_data and torneo_data.get('fecha_inicio') and 
                'fecha_fin' in torneo_data and torneo_data.get('fecha_fin') and 
                torneo_data['fecha_fin'] < torneo_data['fecha_inicio']):
                raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")
            
            # Validar estado si se proporciona
            if 'estado' in torneo_data and torneo_data['estado']:
                try:
                    torneo_data['estado'] = TorneoEstado(torneo_data['estado'].upper())
                except ValueError:
                    raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}")
            else:
                torneo_data['estado'] = TorneoEstado.CREADO
            
            # Crear el torneo
            torneo = Torneo(
                nombre=torneo_data['nombre'],
                club_id=torneo_data['club_id'],
                categoria=torneo_data.get('categoria', None),
                estado=torneo_data['estado'],
                fecha_inicio=torneo_data.get('fecha_inicio', None),
                fecha_fin=torneo_data.get('fecha_fin', None),
                reglamento=torneo_data.get('reglamento', None)
            )
            self.torneo_repo.create(torneo)
            self.db.session.commit()
            return torneo
            
        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al crear el torneo: {str(e)}")
    
    def update(self, torneo_id, torneo_data):
        """
        Actualiza un torneo existente.
        
        Args:
            torneo_id (int): ID del torneo a actualizar
            torneo_data (dict): Datos a actualizar
            
        Returns:
            Torneo: El torneo actualizado
            
        Raises:
            ValueError: Si el torneo no existe o los datos son inválidos
        """
        torneo = self.torneo_repo.get_by_id(torneo_id)
        if not torneo:
            raise ValueError("Torneo no encontrado")
        
        try:
            # La validación de formato de fecha ya se hace en la API.
            # Aquí solo validamos la lógica de negocio.
            fecha_inicio = torneo_data.get('fecha_inicio', torneo.fecha_inicio)
            fecha_fin = torneo_data.get('fecha_fin', torneo.fecha_fin)
            
            if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
                raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")
            
            # Validar estado si se proporciona
            if 'estado' in torneo_data and torneo_data['estado']:
                try:
                    torneo_data['estado'] = TorneoEstado(torneo_data['estado'].upper())
                except ValueError:
                    raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}")
            
            # Actualizar el torneo
            torneo_actualizado = self.torneo_repo.update(torneo, torneo_data)
            self.db.session.commit()
            return torneo_actualizado
            
        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al actualizar el torneo: {str(e)}")
    
    def delete(self, torneo_id):
        """
        Elimina un torneo.
        
        Args:
            torneo_id (int): ID del torneo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            ValueError: Si el torneo no existe o no se puede eliminar
        """
        torneo = self.torneo_repo.get_by_id(torneo_id)
        if not torneo:
            raise ValueError("Torneo no encontrado")
        
        try:
            self.torneo_repo.delete(torneo)
            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al eliminar el torneo: {str(e)}")
    
    def cambiar_estado(self, torneo_id, nuevo_estado):
        """
        Cambia el estado de un torneo.
        
        Args:
            torneo_id (int): ID del torneo
            nuevo_estado (str): Nuevo estado (CREADO, ACTIVO, FINALIZADO, CANCELADO)
            
        Returns:
            Torneo: El torneo actualizado
            
        Raises:
            ValueError: Si el torneo no existe o el estado es inválido
        """
        torneo = self.torneo_repo.get_by_id(torneo_id)
        if not torneo:
            raise ValueError("Torneo no encontrado")
        
        try:
            # Validar el nuevo estado
            try:
                estado_enum = TorneoEstado(nuevo_estado.upper())
            except ValueError:
                raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}")
            
            # Validar transiciones de estado
            if torneo.estado == TorneoEstado.FINALIZADO and estado_enum != TorneoEstado.FINALIZADO:
                raise ValueError("No se puede modificar el estado de un torneo finalizado")
                
            if torneo.estado == TorneoEstado.CANCELADO and estado_enum != TorneoEstado.CANCELADO:
                raise ValueError("No se puede modificar el estado de un torneo cancelado")
            
            # Actualizar el estado
            torneo_actualizado = self.torneo_repo.cambiar_estado(torneo, estado_enum)
            self.db.session.commit()
            return torneo_actualizado
            
        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al cambiar el estado del torneo: {str(e)}")

    def mostrar_tabla_posiciones(self, torneo_id):
        torneo = self.torneo_repo.get_by_id(torneo_id)
        if not torneo:
            raise ValueError("Torneo no encontrado")
        
        for equipo in torneo.equipos:
            puntos = equipo.partidos_ganados * 3 + equipo.partidos_empatados * 1
            print(f"Equipo: {equipo.nombre}")
            print(f"Partidos ganados: {equipo.partidos_ganados}")
            print(f"Partidos perdidos: {equipo.partidos_perdidos}")
            print(f"Partidos empatados: {equipo.partidos_empatados}")
            print(f"Puntos: {puntos}")
            print("-------------------------")