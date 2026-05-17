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


@app.get("/getGraphStats")
async def get_graph(interval: str = "year", region: str = "Almaly"):
    try:
        intervals = {
            "year": "1 year",
            "month": "1 month",
            "day": "1 day"
        }

        group_by_rules = {
            "year": "DATE_TRUNC('month', date::timestamp) + ((EXTRACT(day FROM date::timestamp)-1)/15)::int * interval '15 day'",
            "month": "DATE_TRUNC('day', date::timestamp)",
            "day": "DATE_TRUNC('hour', date::timestamp)"
        }

        with data_base.connect() as conn:
            query = text(f"""
                SELECT 
                    AVG("pm2_5") AS pm25,
                    AVG("co2") AS co2,
                    {group_by_rules[interval]} AS ts
                FROM environment_data
                WHERE region = :region
                AND date::timestamp BETWEEN NOW() - INTERVAL '{intervals[interval]}' AND NOW()
                GROUP BY ts
                ORDER BY ts
            """)

            result_proxy = conn.execute(query, {"region": region})
            df = pd.DataFrame(result_proxy.mappings().all())

            if not df.empty and interval != "day":
                df["ts"] = df["ts"].astype(str).str.split(" ").str[0]

        return {"data": df.to_dict(orient="records")}

    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")
        return {"error": str(e)}

@app.get("/getAllStats")
async def say_hello():
    return {"message": f"Hello"}


@app.get("/getStatsByRegion")
async def get_stats_by_region():
    try:
        with data_base.connect() as conn:
            query = text("""
                SELECT region,
                       AVG("pm2_5") AS avg_pm25,
                       AVG("co2") AS avg_co2
                FROM environment_data
                WHERE date::timestamp BETWEEN NOW() - INTERVAL '1 year' AND NOW()
                GROUP BY region
            """)
            result = conn.execute(query).mappings().all()

            return {"data": [dict(row) for row in result]}
    except Exception as e:
        print(f"Ошибка в get_stats_by_region: {e}")
        return {"error": str(e)}
