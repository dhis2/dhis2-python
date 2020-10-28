import json
import logging
from typing import Any, Dict
from uuid import uuid4

from dhis2.core.http import BaseHttpRequest
from dhis2.core.inventory import HostResolved, Inventory, resolve_one
from dhis2.openhie.resources.mcsd import build_bundle
from fhir.resources.bundle import Bundle
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class MCSDConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: Dict[str, Any] = dict()
    target: Dict[str, Any] = dict()


def get_source(config: MCSDConfig, inventory: Inventory):
    id = config.source["id"]
    host = resolve_one(id, inventory)

    def call():
        req = BaseHttpRequest(host)
        data = req.get(
            "api/organisationUnits",
            params={
                "fields": "id,code,name,geometry,parent[id]",
                "rootJunction": "OR",
                # "filter": list(map(lambda x: f"id:eq:{x}", source_filters)),
                "paging": False,
            },
        )

        return (
            host,
            data,
        )

    return call


def get_target(config: MCSDConfig, inventory: Inventory):
    id = config.target["id"]

    if "log://" == id:

        def fn(data: Any):
            print(json.dumps(data[1].as_json(), indent=2))

        return fn

    host = resolve_one(id, inventory)

    def fn(data: Any):
        payload: Bundle = data[1]
        return BaseHttpRequest(host).post("baseR4", data=payload.as_json())

    return fn


def transform(config: MCSDConfig, data: Any):
    host: HostResolved = data[0]
    payload: Dict[str, Any] = data[1]

    return (
        host,
        build_bundle(payload.get("organisationUnits", []), host.baseUrl),
    )


def run(config: MCSDConfig, inventory: Inventory):
    source = get_source(config, inventory)
    target = get_target(config, inventory)

    data = source()
    data = transform(config, data)
    target(data)
