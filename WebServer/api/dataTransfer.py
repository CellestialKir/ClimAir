from fastapi import APIRouter, HTTPException, Body
from sqlalchemy import text
from typing import Dict
import pandas as pd
from core.db import engine as data_base
from repositories.DataRepo import getLastData, get_raw_data_by_region
from model.DataModel import EnvironmentData
from typing import Optional
from inner.Rate import calculate_rating

router = APIRouter()


@router.get("/getCurrentStats", response_model=Optional[EnvironmentData])
async def get_current_stats(region: str = "Almaly"):
    result = getLastData(region)
    print(f"Данные из БД: {result}")

    if not result:
        raise HTTPException(status_code=404, detail="Region data not found")

    return result


@router.get("/getGraphStats")
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


@router.get("/getAllStats")
async def say_hello():
    return {"message": f"Hello"}


@router.get("/getStatsByRegion")
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


@router.post("/getRegionEnvironmentalRating")
async def get_region_environmental_rating(
        importance: Dict[str, int] = Body(
            default={
                "temperature": 5,
                "humidity": 5,
                "pressure": 3,
                "co2": 8,
                "pm2_5": 10,
                "pm10": 8,
                "noise": 6
            }
        )
):
    try:
        raw_data, start_date, end_date = get_raw_data_by_region()
        final_report = calculate_rating(raw_data, user_importance=importance)

        return final_report
    except Exception as e:
        print(f"Error calculating leaderboard payload: {e}")
        return {"error": str(e)}
