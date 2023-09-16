from uuid import UUID
from pydantic import BaseModel


class Ticket(BaseModel):
    id: UUID
    name: str
    type: str
    description: str
    status: str = "Pending"
