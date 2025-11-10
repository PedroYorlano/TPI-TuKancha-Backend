from app.models.club_horario import ClubHorario
from app import db


class ClubHorarioRepository:
    def get_all(self):
        return ClubHorario.query.all()
    
    def get_by_id(self, id):
        return db.session.get(ClubHorario, id)
    
    def get_by_club_id(self, club_id):
        return ClubHorario.query.filter_by(club_id=club_id).all()
    
    def create(self, club_horario):
        db.session.add(club_horario)
        return club_horario
    
    def update(self, club_horario):
        db.session.add(club_horario)
        return club_horario
    
    def delete(self, club_horario):
        db.session.delete(club_horario)
