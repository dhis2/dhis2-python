import logging

from fhir.resources.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhir.resources.codesystem import CodeSystem, CodeSystemConcept
from fhir.resources.identifier import Identifier
from fhir.resources.valueset import ValueSet, ValueSetCompose, ValueSetComposeInclude

log = logging.getLogger(__name__)


def build_svcm_codesystem(option_set, base_url) -> CodeSystem:
    id = option_set.get("id")

    resource = CodeSystem()
    resource.url = f"{base_url}/api/optionSets/{id}/codeSystem"
    resource.valueSet = f"{base_url}/api/optionSets/{id}/valueSet"

    resource.identifier = [Identifier()]
    resource.identifier[0].system = f"{base_url}/api/optionSets"
    resource.identifier[0].value = id

    resource.publisher = base_url
    resource.status = "active"
    resource.content = "complete"
    resource.version = str(option_set.get("version"))
    resource.name = option_set.get("name")
    resource.title = option_set.get("name")
    resource.description = option_set.get("name")
    resource.experimental = False
    resource.caseSensitive = True
    resource.concept = []

    for option in option_set.get("options", []):
        concept = CodeSystemConcept()
        resource.concept.append(concept)

        concept.code = option.get("code")
        concept.display = option.get("name")
        concept.definition = option.get("name")

    return resource


def build_svcm_valueset(option_set, base_url) -> ValueSet:
    id = option_set.get("id")

    resource = ValueSet()
    resource.url = f"{base_url}/api/optionSets/{id}/valueSet"

    resource.identifier = [Identifier()]
    resource.identifier[0].system = f"{base_url}/api/optionSets"
    resource.identifier[0].value = id

    resource.status = "active"
    resource.version = str(option_set.get("version"))
    resource.name = option_set.get("name")
    resource.title = option_set.get("name")
    resource.description = option_set.get("name")
    resource.experimental = False
    resource.immutable = True
    resource.compose = ValueSetCompose()
    resource.compose.include = [ValueSetComposeInclude()]
    resource.compose.include[0].system = f"{base_url}/api/optionSets/{id}/codeSystem"

    return resource


def build_code_system_bundle_entry(option_set, base_url):
    id = option_set.get("id")
    entry = BundleEntry()

    entry.request = BundleEntryRequest()
    entry.request.method = "PUT"
    entry.request.url = f"CodeSystem?identifier={id}"

    entry.resource = build_svcm_codesystem(option_set, base_url)

    return entry


def build_value_set_bundle_entry(option_set, base_url):
    id = option_set.get("id")
    entry = BundleEntry()

    entry.request = BundleEntryRequest()
    entry.request.method = "PUT"
    entry.request.url = f"ValueSet?identifier={id}"

    entry.resource = build_svcm_valueset(option_set, base_url)

    return entry


def build_bundle(option_sets, base_url):
    bundle = Bundle()
    bundle.type = "transaction"
    bundle.entry = []

    log.info(f"Building FHIR bundle from '{len(option_sets)}' option sets")

    for option_set in option_sets:
        bundle.entry.append(build_value_set_bundle_entry(option_set, base_url))
        bundle.entry.append(build_code_system_bundle_entry(option_set, base_url))

    return bundle
