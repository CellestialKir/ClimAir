from sqlalchemy import create_engine, text
from EnvData import postgresql_url

try:
    engine = create_engine(postgresql_url)
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM environment_data;"))
        for row in res:
            print(row)
        res = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'environment_data';"))
        for row in res:
            print(row)


except Exception as e:
    print("Ошибка подключения или выполнения запроса:", e)

finally:
    if 'conn' in locals():
        conn.close()
