import json
from typing import Any, Dict
from pathlib import Path
from yaml import load as load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def parse_file(filename: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    fp = Path(filename).resolve()

    if not fp.exists() or not fp.is_file():
        return None

    try:
        with open(fp) as f:
            if filename.endswith(".yml"):
                data = load(f, Loader=Loader)
            elif filename.endswith(".json"):
                data = json.load(f)
    except Exception as e:  # noqa
        print(e)
        return None

    return data
