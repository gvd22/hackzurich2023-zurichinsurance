from typing import List
from fastapi import FastAPI, WebSocket
from uuid import uuid4, UUID
import asyncio
from insurance import Insurance
from ticket import Ticket
from ticket_service import TicketServiceInstance
from chat_service import ChatService

app = FastAPI()
ticket_service = TicketServiceInstance
chat_service = ChatService()


@app.get("/insurances")
def read_item() -> List[Insurance]:
    """
    This endpoint returns a list of dummy insurances
    :return: List of insurances
    """
    # Dummy insurances
    insurance_1 = Insurance(id=uuid4(), name="Household Insurance Optimum", price=250.50, type="Home", starting_date="2021-12-31")
    insurance_2 = Insurance(id=uuid4(), name="Health Pro", price=180.75, type="Health", starting_date="2022-08-15")
    insurance_3 = Insurance(id=uuid4(), name="RoadGuard", price=130.30, type="Auto", starting_date="2023-01-01")
    insurance_4 = Insurance(id=uuid4(), name="TravelSafe", price=90.10, type="Travel", starting_date="2023-05-08")
    return [insurance_1, insurance_2, insurance_3, insurance_4]


@app.get("/tickets")
def get_tickets() -> List[Ticket]:
    return ticket_service.get_all_tickets()


@app.post("/tickets")
def add_ticket(ticket: Ticket) -> Ticket:
    ticket.id = uuid4()
    ticket_service.add_ticket(ticket)
    return ticket


@app.post("/tickets/{ticket_id}/close")
def close_ticket(ticket_id: UUID) -> Ticket:
    return ticket_service.close_ticket(ticket_id)


@app.get("/test")
def test(q: str = "Which insurances are available?") -> str:
    response, messages = chat_service.run_conversation(q, [])
    return response


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    This endpoint is used to communicate with the frontend via websockets
    :param websocket:
    :return:
    """
    await websocket.accept()
    await websocket.send_text("Hey, I'm ZüriZap how can I help you?")
    messages = []
    while True:
        data = await websocket.receive_text()
        response, messages = chat_service.run_conversation(data, messages)
        await websocket.send_text(response)
        # for letter in data:
        #     await websocket.send_text(f"{letter}")
        #     await asyncio.sleep(0.01)  # This will add a delay of 10 milliseconds between letters
