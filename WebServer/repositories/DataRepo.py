from model.DataModel import EnvironmentData
from sqlmodel import Session, select, func, and_
from core.db import engine
from datetime import date as dt_date, timedelta


def getLastData(region:str):
    with Session(engine) as session:
        state = select(EnvironmentData).where(EnvironmentData.region == region).order_by(EnvironmentData.date.desc())
        last_data = session.exec(state).first()
        if not last_data:
            return None
        return last_data


def get_raw_data_by_region():
   with Session(engine) as session:
        today = dt_date.today()
        start_date = today - timedelta(days=30)

        with Session(engine) as session:
            statement = (
                select(
                    EnvironmentData.region,
                    func.avg(EnvironmentData.temperature),
                    func.avg(EnvironmentData.humidity),
                    ((func.max(EnvironmentData.pressure_level) - func.min(EnvironmentData.pressure_level)) / 3.0),
                    func.avg(EnvironmentData.co2),
                    func.avg(EnvironmentData.pm2_5),
                    func.avg(EnvironmentData.pm10),
                    func.avg(EnvironmentData.noise_level)
                )
                .where(and_(EnvironmentData.date >= start_date, EnvironmentData.date <= today))
                .group_by(EnvironmentData.region)
            )

            results = session.exec(statement).all()
            return results, start_date, today