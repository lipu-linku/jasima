#!/bin/python3
import csv
import json
import logging
import os
import re
import urllib.request
from io import StringIO
from datetime import datetime as dt

from dotenv import load_dotenv
from git import Git, Repo

LOG_FORMAT = (
    "[%(asctime)s] [%(filename)22s:%(lineno)-4s] [%(levelname)8s]   %(message)s"
)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOG = logging.getLogger()

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_site(link):
    return urllib.request.urlopen(link).read().decode("utf8")


def clean_whitespace(s: str) -> str:
    """Strip whitespace from beginning/end; strip duplicate whitespace other than newlines from middle"""
    s = s.strip()
    s = re.sub(r"\s*\n\s*", "\n", s)
    s = re.sub(r"[ \t\r\f]+", " ", s)
    return s


def build_dict_from_sheet(link):
    raw_sheet = get_site(link)

    # datasheet takes a file-like object, so we use StringIO
    datasheet = csv.reader(StringIO(raw_sheet))

    # next() consumes the first line of the sheet
    keys = next(datasheet)

    ID_COLUMN = keys.index("id")
    keys.pop(ID_COLUMN)

    data = {}
    for row in datasheet:
        entry = {}
        entry_id = row.pop(ID_COLUMN)

        for index, cell in enumerate(row):
            LOG.debug("Index: %s, Value: %s", index, cell)
            cell = clean_whitespace(cell)
            if not cell:
                LOG.info("No data for key %s in entry %s", keys[index], entry_id)
                continue

            if "/" not in keys[index]:
                LOG.info("Inserting key %s for entry %s", keys[index], entry_id)
                entry[keys[index]] = cell
            else:
                # e.g. 'def/en':
                # outer = 'def'
                # inner = 'en'
                outer, inner = keys[index].split("/")
                LOG.info(
                    "Inserting nested key %s/%s for entry %s", outer, inner, entry_id
                )
                LOG.debug(entry)
                if outer == "etymology_data":  # TODO: key agnostic logic?
                    # TODO: assert children of etymology_data have equal # splits?
                    splits = cell.split(";")
                    LOG.debug(splits)
                    splits = [clean_whitespace(split) for split in splits]
                    cell = ";".join(splits)  # user would do this anyway

                if outer not in entry:
                    entry[outer] = {}
                assert isinstance(entry[outer], dict), (
                    "Parent key %s has non-dict child. Is the sheet malformed?" % outer
                )
                # if parent key has same name as a normal key
                entry[outer][inner] = cell

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
