"""
Script de prueba para verificar la creación automática de timeslots al crear una cancha.
Los timeslots se generan con configuración fija: 60 minutos sin solapamiento.
"""
from app import create_app, db
from app.services.cancha_service import CanchaService
from app.models.cancha import Cancha
from app.models.timeslot import Timeslot
from app.models.club import Club
from datetime import date, timedelta
from sqlalchemy import func

def test_cancha_creation_with_timeslots():
    print("="*70)
    print("TEST: Creación de Cancha con Generación Automática de Timeslots")
    print("="*70)
    
    # Obtener el club de prueba
    club = Club.query.filter_by(nombre="Club Atlético TuKancha").first()
    
    if not club:
        print("❌ No se encontró el club de prueba. Ejecuta seed_db.py primero.")
        return
    
    print(f"\n1. Club encontrado: {club.nombre} (ID: {club.id})")
    
    # Contar canchas antes
    canchas_antes = Cancha.query.filter_by(club_id=club.id).count()
    print(f"2. Canchas existentes antes: {canchas_antes}")
    
    # Crear nueva cancha usando el servicio
    print("\n3. Creando nueva cancha...")
    cancha_service = CanchaService(db)
    
    data = {
        "nombre": "Cancha Paddle TEST",
        "deporte": "Paddle",
        "superficie": 3.0,
        "techado": True,
        "iluminacion": True,
        "precio_hora": 200.00,
        "club_id": club.id
    }
    
    try:
        nueva_cancha = cancha_service.create(data)
        print(f"✅ Cancha creada: {nueva_cancha.nombre} (ID: {nueva_cancha.id})")
        
        # Verificar timeslots generados
        print("\n4. Verificando timeslots generados...")
        
        # Contar timeslots de esta cancha
        total_timeslots = Timeslot.query.filter_by(cancha_id=nueva_cancha.id).count()
        print(f"   Total de timeslots: {total_timeslots}")
        
        # Verificar rango de fechas
        fecha_min = db.session.query(func.min(func.date(Timeslot.inicio))).filter_by(cancha_id=nueva_cancha.id).scalar()
        fecha_max = db.session.query(func.max(func.date(Timeslot.inicio))).filter_by(cancha_id=nueva_cancha.id).scalar()
        
        if fecha_min and fecha_max:
            # Convertir strings a objetos date si es necesario
            if isinstance(fecha_min, str):
                from datetime import datetime
                fecha_min = datetime.strptime(fecha_min, '%Y-%m-%d').date()
                fecha_max = datetime.strptime(fecha_max, '%Y-%m-%d').date()
            
            print(f"   Fecha inicial: {fecha_min}")
            print(f"   Fecha final: {fecha_max}")
            dias_cubiertos = (fecha_max - fecha_min).days + 1
            print(f"   Días cubiertos: {dias_cubiertos}")
            
            # Verificar que sea aproximadamente 90 días (3 meses)
            if 85 <= dias_cubiertos <= 95:
                print(f"   ✅ Cobertura de ~3 meses correcta")
            else:
                print(f"   ⚠️  Advertencia: Se esperaban ~90 días, se generaron {dias_cubiertos}")
        
        # Mostrar algunos timeslots de ejemplo
        print("\n5. Primeros 5 timeslots de ejemplo:")
        timeslots_muestra = (
            Timeslot.query
            .filter_by(cancha_id=nueva_cancha.id)
            .order_by(Timeslot.inicio)
            .limit(5)
            .all()
        )
        
        for ts in timeslots_muestra:
            print(f"   - {ts.inicio.strftime('%Y-%m-%d %H:%M')} a {ts.fin.strftime('%H:%M')} - Estado: {ts.estado.value} - Precio: ${ts.precio}")
        
        # Verificar duplicados
        print("\n6. Verificando duplicados...")
        duplicados = (
            db.session.query(
                Timeslot.cancha_id,
                Timeslot.inicio,
                Timeslot.fin,
                func.count(Timeslot.id).label('count')
            )
            .filter(Timeslot.cancha_id == nueva_cancha.id)
            .group_by(Timeslot.cancha_id, Timeslot.inicio, Timeslot.fin)
            .having(func.count(Timeslot.id) > 1)
            .all()
        )
        
        if duplicados:
            print(f"   ❌ ERROR: Se encontraron {len(duplicados)} timeslots duplicados:")
            for dup in duplicados[:5]:  # Mostrar solo los primeros 5
                print(f"      - Cancha {dup.cancha_id}: {dup.inicio} a {dup.fin} ({dup.count} veces)")
        else:
            print(f"   ✅ No se encontraron duplicados")
        
        print("\n" + "="*70)
        print("TEST COMPLETADO EXITOSAMENTE")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR al crear la cancha:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        test_cancha_creation_with_timeslots()
