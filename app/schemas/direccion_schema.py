from app import ma
from app.models.direccion import Direccion

class DireccionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Direccion
        fields = ("calle", "numero", "ciudad", "provincia", "pais") 
        load_instance = True

direccion_schema = DireccionSchema()