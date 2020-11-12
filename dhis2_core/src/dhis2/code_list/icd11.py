import logging
import sys
from typing import List

from dhis2.core.http import BaseHttpRequest
from dhis2.core.inventory import HostResolved

from .models.icd11 import LinearizationEntity

log = logging.getLogger(__name__)


def _icd11_fetch(
    host: HostResolved,
    linearizationname: str,
    release_id: str,
    language: str,
    id: str,
):
    req = BaseHttpRequest(host)
    url = f"icd/release/11/{release_id}/{linearizationname}/{id}"

    data = req.get(
        url,
        headers={
            "Accept-Language": language,
            "API-Version": "v2",
        },
    )

    return LinearizationEntity(**data)


def _icd11_resolve_children(
    child: List[LinearizationEntity],
    host: HostResolved,
    linearizationname: str,
    release_id: str,
    language: str,
) -> List[LinearizationEntity]:
    children: List[LinearizationEntity] = []

    for c in child:
        parts = c.split("/")
        id = None

        if 9 == len(parts):
            id = parts[8]
        elif 10 == len(parts):
            id = f"{parts[8]}/{parts[9]}"

        if id:
            ch = _icd11_fetch(host, linearizationname, release_id, language, id)

            if "category" == ch.classKind:
                children.append(ch)
            elif "block" == ch.classKind:
                children.extend(
                    _icd11_resolve_children(
                        ch.child,
                        host,
                        linearizationname,
                        release_id,
                        language,
                    )
                )
            elif "window" == ch.classKind:
                pass
            else:
                log.error(f"Unhandled classKind `{ch.classKind}`")
                sys.exit(-1)

    return children


def _icd11_fetch_all(
    host: HostResolved,
    linearizationname: str,
    release_id: str,
    language: str,
    root_id: str,
) -> LinearizationEntity:
    root = _icd11_fetch(host, linearizationname, release_id, language, id=root_id)
    root.child = _icd11_resolve_children(root.child, host, linearizationname, release_id, language)

    return root


def _dhis2_make_option_sets(entity: LinearizationEntity):
    options = []

    option_set = {
        "name": entity.title.value,
        "code": entity.codeRange,
        "options": [],
    }

    if entity.definition:
        option_set["description"] = entity.definition.value

    for c in entity.child:
        option = {
            "name": c.title.value,
            "code": c.code,
        }

        option_set["options"].append({"code": c.code})
        options.append(option)

    return {
        "options": options,
        "optionSets": [option_set],
    }


def fetch_icd11_dhis2_option_sets(
    host: HostResolved,
    linearizationname: str,
    release_id: str,
    language: str,
    root_id: str,
):
    log.info("ICD11 export job started")

    icd11 = _icd11_fetch_all(host, linearizationname, release_id, language, root_id)

    log.info("Converting to DHIS2 optionset/options payload")
    dhis2 = _dhis2_make_option_sets(icd11)

    log.info("ICD11 export job finished")

    return dhis2
