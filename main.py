import click
from convert_repeaters import cli as convert_repeaters
from convert_users import cli as convert_users

commands = [
    convert_repeaters,
    convert_users
]


@click.group(cls=click.CommandCollection, sources=commands)
def main():
    """RadioID.net to DJ-MD5 converter"""


if __name__ == '__main__':
    main()
