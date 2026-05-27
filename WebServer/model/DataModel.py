from datetime import date as dt_date
from datetime import time as dt_time
from sqlmodel import Field, SQLModel


class EnvironmentData(SQLModel, table=True):
    __tablename__ = "environment_data"
    id: int = Field(default=None, primary_key=True)
    temperature: float
    humidity: float
    pressure_level: float
    co2: int
    pm2_5: float
    pm10: float
    noise_level: float
    region: str = Field(index=True)
    date: dt_date = Field(index=True)
    time: dt_time
