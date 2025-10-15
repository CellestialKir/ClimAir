import pandas as pd
from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from EnvData import postgresql_url


time = datetime(2025, 10, 13, 11, 0, 0)
regions = ["Алатауский", "Алмалинский", "Ауэзовский", "Бостандыкский", "Жетысуский", "Медеуский", "Наурызбайский", "Турксибский"]

csv_data = pd.read_csv("updated_pollution_dataset.csv")

csv_data.drop(['NO2', 'SO2','Proximity_to_Industrial_Areas', 'Population_Density', 'Air Quality'], axis=1, inplace=True)

region_counter = 0
date_counter = 0
region_column = []
date_column = []
time_column = []
csv_data["pressure_level"] = list(1013 + (random.randint(-40, 40)) for _ in range(5000))
csv_data["noise_level"] = list(60 + (random.randint(-10, 10)) for _ in range(5000))

for i in range(len(csv_data)):
    if region_counter == 8:
        region_counter = 0
        date_counter += 1
        time += timedelta(minutes=10)
    if date_counter == 30:
        region_counter = 0
        date_counter = 0
        time += timedelta(days=1)
        time = datetime.combine(time.date(), datetime.strptime("11:00:00", "%H:%M:%S").time())
    region_column.append(regions[region_counter])
    date_column.append(time.strftime("%Y-%m-%d"))
    time_column.append(time.strftime("%H:%M:%S"))
    region_counter += 1

csv_data["region"] = region_column
csv_data["date"] = date_column
csv_data["time"] = time_column
csv_data = csv_data.rename(columns={"CO": "CO2"})
csv_data = csv_data.rename(columns={"PM2.5": "PM2_5"})
print(csv_data.columns.tolist())

new_csv = pd.DataFrame(csv_data)

engine = create_engine(postgresql_url)
new_csv.to_sql("environment_data", engine, if_exists="replace", index=False)