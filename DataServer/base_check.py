from datetime import datetime, timedelta
import random
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from EnvData import postgresql_url

REGION = "Almaly"
TOTAL_RECORDS = 1000
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 6, 1)


def generate_fake_environment_data():
    print(f"Генерация {TOTAL_RECORDS} записей для региона {REGION}...")

    timestamps = []
    delta_seconds = int((END_DATE - START_DATE).total_seconds())

    for _ in range(TOTAL_RECORDS):
        random_seconds = random.randint(0, delta_seconds)
        timestamps.append(START_DATE + timedelta(seconds=random_seconds))

    timestamps.sort()

    temp = 15.0
    humidity = 50.0
    pressure = 1013.0
    co2 = 400.0
    pm2_5 = 15.0
    pm10 = 35.0
    noise = 45.0

    data_list = []

    for ts in timestamps:
        temp = max(-20.0, min(40.0, temp + random.uniform(-1.5, 1.5)))
        humidity = max(10.0, min(100.0, humidity + random.uniform(-5.0, 5.0)))
        pressure = max(980.0, min(1040.0, pressure + random.uniform(-2.0, 2.0)))
        co2 = max(350.0, min(1200.0, co2 + random.uniform(-20.0, 20.0)))
        pm2_5 = max(0.0, min(150.0, pm2_5 + random.uniform(-3.0, 3.0)))
        pm10 = max(0.0, min(250.0, pm10 + random.uniform(-5.0, 5.0)))
        noise = max(30.0, min(90.0, noise + random.uniform(-4.0, 4.0)))

        data_list.append({
            "temperature": round(temp, 2),
            "humidity": round(humidity, 2),
            "pressure_level": round(pressure, 2),
            "co2": round(co2, 2),
            "pm2_5": round(pm2_5, 2),
            "pm10": round(pm10, 2),
            "noise_level": round(noise, 2),
            "region": REGION,
            "date": ts.date(),
            "time": ts.time()
        })

    return pd.DataFrame(data_list)


if __name__ == "__main__":
    try:
        # Генерация данных
        df = generate_fake_environment_data()
        records = df.to_dict(orient="records")

        # Подключение к PostgreSQL Render
        engine = create_engine(
            postgresql_url,
            connect_args={"sslmode": "require"},
            pool_pre_ping=True,
            pool_recycle=300
        )

        # Проверка подключения
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Подключение к БД успешно.")

        # Проверка существования таблицы
        inspector = inspect(engine)

        if "environment_data" not in inspector.get_table_names():
            print("Таблица environment_data не найдена. Создаем...")

            create_table_query = text("""
                CREATE TABLE environment_data (
                    id SERIAL PRIMARY KEY,
                    temperature NUMERIC(5,2),
                    humidity NUMERIC(5,2),
                    pressure_level NUMERIC(6,2),
                    co2 NUMERIC(6,2),
                    pm2_5 NUMERIC(5,2),
                    pm10 NUMERIC(5,2),
                    noise_level NUMERIC(5,2),
                    region VARCHAR(100),
                    date DATE,
                    time TIME
                )
            """)

            with engine.begin() as conn:
                conn.execute(create_table_query)

            print("Таблица успешно создана.")
        else:
            print("Таблица environment_data уже существует.")

        # Запрос для массовой вставки
        insert_query = text("""
            INSERT INTO environment_data (
                temperature,
                humidity,
                pressure_level,
                co2,
                pm2_5,
                pm10,
                noise_level,
                region,
                date,
                time
            )
            VALUES (
                :temperature,
                :humidity,
                :pressure_level,
                :co2,
                :pm2_5,
                :pm10,
                :noise_level,
                :region,
                :date,
                :time
            )
        """)

        print(f"Начинаем вставку {TOTAL_RECORDS} записей...")

        # Массовая вставка одной транзакцией
        with engine.begin() as conn:
            conn.execute(insert_query, records)

        print(f"Успешно добавлено {TOTAL_RECORDS} записей для региона {REGION}.")

    except Exception as e:
        print("\nКритическая ошибка:")
        print(type(e).__name__)
        print(e)