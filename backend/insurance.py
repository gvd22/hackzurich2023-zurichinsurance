from uuid import UUID
from pydantic import BaseModel


class Insurance(BaseModel):
    id: UUID
    name: str
    price: float
    type: str
    starting_date: str
