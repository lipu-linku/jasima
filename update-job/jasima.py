#! /bin/python3

import urllib.request
import re
import json
import subprocess

import os
from dotenv import load_dotenv
load_dotenv()

GITHUB_ACCOUNT = "lipu-linku"
GITHUB_REPO = "jasima"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


def get_site(link):
    return urllib.request.urlopen(link).read().decode('utf8')


def build_json():
    with open("sheets.json") as file:
        sheets = json.load(file)

    bundle = {key: build_dict_from_sheet(value) for key, value in sheets.items()}

    with open("../data.json", 'w') as f:
        json.dump(bundle, f, indent=2)
    return bundle


def build_dict_from_sheet(link):
    datasheet = get_site(link).split("\r\n")

    keys = datasheet.pop(0).split("\t")
    entries = [line.split("\t") for line in datasheet]

    ID_COLUMN = keys.index("id")
    keys.pop(ID_COLUMN)

    data = {}
    for line in entries:
        entry = {}
        entry_id = line.pop(ID_COLUMN)
        for index, value in enumerate(line):
            if value:
                if "/" not in keys[index]:
                    entry[keys[index]] = value
                else:
                    # e.g. 'def/en':
                    # outer = 'def'
                    # inner = 'en'
                    outer, inner = keys[index].split("/")
                    if outer not in entry:
                        entry[outer] = {}
                    entry[outer][inner] = value
        data[entry_id] = entry
    # Sort by id, case insensitive
    data = {k: v for k, v in sorted(data.items(), key=lambda x: x[0].lower())}
    return data


def upload_json_to_github():
    if os.name == 'nt':
        subprocess.call("git.bat {} {} {}".format(GITHUB_ACCOUNT, GITHUB_REPO, GITHUB_TOKEN))
    else:
        subprocess.call("./git.sh {} {} {}".format(GITHUB_ACCOUNT, GITHUB_REPO, GITHUB_TOKEN))


if __name__ == "__main__":
    bundle = build_json()
    upload_json_to_github()
