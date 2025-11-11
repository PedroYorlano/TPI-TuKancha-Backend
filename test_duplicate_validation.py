"""
Script de prueba para verificar que la validación de duplicados funciona correctamente.
Intentará crear timeslots duplicados y verificará que se detecten.
"""
from app import create_app, db
from app.services.timeslot_service import TimeslotService
from app.models.cancha import Cancha
from app.models.timeslot import Timeslot
from app.models.club import Club
from datetime import date, time, timedelta

def test_duplicate_validation():
    print("="*70)
    print("TEST: Validación de Duplicados en Timeslots")
    print("="*70)
    
    # Obtener una cancha existente
    cancha = Cancha.query.filter_by(nombre="Cancha Paddle TEST").first()
    
    if not cancha:
        print("❌ No se encontró la cancha de prueba. Ejecuta test_cancha_creation.py primero.")
        return
    
    print(f"\n1. Cancha encontrada: {cancha.nombre} (ID: {cancha.id})")
    
    # Contar timeslots antes
    timeslots_antes = Timeslot.query.filter_by(cancha_id=cancha.id).count()
    print(f"2. Timeslots existentes antes: {timeslots_antes}")
    
    # Intentar generar timeslots de nuevo para las mismas fechas
    print("\n3. Intentando generar timeslots para las mismas fechas...")
    print("   (Esto debería detectar duplicados y no crear ninguno nuevo)")
    
    timeslot_service = TimeslotService(db)
    
    fecha_desde = date.today()
    fecha_hasta = fecha_desde + timedelta(days=90)
    horario_apertura = time(8, 0)
    horario_cierre = time(22, 0)
    
    try:
        resultado = timeslot_service.generar_timeslots_para_cancha(
            cancha=cancha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            horario_apertura=horario_apertura,
            horario_cierre=horario_cierre,
            auto_commit=True
        )
        
        print(f"   Resultado: {resultado['mensaje']}")
        print(f"   Cantidad generada: {resultado['cantidad']}")
        
        # Contar timeslots después
        timeslots_despues = Timeslot.query.filter_by(cancha_id=cancha.id).count()
        print(f"\n4. Timeslots existentes después: {timeslots_despues}")
        
        diferencia = timeslots_despues - timeslots_antes
        
        if diferencia == 0:
            print(f"   ✅ CORRECTO: No se crearon duplicados ({timeslots_antes} antes, {timeslots_despues} después)")
        else:
            print(f"   ❌ ERROR: Se crearon {diferencia} timeslots duplicados")
            print(f"   Había {timeslots_antes}, ahora hay {timeslots_despues}")
        
        # Intentar generar para fechas parcialmente nuevas
        print("\n5. Intentando generar timeslots para fechas parcialmente nuevas...")
        print("   (Los días que ya existen deberían omitirse)")
        
        fecha_desde_nueva = date.today() + timedelta(days=85)  # Overlap de 5 días
        fecha_hasta_nueva = fecha_desde_nueva + timedelta(days=10)  # 5 días nuevos
        
        timeslots_antes_2 = Timeslot.query.filter_by(cancha_id=cancha.id).count()
        
        resultado2 = timeslot_service.generar_timeslots_para_cancha(
            cancha=cancha,
            fecha_desde=fecha_desde_nueva,
            fecha_hasta=fecha_hasta_nueva,
            horario_apertura=horario_apertura,
            horario_cierre=horario_cierre,
            auto_commit=True
        )
        
        timeslots_despues_2 = Timeslot.query.filter_by(cancha_id=cancha.id).count()
        nuevos_creados = timeslots_despues_2 - timeslots_antes_2
        
        print(f"   {resultado2['mensaje']}")
        print(f"   Timeslots nuevos creados: {nuevos_creados}")
        
        # Con 14 horas al día (8:00 a 22:00), deberían ser ~70 timeslots (5 días × 14)
        if 60 <= nuevos_creados <= 80:
            print(f"   ✅ Cantidad esperada de nuevos timeslots (~5 días)")
        else:
            print(f"   ⚠️  Se esperaban ~70 timeslots nuevos, se crearon {nuevos_creados}")
        
        print("\n" + "="*70)
        print("TEST DE VALIDACIÓN DE DUPLICADOS COMPLETADO")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR durante el test:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        test_duplicate_validation()
