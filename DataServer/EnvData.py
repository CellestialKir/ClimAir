import os
from dotenv import load_dotenv


result = load_dotenv(dotenv_path=".env")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
secret_token = os.getenv("SECRET_TOKEN")
postgresql_url = f"postgresql://{user}:{password}@{host}.oregon-postgres.render.com/{dbname}"