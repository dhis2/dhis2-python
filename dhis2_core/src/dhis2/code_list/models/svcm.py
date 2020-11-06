from datetime import date
from typing import List, Literal, Optional, Union
from uuid import uuid4

from dhis2.core.metadata.models import Translation
from pydantic import BaseModel, Field


class BaseSource(BaseModel):
    id: str
    lastUpdated: Optional[date]


class BaseTarget(BaseModel):
    id: str = "log://"


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
