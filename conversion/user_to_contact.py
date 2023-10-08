import typing
from loading.users import User
from saving.digital_contact_list import UserContact

def _convert_user_to_contact(user: User) -> UserContact:
    return UserContact(
        radio_id=user.radio_id,
        callsign=user.callsign,
        name=user.name,
        city=user.city,
        state=user.state,
        country=user.country,
        remarks=f"{user.fname} {user.surname}"
    )


def convert(users: typing.List[User]) -> typing.List[UserContact]:
    contacts = []
    for user in users:
        contacts.append(_convert_user_to_contact(user))
    return contacts
