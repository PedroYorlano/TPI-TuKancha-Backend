from app import create_app, db
from app.models.club import Club
from app.models.direccion import Direccion

app = create_app()

with app.app_context():
    # Crear tablas
    db.create_all()
    
    # datos de prueba
    direccion = Direccion(
        calle="Calle Falsa",
        numero="123",
        ciudad="Ciudad Ejemplo",
        provincia="Provincia Ejemplo"
    )
    db.session.add(direccion)
    db.session.commit()
    
    club = Club(
        nombre="Club de Prueba",
        cuit="30-12345678-9",
        telefono="1234567890",
        direccion_id=direccion.id
    )
    db.session.add(club)
    db.session.commit()
    
    print("Base de datos inicializada con datos de prueba")