from typing import List
from fastapi import FastAPI, WebSocket
from uuid import uuid4
import asyncio
from insurance import Insurance

app = FastAPI()


@app.get("/insurances")
def read_item() -> List[Insurance]:
    """
    This endpoint returns a list of dummy insurances
    :return: List of insurances
    """
    # Dummy insurances
    insurance_1 = Insurance(id=uuid4(), name="Home Shield", price=250.50, type="Home")
    insurance_2 = Insurance(id=uuid4(), name="Health Pro", price=180.75, type="Health")
    insurance_3 = Insurance(id=uuid4(), name="RoadGuard", price=130.30, type="Auto")
    insurance_4 = Insurance(id=uuid4(), name="TravelSafe", price=90.10, type="Travel")
    return [insurance_1, insurance_2, insurance_3, insurance_4]


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    This is a websocket endpoint echo server. It will echo back any message sent to
     it letter by letter with a delay of 10 milliseconds between letters.
    :param websocket:
    :return:
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        websocket.send(f"Message text was: {data}")
        await websocket.send_text(f"ECHO: ")
        for letter in data:
            await websocket.send_text(f"{letter}")
            await asyncio.sleep(0.01)  # This will add a delay of 10 milliseconds between letters
