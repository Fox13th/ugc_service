from pydantic import BaseModel


class Events(BaseModel):
    topic: str
    value: str
    key: str
