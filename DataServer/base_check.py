import psycopg2
from psycopg2.extras import RealDictCursor

from EnvData import postgresql_url

try:
    conn = psycopg2.connect(postgresql_url)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM environment_data;")
    rows = cur.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    print("Ошибка подключения или выполнения запроса:", e)

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
