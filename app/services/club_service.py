from app.repositories.club_repo import ClubRepository
from app.models.club import Club
from app.services.direccion_service import DireccionService

class ClubService:
    def __init__(self, db):
        self.club_repo = ClubRepository()
        self.direccion_service = DireccionService(db)

    def get_all(self):
        return self.club_repo.get_all()

    def get_by_id(self, id):
        return self.club_repo.get_by_id(id)

    def create(self, data):
    
        required_fields = ['nombre', 'cuit', 'telefono', 'direccion']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"El campo '{field}' es requerido")

        # Validar campos requeridos de dirección
        required_direccion_fields = ['calle', 'numero', 'ciudad', 'provincia']
        for field in required_direccion_fields:
            if field not in data['direccion'] or not data['direccion'][field]:
                raise ValueError(f"El campo 'direccion.{field}' es requerido")

        # Buscar o crear la dirección
        direccion = self.direccion_service.find_or_create_direccion(data['direccion'])

        # Crear el club
        nuevo_club = Club(
            nombre=data['nombre'],
            cuit=data['cuit'],
            telefono=data['telefono'],
            direccion_id=direccion.id
        )
        
        return self.club_repo.create(nuevo_club)

    def update(self, club_id, data):
        # Obtener el club existente
        club = self.get_by_id(club_id)
        if not club:
            raise ValueError("Club no encontrado")
    
        # Actualizar campos directos
        if 'nombre' in data:
            club.nombre = data['nombre']
        if 'cuit' in data:
            club.cuit = data['cuit']
        if 'telefono' in data:
            club.telefono = data['telefono']
        
        # Manejar la actualización de dirección si se proporciona
        if 'direccion' in data:
            # Validar campos requeridos de dirección
            required_direccion_fields = ['calle', 'numero', 'ciudad', 'provincia']
            for field in required_direccion_fields:
                if field not in data['direccion'] or not data['direccion'][field]:
                    raise ValueError(f"El campo 'direccion.{field}' es requerido")
            
            # Buscar o crear la nueva dirección
            direccion = self.direccion_service.find_or_create_direccion(data['direccion'])
            club.direccion_id = direccion.id
        
        return self.club_repo.update(club)

    def delete(self, club_id):
        return self.club_repo.delete(club_id)
    
    
