from datetime import datetime, date
from typing import Optional, List
from calendar import monthrange

from sqlalchemy import func

from app import db
from app.models.reserva import Reserva
from app.models.timeslot import Timeslot
from app.models.cancha import Cancha


def _month_iter(start: date, end: date) -> List[str]:
    """Return list of month strings 'YYYY-MM' from start to end inclusive."""
    months = []
    y = start.year
    m = start.month
    while (y, m) <= (end.year, end.month):
        months.append(f"{y:04d}-{m:02d}")
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1
    return months


def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def build_utilizacion_mensual(cancha_id: Optional[int] = None, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None):
    """
    Construye datos para un gráfico de utilización mensual de canchas.

    Parámetros:
      - cancha_id: opcional para filtrar una sola cancha
      - fecha_inicio / fecha_fin: rango en formato YYYY-MM-DD (opcional)

    Salida (JSON): {
      "months": ["2025-10","2025-11",...],
      "series": [
         {"cancha": {id,nombre,deporte}, "data": [count_for_month,...] },
         ...
      ]
    }
    """
    start_date = _parse_date(fecha_inicio)
    end_date = _parse_date(fecha_fin)

    # Prepare base query joining reservas -> timeslots
    base_q = db.session.query(
        Reserva.cancha_id.label('cancha_id'),
        func.strftime('%Y-%m', Timeslot.inicio).label('month'),
        func.count(func.distinct(Reserva.id)).label('count')
    ).join(Reserva.timeslots).join(Timeslot)

    if cancha_id:
        base_q = base_q.filter(Reserva.cancha_id == cancha_id)
    if start_date:
        base_q = base_q.filter(Timeslot.inicio >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        # include full day
        base_q = base_q.filter(Timeslot.inicio <= datetime.combine(end_date, datetime.max.time()))

    base_q = base_q.group_by(Reserva.cancha_id, 'month')

    rows = base_q.all()

    if not rows:
        # if no rows and no explicit date range, return empty structure
        if not (start_date and end_date):
            return {"months": [], "series": []}

    # Determine months range
    if start_date and end_date:
        months = _month_iter(start_date, end_date)
    else:
        # infer from rows
        months_set = set(r.month for r in rows)
        if not months_set:
            return {"months": [], "series": []}
        min_month = min(months_set)
        max_month = max(months_set)
        start_date = datetime.strptime(min_month + "-01", "%Y-%m-%d").date()
        y, m = map(int, max_month.split('-'))
        last_day = monthrange(y, m)[1]
        end_date = date(y, m, last_day)
        months = _month_iter(start_date, end_date)

    # Build mapping cancha_id -> {month: count}
    data_map = {}
    cancha_ids = set()
    for r in rows:
        cid = int(r.cancha_id)
        cancha_ids.add(cid)
        data_map.setdefault(cid, {})[r.month] = int(r.count)

    # If filtering by cancha_id but no rows, ensure series empty
    series = []
    if cancha_id and cancha_id not in cancha_ids:
        # return empty data for requested cancha
        cancha = db.session.get(Cancha, cancha_id)
        if cancha:
            series.append({
                "cancha": {"id": cancha.id, "nombre": cancha.nombre, "deporte": cancha.deporte},
                "data": [0 for _ in months]
            })
        return {"months": months, "series": series}

    # For each cancha found, build series aligned to months
    for cid in sorted(cancha_ids):
        cancha = db.session.get(Cancha, cid)
        if not cancha:
            continue
        counts = [data_map.get(cid, {}).get(month, 0) for month in months]
        series.append({
            "cancha": {"id": cancha.id, "nombre": cancha.nombre, "deporte": cancha.deporte},
            "data": counts
        })

    return {"months": months, "series": series}
