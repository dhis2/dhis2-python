import logging
from typing import List

from dhis2.core.http import BaseHttpRequest
from dhis2.core.inventory import HostResolved

from .models.icd10 import ICD10Entity

log = logging.getLogger(__name__)


def _icd10_fetch(
    host: HostResolved,
    release_id: str,
    language: str,
    id: str,
):
    req = BaseHttpRequest(host)
    url = f"icd/release/10/{release_id}"

    if id:
        url = f"icd/release/10/{release_id}/{id}"

    data = req.get(
        url,
        headers={
            "Accept-Language": language,
            "API-Version": "v2",
        },
    )

    return ICD10Entity(**data)


def _icd10_resolve_children(
    child: List[ICD10Entity],
    host: HostResolved,
    release_id: str,
    language: str,
) -> List[ICD10Entity]:
    children: List[ICD10Entity] = []

    for c in child:
        parts = c.split("/")
        id = None

        if 8 == len(parts):
            id = parts[7]
        elif 9 == len(parts):
            id = f"{parts[7]}/{parts[8]}"

        if id:
            ch = _icd10_fetch(host, release_id, language, id)

            if "category" == ch.classKind or "modifiedcategory" == ch.classKind:
                children.append(ch)

            if ch.child:
                children.extend(
                    _icd10_resolve_children(
                        ch.child,
                        host,
                        release_id,
                        language,
                    )
                )

    return children


def _icd10_fetch_all(
    host: HostResolved,
    release_id: str,
    language: str,
    root_id: str,
) -> ICD10Entity:
    root = _icd10_fetch(host, release_id, language, id=root_id)
    root.child = _icd10_resolve_children(root.child, host, release_id, language)

    return root


def _dhis2_make_option_sets(entity: ICD10Entity):
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
            "valueType": "TEXT"
        }

        option_set["options"].append({"code": c.code})
        options.append(option)

    return {
        "options": options,
        "optionSets": [option_set],
    }


def fetch_icd10_dhis2_option_sets(
    host: HostResolved,
    release_id: str,
    language: str,
    root_id: str,
):
    log.info("ICD10 export job started")

    icd10 = _icd10_fetch_all(host, release_id, language, root_id)

    log.info("Converting to DHIS2 optionset/options payload")
    dhis2 = _dhis2_make_option_sets(icd10)

    log.info("ICD10 export job finished")

    return dhis2
