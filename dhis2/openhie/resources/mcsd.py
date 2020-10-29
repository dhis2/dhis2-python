import json
import logging
from base64 import b64encode

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


def build_mcsd_location(org_unit, base_url) -> Location:
    id = org_unit.get("id")

    resource = Location()
    resource.id = id
    resource.meta = Meta()
    resource.meta.profile = [
        "http://ihe.net/fhir/StructureDefinition/IHE_mCSD_Location",
    ]

    resource.identifier = [Identifier()]
    resource.identifier[0].system = f"{base_url}/api/organisationUnits"
    resource.identifier[0].value = id

    resource.name = org_unit.get("name")
    resource.description = org_unit.get("name")
    resource.type = [CodeableConcept()]
    resource.type[0].text = "OF"
    resource.status = "active"
    resource.mode = "instance"

    resource.physicalType = CodeableConcept()
    resource.physicalType.coding = [Coding()]
    resource.physicalType.coding[0].system = "http://terminology.hl7.org/CodeSystem/location-physical-type"
    resource.physicalType.coding[0].code = "si"

    resource.managingOrganization = FHIRReference()
    resource.managingOrganization.reference = f"Organization/{id}"

    if "parent" in org_unit:
        resource.partOf = FHIRReference()
        resource.partOf.reference = f"Location/{org_unit.get('parent').get('id')}"

    if "geometry" in org_unit:
        geometry = org_unit.get("geometry")

        if "Point" == geometry.get("type"):
            coordinates = geometry.get("coordinates")
            resource.position = LocationPosition()
            resource.position.latitude = coordinates[1]
            resource.position.longitude = coordinates[0]

        resource.extension = [Extension()]
        resource.extension[0].url = "http://hl7.org/fhir/StructureDefinition/location-boundary-geojson"
        resource.extension[0].valueAttachment = Attachment()
        resource.extension[0].valueAttachment.contentType = "application/geo+json"
        resource.extension[0].valueAttachment.data = str(b64encode(json.dumps(geometry).encode("utf-8")), "utf-8")

    return resource


def build_mcsd_organization(org_unit, base_url) -> Organization:
    id = org_unit.get("id")

    resource = Organization()
    resource.id = id
    resource.meta = Meta()
    resource.meta.profile = [
        "http://ihe.net/fhir/StructureDefinition/IHE_mCSD_Organization",
        "http://ihe.net/fhir/StructureDefinition/IHE_mCSD_FacilityOrganization",
    ]

    resource.identifier = [Identifier()]
    resource.identifier[0].system = f"{base_url}/api/organisationUnits"
    resource.identifier[0].value = id

    resource.name = org_unit.get("name")
    resource.type = []

    c1 = CodeableConcept()
    c1.coding = [Coding()]
    c1.coding[0].system = "http://terminology.hl7.org/CodeSystem/organization-type"
    c1.coding[0].code = "prov"

    resource.type.append(c1)

    c2 = CodeableConcept()
    c2.coding = [Coding()]
    c2.coding[0].system = "urn:ietf:rfc:3986"
    c2.coding[0].code = "urn:ihe:iti:mcsd:2019:facility"

    resource.type.append(c2)

    return resource


def build_location_bundle_entry(org_unit, base_url):
    id = org_unit.get("id")
    entry = BundleEntry()

    entry.request = BundleEntryRequest()
    entry.request.method = "PUT"
    entry.request.url = f"Location?identifier={id}"

    entry.resource = build_mcsd_location(org_unit, base_url)

    return entry


def build_organization_bundle_entry(org_unit, base_url):
    id = org_unit.get("id")
    entry = BundleEntry()

    entry.request = BundleEntryRequest()
    entry.request.method = "PUT"
    entry.request.url = f"Organization?identifier={id}"

    entry.resource = build_mcsd_organization(org_unit, base_url)

    return entry


def build_bundle(org_units, base_url):
    bundle = Bundle()
    bundle.type = "transaction"
    bundle.entry = []

    log.info(f"Building FHIR bundle from '{len(org_units)}' organisation units")

    for org_unit in org_units:
        bundle.entry.append(build_location_bundle_entry(org_unit, base_url))
        bundle.entry.append(build_organization_bundle_entry(org_unit, base_url))

    return bundle
