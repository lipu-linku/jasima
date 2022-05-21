#!/bin/python3

import urllib.request
import re
import json
import sys
from git import Git


import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')


def get_site(link):
    return urllib.request.urlopen(link).read().decode('utf8')


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


if __name__ == "__main__":
    with open("sheets.json") as file:
        sheets = json.load(file)
    bundle = {key: build_dict_from_sheet(value) for key, value in sheets.items()}
    with open("../data.json", 'w') as f:
        json.dump(bundle, f, indent=2)

    git = Git("..")
    git.add("-A")
    git.commit("-m", "Updating repo")
    git.push(f"https://{GITHUB_TOKEN}@github.com/lipu-linku/jasima.git")
