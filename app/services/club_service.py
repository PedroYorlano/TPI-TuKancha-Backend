from app.repositories.club_repo import ClubRepository
from app.models.club import Club

class ClubService:
    def __init__(self, db):
        self.club_repo = ClubRepository(db)

    def get_all(self):
        return self.club_repo.get_all()
    
    
