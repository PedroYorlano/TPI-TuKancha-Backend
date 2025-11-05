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
        'data' debe ser:
        {
            "timeslot_ids": [10, 11, 12],
            "cliente_nombre": "Juan Perez",
            "cliente_telefono": "351-123456"
        }
        """
        timeslot_ids = data.get('timeslot_ids')
        if not timeslot_ids:
            raise ValueError("Se requiere al menos un 'timeslot_id'")

        try:
            # bloquear timeslots
            timeslots = Timeslot.query.filter(Timeslot.id.in_(timeslot_ids))\
                                     .with_for_update()\
                                     .all()

            if len(timeslots) != len(timeslot_ids):
                raise ValueError("Uno o más timeslots no existen o ya fueron reservados.")

            precio_total = 0
            
            # validar
            for ts in timeslots:
                if ts.estado != TimeslotEstado.DISPONIBLE:
                    raise ValueError(f"El timeslot {ts.id} (de {ts.inicio}) ya no está disponible.")
                precio_total += ts.precio

            # crear reserva
            nueva_reserva = Reserva(
                cliente_nombre=data['cliente_nombre'],
                cliente_telefono=data.get('cliente_telefono'),
                precio_total=precio_total,
                estado_pago='PENDIENTE'
            )
            self.db.session.add(nueva_reserva)
            # Hacemos "flush" para que nueva_reserva.id tenga un valor
            self.db.session.flush()

            # vincular y actualizar timeslots
            for ts in timeslots:
                # Cambiamos el estado del timeslot
                ts.estado = TimeslotEstado.RESERVADO
                
                # Creamos el vínculo en la tabla pivot
                link = ReservaTimeslot(
                    reserva_id=nueva_reserva.id,
                    timeslot_id=ts.id
                )
                self.db.session.add(link)

            # confirmar transaccion
            self.db.session.commit()
            return nueva_reserva

        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al crear la reserva: {str(e)}")

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
        try:
            reserva = self.reserva_repo.get_by_id(reserva_id)
            if not reserva:
                raise ValueError("Reserva no encontrada")
            
            reserva.estado_pago = 'PAGADO'
            self.db.session.commit()
            return reserva
        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error al actualizar el pago: {str(e)}")