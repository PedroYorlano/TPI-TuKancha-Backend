from flask import Blueprint, jsonify
from app.db import db
from app.services.club_service import ClubService

bp = Blueprint("club", __name__, url_prefix="/api/v1/club")

club_service = ClubService(db)

@bp.get('/')
def listar_clubes():
    clubes = club_service.get_all()
    return jsonify([{"id": c.id, "nombre": c.nombre} for c in clubes])
    
