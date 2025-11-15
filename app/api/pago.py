from flask import Blueprint, jsonify, request
from app.services.mercadopago_service import MercadoPagoService

bp_pago = Blueprint("pago", __name__, url_prefix="/api/v1/pagos")

mercadopago_service = MercadoPagoService()


@bp_pago.post("/crear-preferencia/<int:reserva_id>")
def crear_preferencia(reserva_id):
    """
    Crea una preferencia de pago en Mercado Pago para una reserva.
    
    Returns:
        - preference_id: ID de la preferencia
        - init_point: URL para redirigir al usuario al checkout
        - sandbox_init_point: URL para testing (si estás en modo sandbox)
    """
    try:
        resultado = mercadopago_service.crear_preferencia_pago(reserva_id)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print("=" * 50)
        print("ERROR AL CREAR PREFERENCIA DE PAGO:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({"error": "Error al crear preferencia de pago", "details": str(e)}), 500


@bp_pago.post("/webhook")
def webhook():
    """
    Webhook para recibir notificaciones de Mercado Pago.
    Este endpoint será llamado por Mercado Pago cuando haya cambios en los pagos.
    """
    try:
        data = request.json
        resultado = mercadopago_service.procesar_notificacion_webhook(data)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print("=" * 50)
        print("ERROR EN WEBHOOK DE MERCADO PAGO:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print(f"Data recibida: {request.json}")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({"error": "Error al procesar webhook"}), 500


@bp_pago.get("/verificar-pago/<int:reserva_id>")
def verificar_pago(reserva_id):
    """
    Verifica el estado actual del pago de una reserva.
    Útil para consultar desde el frontend después de la redirección.
    """
    try:
        from app import db
        from app.models.reserva import Reserva
        
        reserva = db.session.get(Reserva, reserva_id)
        if not reserva:
            return jsonify({"error": "Reserva no encontrada"}), 404
        
        return jsonify({
            "reserva_id": reserva_id,
            "estado": reserva.estado.value,
            "pagado": reserva.estado.name == "CONFIRMADA"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
