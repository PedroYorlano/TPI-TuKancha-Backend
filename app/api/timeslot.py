from flask import Blueprint, jsonify, request
from app import db
from app.services.timeslot_service import TimeslotService
from datetime import datetime

bp_timeslot = Blueprint("timeslot", __name__, url_prefix="/api/v1/timeslots")

timeslot_service = TimeslotService(db)


@bp_timeslot.get('/disponibilidad')
def get_disponibilidad():
    """
    Obtiene la disponibilidad de canchas por horario para un club y fecha.
    
    Query Parameters:
        club_id (int): ID del club - REQUERIDO
        fecha (str): Fecha en formato YYYY-MM-DD - REQUERIDO
    
    Response (200):
        {
            "club_id": 1,
            "fecha": "2025-11-15",
            "total_horarios": 12,
            "horarios": [
                {
                    "hora": "08:00",
                    "total_disponibles": 2,
                    "canchas_disponibles": [
                        {
                            "timeslot_id": 1,
                            "cancha_id": 1,
                            "nombre": "Cancha 1",
                            "deporte": "Fútbol 5",
                            "techado": true,
                            "iluminacion": true,
                            "superficie": 5.0,
                            "precio": 150.00,
                            "hora_inicio": "08:00",
                            "hora_fin": "09:00"
                        }
                    ]
                }
            ]
        }
    """
    # Validar parámetros requeridos
    club_id = request.args.get('club_id', type=int)
    fecha_str = request.args.get('fecha')
    
    if not club_id:
        return jsonify({"error": "El parámetro 'club_id' es requerido"}), 400
    
    if not fecha_str:
        return jsonify({"error": "El parámetro 'fecha' es requerido (formato: YYYY-MM-DD)"}), 400
    
    # Parsear y validar fecha
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
    
    # Obtener disponibilidad
    try:
        disponibilidad = timeslot_service.get_disponibilidad_por_club_y_fecha(club_id, fecha)
        return jsonify(disponibilidad), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
    except Exception as e:
        import traceback
        print("=" * 50)
        print("ERROR AL OBTENER DISPONIBILIDAD:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({
            "error": "Error al obtener disponibilidad",
            "details": str(e)
        }), 500


@bp_timeslot.post('/generar')
def generar_timeslots():
    """
    Genera timeslots para un club en un rango de fechas.
    
    Puede usar los horarios definidos en el club (recomendado) o especificar horarios fijos.
    
    Body (JSON) - Opción 1 (usa horarios del club por día de semana):
        {
            "club_id": 1,
            "fecha_desde": "2025-11-15",
            "fecha_hasta": "2025-11-30"
        }
    
    Body (JSON) - Opción 2 (usa horarios fijos para todos los días):
        {
            "club_id": 1,
            "fecha_desde": "2025-11-15",
            "fecha_hasta": "2025-11-30",
            "horario_apertura": "08:00",
            "horario_cierre": "22:00"
        }
    
    Response (201):
        {
            "mensaje": "Se generaron y guardaron 240 nuevos timeslots."
        }
    """
    data = request.get_json()
    
    # Validar campos requeridos mínimos
    required_fields = ['club_id', 'fecha_desde', 'fecha_hasta']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"El campo '{field}' es requerido"}), 400
    
    try:
        # Parsear fechas
        fecha_desde = datetime.strptime(data['fecha_desde'], '%Y-%m-%d').date()
        fecha_hasta = datetime.strptime(data['fecha_hasta'], '%Y-%m-%d').date()
        
        # Verificar si se proporcionan horarios específicos
        usar_horarios_club = True
        horario_apertura = None
        horario_cierre = None
        
        if 'horario_apertura' in data and 'horario_cierre' in data:
            # Usar horarios fijos
            usar_horarios_club = False
            horario_apertura = datetime.strptime(data['horario_apertura'], '%H:%M').time()
            horario_cierre = datetime.strptime(data['horario_cierre'], '%H:%M').time()
        
        # Generar timeslots
        resultado = timeslot_service.generar_timeslots_para_club(
            club_id=data['club_id'],
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            horario_apertura=horario_apertura,
            horario_cierre=horario_cierre,
            usar_horarios_club=usar_horarios_club
        )
        
        return jsonify(resultado), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        import traceback
        print("=" * 50)
        print("ERROR AL GENERAR TIMESLOTS:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({
            "error": "Error al generar timeslots",
            "details": str(e)
        }), 500