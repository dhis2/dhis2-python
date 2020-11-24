from datetime import datetime
from typing import Union

from .models.e2b import Enrollment, Event, EventDataValue, TrackedEntity


def date_format_102(dt: datetime) -> str:
    return dt.strftime("%Y%m%d")


def date_format_204(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M%S")


def get_attribute_value(at: str, te: TrackedEntity) -> Union[str, None]:
    if te.attributes[at]:
        return te.attributes[at].value


def get_data_value(de: str, te: TrackedEntity, idx: int = 0) -> Union[str, None]:
    en: Enrollment = te.enrollments[idx]
    ev: Event = en.events["so8YZ9J3MeO"]  # AEFI stage

    if de not in ev.dataValues:
        return None

    dv: EventDataValue = ev.dataValues[de]

    if dv:
        return dv.value

    return None


def get_patient_age(te: TrackedEntity) -> str:
    value = get_attribute_value("BiTsLcJQ95V", te)
    dt = datetime.fromisoformat(value)
    now = datetime.now()

    return str(now.year - dt.year)


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

    return "9"
