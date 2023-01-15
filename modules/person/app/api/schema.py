from marshmallow import Schema, fields

from app.api.model import Person


class PersonSchema(Schema): # translate objects to a schema
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    company_name = fields.String()

    class Meta:
        model = Person


