from app.models.club import Club
from app import db

class ClubRepository:
    def __init__(self):
        pass

    def get_all(self):
        return Club.query.all()
    
    def get_by_id(self, id):
        return Club.query.get(id)
    
    def create(self, club):
        db.session.add(club)
        return club
    
    def delete(self, club):
        db.session.delete(club)
