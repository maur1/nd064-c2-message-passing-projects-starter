
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from modules.udaconnect.location.app.api.model import Location
from modules.udaconnect.location.app.api.schema import LocationSchema
from modules.udaconnect.location.app.api.service import LocationService

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling
# Controller first pint
# controller uses schemas to respond in json
@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location

