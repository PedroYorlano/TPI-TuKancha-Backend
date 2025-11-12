import os
from datetime import datetime, timedelta
from app import create_app, db
from app.models.rol import Rol
from app.models.user import User
from app.models.club import Club
from app.models.direccion import Direccion
from app.models.cancha import Cancha
from app.models.timeslot import Timeslot, TimeslotEstado
from werkzeug.security import generate_password_hash

# --- CONFIGURACIÓN ---
ADMIN_EMAIL = "admin@tukancha.com"
ADMIN_PASS = "admin123"

# --- EJECUCIÓN ---

def seed_data():
    """
    Puebla la base de datos con datos iniciales de prueba.
    Es idempotente: no duplicará datos si se corre múltiples veces.
    """
    print("Iniciando 'sembrado' de la base de datos...")
    
    # 1. Crear Roles
    try:
        if Rol.query.first():
            print("Roles ya existen. Omitiendo.")
            rol_admin = Rol.query.filter_by(nombre="admin").first()
        else:
            print("Creando Roles...")
            rol_admin = Rol(nombre="admin")
            rol_encargado = Rol(nombre="encargado")
            rol_recepcionista = Rol(nombre="recepcionista")
            db.session.add_all([rol_admin, rol_encargado, rol_recepcionista])
            db.session.flush() 
            print("✅ Roles creados: admin, encargado, recepcionista")
        
        # 2. Crear Usuario Admin (OMITIDO - los usuarios se crean con sus clubes)
        # No creamos usuario admin sin club porque club_id es NOT NULL
        print("NOTA: Los usuarios admin se crearán automáticamente al crear clubes.")

        # 3. Crear Club de Prueba y Dirección
        club_prueba = Club.query.filter_by(nombre="Club Atlético TuKancha").first()
        if club_prueba:
            print("Club de prueba ya existe. Omitiendo.")
            club_prueba = Club.query.filter_by(nombre="Club Atlético TuKancha").first()
        else:
            print("Creando Club de prueba...")
            dir_prueba = Direccion(
                calle="Av. Siempre Viva",
                numero="742",
                ciudad="Springfield",
                provincia="Springfield",
                pais="Argentina" 
            )
            
            club_prueba = Club(
                nombre="Club Atlético TuKancha",
                cuit="30-12345678-9",   
                telefono="351-000111", 
                direccion=dir_prueba 
            )
            db.session.add(club_prueba)
            db.session.flush() 
        
        # 4. Crear Canchas para el Club
        cancha_f5 = Cancha.query.filter_by(nombre="Cancha F5 (Techada)").first()
        if cancha_f5:
            print("Canchas de prueba ya existen. Omitiendo.")
            cancha_f5 = Cancha.query.filter_by(nombre="Cancha F5 (Techada)").first()
        else:
            print("Creando Canchas de prueba...")
            cancha_f5 = Cancha(
                nombre="Cancha F5 (Techada)",
                deporte="Fútbol 5",
                superficie=5.0,
                techado=True,
                iluminacion=True,
                precio_hora=100.00,
                activa=True,
                club_id=club_prueba.id
            )
            cancha_f7 = Cancha(
                nombre="Cancha F7 (Aire Libre)",
                deporte="Fútbol 7",
                superficie=7.0, 
                techado=False,
                iluminacion=True,
                precio_hora=150.00,
                activa=True,
                club_id=club_prueba.id
            )
            db.session.add_all([cancha_f5, cancha_f7])
            db.session.flush() 

        # 5. Crear Timeslots de prueba para la Cancha F5 para hoy
        if Timeslot.query.first():
             print("Timeslots de prueba ya existen. Omitiendo.")
        else:
            print(f"Creando Timeslots de prueba para hoy en '{cancha_f5.nombre}'...")
            hoy = datetime.now().date()
            hora_inicio = datetime(hoy.year, hoy.month, hoy.day, 18, 0, 0)
            
            for i in range(5):
                inicio_turno = hora_inicio + timedelta(hours=i)
                fin_turno = inicio_turno + timedelta(hours=1)
                
                ts = Timeslot(
                    cancha_id=cancha_f5.id,
                    inicio=inicio_turno,
                    fin=fin_turno,
                    estado=TimeslotEstado.DISPONIBLE,
                    precio=cancha_f5.precio_hora
                )
                db.session.add(ts)

        """ # 6. Crear Servicios Adicionales
        if Servicio.query.first():
            print("Servicios ya existen. Omitiendo.")
        else:
            print("Creando Servicios...")
            s_parrilla = Servicio(nombre="Parrilla")
            s_bebidas = Servicio(nombre="Bebidas")
            s_utileria = Servicio(nombre="Utilería")
            db.session.add_all([s_parrilla, s_bebidas, s_utileria]) """

        # --- Commit Final ---
        db.session.commit()
        print("\n¡Base de datos 'semeada' (poblada) con éxito!")

    except Exception as e:
        db.session.rollback()
        print(f"\nERROR: Ocurrió un error al 'semear' la base de datos.")
        print(f"Detalle: {e}")
    finally:
        db.session.remove()
        print("Cerrando sesión de base de datos.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_data()