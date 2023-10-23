from pydantic import BaseModel

class Query(BaseModel):
    url: str
    query: str