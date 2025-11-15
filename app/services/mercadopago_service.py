import mercadopago
from flask import current_app
from app.models.reserva import Reserva
from app.models.enums import ReservaEstado
from app import db


class MercadoPagoService:
    def __init__(self):
        """
        Inicializa el SDK de Mercado Pago con el access token.
        """
        self.sdk = None
    
    def _get_sdk(self):
        """
        Obtiene una instancia del SDK de Mercado Pago.
        Se inicializa de forma lazy para tener acceso al current_app.
        """
        if self.sdk is None:
            access_token = current_app.config.get('MERCADOPAGO_ACCESS_TOKEN')
            if not access_token:
                raise ValueError("MERCADOPAGO_ACCESS_TOKEN no está configurado")
            self.sdk = mercadopago.SDK(access_token)
        return self.sdk
    
    def crear_preferencia_pago(self, reserva_id):
        """
        Crea una preferencia de pago en Mercado Pago para una reserva específica.
        
        Args:
            reserva_id (int): ID de la reserva a pagar
            
        Returns:
            dict: Contiene 'init_point' (URL de pago) y 'preference_id'
        """
        # Obtener la reserva
        reserva = db.session.get(Reserva, reserva_id)
        if not reserva:
            raise ValueError("Reserva no encontrada")
        
        # Verificar que la reserva esté en estado PENDIENTE
        if reserva.estado != ReservaEstado.PENDIENTE:
            raise ValueError(f"La reserva debe estar en estado PENDIENTE para poder pagar. Estado actual: {reserva.estado.value}")
        
        # Construir los items del pago
        items = []
        
        # Agregar los timeslots como items
        for reserva_timeslot in reserva.timeslots:
            timeslot = reserva_timeslot.timeslot
            items.append({
                "title": f"Cancha {reserva.cancha.nombre} - {timeslot.inicio.strftime('%d/%m/%Y %H:%M')}",
                "description": f"Reserva de cancha desde {timeslot.inicio.strftime('%H:%M')} hasta {timeslot.fin.strftime('%H:%M')}",
                "quantity": 1,
                "currency_id": "ARS",  # Cambiar según tu moneda
                "unit_price": float(timeslot.precio)
            })
        
        # URLs de retorno
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        backend_url = current_app.config.get('BACKEND_URL', 'http://localhost:5000')
        
        # Crear preferencia
        preference_data = {
            "items": items,
            "payer": {
                "name": reserva.cliente_nombre,
                "email": reserva.cliente_email,
                "phone": {
                    "number": reserva.cliente_telefono if reserva.cliente_telefono else ""
                }
            },
            "back_urls": {
                "success": f"{frontend_url}/reservas/{reserva_id}/pago/success",
                "failure": f"{frontend_url}/reservas/{reserva_id}/pago/failure",
                "pending": f"{frontend_url}reservas/{reserva_id}/pago/pending"
            },
            # "auto_return": "approved",  # Retorno automático cuando se aprueba
            # "back_urls": {
            #     "success": "https://www.tu-sitio/success",
            #     "failure": "https://www.tu-sitio/failure",
            #     "pending": "https://www.tu-sitio/pendings"
            # },
            "auto_return": "approved",
            "external_reference": str(reserva_id),  # Para identificar la reserva
            "notification_url": f"{backend_url}/api/v1/pagos/webhook",  # Webhook para notificaciones
            "statement_descriptor": "TuKancha Reserva",  # Aparece en el resumen de la tarjeta
            "metadata": {
                "reserva_id": reserva_id,
                "cliente_email": reserva.cliente_email
            }
        }

        print(preference_data)
        
        # Crear la preferencia en Mercado Pago
        sdk = self._get_sdk()
        preference_response = sdk.preference().create(preference_data)
        
        if preference_response["status"] != 201:
            raise ValueError(f"Error al crear preferencia de pago: {preference_response}")
        
        preference = preference_response["response"]
        
        return {
            "preference_id": preference["id"],
            "init_point": preference["init_point"],  # URL para entorno productivo
            "sandbox_init_point": preference.get("sandbox_init_point"),  # URL para testing
        }
    
    def obtener_pago(self, payment_id):
        """
        Obtiene información de un pago por su ID.
        
        Args:
            payment_id (str): ID del pago en Mercado Pago
            
        Returns:
            dict: Información del pago
        """
        sdk = self._get_sdk()
        payment_response = sdk.payment().get(payment_id)
        
        if payment_response["status"] != 200:
            raise ValueError(f"Error al obtener información del pago: {payment_response}")
        
        return payment_response["response"]
    
    def procesar_notificacion_webhook(self, data):
        """
        Procesa las notificaciones webhook de Mercado Pago.
        
        Args:
            data (dict): Datos del webhook
            
        Returns:
            dict: Resultado del procesamiento
        """
        # Mercado Pago envía diferentes tipos de notificaciones
        if data.get("type") == "payment":
            payment_id = data.get("data", {}).get("id")
            
            if not payment_id:
                raise ValueError("Payment ID no encontrado en la notificación")
            
            # Obtener información del pago
            payment_info = self.obtener_pago(payment_id)
            
            # Obtener la reserva asociada
            reserva_id = int(payment_info.get("external_reference"))
            reserva = db.session.get(Reserva, reserva_id)
            
            if not reserva:
                raise ValueError(f"Reserva {reserva_id} no encontrada")
            
            # Actualizar estado de la reserva según el estado del pago
            payment_status = payment_info.get("status")
            
            if payment_status == "approved":
                reserva.estado = ReservaEstado.CONFIRMADA
            elif payment_status in ["pending", "in_process"]:
                reserva.estado = ReservaEstado.PENDIENTE
            elif payment_status in ["rejected", "cancelled"]:
                reserva.estado = ReservaEstado.CANCELADA
            
            db.session.commit()
            
            return {
                "message": "Notificación procesada",
                "reserva_id": reserva_id,
                "payment_status": payment_status,
                "reserva_estado": reserva.estado.value
            }
        
        return {"message": "Tipo de notificación no manejada"}
