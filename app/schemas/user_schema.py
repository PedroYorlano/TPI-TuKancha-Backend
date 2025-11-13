from app.models.user import User
from app import ma
from app.schemas.club_schema import ClubSchema
from app.schemas.rol_schema import RolSchema

# Schema de entrada
class UserCreateSchema(ma.Schema):
    nombre = ma.String(required=True)
    email = ma.Email(required=True)
    password = ma.String(required=True)
    rol_id = ma.Integer(required=True)
    club_id = ma.Integer(required=True)
    telefono = ma.Str(required=False)

# Schema de salida
class UserSchema(ma.SQLAlchemyAutoSchema):
    club = ma.Nested(ClubSchema)
    rol = ma.Nested(RolSchema)
    class Meta:
        model = User
        fields = (
            "id", 
            "club", 
            "rol", 
            "nombre", 
            "email", 
            "telefono", 
            "activo", 
            "created_at",
            "updated_at"
        )
        load_instance = True
        include_relationships = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_create_schema = UserCreateSchema()
