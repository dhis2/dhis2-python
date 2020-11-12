from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field


class LanguageSpecificText(BaseModel):
    language: Optional[str] = Field(alias="@language")
    value: Optional[str] = Field(alias="@value")


class ICD10Entity(BaseModel):
    id: str = Field(alias="@id")
    context: str = Field(alias="@context")
    title: Optional[LanguageSpecificText]
    definition: Optional[LanguageSpecificText]
    longDefinition: Optional[LanguageSpecificText]
    fullySpecifiedName: Optional[LanguageSpecificText]
    source: Optional[str]
    code: Optional[str]
    note: Optional[LanguageSpecificText]
    codeRange: Optional[str]

    # chapter : if the entity is a chapter. (i.e. at the top level of the classification
    # block : higher level entity which don't have codes
    # category : An ICD entity that bears a code

    classKind: Literal["block", "category", "chapter"]
    child: Union[List[str], List["ICD10Entity"]] = []
    parent: Union[List[str], List["ICD10Entity"]] = []
    browserUrl: Optional[str]


ICD10Entity.update_forward_refs()
