from marshmallow import Schema, fields

from app.api.model import Location


# one layer above db mappings
# schema = msg to what api uses - models -> schemas almost = 1:1
class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creation_time = fields.DateTime()

    class Meta:
        model = Location
