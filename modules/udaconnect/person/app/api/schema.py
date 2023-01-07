from marshmallow import Schema, fields

from modules.api.app.udaconnect.connection.models import Person


# one layer above db mappings
# schema = msg to what api uses - models -> schemas almost = 1:1

class PersonSchema(Schema): # translate objects to a schema
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    company_name = fields.String()

    class Meta:
        model = Person
