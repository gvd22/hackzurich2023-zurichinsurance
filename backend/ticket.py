from uuid import UUID
from pydantic import BaseModel


class Ticket(BaseModel):
    id: UUID
    name: str
    type: str
    description: str
    status: str = "Pending"

    def dump(self):
        return "Ticket: " + self.name + "\n" + "Type: " + self.type + "\n" + "Description: " + self.description + "\n" + "Status: " + self.status + "\n"
