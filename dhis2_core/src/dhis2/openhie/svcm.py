import json
import logging
import sys
from typing import Any, Callable, Dict, List

from dhis2.core.http import BaseHttpRequest
from dhis2.core.inventory import HostResolved, Inventory, resolve_one
from fhir.resources.bundle import Bundle

from .models import CodeList, SVCMConfig
from .resources.svcm import build_bundle

log = logging.getLogger(__name__)


def get_source(config: SVCMConfig, inventory: Inventory) -> Callable[[Any], Any]:
    host = resolve_one(config.source.id, inventory)

    if "dhis2" not in host.type:
        log.error("Only 'dhis2' source type is currently supported")
        sys.exit(-1)

    log.info(f"Creating source from '{host.key}' with base url '{host.baseUrl}'")

    def fn():
        filters = []

        # https://docs.dhis2.org/2.35/en/developer/html/webapi_metadata_object_filter.html
        if config.source.lastUpdated:
            filters.append(f"lastUpdated:ge:{config.source.lastUpdated}")

        option_sets_filter = list(map(lambda x: f"id:eq:{x}", config.source.filters.optionSets))
        option_sets_filter.extend(filters)

        option_sets = BaseHttpRequest(host).get(
            "api/optionSets",
            params={
                "fields": "id,code,name,version,translations,options[id,code,name,translations]",
                "rootJunction": "OR",
                "filter": option_sets_filter,
                "paging": False,
            },
        )

        categories_filter = list(map(lambda x: f"id:eq:{x}", config.source.filters.categories))
        categories_filter.extend(filters)

        categories = BaseHttpRequest(host).get(
            "api/categories",
            params={
                "fields": "id,code,name,translations,categoryOptions::rename(options)[id,code,name,translations]",
                "rootJunction": "OR",
                "filter": categories_filter,
                "paging": False,
            },
        )

        data = {
            "optionSets": option_sets.get("optionSets", []),
            "categories": categories.get("categories", []),
        }

        return (
            host,
            data,
        )

    return fn


def get_target(config: SVCMConfig, inventory: Inventory) -> Callable[[Any], Any]:
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


def transform(config: SVCMConfig, data: Any):
    host: HostResolved = data[0]
    payload: Dict[str, Any] = data[1]

    code_lists: List[CodeList] = []

    option_sets = payload.get("optionSets", [])
    categories = payload.get("categories", [])

    for option_set in option_sets:
        code_lists.append(CodeList(**option_set))

    for category in categories:
        code_lists.append(CodeList(**category, type="categories"))

    return (
        host,
        build_bundle(code_lists, host.baseUrl),
    )


def run(config: SVCMConfig, inventory: Inventory):
    log.info(f"SVCM job '{config.id}'' starting")

    source = get_source(config, inventory)
    target = get_target(config, inventory)

    data = source()
    data = transform(config, data)
    data = target(data)

    if data:
        log.info(f"Got response from target system {data}")

    log.info(f"SVCM job '{config.id}'' finished")
