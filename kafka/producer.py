import asyncio
from time import sleep
from json import dumps
from kafka import KafkaProducer
import websockets

WS_URI = "wss://api.tiingo.com/crypto"

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)


subscribe = {
    "eventName": "subscribe",
    "authorization": "0e92eb063d076ad8bd5f5a1d15c9c10d27d83e00",
    "eventData": {"thresholdLevel": 2},
}


async def receive_msg():
    async with websockets.connect(WS_URI) as websocket:
        await websocket.send(dumps(subscribe))
        print("subscribed :)")

        while True:
            msg = await websocket.recv()
            print("received msg:", msg)
            producer.send("tiingo", value=msg)
            sleep(1)


asyncio.get_event_loop().run_until_complete(receive_msg())
