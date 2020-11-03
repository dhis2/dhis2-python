from datetime import date
from typing import Any, List, Literal, Optional, Union
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


class SVCMFilters(BaseModel):
    optionSets: List[str] = []
    categories: List[str] = []


class SVCMSource(BaseSource):
    filters: SVCMFilters = SVCMFilters()


class SVCMTarget(BaseTarget):
    pass


class SVCMConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: SVCMSource
    target: SVCMTarget


class BaseEntity(BaseModel):
    id: str
    code: Optional[str]
    name: Optional[str]
    translations: List[Translation] = []


class Code(BaseEntity):
    pass


class CodeList(BaseEntity):
    type: Literal["optionSets", "categories"] = "optionSets"
    version: Union[str, int] = "1"
    codes: List[Code] = []


class OrgUnitGeometry(BaseModel):
    type: str
    coordinates: List[Any] = []


class OrgUnit(BaseEntity):
    geometry: Optional[OrgUnitGeometry]
    parent: Optional[BaseEntity]
