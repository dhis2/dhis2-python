import json
import logging
import sys
from typing import Any, Callable, Dict
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


def get_source(config: MCSDConfig, inventory: Inventory) -> Callable[[Any], Any]:
    id = config.source["id"]
    host = resolve_one(id, inventory)

    if "dhis2" not in host.type:
        log.error("Only 'dhis2' source type is currently supported")
        sys.exit(-1)

    log.info(f"Creating source from '{host.key}' with base url '{host.baseUrl}'")

    def call():
        source_filters = config.source.get("filters", [])
        req = BaseHttpRequest(host)

        data = req.get(
            "api/organisationUnits",
            params={
                "fields": "id,code,name,geometry,parent[id]",
                "rootJunction": "OR",
                "filter": list(map(lambda x: f"id:eq:{x}", source_filters)),
                "paging": False,
            },
        )

        return (
            host,
            data,
        )

    return call


def get_target(config: MCSDConfig, inventory: Inventory) -> Callable[[Any], Any]:
    id = config.target["id"]

    if "log://" == id:

        log.info("Creating 'log://' target")

        def fn(data: Any):
            print(json.dumps(data[1].as_json(), indent=2))

        return fn
    elif "null://" == id:

        log.info("Creating 'null://' target")

        def fn(data: Any):
            pass

        return fn

    host = resolve_one(id, inventory)

    if "dhis2" in host.type:
        log.error("'dhis2' target type is not currently supported")
        sys.exit(-1)

    log.info(f"Creating target from '{host.key}' with base url '{host.baseUrl}'")

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
    log.info(f"mCSD job '{config.id}'' starting")

    source = get_source(config, inventory)
    target = get_target(config, inventory)

    data = source()
    data = transform(config, data)
    data = target(data)

    log.info(f"Got response from target system {data}")
    log.info(f"mCSD job '{config.id}'' finished")
