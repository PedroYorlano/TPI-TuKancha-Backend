from app.repositories.club_repo import ClubRepository
from app.models.club import Club
from app.repositories.direccion_repo import DireccionRepository
from app.models.direccion import Direccion

class ClubService:
    def __init__(self, db):
        self.club_repo = ClubRepository()
        self.direccion_repo = DireccionRepository(db)

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
        direccion_data = data['direccion']
        for field in required_direccion_fields:
            if field not in direccion_data or not direccion_data[field]:
                raise ValueError(f"El campo 'direccion.{field}' es requerido")

        # Buscar o crear la dirección
        direccion = self.direccion_repo.find_or_create_direccion(direccion_data)

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
        
        # Manejar la actualización de dirección si se proporciona
        if 'direccion' in data:
            direccion_data = data.pop('direccion')
            direccion = self.direccion_repo.find_or_create_direccion(direccion_data)
            club.direccion_id = direccion.id

        for key, value in data.items():
            if hasattr(club, key):
                setattr(club, key, value)
        
        return self.club_repo.update(club)

    def delete(self, club_id):
        return self.club_repo.delete(club_id)
    
    
