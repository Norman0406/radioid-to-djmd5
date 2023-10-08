import csv
from enum import Enum
from pathlib import Path
import typing

HEADER=["No.","Radio ID","Callsign","Name","City","State","Country","Remarks","Call Type","Call Alert"]

class CallType(str, Enum):
    PRIVATE_CALL = "Private Call",
    GROUP_CALL = "Group Call",
    ALL_CALL = "All Call"


class CallAlert(str, Enum):
    NONE = "None",
    RING = "Ring",
    ONLINE_ALERT = "Online Alert"


class UserContact(typing.NamedTuple):
    radio_id: int
    callsign: str
    name: str
    city: str
    state: str
    country: str
    remarks: str


class _Contact(typing.NamedTuple):
    id: int
    call_type: CallType
    call_alert: CallAlert
    user_contact: UserContact

    def __str__(self):
        return f"{self.user_contact.callsign} {self.user_contact.name} {self.user_contact.city} {self.user_contact.state} {self.user_contact.country} {self.user_contact.remarks}"


def _create_contact_list(user_contacts: typing.List[UserContact]) -> typing.List[_Contact]:
    contacts = []

    id = 1
    for user_contact in user_contacts:
        contacts.append(_Contact(
            id,
            CallType.PRIVATE_CALL,
            CallAlert.NONE,
            user_contact
        ))
        id = id + 1

    return contacts


def write_to_file(filename: Path, contacts: typing.List[UserContact]):
    print(f"Exporting {len(contacts)} contacts to {filename}")

    contacts = _create_contact_list(contacts)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
        writer.writerow(HEADER)

        contacts_written = 0
        for contact in contacts:
            try:
                writer.writerow([
                    contact.id,
                    contact.user_contact.radio_id,
                    contact.user_contact.callsign,
                    contact.user_contact.name,
                    contact.user_contact.city,
                    contact.user_contact.state,
                    contact.user_contact.country,
                    contact.user_contact.remarks,
                    contact.call_type.value,
                    contact.call_alert.value
                ])
                contacts_written = contacts_written + 1
            except Exception as e:
                print(f"Contact '{contact}' could not be written: \n\t{e}")

        print(f"Exported {contacts_written} contacts")
