from io import FileIO
import json
from pathlib import Path
import typing

import charset_normalizer


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


def _sanitize_data(user: User, data: typing.Any) -> typing.Any:
    if type(data) is not str:
        return data

    encoding = charset_normalizer.detect('AA')
    print(encoding)

    sanitized_string = ''.join(c for c in data if ord(c) < 256)

    if sanitized_string != data:
        print(
            f"User string for user {user} had to be sanitized: {sanitized_string}")

    return sanitized_string


def load_from_data(data) -> typing.List[User]:
    users = []
    for user in json.loads(data)["users"]:
        # for data in user:
        #     user[data] = _sanitize_data(user, user[data])

        users.append(User(**user))
    return users


def load_from_file(filename: Path) -> typing.List[User]:
    with open(filename, "r", encoding="utf-8") as file:
        return load_from_data(file.read())


def filter_by_countries(users: typing.List[User], countries: typing.List[str]) -> typing.List[User]:
    return list(filter(lambda user: user.country in countries, users))
