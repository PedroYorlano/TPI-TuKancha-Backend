from datetime import datetime
from typing import Optional
from sqlalchemy import func

from app import db
from app.models.reserva import Reserva
from app.models.timeslot import Timeslot
from app.models.cancha import Cancha
from sqlalchemy import literal_column


def parse_date(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None


def build_canchas_mas_utilizadas(limit: int = 10, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None):
    """
    Devuelve un ranking de canchas más utilizadas (por cantidad de reservas) dentro de un periodo.

    Params:
      - limit: cantidad máxima de canchas a devolver
      - fecha_inicio / fecha_fin: strings 'YYYY-MM-DD' para filtrar por inicio de timeslot

    Retorna lista de objetos:
      [ { "cancha": {id,nombre,deporte,precio_hora}, "reservas_count": N, "total_ingresos": "123.45" }, ... ]
    """
    start_dt = parse_date(fecha_inicio)
    end_dt = parse_date(fecha_fin)
    if end_dt:
        end_dt = end_dt.replace(hour=23, minute=59, second=59)

    # Query agregada: contar reservas por cancha
    q = db.session.query(
        Reserva.cancha_id.label('cancha_id'),
        func.count(func.distinct(Reserva.id)).label('reservas_count'),
        func.coalesce(func.sum(Reserva.precio_total), 0).label('total_ingresos')
    ).join(Reserva.timeslots).join(Timeslot)

    if start_dt:
        q = q.filter(Timeslot.inicio >= start_dt)
    if end_dt:
        q = q.filter(Timeslot.inicio <= end_dt)

    # Asegurar que se ordena por el conteo DISTINCT de reservas por cancha
    q = q.group_by(Reserva.cancha_id).order_by(func.count(func.distinct(Reserva.id)).desc()).limit(limit)

    rows = q.all()

    # Calcular total de reservas en el periodo (para porcentaje)
    q_total = db.session.query(func.count(func.distinct(Reserva.id)))
    q_total = q_total.join(Reserva.timeslots).join(Timeslot)
    if start_dt:
        q_total = q_total.filter(Timeslot.inicio >= start_dt)
    if end_dt:
        q_total = q_total.filter(Timeslot.inicio <= end_dt)
    total_reservas_period = int(q_total.scalar() or 0)

    resultado = []
    for row in rows:
        cancha = db.session.get(Cancha, row.cancha_id)
        if not cancha:
            continue
        reservas_count = int(row.reservas_count)
        total_ingresos = float(row.total_ingresos or 0)
        porcentaje = 0.0
        if total_reservas_period > 0:
            porcentaje = (reservas_count / total_reservas_period) * 100.0

        resultado.append({
            "cancha": {
                "id": cancha.id,
                "nombre": cancha.nombre,
                "deporte": cancha.deporte,
                "precio_hora": cancha.precio_hora
            },
            "reservas_count": reservas_count,
            "total_ingresos": f"{total_ingresos:.2f}",
            "porcentaje_utilizacion": f"{porcentaje:.2f}%"
        })

    return resultado
