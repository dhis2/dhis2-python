from pydantic import BaseModel


class Translation(BaseModel):
    property: str
    locale: str
    value: str
