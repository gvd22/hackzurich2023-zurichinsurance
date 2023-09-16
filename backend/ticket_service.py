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

    def get_ticket_by_id(self, ticket_id: UUID) -> Ticket:
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                return ticket
        raise Exception(f"Ticket with id {ticket_id} not found")

    def get_ticket_by_name(self, ticket_name: str) -> Ticket:
        for ticket in self.tickets:
            if ticket.name == ticket_name:
                return ticket
        raise Exception(f"Ticket with name {ticket_name} not found")

    def close_ticket(self, ticket_id: UUID) -> Ticket:
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                ticket.status = "Closed"
                return ticket
        raise Exception(f"Ticket with id {ticket_id} not found")


TicketServiceInstance = TicketService()
