from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.auth.decorators import role_required

from reports.listado_reservas_por_cliente import build_reservas_por_cliente
from reports.listado_reservas_por_cancha import build_reservas_por_cancha
from reports.canchas_mas_utilizadas import build_canchas_mas_utilizadas
from reports.utilizacion_mensual import build_utilizacion_mensual

bp_reportes = Blueprint("reportes", __name__, url_prefix="/api/v1/reportes")


@bp_reportes.get('/reservas-por-cliente')
@jwt_required()
@role_required(['admin'])
def reservas_por_cliente():
    """Endpoint que devuelve las reservas agrupadas por cliente.

    Query params opcionales:
    - q: búsqueda por nombre o email (contiene)
    - cliente_email: búsqueda exacta por email
    """
    q = request.args.get('q')
    cliente_email = request.args.get('cliente_email')

    resultado = build_reservas_por_cliente(q=q, cliente_email=cliente_email)

    return jsonify(resultado), 200


@bp_reportes.get('/reservas-por-cancha')
@jwt_required()
@role_required(['admin'])
def reservas_por_cancha():
    """Endpoint que devuelve las reservas agrupadas por cancha en un período.

    Query params opcionales:
    - cancha_id: id de la cancha para filtrar (opcional)
    - fecha_inicio: YYYY-MM-DD (opcional)
    - fecha_fin: YYYY-MM-DD (opcional)
    """
    cancha_id = request.args.get('cancha_id', type=int)
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    resultado = build_reservas_por_cancha(cancha_id=cancha_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    return jsonify(resultado), 200


@bp_reportes.get('/canchas-mas-utilizadas')
@jwt_required()
@role_required(['admin'])
def canchas_mas_utilizadas():
    """Endpoint que devuelve el top de canchas más utilizadas.

    Query params opcionales:
    - limit: número máximo de canchas a devolver (int)
    - fecha_inicio: YYYY-MM-DD (opcional)
    - fecha_fin: YYYY-MM-DD (opcional)
    """
    limit = request.args.get('limit', default=10, type=int)
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    resultado = build_canchas_mas_utilizadas(limit=limit, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    return jsonify(resultado), 200


@bp_reportes.get('/utilizacion-mensual')
@jwt_required()
@role_required(['admin'])
def utilizacion_mensual():
    """Endpoint que devuelve datos ya procesados para gráfico de utilización mensual.

    Query params opcionales:
    - cancha_id: id de cancha a filtrar (int)
    - fecha_inicio: YYYY-MM-DD (opcional)
    - fecha_fin: YYYY-MM-DD (opcional)
    """
    cancha_id = request.args.get('cancha_id', type=int)
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    resultado = build_utilizacion_mensual(cancha_id=cancha_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    return jsonify(resultado), 200
