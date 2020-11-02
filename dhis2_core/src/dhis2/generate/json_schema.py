import logging
import sys
from typing import Any, Dict, List

from dhis2.core.metadata.models import Property, Schema

log = logging.getLogger(__name__)


def handle_reference(dhis2_property: Property, property: Dict[str, Any]):
    if dhis2_property.identifiableObject and not dhis2_property.embeddedObject:
        property["$ref"] = "#/definitions/identifiableObject"
    else:
        property["$ref"] = f"#/definitions/{dhis2_property.name}"


def handle_collection(dhis2_property: Property, property: Dict[str, Any]):
    property["type"] = "array"

    if "REFERENCE" in dhis2_property.itemPropertyType:
        property["item"] = {"$ref": "#/definitions/identifiableObject"}
    else:
        property["item"] = {"$ref": f"#/definitions/{dhis2_property.name}"}


def handle_property(dhis2_property: Property):
    if (not dhis2_property.persisted or not dhis2_property.owner) and not dhis2_property.required:
        return None

    property = {}

    if dhis2_property.description:
        property["description"] = dhis2_property.description

    if "BOOLEAN" in dhis2_property.propertyType:
        property["type"] = "boolean"
    elif "INTEGER" in dhis2_property.propertyType:
        property["type"] = "integer"
    elif "NUMBER" in dhis2_property.propertyType:
        property["type"] = "number"
    elif "EMAIL" in dhis2_property.propertyType:
        property["type"] = "string"
        property["format"] = "email"
    elif "URL" in dhis2_property.propertyType:
        property["type"] = "string"
        property["format"] = "uri"
    elif "DATE" in dhis2_property.propertyType:
        property["type"] = "date-time"
    elif "TEXT" in dhis2_property.propertyType:
        property["type"] = "string"
    elif "PHONENUMBER" in dhis2_property.propertyType:
        property["type"] = "string"
    elif "GEOLOCATION" in dhis2_property.propertyType:
        property["type"] = "string"
    elif "COLOR" in dhis2_property.propertyType:
        property["type"] = "string"
    elif "IDENTIFIER" in dhis2_property.propertyType:
        property["type"] = "string"
    elif "CONSTANT" in dhis2_property.propertyType:
        property["type"] = "string"
        property["enum"] = dhis2_property.constants
    elif "COMPLEX" in dhis2_property.propertyType and (
        dhis2_property.embeddedObject or not dhis2_property.identifiableObject
    ):
        handle_reference(dhis2_property, property)
    elif "REFERENCE" in dhis2_property.propertyType and dhis2_property.identifiableObject:
        handle_reference(dhis2_property, property)
    elif "COLLECTION" in dhis2_property.propertyType:
        handle_collection(dhis2_property, property)
    else:
        print(f"PROPERTY={dhis2_property}", file=sys.stderr)

    return property


def handle_object(dhis2_schema: Schema):
    object_property = {
        "type": "object",
        "properties": {},
        "required": [],
    }

    for dhis2_property in dhis2_schema.properties:
        if property := handle_property(dhis2_property):
            name = dhis2_property.collectionName if dhis2_property.collection else dhis2_property.name
            object_property.get("properties")[name] = property

            if dhis2_property.required:
                object_property.get("required").append(name)

    return object_property


def generate_json_schema(dhis2_schema: Schema):
    schema = {
        "$id": "https://dhis2.org/schemas/metadata",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "definitions": {
            "identifiableObject": {
                "oneOf": [
                    {"type": "object", "properties": {"id": {"type": "string"}}},
                    {"type": "object", "properties": {"code": {"type": "string"}}},
                ]
            }
        },
        "properties": {},
        "required": [],
    }

    schema["properties"] = handle_object(dhis2_schema).get("properties", {})

    return schema


def generate_json_schema_metadata(dhis2_schemas: List[Schema]):
    schema = {
        "$id": "https://dhis2.org/schemas/metadata",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "definitions": {
            "identifiableObject": {
                "oneOf": [
                    {"type": "object", "properties": {"id": {"type": "string"}}},
                    {"type": "object", "properties": {"code": {"type": "string"}}},
                ]
            }
        },
        "properties": {},
        "required": [],
    }

    for dhis2_schema in dhis2_schemas:
        if not dhis2_schema.metadata:
            continue

        property = {"type": "array", "items": {"$ref": f"#/definitions/{dhis2_schema.name}"}}
        schema.get("properties")[dhis2_schema.plural] = property

    for dhis2_schema in dhis2_schemas:
        if not dhis2_schema.metadata and not dhis2_schema.embeddedObject:
            continue

        property = handle_object(dhis2_schema)
        schema.get("definitions")[dhis2_schema.singular] = property

    return schema
