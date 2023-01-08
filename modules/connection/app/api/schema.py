from marshmallow import Schema, fields

from api.schema import PersonSchema, LocationSchema


# one layer above db mappings
# schema = msg to what api uses - models -> schemas almost = 1:1
class ConnectionSchema(Schema):
    location = fields.Nested(LocationSchema)
    person = fields.Nested(PersonSchema)
