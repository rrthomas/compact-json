import pytest
import pytest_check as check
import json

from compact_json import Formatter
from pathlib import Path


def test_json():
    test_data_path = Path("tests/data")
    for source_filename in test_data_path.rglob("*.json"):
        with open(source_filename) as f:
            obj = json.load(f)

        for ref_filename in test_data_path.rglob(source_filename.stem + ".ref.*"):
            formatter = Formatter()
            with open(ref_filename) as f:
                ref_json = ""
                for line in f.readlines():
                    if line.startswith("@"):
                        (param, value) = line[1:].split("=")
                        value = value.strip()
                        param_type = eval(f"type(formatter.{param})")
                        if param_type == int:
                            setattr(formatter, param, int(value))
                        elif param_type == bool:
                            setattr(formatter, param, bool(value))
                        else:
                            setattr(formatter, param, value)
                    else:
                        ref_json += line
            # No final newline
            ref_json = ref_json.rstrip()

            json_string = formatter.serialize(obj)
            assert json_string == ref_json
