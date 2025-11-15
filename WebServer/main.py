from contextlib import asynccontextmanager

from faststream.rabbit import RabbitBroker
from fastapi import FastAPI, WebSocket
import json
from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine
from EnvData import postgresql_url, rabbit_uri

@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    yield
    await broker.stop()


app = FastAPI(lifespan=lifespan)
broker = RabbitBroker(rabbit_uri)
data_base = create_engine(postgresql_url)

@app.on_event("startup")
async def start_broker():
    await broker.start()

@app.on_event("shutdown")
async def stop_broker():
    await broker.close()

@broker.subscriber("newRow")
async def handle_newRow(msg: str):
    print(msg)
    try:
        data = json.loads(msg)
        with data_base.connect() as conn:
            query = text("""
                INSERT INTO environment_data ("Temperature", "Humidity", "pressure_level", "CO2", "PM2_5", "PM10",
                 "noise_level", "region", "date", "time")
                VALUES (:Temperature, :Humidity, :pressure_level, :CO2, :PM2_5, :PM10,
                        :noise_level, :region, :date, :time)
            """)
            conn.execute(query, data)
            conn.commit()
            print("New row inserted")
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")

@app.get("/getGraphStats")
async def get_graph(interval: str = "year", region: str = "Алатау"):
    try:
        intervals = {
            "year": "1 year",
            "month": "1 month",
            "day": "1 day"
        }

        with data_base.connect() as conn:
            query = text(f"""
                SELECT "PM2_5" AS pm25,
                       "CO2" AS co2
                FROM environment_data
                WHERE region = :region
                AND to_timestamp(date, 'YYYY-MM-DD') 
                    BETWEEN NOW() - INTERVAL '{intervals[interval]}' AND NOW()
            """)

            result = conn.execute(query, {"region": region}).mappings().all()

        return {"data": result}

    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")
        return {"error": "Server error"}





@app.get("/getAllStats")
async def say_hello():
    return {"message": f"Hello"}

@app.get("/getStatsByRegion")
async def get_stats_by_region():
    try:
        with data_base.connect() as conn:
            query = text("""
                SELECT region,
                       AVG("PM2_5") AS avg_pm25,
                       AVG("CO2") AS avg_co2
                FROM environment_data
                WHERE to_timestamp(date, 'YYYY-MM-DD') BETWEEN NOW() - INTERVAL '1 year' AND NOW()
                GROUP BY region
            """)
            result = conn.execute(query).mappings().all()
            return {"data": result}
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")
