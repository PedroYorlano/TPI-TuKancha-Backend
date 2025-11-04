from app.models.club import Club
from app.db import db

class ClubRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return Club.query.all()
    
    def get_by_id(self, id):
        return Club.query.get(id)
    
    def create(self, club):
        self.db.session.add(club)
        self.db.session.commit()
        return club
    
    def update(self, club):
        self.db.session.commit()
        return club
    
    def delete(self, club):
        self.db.session.delete(club)
        self.db.session.commit()
