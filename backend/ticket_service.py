from ticket import Ticket
from uuid import UUID
from typing import List


class TicketService:
    def __init__(self):
        self.tickets: List[Ticket] = []

    def add_ticket(self, ticket: Ticket) -> None:
        self.tickets.append(ticket)

    def get_all_tickets(self) -> List[Ticket]:
        return self.tickets

    def close_ticket(self, ticket_id: UUID) -> Ticket:
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                ticket.status = "Closed"
                return ticket
        raise Exception(f"Ticket with id {ticket_id} not found")