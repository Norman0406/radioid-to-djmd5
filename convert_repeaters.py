from pathlib import Path
import typing
import click
import urllib3

from loading import repeaters
from conversion import repeaters_to_channels
from saving import channels

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
    default="channels.csv",
    help="Output CSV file location.")
def convert_repeaters(countries: typing.List[str], input: typing.Optional[Path], output: Path):
    """Convert RadioID.net repeaters to channels"""

    if input:
        repeater_list = repeaters.load_from_file(input)
    else:
        http = urllib3.PoolManager()
        response = http.request("GET", REPEATERS_URL)
        repeater_list = repeaters.load_from_data(response.data.decode())

    print(f"Loaded {len(repeater_list)} repeaters")

    if len(countries) > 0:
        repeater_list = repeaters.filter_by_countries(
            repeater_list, countries)
        print(
            f"Repeater list has been filtered to {len(repeater_list)} repeaters")

    channel_list = repeaters_to_channels.convert(repeater_list)
    channels.write_to_file(output, channel_list)

    print("Finished")
