
# repeaters.json = https://radioid.net/static/rptrs.json
# users.json =https://radioid.net/static/users.json

from pathlib import Path

import urllib3
import loading.users as users
import loading.repeaters as repeaters


USERS_URL = "https://radioid.net/static/users.json"
REPEATERS_URL = "https://radioid.net/static/rptrs.json"

http = urllib3.PoolManager()

country = "Switzerland"

# users_response = http.request("GET", USERS_URL)
# users = list(users.load_from_data(users_response.data.decode()))
user_list = list(users.load_from_file(Path("data/users.json")))
filtered_users = users.filter_by_country(user_list, country)

# repeaters_response = http.request("GET", REPEATERS_URL)
# repeaters = list(repeaters.load_from_data(repeaters_response.data.decode()))
repeater_list = list(repeaters.load_from_file(Path("data/rptrs.json")))
filtered_repeaters = users.filter_by_country(repeater_list, country)
