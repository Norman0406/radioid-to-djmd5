
from pathlib import Path
import typing
import click
import urllib3

from loading import repeaters

REPEATERS_URL = "https://radioid.net/static/rptrs.json"


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--country",
    "countries",
    multiple=True,
    help="One or more countries by which the result should be filtered.")
@click.option(
    "--input",
    type=Path,
    required=False,
    help="Optional input file. If set, this JSON file will be used as input. If not set, RadioID.net will be queried.")
@click.option(
    "--output",
    type=Path,
    default="digital_contact_list.csv",
    help="Output CSV file location.")
def convert_repeaters(countries: typing.List[str], input: typing.Optional[Path], output: Path):
    """Convert RadioID.net repeaters to channels"""

    if input:
        user_list = repeaters.load_from_file(input)
    else:
        http = urllib3.PoolManager()
        response = http.request("GET", REPEATERS_URL)
        user_list = repeaters.load_from_data(response.data.decode())

    if len(countries) > 0:
        user_list = repeaters.filter_by_countries(user_list, countries)

    print("Warning: export functionality not yet implemented")
