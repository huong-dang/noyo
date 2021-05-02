"""Define the schema useful for returning database results to the client"""
from ma import ma
from models.person import PersonModel

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonModel
        load_instance = True