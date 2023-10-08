
# repeaters.json = https://radioid.net/static/rptrs.json
# users.json =https://radioid.net/static/users.json

from pathlib import Path

import urllib3
import loading.users as users
import loading.repeaters as repeaters
import conversion.user_to_contact as user_to_contact
import saving.digital_contact_list as digital_contact_list


USERS_URL = "https://radioid.net/static/users.json"
REPEATERS_URL = "https://radioid.net/static/rptrs.json"

http = urllib3.PoolManager()

countries = ["Germany", "Switzerland", "Italy", "France"]

def convert_users_to_contacts():
    # users_response = http.request("GET", USERS_URL)
    # users = users.load_from_data(users_response.data.decode())
    user_list = users.load_from_file("data/users.json")
    filtered_users = users.filter_by_countries(user_list, countries)
    contacts = user_to_contact.convert(filtered_users)
    digital_contact_list.write_to_file("contact_list.csv", contacts)


def convert_repeaters_to_channels():
    # repeaters_response = http.request("GET", REPEATERS_URL)
    # repeaters = repeaters.load_from_data(repeaters_response.data.decode())
    repeater_list = repeaters.load_from_file(Path("data/rptrs.json"))
    filtered_repeaters = users.filter_by_countries(repeater_list, countries)

convert_users_to_contacts()
