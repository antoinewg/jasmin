from kafka import KafkaConsumer
from json import loads


consumer = KafkaConsumer(
    "tiingo",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group",
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)


for message in consumer:
    message = message.value
    print("{}\n".format(message))
