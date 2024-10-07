from pydantic import BaseModel

class Event(BaseModel):
    txt: str
    desc: str