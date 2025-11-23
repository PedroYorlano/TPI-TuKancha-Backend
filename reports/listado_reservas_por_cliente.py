from collections import defaultdict
from app.models.reserva import Reserva
from app.schemas.reserva_schema import reservas_schema


def build_reservas_por_cliente(q: str = None, cliente_email: str = None):
    """
    Construye un listado de reservas agrupadas por cliente.

    Parámetros:
    - q: búsqueda libre que compara con nombre o email del cliente (opcional)
    - cliente_email: búsqueda exacta por email del cliente (opcional)

    Retorna una lista de objetos con la forma:
    [
      {
        "cliente_email": "...",
        "cliente_nombre": "...",
        "cliente_telefono": "...",
        "reservas": [ ...reservas serializadas... ]
      },
      ...
    ]
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

    reservas = query.order_by(Reserva.cliente_email, Reserva.created_at).all()

    grupos = defaultdict(list)
    info_cliente = {}

    for r in reservas:
        key = (r.cliente_email or "", r.cliente_nombre or "")
        grupos[key].append(r)
        # Guardar telefono (último valor disponible)
        info_cliente[key] = r.cliente_telefono

    resultado = []
    for (email, nombre), lista in grupos.items():
        resultado.append({
            "cliente_email": email,
            "cliente_nombre": nombre,
            "cliente_telefono": info_cliente.get((email, nombre)),
            "reservas": reservas_schema.dump(lista)
        })

    return resultado
