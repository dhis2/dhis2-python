import logging
from typing import List

from fhir.resources.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhir.resources.codesystem import CodeSystem, CodeSystemConcept
from fhir.resources.identifier import Identifier
from fhir.resources.valueset import ValueSet, ValueSetCompose, ValueSetComposeInclude

from ..models import CodeList

log = logging.getLogger(__name__)


def build_svcm_codesystem(code_list: CodeList, base_url: str) -> CodeSystem:
    resource = CodeSystem()
    resource.url = f"{base_url}/api/{code_list.type}/{code_list.id}/codeSystem"
    resource.valueSet = f"{base_url}/api/{code_list.type}/{code_list.id}/valueSet"

    resource.identifier = [Identifier()]
    resource.identifier[0].system = f"{base_url}/api/{code_list.type}"
    resource.identifier[0].value = code_list.id

    if code_list.code:
        identifier = Identifier()
        identifier.system = f"{base_url}/api/{code_list.type}"
        identifier.value = code_list.code

        resource.identifier.append(identifier)

    resource.publisher = base_url
    resource.status = "active"
    resource.content = "complete"
    resource.version = str(code_list.version)
    resource.name = code_list.name
    resource.title = code_list.name
    resource.description = code_list.name
    resource.experimental = False
    resource.caseSensitive = True
    resource.concept = []

    for code in code_list.codes:
        concept = CodeSystemConcept()
        resource.concept.append(concept)

        concept.code = code.get("code")
        concept.display = code.get("name")
        concept.definition = code.get("name")

    return resource


def build_svcm_valueset(code_list: CodeList, base_url: str) -> ValueSet:
    resource = ValueSet()
    resource.url = f"{base_url}/api/{code_list.type}/{code_list.id}/valueSet"

    resource.identifier = [Identifier()]
    resource.identifier[0].system = f"{base_url}/api/{code_list.type}"
    resource.identifier[0].value = code_list.id

    if code_list.code:
        identifier = Identifier()
        identifier.system = f"{base_url}/api/{code_list.type}"
        identifier.value = code_list.code

        resource.identifier.append(identifier)

    resource.status = "active"
    resource.version = str(code_list.version)
    resource.name = code_list.name
    resource.title = code_list.name
    resource.description = code_list.name
    resource.experimental = False
    resource.immutable = True
    resource.compose = ValueSetCompose()
    resource.compose.include = [ValueSetComposeInclude()]
    resource.compose.include[0].system = f"{base_url}/api/{code_list.type}/{code_list.id}/codeSystem"

    return resource


def build_code_system_bundle_entry(code_list: CodeList, base_url: str) -> BundleEntry:
    entry = BundleEntry()

    entry.request = BundleEntryRequest()
    entry.request.method = "PUT"
    entry.request.url = f"CodeSystem?identifier={code_list.id}"

    entry.resource = build_svcm_codesystem(code_list, base_url)

    return entry


def build_value_set_bundle_entry(code_list: CodeList, base_url: str) -> BundleEntry:
    entry = BundleEntry()

    entry.request = BundleEntryRequest()
    entry.request.method = "PUT"
    entry.request.url = f"ValueSet?identifier={code_list.id}"

    entry.resource = build_svcm_valueset(code_list, base_url)

    return entry


def build_bundle(code_lists: List[CodeList], base_url: str) -> Bundle:
    bundle = Bundle()
    bundle.type = "transaction"
    bundle.entry = []

    log.info(f"Building FHIR bundle from '{len(code_lists)}' DHIS2 code lists")

    for code_list in code_lists:
        bundle.entry.append(build_value_set_bundle_entry(code_list, base_url))
        bundle.entry.append(build_code_system_bundle_entry(code_list, base_url))

    return bundle
