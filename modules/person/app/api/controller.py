from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
from app.api.model import Person
from app.api.schema import PersonSchema
from app.api.service import PersonService
DATE_FORMAT = "%Y-%m-%d"

uda_api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa



@uda_api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema())
    @responds(schema=PersonSchema())
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@uda_api.route("/persons/<person_id>")
@uda_api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person
