from pydantic import BaseModel


class Request(BaseModel):
    headline: str
