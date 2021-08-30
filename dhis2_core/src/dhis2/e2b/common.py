from datetime import datetime
from typing import Union

from .models.e2b import AttributeValue, Enrollment, Event, EventDataValue, TrackedEntity


def date_format_102(dt: datetime) -> str:
    return dt.strftime("%Y%m%d")


def date_format_204(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M%S")


def date_format_203(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M")


def get_attribute_value(at: str, te: TrackedEntity, defaultValue=None) -> Union[str, None]:
    av = te.attributes.get(at, defaultValue)

    if not av:
        return defaultValue

    if "value" in av:
        return av.value


def get_data_value(de: str, te: TrackedEntity, idx: int = 0, defaultValue=None) -> Union[str, None]:
    en: Enrollment = te.enrollments[idx]
    ev: Event = en.events["so8YZ9J3MeO"]  # AEFI stage

    if de not in ev.dataValues:
        return defaultValue

    dv: EventDataValue = ev.dataValues[de]

    if dv:
        return dv.value

    return defaultValue


def get_patient_age(te: TrackedEntity):
    value = get_attribute_value("BiTsLcJQ95V", te)
    dt = datetime.fromisoformat(value)
    now = datetime.now()

    year = now.year - dt.year

    if year > 0:
        return ("801", str(year))

    months = now.month - dt.month

    if months > 0:
        return ("802", str(months))

    return ("804", str(now.day - dt.day))


def get_yes_no(de: str, te: TrackedEntity, idx: int = 0):
    dv: EventDataValue = get_data_value(de, te, idx)

    if "true" == dv:
        return "1"

    return "2"


def get_patient_sex(te: TrackedEntity) -> str:
    value = get_attribute_value("CklPZdOd6H1", te)

    if "MALE" == value:
        return "1"
    elif "FEMALE" == value:
        return "0"

    return ""


def get_reaction_outcome(te: TrackedEntity):
    value = get_data_value("yRrSDiR5v1M", te)

    if "Recovered/resolved" == value:
        return "1"
    elif "Recovering/resolving" == value:
        return "2"
    elif "Not recovered/not resolved" == value:
        return "3"
    elif "Recovered/resolved with sequelae" == value:
        return "4"
    elif "Died" == value or "Autopsy done" == value:
        return "5"
    elif "Unknown" == value:
        return "6"

    return value
