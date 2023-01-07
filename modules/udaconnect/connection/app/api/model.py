from __future__ import annotations

from dataclasses import dataclass

from app import db  # noqa

from modules.api.app.udaconnect.location.models import Location
from modules.api.app.udaconnect.person.models import Person


@dataclass
class Connection:
    location: Location
    person: Person
