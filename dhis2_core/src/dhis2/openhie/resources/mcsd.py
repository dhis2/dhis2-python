import logging
from base64 import b64encode
from typing import List

from dhis2.openhie.models import OrgUnit
from fhir.resources.attachment import Attachment
from fhir.resources.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.extension import Extension
from fhir.resources.fhirreference import FHIRReference
from fhir.resources.identifier import Identifier
from fhir.resources.location import Location, LocationPosition
from fhir.resources.meta import Meta
from fhir.resources.organization import Organization

log = logging.getLogger(__name__)


def is_facility(org_unit: OrgUnit) -> bool:
    if geometry := org_unit.geometry:
        if "Point" == geometry.type:
            return True

    return False


def build_mcsd_location(org_unit: OrgUnit, base_url) -> Location:
    resource = Location()
    resource.id = org_unit.id
    resource.meta = Meta()
    resource.meta.profile = [
        "http://ihe.net/fhir/StructureDefinition/IHE_mCSD_Location",
    ]

    resource.identifier = [Identifier()]
    resource.identifier[0].system = f"{base_url}/api/organisationUnits"
    resource.identifier[0].value = org_unit.id

    if org_unit.code:
        identifier = Identifier()
        identifier.system = f"{base_url}/api/organisationUnits"
        identifier.value = org_unit.code

        resource.identifier.append(identifier)

    resource.name = org_unit.name
    resource.description = org_unit.name
    resource.type = [CodeableConcept()]
    resource.type[0].text = "OF"
    resource.status = "active"
    resource.mode = "instance"

    resource.physicalType = CodeableConcept()
    resource.physicalType.coding = [Coding()]
    resource.physicalType.coding[0].system = "http://terminology.hl7.org/CodeSystem/location-physical-type"
    resource.physicalType.coding[0].code = "si"

    resource.managingOrganization = FHIRReference()
    resource.managingOrganization.reference = f"Organization/{org_unit.id}"

    if org_unit.parent:
        resource.partOf = FHIRReference()
        resource.partOf.reference = f"Location/{org_unit.parent.id}"

    if org_unit.geometry:
        geometry = org_unit.geometry
        geometry_str = geometry.json().encode("utf-8")

        if "Point" == geometry.type:
            coordinates = geometry.coordinates
            resource.position = LocationPosition()
            resource.position.latitude = coordinates[1]
            resource.position.longitude = coordinates[0]

        resource.extension = [Extension()]
        resource.extension[0].url = "http://hl7.org/fhir/StructureDefinition/location-boundary-geojson"
        resource.extension[0].valueAttachment = Attachment()
        resource.extension[0].valueAttachment.contentType = "application/geo+json"
        resource.extension[0].valueAttachment.data = str(b64encode(geometry_str), "utf-8")

    return resource


def build_mcsd_organization(org_unit: OrgUnit, base_url) -> Organization:
    resource = Organization()
    resource.id = org_unit.id
    resource.meta = Meta()
    resource.meta.profile = [
        "http://ihe.net/fhir/StructureDefinition/IHE_mCSD_Organization",
    ]

    if is_facility(org_unit):
        resource.meta.profile.append("http://ihe.net/fhir/StructureDefinition/IHE_mCSD_FacilityOrganization")

    resource.identifier = [Identifier()]
    resource.identifier[0].system = f"{base_url}/api/organisationUnits"
    resource.identifier[0].value = org_unit.id

    if org_unit.code:
        identifier = Identifier()
        identifier.system = f"{base_url}/api/organisationUnits"
        identifier.value = org_unit.code

        resource.identifier.append(identifier)

    resource.name = org_unit.name
    resource.type = []

    c1 = CodeableConcept()
    c1.coding = [Coding()]
    c1.coding[0].system = "http://terminology.hl7.org/CodeSystem/organization-type"
    c1.coding[0].code = "prov"

    resource.type.append(c1)

    if is_facility(org_unit):
        c2 = CodeableConcept()
        c2.coding = [Coding()]
        c2.coding[0].system = "urn:ietf:rfc:3986"
        c2.coding[0].code = "urn:ihe:iti:mcsd:2019:facility"

        resource.type.append(c2)

    return resource


def build_location_bundle_entry(org_unit: OrgUnit, base_url: str) -> BundleEntry:
    entry = BundleEntry()

    entry.request = BundleEntryRequest()
    entry.request.method = "PUT"
    entry.request.url = f"Location?identifier={org_unit.id}"

    entry.resource = build_mcsd_location(org_unit, base_url)

    return entry


def build_organization_bundle_entry(org_unit: OrgUnit, base_url: str) -> BundleEntry:
    entry = BundleEntry()

    entry.request = BundleEntryRequest()
    entry.request.method = "PUT"
    entry.request.url = f"Organization?identifier={org_unit.id}"

    entry.resource = build_mcsd_organization(org_unit, base_url)

    return entry


def build_bundle(org_units: List[OrgUnit], base_url: str) -> Bundle:
    bundle = Bundle()
    bundle.type = "transaction"
    bundle.entry = []

    log.info(f"Building FHIR bundle from '{len(org_units)}' organisation units")

    for org_unit in org_units:
        bundle.entry.append(build_location_bundle_entry(org_unit, base_url))
        bundle.entry.append(build_organization_bundle_entry(org_unit, base_url))

    return bundle
