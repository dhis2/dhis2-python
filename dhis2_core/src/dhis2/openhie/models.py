from typing import List, Literal, Optional, Union
from uuid import uuid4

from dhis2.core.metadata.models import Translation
from pydantic import BaseModel, Field


class BaseSource(BaseModel):
    id: str


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


class Code(BaseModel):
    id: str
    code: str
    name: str
    translations: List[Translation] = []


class CodeList(BaseModel):
    id: str
    code: Optional[str]
    type: Literal["optionSets", "categories"] = "optionSets"
    name: str
    translations: List[Translation] = []
    version: Union[str, int] = "1"
    codes: List[Code] = []
