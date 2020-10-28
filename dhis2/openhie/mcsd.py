import json
import logging
from typing import Any, Dict
from uuid import uuid4

from dhis2.core.http import BaseHttpRequest
from dhis2.core.inventory import Inventory, resolve_one
from dhis2.openhie.resources.mcsd import build_bundle
from fhir.resources.bundle import Bundle
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class MCSDConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: Dict[str, Any] = dict()
    target: Dict[str, Any] = dict()


def __get_source(config: MCSDConfig, inventory: Inventory):
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


def __get_target(config: MCSDConfig, inventory: Inventory):
    id = config.target["id"]

    if "log://" == id:

        def call(data: Bundle):
            print(json.dumps(data.as_json(), indent=2))

        return call

    host = resolve_one(id, inventory)

    def call():
        req = BaseHttpRequest(host)
        return req

    return call


def __transform(config: MCSDConfig, data: Any):
    return build_bundle(data[1].get("organisationUnits", []), data[0].baseUrl)


def run(config: MCSDConfig, inventory: Inventory):
    source = __get_source(config, inventory)
    target = __get_target(config, inventory)

    data = source()
    data = __transform(config, data)
    target(data)
