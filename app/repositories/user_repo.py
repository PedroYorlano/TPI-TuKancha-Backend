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
    
    def create(self, user):
        user = User(**user)
        return user
    
    def update(self, user):
        return user
    
    def delete(self, user):
        db.session.delete(user)
