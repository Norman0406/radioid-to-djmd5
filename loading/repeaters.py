from io import FileIO
import json
from pathlib import Path
import typing


class Repeater(typing.NamedTuple):
    locator: str
    id: int
    callsign: str
    city: str
    state: str
    country: str
    frequency: str
    color_code: int
    offset: str
    assigned: str
    ts_linked: str
    trustee: str
    map_info: str
    map: int
    ipsc_network: str


def load_from_data(data) -> typing.List[Repeater]:
    repeaters = []
    for repeater in json.loads(data)["rptrs"]:
        repeaters.append(Repeater(**repeater))
    return repeaters


def load_from_file(filename: Path) -> typing.List[Repeater]:
    with open(filename, "r", encoding="utf-8") as file:
        return load_from_data(file.read())


def filter_by_countries(repeaters: typing.List[Repeater], countries: typing.List[str]) -> typing.List[Repeater]:
    return list(filter(lambda repeater: repeater.country in countries, repeaters))
