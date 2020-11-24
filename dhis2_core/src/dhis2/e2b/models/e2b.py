from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4


class AttributeValue(BaseModel):
    created: datetime
    lastUpdated: datetime
    attribute: str
    value: str
    storedBy: Optional[str]


class EventDataValue(BaseModel):
    created: datetime
    lastUpdated: datetime
    dataElement: str
    value: str
    providedElsewhere: bool
    storedBy: Optional[str]


class Event(BaseModel):
    created: datetime
    lastUpdated: datetime
    event: str
    program: str
    programStage: str
    trackedEntityInstance: str
    orgUnit: str
    status: str
    dueDate: datetime
    eventDate: datetime
    completedDate: Optional[str]
    storedBy: Optional[str]
    dataValues: Union[Dict[str, EventDataValue], List[EventDataValue]] = []


class Enrollment(BaseModel):
    created: datetime
    lastUpdated: datetime
    enrollment: str
    trackedEntityInstance: str
    orgUnit: str
    storedBy: Optional[str]
    status: str
    completedDate: Optional[str]
    events: List[Event] = []
    attributes: Union[Dict[str, AttributeValue], List[AttributeValue]] = []


class TrackedEntity(BaseModel):
    created: datetime
    lastUpdated: datetime
    trackedEntityInstance: str
    trackedEntityType: str
    orgUnit: str
    storedBy: Optional[str]
    enrollments: List[Enrollment] = []
    attributes: Union[Dict[str, AttributeValue], List[AttributeValue]] = []


class E2BR2Source(BaseModel):
    id: str


class E2BR2Config(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: E2BR2Source
