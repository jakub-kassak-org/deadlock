import xmltodict
import urllib.request
import urllib.parse
from typing import List
from constants import USERS_RETREIVE_URL, USERS_UPDATE_URL


def retreive_students() -> List[str]:
    with urllib.request.urlopen(USERS_RETREIVE_URL) as f:
        students_xml_str = f.read().decode('utf-8')
    students_dict = xmltodict.parse(students_xml_str)
    students = students_dict['cdo:Osoby']['cdo:Osoba']
    card_numbers = [s['cdo:snr'] for s in students]
    return card_numbers


def update_db(card_numbers: List[str]):
    data = urllib.parse.urlencode({'cards': retreive_students()})
    req = urllib.request.Request(USERS_UPDATE_URL, data=data)
    res = urllib.request.urlopen(req)
    return res


update_db(retreive_students())
