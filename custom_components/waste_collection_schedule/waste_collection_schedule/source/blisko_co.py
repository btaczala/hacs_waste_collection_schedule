from datetime import datetime
import urllib.request
import json
from string import Template
from waste_collection_schedule import Collection

TITLE = "Blisko"  # Title will show up in README.md and info.md
DESCRIPTION = "Blisko "  # Describe your source
# Insert url to service homepage. URL will show up in README.md and info.md
URL = "https://gateway.sisms.pl"
TEST_CASES = {  # Insert arguments for test cases to be used by test_sources.py script
    "Grzepnica/Rezydencka": {"city": "0774204", "street": "42719", "house": "32"},
}

API_URL = "https://gateway.sisms.pl"
ICON_MAP = {
    "Zmieszane odpady komunalne": "mdi:trash-can",
    "Papier i tektura": "mdi:recycle",
    "Odpady biodegradowalne": "mdi:leaf",
}

schedule_url_template = Template(
    "https://gateway.sisms.pl/akun/api/owners/112/timetable/get?unitId=32:11:01:2:${city}:${street}:${house}")
bins_url_template = Template(
    "https://gateway.sisms.pl/akun/api/owners/112/bins/list?unitId=32:11:01:2:${city}:${street}:${house}")


def find_bin_name(binId, json):
    for entry in json:
        if entry['id'] == binId:
            return entry['name']
    raise Exception


class Source:
    # argX correspond to the args dict in the source configuration
    def __init__(self, city, street, house):

        self._schedule_url = schedule_url_template.safe_substitute(
            city=city, street=street, house=house)
        self._bins_url = bins_url_template.safe_substitute(
            city=city, street=street, house=house)

    def fetch(self):

        entries = []  # List that holds collection schedule

        bins_data = urllib.request.urlopen(self._bins_url)
        bins = json.load(bins_data)['data']
        timetable_data = urllib.request.urlopen(self._schedule_url)
        timetable_json = json.load(timetable_data)["data"]

        for month_data in timetable_json:
            for reception in month_data['receptions']:
                entries.append(
                    Collection(
                        date=datetime.strptime(
                            reception['date'], '%Y-%m-%d').date(),
                        t=find_bin_name(binId=reception['binId'], json=bins),
                        icon=ICON_MAP.get("Waste Type"),  # Collection icon
                    )
                )

        return entries
