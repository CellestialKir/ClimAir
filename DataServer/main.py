from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
import json
from sqlalchemy import create_engine, text
import pandas as pd
from EnvData import postgresql_url, secret_token, rabbit_uri
from collections import deque, defaultdict
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit import RabbitBroker

router = RabbitRouter(rabbit_uri)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start")
    yield
    print("stop")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
data_base = create_engine(postgresql_url)
allowed_columns = {"Temperature", "Humidity", "pressure_level", "CO2", "PM2_5", "PM10", "noise_level", "region", "date", "time"}
recent_data = defaultdict(lambda: deque(maxlen=10))


def validate_data(data):
    print("Validating...")
    required = ["date", "time", "region"]

    # 1. Базовая проверка обязательных полей
    if not all(data.get(k) for k in required):
        return None

    region = data["region"]

    clean_payload = {k: v for k, v in data.items() if k in allowed_columns}

    history_df = None
    if recent_data[region]:
        history_df = pd.DataFrame(list(recent_data[region]))
    else:
        with data_base.connect() as conn:
            query = text("""
                SELECT * FROM environment_data 
                WHERE region = :region 
                ORDER BY date DESC, time DESC 
                LIMIT 10
            """)
            db_data = pd.read_sql(query, conn, params={"region": region})
            if not db_data.empty:
                history_df = db_data

    for key in allowed_columns:
        if clean_payload.get(key) in (None, "", "null"):
            if history_df is not None and key in history_df.columns:
                avg_val = history_df[key].replace("null", None).mean()
                if pd.notnull(avg_val):
                    clean_payload[key] = round(float(avg_val), 2)
                else:
                    clean_payload[key] = 0
            else:
                clean_payload[key] = 0

    return clean_payload


@app.websocket("/ws/data")
async def websocket_data_acceptation(websocket: WebSocket, token: str = None):
    if token != secret_token:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    try:
        while True:
            raw_data = await websocket.receive_text()
            payload = json.loads(raw_data)
            validated = validate_data(payload)

            if validated:
                print(f"Запись данных в БД: {validated}")
                pd.DataFrame([validated]).to_sql(
                    "environment_data",
                    data_base,
                    if_exists="append",
                    index=False,
                    method='multi'
                )

                recent_data[validated["region"]].append(validated)
                await router.broker.publish(validated, queue="newRow")
            else:
                print("Данные не прошли валидацию!")

    except Exception as e:
        print(f"Connection closed for {websocket.client}: {e}")