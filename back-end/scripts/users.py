#!/usr/bin/env python3
import os
from urllib.error import HTTPError

import xmltodict
import json
import urllib.request
import urllib.parse
from typing import OrderedDict, Dict


def get_token() -> str:
    try:
        data = {"username": "stlpik", "password": "secret"}
        body = urllib.parse.urlencode(data)
        req = urllib.request.Request('http://localhost/token/', body.encode("utf-8"))
        res = urllib.request.urlopen(req)
        res = json.loads(res.read())
        return f"{res['token_type']} {res['access_token']}"
    except urllib.error.URLError as e:
        print(e, e.reason)
        return ""


def create_req(url: str, token=None) -> urllib.request.Request:
    if token is None:
        token = get_token()
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Authorization', token)
    return req


def open_users_xml():
    try:
        with urllib.request.urlopen(os.environ["USERS_RETRIEVE_URL"]) as f:
            return f.read().decode("utf-8")
    except KeyError:
        pass
    try:
        with open(os.environ["USERS_RETRIEVE_FILENAME"], 'rb') as f:
            return f.read().decode("utf-8")
    except KeyError:
        print("USERS_RETRIEVE_URL nor USERS_RETRIEVE_FILENAME was set")
        raise


def load_users():
    users_dict = xmltodict.parse(open_users_xml())
    return [create_user(u) for u in users_dict['cdo:Osoby']['cdo:Osoba']]


def create_user(user: OrderedDict) -> Dict:
    groups = []
    if "cdo:Student" in user.keys():
        groups.append("Student")
    if "cdo:Zamestnanec" in user.keys():
        groups.append("Zamestnanec")
    return {
        "card": user["cdo:snr"],
        "username": user['cdo:Login']["cdo:LoginUK"],
        "first_name": user["cdo:Meno"],
        "last_name": user["cdo:Priezvisko"],
        "is_staff": False,
        "groups": groups
    }


def post_users(users):
    groups = {
        "Student": {
            "id": 2,
            "users": [],
        },
        "Zamestnanec": {
            "id": 3,
            "users": [],
        }
    }
    req = create_req('http://localhost/users/')
    for user in users:
        user_groups = user.pop("groups")
        body = json.dumps(user).encode('utf-8')
        try:
            res = urllib.request.urlopen(req, body)
            res = json.loads(res.read())
            for g in user_groups:
                groups[g]["users"].append(int(res["id"]))
            print(res)
        except HTTPError as e:
            print(e, e.read())
    return groups


def add_users_to_group(group_id, user_ids):
    token = get_token()
    for u in user_ids:
        data = {
            "user_id": u,
            "group_id": group_id
        }
        url = 'http://localhost/usergroup/add/' + '?' + urllib.parse.urlencode(data)
        # print(data)
        try:
            req = create_req(url, token)
            res = urllib.request.urlopen(req, json.dumps({}).encode("utf-8"))
            print(res.read())
        except HTTPError as e:
            print(e.read())


def update_users():
    for group in post_users(load_users()).values():
        add_users_to_group(group["id"], group["users"])


if __name__ == '__main__':
    update_users()
