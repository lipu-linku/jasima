#!/bin/python3

import urllib.request
import re
import json
import csv
from io import StringIO
from datetime import datetime as dt
from git import Git, Repo

import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_site(link):
    return urllib.request.urlopen(link).read().decode("utf8")


def build_dict_from_sheet(link):
    raw_sheet = get_site(link)

    # datasheet takes a file-like object, so we use StringIO
    datasheet = csv.reader(StringIO(raw_sheet))

    # next() consumes the first line of the sheet
    keys = next(datasheet)

    ID_COLUMN = keys.index("id")
    keys.pop(ID_COLUMN)

    data = {}
    for line in datasheet:
        entry = {}
        entry_id = line.pop(ID_COLUMN)

        for index, value in enumerate(line):
            # remove excess whitespace from beginning and end
            value = value.strip()

            # remove excess whitespace from middle but preserve newlines
            value = re.sub(r"\s*\n\s*", "\n", value)
            value = re.sub(r"[ \t\r\f]+", " ", value)

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


def commit_push(path):
    git = Git(path)
    git.add("-A")
    if not Repo(path).is_dirty(untracked_files=True):
        # Nothing to commit, up to date
        return
    git.commit("-m", f"Autosync for {dt.now().strftime('%Y-%m-%d')}")
    git.push(f"https://{GITHUB_TOKEN}@github.com/lipu-linku/jasima.git")


if __name__ == "__main__":
    with open("sheets.json") as file:
        sheets = json.load(file)
    bundle = {key: build_dict_from_sheet(value) for key, value in sheets.items()}
    with open("../data.json", "w") as f:
        json.dump(bundle, f, indent=2)
    commit_push("..")
