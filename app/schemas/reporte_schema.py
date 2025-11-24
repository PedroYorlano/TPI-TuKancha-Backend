from marshmallow import Schema, fields


class CanchaReporteSchema(Schema):
    """Schema para información básica de cancha en reportes"""
    id = fields.Int(dump_only=True)
    nombre = fields.Str()
    deporte = fields.Str()
    precio_hora = fields.Decimal(as_string=True)


class ReservasPorClienteSchema(Schema):
    """Schema para el reporte de reservas agrupadas por cliente"""
    cliente_email = fields.Str()
    cliente_nombre = fields.Str()
    cliente_telefono = fields.Str()
    reservas = fields.List(fields.Dict())


class ReservasPorCanchaSchema(Schema):
    """Schema para el reporte de reservas agrupadas por cancha"""
    cancha = fields.Nested(CanchaReporteSchema)
    total_reservas = fields.Int()
    total_ingresos = fields.Str()
    reservas = fields.List(fields.Dict())


class CanchaUtilizadaSchema(Schema):
    """Schema para el reporte de canchas más utilizadas"""
    cancha = fields.Nested(CanchaReporteSchema)
    reservas_count = fields.Int()
    total_ingresos = fields.Str()
    porcentaje_utilizacion = fields.Str()


class SerieUtilizacionMensualSchema(Schema):
    """Schema para una serie de utilización mensual"""
    cancha = fields.Nested(CanchaReporteSchema)
    data = fields.List(fields.Int())


class UtilizacionMensualSchema(Schema):
    """Schema para el reporte de utilización mensual"""
    months = fields.List(fields.Str())
    series = fields.List(fields.Nested(SerieUtilizacionMensualSchema))


# Instancias de los schemas para uso en servicios
cancha_reporte_schema = CanchaReporteSchema()
reservas_por_cliente_schema = ReservasPorClienteSchema(many=True)
reservas_por_cancha_schema = ReservasPorCanchaSchema(many=True)
canchas_utilizadas_schema = CanchaUtilizadaSchema(many=True)
utilizacion_mensual_schema = UtilizacionMensualSchema()
