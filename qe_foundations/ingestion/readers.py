"""Read raw test records from CSV, JSON, and XML sources."""

import csv
import json
import xml.etree.ElementTree as ET

from .contexts import open_source
from .exceptions import MalformedSourceError, MissingColumnsError
from .validation import REQUIRED_FIELDS


def read_csv_records(path):
    """Return CSV rows as raw dictionaries."""
    with open_source(path) as handle:
        try:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []

            missing = [
                field for field in REQUIRED_FIELDS
                if field not in headers
            ]

            if missing:
                raise MissingColumnsError(path, missing)

            return list(reader)
        except csv.Error as error:
            raise MalformedSourceError(path, str(error)) from error


def read_json_records(path):
    """Return the untouched tests list from a JSON object."""
    with open_source(path) as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError as error:
            detail = (
                f"invalid JSON at line {error.lineno}, "
                f"column {error.colno}: {error.msg}"
            )
            raise MalformedSourceError(path, detail) from error

    if not isinstance(data, dict):
        raise MalformedSourceError(
            path, "JSON top level must be an object"
        )

    if "tests" not in data or not isinstance(data["tests"], list):
        raise MalformedSourceError(
            path, "'tests' must be present and contain a list"
        )

    return data["tests"]


def read_xml_records(path):
    """Return raw dictionaries for testcase elements at any depth."""
    with open_source(path) as handle:
        try:
            tree = ET.parse(handle)
        except ET.ParseError as error:
            line, column = error.position
            detail = (
                f"invalid XML at line {line}, "
                f"column {column}: {error}"
            )
            raise MalformedSourceError(path, detail) from error

    records = []

    for testcase in tree.getroot().iter("testcase"):
        records.append({
            "id": testcase.get("id"),
            "status": testcase.get("status"),
            "title": testcase.findtext("title"),
            "duration": testcase.findtext("duration"),
        })

    return records