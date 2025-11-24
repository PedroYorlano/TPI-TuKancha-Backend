from collections import defaultdict
from datetime import datetime
from typing import Optional

from app.models.reserva import Reserva
from app.models.timeslot import Timeslot
from app.schemas.reserva_schema import reservas_schema


def parse_date(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    # Esperamos formato YYYY-MM-DD
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None


def build_reservas_por_cancha(cancha_id: Optional[int] = None, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None):
    """
    Construye un listado de reservas agrupadas por cancha dentro de un período.

    Parámetros:
    - cancha_id: filtrar por una cancha específica (opcional)
    - fecha_inicio, fecha_fin: strings en formato 'YYYY-MM-DD' que definen el periodo (opcional)

    Retorna lista de objetos:
    [ {
        "cancha": { ... },
        "total_reservas": 3,
        "total_ingresos": "300.00",
        "reservas": [ ...reservas serializadas... ]
    }, ... ]
    """

    start_dt = parse_date(fecha_inicio)
    end_dt = parse_date(fecha_fin)
    if end_dt:
        # incluir todo el día final
        end_dt = end_dt.replace(hour=23, minute=59, second=59)

    # Base query: reservas con join a timeslots para filtrar por inicio de timeslot
    query = Reserva.query.join(Reserva.timeslots).join(Timeslot)

    if cancha_id:
        query = query.filter(Reserva.cancha_id == cancha_id)

    if start_dt:
        query = query.filter(Timeslot.inicio >= start_dt)
    if end_dt:
        query = query.filter(Timeslot.inicio <= end_dt)

    # ordenar por cancha y timeslot inicio
    reservas = query.order_by(Reserva.cancha_id, Timeslot.inicio).all()

    grupos = defaultdict(list)
    cancha_info = {}

    for r in reservas:
        key = r.cancha_id
        grupos[key].append(r)
        cancha_info[key] = r.cancha

    resultado = []
    for cancha_id_key, lista in grupos.items():
        total = sum([float(r.precio_total) if r.precio_total is not None else 0 for r in lista])
        resultado.append({
            "cancha": {
                "id": cancha_info[cancha_id_key].id,
                "nombre": cancha_info[cancha_id_key].nombre,
                "deporte": cancha_info[cancha_id_key].deporte,
                "precio_hora": cancha_info[cancha_id_key].precio_hora,
            },
            "total_reservas": len(lista),
            "total_ingresos": f"{total:.2f}",
            "reservas": reservas_schema.dump(lista)
        })

    return resultado
