from app.repositories.reserva_repo import ReservaRepository
from app.models.reserva import Reserva
from app.models.timeslot import Timeslot, TimeslotEstado
from app.models.reserva_timeslot import ReservaTimeslot
from app import db
from datetime import datetime

class ReservaService:
    def __init__(self):
        self.db = db
        self.reserva_repo = ReservaRepository()

    def get_all(self):
        return self.reserva_repo.get_all()

    def get_by_id(self, id):
        return self.reserva_repo.get_by_id(id)

    def create(self, data):
        """
        Crea una reserva bloqueando uno o más timeslots.
        
        Campos requeridos:
        - timeslot_ids: lista de IDs de timeslots a reservar
        - cliente_nombre: nombre del cliente
        - cliente_telefono: teléfono del cliente  
        - cliente_email: email del cliente (OBLIGATORIO)
        - fuente: origen de la reserva (WEB, TELEFONO, PRESENCIAL, WHATSAPP)
        - servicios: lista de servicios adicionales separados por coma (opcional)
        """
        # Validar campos requeridos
        required_fields = ['timeslot_ids', 'cliente_nombre', 'cliente_email', 'fuente']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"El campo '{field}' es requerido")
        
        timeslot_ids = data.get('timeslot_ids')
        if not isinstance(timeslot_ids, list) or len(timeslot_ids) == 0:
            raise ValueError("'timeslot_ids' debe ser una lista con al menos un ID")

        try:
            # Bloquear timeslots
            timeslots = Timeslot.query.filter(Timeslot.id.in_(timeslot_ids))\
                                     .with_for_update()\
                                     .all()

            if len(timeslots) != len(timeslot_ids):
                raise ValueError("Uno o más timeslots no existen.")

            precio_total = 0
            
            # Validar disponibilidad
            for ts in timeslots:
                if ts.estado != TimeslotEstado.DISPONIBLE:
                    raise ValueError(f"El timeslot {ts.id} (de {ts.inicio}) ya no está disponible.")
                precio_total += ts.precio

            # Crear reserva
            nueva_reserva = Reserva(
                cancha_id=timeslots[0].cancha_id,  # Todas deben ser de la misma cancha
                cliente_nombre=data['cliente_nombre'],
                cliente_telefono=data.get('cliente_telefono'),
                cliente_email=data['cliente_email'],
                fuente=data['fuente'],
                servicios=data.get('servicios', ''),  # Lista separada por comas
                precio_total=precio_total
            )
            self.db.session.add(nueva_reserva)
            self.db.session.flush()

            # Vincular y actualizar timeslots
            for ts in timeslots:
                ts.estado = TimeslotEstado.RESERVADO
                
                link = ReservaTimeslot(
                    reserva_id=nueva_reserva.id,
                    timeslot_id=ts.id
                )
                self.db.session.add(link)

            # Confirmar transacción
            self.db.session.commit()
            return nueva_reserva

        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al crear la reserva: {str(e)}")


    # ESTO ES PELIGROSO: cuando borro una reserva quiero que se liberen los timeslots asociados.
    # def delete(self, reserva_id):
    #     try:
    #         reserva = self.reserva_repo.get_by_id(reserva_id)
    #         if not reserva:
    #             raise ValueError("Reserva no encontrada")
    #         self.db.session.delete(reserva)
    #         self.db.session.commit()
    #         return {"message": "Reserva eliminada exitosamente"}
    #     except Exception as e:
    #         self.db.session.rollback()
    #         raise ValueError(f"Error al eliminar la reserva: {str(e)}")

    def cancelar_reserva(self, reserva_id):
        """
        Cancela una reserva y libera los timeslots.
        """
        try:
            reserva = self.reserva_repo.get_by_id(reserva_id)
            if not reserva:
                raise ValueError("Reserva no encontrada")

            links = ReservaTimeslot.query.filter_by(reserva_id=reserva_id).all()
            timeslot_ids = [link.timeslot_id for link in links]

            # Liberar timeslots
            if timeslot_ids:
                # Bloquear timeslots para actualizarlos
                timeslots = Timeslot.query.filter(Timeslot.id.in_(timeslot_ids))\
                                         .with_for_update()\
                                         .all()
                
                for ts in timeslots:
                    ts.estado = TimeslotEstado.DISPONIBLE
            
            # borrar links
            for link in links:
                self.db.session.delete(link)

            # borrar reserva
            self.db.session.delete(reserva)
            
            self.db.session.commit()
            return {"mensaje": "Reserva cancelada y timeslots liberados."}

        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al cancelar la reserva: {str(e)}")

    def marcar_reserva_pagada(self, reserva_id):
        """
        Marca una reserva como pagada (cambia el estado a PAGADO).
        """
        try:
            reserva = self.reserva_repo.get_by_id(reserva_id)
            if not reserva:
                raise ValueError("Reserva no encontrada")
            
            from app.models.enums import ReservaEstado
            reserva.estado = ReservaEstado.PAGADO
            self.db.session.commit()
            return reserva
        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al actualizar el pago: {str(e)}")