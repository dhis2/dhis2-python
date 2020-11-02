import json
import logging
import sys
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from urllib.parse import urlparse

from pydantic import BaseModel, Field, ValidationError
from yaml import load as load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

log = logging.getLogger(__name__)


# officially supported types
class HostType(str, Enum):
    dhis2 = "dhis2"
    fhir = "fhir"


class BasicAuthtype(BaseModel):
    type: Literal["http-basic"] = "http-basic"
    username: str
    password: str


class NoopAuthtype(BaseModel):
    type: Literal["no-op"] = "no-op"


class Host(BaseModel):
    type: Union[HostType, str] = HostType.dhis2
    baseUrl: str
    auth: Optional[Dict[str, Union[NoopAuthtype, BasicAuthtype]]] = {"default": NoopAuthtype()}

    class Config:
        extra = "allow"


class HostResolved(BaseModel):
    type: Union[HostType, str] = HostType.dhis2
    key: str
    baseUrl: str
    auth: Union[NoopAuthtype, BasicAuthtype]


class Inventory(BaseModel):
    hosts: Dict[str, Host]
    groups: Dict[str, List[str]] = Field(default_factory=dict)

    def get_many_by_id(self, ids) -> Dict[str, Host]:
        if not isinstance(ids, (list, set, tuple)):
            ids = [ids]

        hosts = {}

        for id in ids:  # add from self.hosts first
            if id in self.hosts:
                hosts[id] = self.hosts[id]

        for id in ids:
            if id in self.groups:
                for gid in self.groups[id]:
                    if gid in self.hosts:
                        hosts[gid] = self.hosts.get(gid)

        return hosts

    def get_one_by_id(self, id):
        hosts = self.get_many_by_id(id)

        if not hosts or len(hosts) > 1:
            print(f"got {len(hosts)} results for host id")

        return hosts[0]


def _process_inventory_data(inventory: Dict[str, Any]):
    # since pydantic validation hasn't been run yet, do some basic checks here
    if "hosts" not in inventory or not isinstance(inventory["hosts"], dict):
        return  # return and let pydantic handle the error

    for host in inventory["hosts"].items():
        _, value = host

        if "username" in value and "password" in value:
            value["auth"] = {
                "default": {
                    "type": "http-basic",
                    "username": value["username"],
                    "password": value["password"],
                }
            }

            del value["username"]
            del value["password"]


def parse_file(filename: str) -> Inventory:
    data: Dict[str, Any] = {}

    with open(filename) as f:
        if filename.endswith(".yml"):
            data = load(f, Loader=Loader)
        elif filename.endswith(".json"):
            data = json.load(f)

    return parse_obj(data)


def parse_obj(data: Dict[str, Any]) -> Inventory:
    _process_inventory_data(data)

    try:
        data = Inventory.parse_obj(data)
    except ValidationError as e:
        log.error(e.json(indent=None))
        sys.exit(-1)

    return data


def normalize(id: str):
    if "://" not in id:
        id = f"http://{id}"

    id_parsed = urlparse(id)
    normalized = ""

    if id_parsed.scheme:
        normalized = f"{id_parsed.scheme}://"
    else:
        normalized = "http://"

    if id_parsed.username:
        normalized += f"{id_parsed.username}@"
    else:
        normalized += "default@"

    normalized += id_parsed.hostname

    return normalized


def resolve(id: str, inventory: Inventory) -> List[HostResolved]:
    id = normalize(id)
    id_parsed = urlparse(id)

    hosts = inventory.get_many_by_id(id_parsed.hostname)
    host_resolved = []

    for host in hosts.items():
        key, value = host
        auth = None

        if id_parsed.username in value.auth:
            auth = value.auth[id_parsed.username]

        if not auth:
            log.error(f"No auth block with id '{id_parsed.username}'' found for host '{key}''")
            sys.exit(-1)

        hr = HostResolved(
            type=value.type,
            key=key,
            baseUrl=value.baseUrl,
            auth=auth,
        )

        host_resolved.append(hr)

    return host_resolved


def resolve_one(id: str, inventory: Inventory):
    hosts = resolve(id, inventory)

    if not hosts or len(hosts) > 1:
        log.error("Expected only one result from inventory (did you use a group id?)")
        sys.exit(-1)

    return hosts[0]
