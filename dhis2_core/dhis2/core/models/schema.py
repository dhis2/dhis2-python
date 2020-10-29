from typing import List, Optional

from pydantic import BaseModel

from .property import Property


class Authority(BaseModel):
    type: str
    authorities: List[str] = []


class Schema(BaseModel):
    klass: str
    shareable: bool
    metadata: bool
    relativeApiEndpoint: Optional[str]
    plural: str
    displayName: str
    singular: str
    secondaryMetadata: bool
    collectionName: Optional[str]
    implicitPrivateAuthority: bool
    nameableObject: bool
    href: str
    subscribable: bool
    order: int
    translatable: bool
    identifiableObject: bool
    favoritable: bool
    subscribableObject: bool
    dataShareable: bool
    apiEndpoint: Optional[str]
    embeddedObject: bool
    defaultPrivate: str
    name: str
    namespace: Optional[str]
    persisted: bool
    references: List[str] = []
    authorities: List[Authority] = []
    properties: List[Property] = []


class Schemas(BaseModel):
    schemas: List[Schema] = []
