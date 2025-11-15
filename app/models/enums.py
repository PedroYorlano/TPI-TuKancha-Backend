from enum import Enum


class ReservaEstado(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    NO_ASISTIO = "NO_ASISTIO"
    PAGADO = "PAGADO"


class FuenteReserva(Enum):
    WEB = "WEB"
    PRESENCIAL = "PRESENCIAL"
    TELEFONICA = "TELEFONICA"


class TorneoEstado(Enum):
    CREADO = "CREADO"
    ACTIVO = "ACTIVO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"


class DiaSemana(Enum):
    LUN = "LUN"
    MAR = "MAR"
    MIE = "MIE"
    JUE = "JUE"
    VIE = "VIE"
    SAB = "SAB"
    DOM = "DOM"


class TimeslotEstado(Enum):
    DISPONIBLE = "DISPONIBLE"
    RESERVADO = "RESERVADO"
    BLOQUEADO = "BLOQUEADO"
    NO_GENERADO = "NO_GENERADO"
