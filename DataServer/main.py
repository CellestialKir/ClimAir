from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
import json
from sqlalchemy import create_engine, text
import pandas as pd
from EnvData import postgresql_url, secret_token
from collections import deque, defaultdict
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit import RabbitBroker

router = RabbitRouter()

app = FastAPI()

app.include_router(router)
data_base = create_engine(postgresql_url)
allowed_columns = {"Temperature", "Humidity", "pressure_level", "CO2", "PM2_5", "PM10", "noise_level", "region", "date", "time"}
recent_data = defaultdict(lambda: deque(maxlen=10))

def validate_data(data):
    required = ["date", "time", "region"]
    for key in required:
        if key not in data or not data[key]:
            return None

    region = data["region"]
    region_history = recent_data.get(region)


    if not region_history:
        for key, value in data.items():
            if key not in allowed_columns:
                return None
            if value in (None, "", "null"):
                with data_base.connect() as conn:
                    query = text(f"""
                                        SELECT AVG({key}) AS avg_value
                                        FROM (
                                            SELECT {key}
                                            FROM environment_data
                                            WHERE region = :region
                                            ORDER BY date DESC, time DESC
                                            LIMIT 10
                                        ) AS recent_data
                                    """)
                    result = conn.execute(query, {"region": data["region"]}).fetchone()
                    avg_val = result.avg_value if result and result.avg_value is not None else None
                    if avg_val is not None:
                        data[key] = round(avg_val, 2)
                    else:
                        return None
        return data
    else:
        history_df = pd.DataFrame(list(region_history))
        for key, value in data.items():
            if value in (None, "", "null"):
                if key in history_df.columns:
                    data[key] = round(history_df[key].mean(), 2)

        return data


@app.websocket("/ws/data")
async def websocket_data_acceptation(websocket: WebSocket, token: str = None):
    if token != secret_token:
        await websocket.close()
        print("Неверный токен")
        return
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            validated = validate_data(payload)
            if validated:
                pd.DataFrame([validated]).to_sql("environment_data", data_base, if_exists="append", index=False)
                recent_data[validated["region"]].append(validated)

                await router.broker.publish(json.dumps(validated), queue="newRow")


    except Exception as e:
        print("Клиент отключился:", e)