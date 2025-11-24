from datetime import datetime, date
from typing import Optional, List
from calendar import monthrange
from sqlalchemy import func

from app import db
from app.models.reserva import Reserva
from app.models.timeslot import Timeslot
from app.models.cancha import Cancha


class ReporteRepository:
    """
    Repositorio para obtener datos de reportes desde la base de datos.
    Contiene queries especializadas para análisis y reportes.
    """
    
    def __init__(self):
        pass
    
    def get_reservas_filtradas(self, cliente_email: Optional[str] = None, q: Optional[str] = None):
        """
        Obtiene reservas filtradas por email o búsqueda general.
        
        Args:
            cliente_email: Email exacto del cliente
            q: Búsqueda libre por nombre o email (contiene)
            
        Returns:
            Lista de reservas ordenadas por email y fecha de creación
        """
        query = Reserva.query
        
        if cliente_email:
            query = query.filter(Reserva.cliente_email == cliente_email)
        elif q:
            like = f"%{q}%"
            query = query.filter(
                (Reserva.cliente_email.ilike(like)) |
                (Reserva.cliente_nombre.ilike(like))
            )
        
        return query.order_by(Reserva.cliente_email, Reserva.created_at).all()
    
    def get_reservas_por_cancha(
        self, 
        cancha_id: Optional[int] = None,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None
    ):
        """
        Obtiene reservas agrupadas por cancha con filtros de periodo.
        
        Args:
            cancha_id: ID de cancha específica (opcional)
            start_dt: Fecha/hora de inicio del periodo
            end_dt: Fecha/hora de fin del periodo
            
        Returns:
            Lista de reservas con sus timeslots
        """
        query = Reserva.query.join(Reserva.timeslots).join(Timeslot)
        
        if cancha_id:
            query = query.filter(Reserva.cancha_id == cancha_id)
        
        if start_dt:
            query = query.filter(Timeslot.inicio >= start_dt)
        if end_dt:
            query = query.filter(Timeslot.inicio <= end_dt)
        
        return query.order_by(Reserva.cancha_id, Timeslot.inicio).all()
    
    def get_canchas_mas_utilizadas_query(
        self,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None,
        limit: int = 10
    ):
        """
        Query agregada que devuelve canchas ordenadas por cantidad de reservas.
        
        Args:
            start_dt: Fecha/hora de inicio del periodo
            end_dt: Fecha/hora de fin del periodo
            limit: Número máximo de canchas a retornar
            
        Returns:
            Lista de tuplas (cancha_id, reservas_count, total_ingresos)
        """
        q = db.session.query(
            Reserva.cancha_id.label('cancha_id'),
            func.count(func.distinct(Reserva.id)).label('reservas_count'),
            func.coalesce(func.sum(Reserva.precio_total), 0).label('total_ingresos')
        ).join(Reserva.timeslots).join(Timeslot)
        
        if start_dt:
            q = q.filter(Timeslot.inicio >= start_dt)
        if end_dt:
            q = q.filter(Timeslot.inicio <= end_dt)
        
        q = q.group_by(Reserva.cancha_id)\
             .order_by(func.count(func.distinct(Reserva.id)).desc())\
             .limit(limit)
        
        return q.all()
    
    def get_total_reservas_periodo(
        self,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None
    ) -> int:
        """
        Cuenta el total de reservas en un periodo dado.
        
        Args:
            start_dt: Fecha/hora de inicio del periodo
            end_dt: Fecha/hora de fin del periodo
            
        Returns:
            Número total de reservas en el periodo
        """
        q_total = db.session.query(func.count(func.distinct(Reserva.id)))
        q_total = q_total.join(Reserva.timeslots).join(Timeslot)
        
        if start_dt:
            q_total = q_total.filter(Timeslot.inicio >= start_dt)
        if end_dt:
            q_total = q_total.filter(Timeslot.inicio <= end_dt)
        
        return int(q_total.scalar() or 0)
    
    def get_utilizacion_mensual_query(
        self,
        cancha_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ):
        """
        Query agregada que devuelve cantidad de reservas por cancha y mes.
        
        Args:
            cancha_id: ID de cancha específica (opcional)
            start_date: Fecha de inicio del periodo
            end_date: Fecha de fin del periodo
            
        Returns:
            Lista de tuplas (cancha_id, month, count)
        """
        base_q = db.session.query(
            Reserva.cancha_id.label('cancha_id'),
            func.strftime('%Y-%m', Timeslot.inicio).label('month'),
            func.count(func.distinct(Reserva.id)).label('count')
        ).join(Reserva.timeslots).join(Timeslot)
        
        if cancha_id:
            base_q = base_q.filter(Reserva.cancha_id == cancha_id)
        if start_date:
            base_q = base_q.filter(
                Timeslot.inicio >= datetime.combine(start_date, datetime.min.time())
            )
        if end_date:
            base_q = base_q.filter(
                Timeslot.inicio <= datetime.combine(end_date, datetime.max.time())
            )
        
        base_q = base_q.group_by(Reserva.cancha_id, 'month')
        
        return base_q.all()
    
    def get_cancha_by_id(self, cancha_id: int):
        """
        Obtiene una cancha por su ID.
        
        Args:
            cancha_id: ID de la cancha
            
        Returns:
            Instancia de Cancha o None
        """
        return db.session.get(Cancha, cancha_id)
