import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from yaml import load as load

from .http import BaseHttpRequest
from .inventory import HostResolved
from .metadata.models import Schema, Schemas

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

log = logging.getLogger(__name__)


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


def load_and_parse_schema(host: HostResolved) -> List[Schema]:
    if "dhis2" not in host.type:
        log.error(f"'{host.key}' is of unsupported type '{host.type}', only 'dhis2' is supported for this command")
        return None

    req = BaseHttpRequest(host)
    data = req.get("api/schemas")

    schemas = Schemas(**data)

    return schemas.schemas
