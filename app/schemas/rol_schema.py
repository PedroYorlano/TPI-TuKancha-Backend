from app.models.rol import Rol
from app import ma


class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        fields = (
            "id", 
            "nombre", 
        )
        load_instance = True
        include_relationships = True

rol_schema = RolSchema()
rols_schema = RolSchema(many=True)
