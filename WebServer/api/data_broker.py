from faststream.rabbit import RabbitBroker
from EnvData import rabbit_uri
from core.db import engine as data_base
from sqlalchemy import text

broker = RabbitBroker(rabbit_uri)


@broker.subscriber("newRow")
async def handle_newRow(msg: dict):
    print(msg)
    try:
        data = msg
        with data_base.connect() as conn:
            query = text("""
                INSERT INTO environment_data ("temperature", "humidity", "pressure_level", "co2", "pm2_5", "pm10",
                 "noise_level", "region", "date", "time")
                VALUES (:temperature, :humidity, :pressure_level, :co2, :pm2_5, :pm10,
                        :noise_level, :region, :date, :time)
            """)
            conn.execute(query, data)
            conn.commit()
            print("New row inserted")
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")