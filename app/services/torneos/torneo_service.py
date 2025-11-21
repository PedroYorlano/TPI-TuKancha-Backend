from app.repositories.torneos.torneo_repo import TorneoRepository
from app.models.torneo import Torneo
from app import db
from datetime import datetime, date
from app.models.enums import TorneoEstado

from app.errors import ValidationError, NotFoundError, AppError

def _parse_date(date_string, field_name):
    """Helper interno para convertir string YYYY-MM-DD a objeto date."""
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        raise ValidationError(f"Formato de fecha inválido para '{field_name}'. Usar YYYY-MM-DD.")

class TorneoService:
    def __init__(self, db):
        self.db = db
        self.torneo_repo = TorneoRepository()
    
    def get_all(self):
        return self.torneo_repo.get_all()
    
    def get_by_id(self, torneo_id):
        torneo = self.torneo_repo.get_by_id(torneo_id)
        if not torneo:
            raise NotFoundError("Torneo no encontrado")
        return torneo
    
    def get_equipos_torneo(self, torneo_id):
        equipos = self.torneo_repo.get_equipos_torneo(torneo_id)
        if not equipos:
            raise NotFoundError("No se encontraron equipos para el torneo")
        return equipos

    def get_torneos_activos(self):
        torneos_activos = self.torneo_repo.get_torneos_activos()
        if not torneos_activos:
            raise NotFoundError("No se encontraron torneos activos")
        return torneos_activos

    def get_torneos_por_fecha(self, fecha_inicio_str, fecha_fin_str=None):
        fecha_inicio = _parse_date(fecha_inicio_str, "fecha_inicio")
        fecha_fin = _parse_date(fecha_fin_str, "fecha_fin")

        if not fecha_inicio:
            raise ValidationError("El parámetro 'fecha_inicio' es requerido.")

        torneo_por_fecha = self.torneo_repo.get_torneos_por_fecha(fecha_inicio, fecha_fin)
        if not torneo_por_fecha:
            raise NotFoundError("No se encontraron torneos para esta(s) fecha(s)")
        return torneo_por_fecha
    
    def create(self, torneo_data):
        required_fields = ['nombre', 'club_id']
        for field in required_fields:
            if field not in torneo_data or not torneo_data[field]:
                raise ValidationError(f"El campo '{field}' es requerido")
        
        try:
            fecha_inicio = _parse_date(torneo_data.get('fecha_inicio'), 'fecha_inicio')
            fecha_fin = _parse_date(torneo_data.get('fecha_fin'), 'fecha_fin')
            
            if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
                raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio")
            
            estado_enum = TorneoEstado.CREADO
            if 'estado' in torneo_data and torneo_data['estado']:
                try:
                    estado_enum = TorneoEstado(torneo_data['estado'].upper())
                except ValueError:
                    raise ValidationError(f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}")
            
            # Crear el torneo
            torneo = Torneo(
                nombre=torneo_data['nombre'],
                club_id=torneo_data['club_id'],
                categoria=torneo_data.get('categoria'),
                estado=estado_enum,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                reglamento=torneo_data.get('reglamento'),
            )
            self.torneo_repo.create(torneo)
            self.db.session.commit()
            return torneo
            
        except ValidationError as e:
            self.db.session.rollback()
            raise e
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al crear el torneo: {str(e)}")
    
    def update(self, torneo_id, torneo_data):
        torneo = self.get_by_id(torneo_id)
        
        try:
            fecha_inicio_str = torneo_data.get('fecha_inicio')
            fecha_fin_str = torneo_data.get('fecha_fin')

            fecha_inicio = _parse_date(fecha_inicio_str, 'fecha_inicio') if fecha_inicio_str else torneo.fecha_inicio
            fecha_fin = _parse_date(fecha_fin_str, 'fecha_fin') if fecha_fin_str else torneo.fecha_fin
            
            if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
                raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio")
            
            if 'estado' in torneo_data and torneo_data['estado']:
                try:
                    torneo.estado = TorneoEstado(torneo_data['estado'].upper())
                except ValueError:
                    raise ValidationError(f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}")
            
            # Actualizar campos (usando el patrón 'get' para permitir PATCH)
            torneo.nombre = torneo_data.get('nombre', torneo.nombre)
            torneo.club_id = torneo_data.get('club_id', torneo.club_id)
            torneo.categoria = torneo_data.get('categoria', torneo.categoria)
            torneo.fecha_inicio = fecha_inicio
            torneo.fecha_fin = fecha_fin
            torneo.reglamento = torneo_data.get('reglamento', torneo.reglamento)

            self.db.session.commit()
            return torneo
            
        except ValidationError as e:
            self.db.session.rollback()
            raise e
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al actualizar el torneo: {str(e)}")
    
    def delete(self, torneo_id):
        torneo = self.get_by_id(torneo_id)
        
        try:
            self.torneo_repo.delete(torneo)
            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al eliminar el torneo: {str(e)}")
    
    def cambiar_estado(self, torneo_id, data):
        torneo = self.get_by_id(torneo_id)
        
        if not data or 'estado' not in data:
            raise ValidationError("El campo 'estado' es requerido")
        nuevo_estado_str = data['estado']
        
        try:
            try:
                estado_enum = TorneoEstado(nuevo_estado_str.upper())
            except ValueError:
                raise ValidationError(f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}")
            
            if torneo.estado == TorneoEstado.FINALIZADO:
                raise ValidationError("No se puede modificar el estado de un torneo finalizado")
            
            torneo.estado = estado_enum
            self.db.session.commit()
            return torneo
            
        except ValidationError as e:
            self.db.session.rollback()
            raise e
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al cambiar el estado del torneo: {str(e)}")

    def agregar_equipo(self, torneo_id, equipo_id):
        torneo = self.get_by_id(torneo_id)
        equipo = equipo_service.get_by_id(equipo_id)
        
        try:
            torneo.equipos.append(equipo)
            self.db.session.commit()
            return torneo
        except Exception as e:
            self.db.session.rollback()
            raise AppError(f"Error al agregar el equipo al torneo: {str(e)}")

    def get_tabla_posiciones(self, torneo_id):
        """
        Calcula la tabla de posiciones para un torneo en tiempo real.
        Utiliza las relaciones de 'partidos_local', 'partidos_visitante'
        y la nueva 'partidos_ganador' para eficiencia.
        """
        torneo = self.get_by_id(torneo_id) 
        tabla_calculada = []
        for equipo in torneo.equipos:
            stats = {
                "id": equipo.id,
                "nombre": equipo.nombre,
                "PJ": 0, # Partidos Jugados
                "PG": 0, # Partidos Ganados
                "PE": 0, # Partidos Empatados
                "PP": 0, # Partidos Perdidos
                "GF": 0, # Goles a Favor
                "GC": 0, # Goles en Contra
                "Puntos": 0
            }

            partidos_local = equipo.partidos_local
            partidos_visitante = equipo.partidos_visitante
            
            stats["PJ"] = len(partidos_local) + len(partidos_visitante)
            stats["PG"] = len(equipo.partidos_ganador)

            for p in partidos_local:
                stats["GF"] += p.goles_equipo1
                stats["GC"] += p.goles_equipo2
                if p.goles_equipo1 == p.goles_equipo2:
                    stats["PE"] += 1

            for p in partidos_visitante:
                stats["GF"] += p.goles_equipo2
                stats["GC"] += p.goles_equipo1
                if p.goles_equipo1 == p.goles_equipo2:
                    stats["PE"] += 1

            stats["PP"] = stats["PJ"] - stats["PG"] - stats["PE"]
            stats["Puntos"] = (stats["PG"] * 3) + (stats["PE"] * 1)
            
            tabla_calculada.append(stats)

        tabla_ordenada = sorted(tabla_calculada, key=lambda x: x["Puntos"], reverse=True)
        
        return tabla_ordenada
