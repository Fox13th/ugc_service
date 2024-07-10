from pydantic import BaseModel


class Event(BaseModel):
    event_data: dict
