import json
import logging
from typing import Any, Dict
from uuid import uuid4

from dhis2.core.http import BaseHttpRequest
from dhis2.core.inventory import Inventory, resolve_one
from dhis2.openhie.resources.svcm import build_bundle
from fhir.resources.bundle import Bundle
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class SVCMConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: Dict[str, Any] = dict()
    target: Dict[str, Any] = dict()


def __get_source(config: SVCMConfig, inventory: Inventory):
    id = config.source["id"]
    host = resolve_one(id, inventory)

    def call():
        req = BaseHttpRequest(host)
        data = req.get(
            "api/optionSets",
            params={
                "fields": "id,code,version,name,options[id,name,code]",
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


def __get_target(config: SVCMConfig, inventory: Inventory):
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


def __transform(config: SVCMConfig, data: Any):
    return build_bundle(data[1].get("optionSets", []), data[0].baseUrl)


def run(config: SVCMConfig, inventory: Inventory):
    source = __get_source(config, inventory)
    target = __get_target(config, inventory)

    data = source()
    data = __transform(config, data)
    target(data)
