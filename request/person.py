"""Define the schema used to validate the REST endpoint inputs for API 
calls relating to modifying the Persons table"""
from marshmallow import Schema, fields, post_load

class PersonRequestSchema(Schema):
    first_name = fields.Str(required=True)
    middle_name = fields.Str(default="")
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    age = fields.Integer(required=True)

    class Meta:
        unknown = 'EXCLUDE'