"""
PM 2.5 target value - 15
PM 2.5 Deviation - (37.5 - 15)

PM 10 target value - 45
PM 10 Deviation - (75 - 45)

CO2 target value - 700
CO2 Deviation - 300

Noise target value - 45
Noise Deviation - (60 - 45)

Autumn/Spring target temperature - 10
Autumn/Spring temperature Deviation - 5

Winter target temperature - -10
Winter temperature Deviation - 5

Summer target temperature - 20
Summer temperature Deviation - 5

Autumn/Spring target humidity - 55
Autumn/Spring humidity Deviation - 15

Winter target humidity - 60
Winter humidity Deviation - 20

Summer target humidity - 50
Summer humidity Deviation - 10

Pressure value - must be evaluated as daytime deviation
deviation - 3
(min - max) / deviation for Pressure
"""

from datetime import date as dt_date


ALL_REGIONS = [
    "Almaly",
    "Auezov",
    "Bostandyk",
    "Alatau",
    "Zhetysu",
    "Turksib",
    "Medeu",
    "Nauryzbay"
]


def get_season(month: int) -> str:
    if month in [12, 1, 2]:
        return "winter"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "transition"  # Autumn / Spring


def calculate_penalty_score(value: float, v_norm: float, d: float) -> float:
    if value is None:
        return 0.0
    if value <= v_norm:
        return 1.0
    x = 1.0 - (value - v_norm) / d
    return max(0.0, x)


def calculate_optimal_score(value: float, optimal: float, range_val: float) -> float:
    if value is None:
        return 0.0
    x = 1.0 - abs(value - optimal) / range_val
    return max(0.0, x)


def calculate_rating(raw_db_results, user_importance: dict = None) -> list:
    default_importance = {
        "temperature": 5,
        "humidity": 5,
        "pressure": 3,
        "co2": 8,
        "pm2_5": 10,
        "pm10": 8,
        "noise": 6
    }
    importance = user_importance or default_importance

    total_importance = sum(importance.values())
    weights = {k: v / total_importance for k, v in importance.items()}

    current_month = dt_date.today().month
    season = get_season(current_month)

    if season == "winter":
        t_opt, t_dev = -10.0, 5.0
        h_opt, h_dev = 60.0, 20.0
    elif season == "summer":
        t_opt, t_dev = 20.0, 5.0
        h_opt, h_dev = 50.0, 10.0
    else:
        t_opt, t_dev = 10.0, 5.0
        h_opt, h_dev = 55.0, 15.0

    processed_regions = set()
    raw_report = []

    for row in raw_db_results:
        region, temp, hum, press_dev, co2, pm25, pm10, noise = row
        processed_regions.add(region)

        scores = {
            "temperature": calculate_optimal_score(temp, t_opt, t_dev),
            "humidity": calculate_optimal_score(hum, h_opt, h_dev),
            "pressure": max(0.0, 1.0 - press_dev) if press_dev is not None else 0.0,
            "co2": calculate_penalty_score(co2, 700.0, 300.0),
            "pm2_5": calculate_penalty_score(pm25, 15.0, 22.5),
            "pm10": calculate_penalty_score(pm10, 45.0, 30.0),
            "noise": calculate_penalty_score(noise, 45.0, 15.0)
        }

        final_score = sum(weights[key] * scores[key] for key in weights)
        final_score_scaled = round(final_score * 100, 1)

        if final_score_scaled >= 80:
            category = "Excellent"
        elif final_score_scaled >= 50:
            category = "Good"
        else:
            category = "Poor"

        raw_report.append({
            "region": region,
            "final_score": final_score_scaled,
            "category": category,
            "has_data": True,
            "raw_averages": {
                "temperature": round(temp, 1) if temp else 0,
                "humidity": round(hum, 1) if hum else 0,
                "pressure_daytime_deviation": round(press_dev, 2) if press_dev else 0,
                "co2": round(co2, 1) if co2 else 0,
                "pm2_5": round(pm25, 1) if pm25 else 0,
                "pm10": round(pm10, 1) if pm10 else 0,
                "noise": round(noise, 1) if noise else 0
            }
        })

    raw_report.sort(key=lambda x: x["final_score"], reverse=True)

    final_rating_list = []
    place_counter = 1

    for data in raw_report:
        final_rating_list.append({
            "place": place_counter,
            "region": data["region"],
            "final_score": data["final_score"],
            "category": data["category"],
            "average_data": data["raw_averages"]
        })
        place_counter += 1

    for region in ALL_REGIONS:
        if region not in processed_regions:
            final_rating_list.append({
                "place": place_counter,
                "region": region,
                "final_score": None,
                "category": "No data",
                "average_data": {
                    "temperature": "No data",
                    "humidity": "No data",
                    "pressure_daytime_deviation": "No data",
                    "co2": "No data",
                    "pm2_5": "No data",
                    "pm10": "No data",
                    "noise": "No data"
                }
            })
            place_counter += 1

    return final_rating_list

