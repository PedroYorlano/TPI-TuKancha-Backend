from app.models.user import User
from app import db

class UserRepository:
    def __init__(self):
        pass
    
    def get_all(self):
        return User.query.all()
    
    def get_by_id(self, id):
        return User.query.get(id)
    
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def get_by_club(self, club_id):
        return User.query.filter_by(club_id=club_id).all()
    
    def create(self, user):
        db.session.add(user)
        return user
    
    def update(self, user, data):
        for key, value in data.items():
            if hasattr(user, key) and key != 'id':
                setattr(user, key, value)
        db.session.add(user)
        return user 
    
    def delete(self, user):
        db.session.delete(user)