import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))  # <-- важно!
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
secret_token = os.getenv("SECRET_TOKEN")
rabbit_uri = os.getenv("RABBIT_URI")

postgresql_url = f"postgresql+psycopg2://{user}:{password}@{host}.oregon-postgres.render.com/{dbname}"
