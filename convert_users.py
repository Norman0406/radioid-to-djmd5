from pathlib import Path
import typing
import click
import urllib3

from loading import users
from conversion import users_to_contacts
from saving import digital_contact_list

USERS_URL = "https://radioid.net/static/users.json"


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
def convert_users(countries: typing.List[str], input: typing.Optional[Path], output: Path):
    """Convert RadioID.net users to digital contacts"""

    if input:
        user_list = users.load_from_file(input)
    else:
        http = urllib3.PoolManager()
        response = http.request("GET", USERS_URL)
        user_list = users.load_from_data(response.data.decode())

    print(f"Loaded {len(user_list)} users")

    if len(countries) > 0:
        user_list = users.filter_by_countries(user_list, countries)
        print(f"Users list has been filtered to {len(user_list)} users")

    contact_list = users_to_contacts.convert(user_list)
    digital_contact_list.write_to_file(output, contact_list)

    print("Finished")
