from marshmallow import Schema, fields

from modules.api.app.udaconnect.location.schemas import LocationSchema
from modules.api.app.udaconnect.person.schemas import PersonSchema


# one layer above db mappings
# schema = msg to what api uses - models -> schemas almost = 1:1
class ConnectionSchema(Schema):
    location = fields.Nested(LocationSchema)
    person = fields.Nested(PersonSchema)
