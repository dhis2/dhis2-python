from datetime import date
from typing import Any, List, Optional
from uuid import uuid4

from dhis2.core.metadata.models import Translation
from pydantic import BaseModel, Field


class BaseSource(BaseModel):
    id: str
    lastUpdated: Optional[date]


class BaseTarget(BaseModel):
    id: str = "log://"


class MCSDSource(BaseSource):
    filters: List[str] = []


class MCSDTarget(BaseTarget):
    pass


class MCSDConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: MCSDSource
    target: MCSDTarget


class BaseEntity(BaseModel):
    id: str
    code: Optional[str]
    name: Optional[str]
    translations: List[Translation] = []


class OrgUnitGeometry(BaseModel):
    type: str
    coordinates: List[Any] = []


class OrgUnit(BaseEntity):
    geometry: Optional[OrgUnitGeometry]
    parent: Optional[BaseEntity]
