import json
# import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer(
    'ecommerce.tracker',
    auto_offset_reset = "earliest",
    bootstrap_servers = ['kafka:9092'],
    value_deserializer = lambda m: json.loads(m.decode('utf-8')) 
)



for message in consumer:
    # print(message.value)
    with open("result.json", "a") as file:
        file.write(json.dumps(message.value))
        file.write("\n")

    json_data = message.value
    event = {
        "page_type": json_data["core"]["page_type"],
        "page_url": json_data["core"]["page_url"],
        "user_id": json_data["user"]["user_id"],
        "session_id": json_data["user"]["session_id"],
        "event_timestamp": json_data["event_timestamp"]
    }

    conn = create_engine('postgresql://postgres:root@postgres:5434/')

    with conn.begin() as connection:
        connection.execute(
            text("INSERT INTO events VALUES(:page_type, :page_url, :user_id, :session_id, :event_timestamp)"),
            [event]
        )
    # print(flatten_data)

    # for data in flatten_data:
    #     df = pd.read_json()

    #     # connection
    #     url = 'postgresql+psycopg2://postgres:root@postgres:5434/events'
    #     engine = create_engine(url=url)


