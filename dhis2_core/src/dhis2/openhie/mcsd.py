import json
import logging
import sys
from typing import Any, Callable, Dict, List

from dhis2.core.http import BaseHttpRequest
from dhis2.core.inventory import HostResolved, Inventory, resolve_one
from fhir.resources.bundle import Bundle

from .models import MCSDConfig, OrgUnit
from .resources.mcsd import build_bundle

log = logging.getLogger(__name__)


def get_source(config: MCSDConfig, inventory: Inventory) -> Callable[[Any], Any]:
    host = resolve_one(config.source.id, inventory)

    if "dhis2" not in host.type:
        log.error("Only 'dhis2' source type is currently supported")
        sys.exit(-1)

    log.info(f"Creating source from '{host.key}' with base url '{host.baseUrl}'")

    def call():
        req = BaseHttpRequest(host)
        filter = list(map(lambda x: f"id:eq:{x}", config.source.filters))

        # https://docs.dhis2.org/2.35/en/developer/html/webapi_metadata_object_filter.html
        if config.source.lastUpdated:
            filter.append(f"lastUpdated:ge:{config.source.lastUpdated}")

        data = req.get(
            "api/organisationUnits",
            params={
                "fields": "id,code,name,translations,geometry,parent[id,code]",
                "rootJunction": "OR",
                "filter": filter,
                "paging": False,
            },
        )

        return (
            host,
            data,
        )

    return call


def get_target(config: MCSDConfig, inventory: Inventory) -> Callable[[Any], Any]:
    id = config.target.id

    if "log://" == id:

        log.info("Creating 'log://' target")

        def target_log(data: Any):
            log.info("Writing result to stdout")
            print(json.dumps(data[1].as_json(), indent=2))

        return target_log
    elif "null://" == id:

        log.info("Creating 'null://' target")

        def target_null(data: Any):
            log.info("Doing nothing with result")

        return target_null

    host = resolve_one(id, inventory)

    if "dhis2" in host.type:
        log.error("'dhis2' target type is not currently supported")
        sys.exit(-1)

    log.info(f"Creating target from '{host.key}' with base url '{host.baseUrl}'")

    def target_push(data: Any):
        payload: Bundle = data[1]
        return BaseHttpRequest(host).post("baseR4", data=payload.as_json())

    return target_push


def transform(config: MCSDConfig, data: Any):
    host: HostResolved = data[0]
    payload: Dict[str, Any] = data[1]

    org_units: List[OrgUnit] = []

    for org_unit in payload.get("organisationUnits", []):
        org_units.append(OrgUnit(**org_unit))

    return (
        host,
        build_bundle(org_units, host.baseUrl),
    )


def run(config: MCSDConfig, inventory: Inventory):
    log.info(f"mCSD job '{config.id}'' starting")

    source = get_source(config, inventory)
    target = get_target(config, inventory)

    data = source()
    data = transform(config, data)
    data = target(data)

    if data:
        log.info(f"Got response from target system {data}")

    log.info(f"mCSD job '{config.id}'' finished")
