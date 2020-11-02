from typing import List, Optional

from pydantic import BaseModel


class Property(BaseModel):
    fieldName: Optional[str]
    description: Optional[str]
    simple: bool
    required: bool
    writable: bool
    collectionName: Optional[str]
    min: Optional[int]
    nameableObject: bool
    klass: str
    propertyType: str
    oneToOne: bool
    propertyTransformer: bool
    attribute: bool
    owner: bool
    readable: bool
    ordered: bool
    identifiableObject: bool
    max: Optional[int]
    manyToMany: bool
    collection: bool
    itemPropertyType: Optional[str]
    collectionWrapping: Optional[bool]
    itemKlass: Optional[str]
    analyticalObject: bool
    embeddedObject: bool
    unique: bool
    name: str
    namespace: Optional[str]
    persisted: bool
    manyToOne: bool
    constants: List[str] = []
