from io import FileIO
import json
from pathlib import Path
import typing


class User(typing.NamedTuple):
    fname: str
    name: str
    country: str
    callsign: str
    city: str
    state: str
    surname: str
    radio_id: int
    id: int


def load_from_data(data) -> typing.List[User]:
    users = []
    for user in json.loads(data)["users"]:
        users.append(User(**user))
    return users


def load_from_file(filename: Path) -> typing.List[User]:
    with open(filename) as file:
        return load_from_data(file.read())


def filter_by_country(users: typing.List[User], country: str) -> typing.List[User]:
    return list(filter(lambda user: user.country == country, users))
