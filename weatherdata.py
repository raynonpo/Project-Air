import pandas as pd
import requests
import os
from retry_requests import retry
apikey=os.getenv("WEATHER_DATA_API") 
body={"place_id":"kuala-lumpur",
      "sections":"current,hourly",
"language":"en",
"units":"metric"



      }
response= requests.get("https://www.meteosource.com/api/v1/free/point", headers={"X-API-Key": apikey}, params=body)
print(response.status_code)
print(response)
data = response.json()
for i in data:
    if i  not in ("current", "hourly", "daily"):
        print(i, data[i])
print(data["hourly"]["data"])


# Newdata=pd.json_normalize(data["hourly"]["data"],sep="_")
# Newdata["date"] =  pd.to_datetime(Newdata["date"])
# historical_data = pd.read_csv("hourly_Weather_data.csv")
# df = pd.concat([historical_data, Newdata], ignore_index=True)
# print(df["date"])


# df = df.drop_duplicates(subset=["date"], keep="last")

# current_hour = pd.Timestamp.now().floor("h")

# print(f"Current hour: {current_hour}")
# print("dataset date:",df["date"][0])
# current_data = df[df["date"] <= current_hour]
# future_data = df[df["date"] > current_hour]
# current_data.to_csv("hourly_Weather_data.csv", index = False)
# print(current_data)
# print(future_data)
Newdata = pd.json_normalize(data["hourly"]["data"], sep="_")

# Convert new data date
Newdata["date"] = pd.to_datetime(Newdata["date"])

# Read historical data
historical_data = pd.read_csv("hourly_Weather_data.csv")

# Convert historical data date too
historical_data["date"] = pd.to_datetime(historical_data["date"])

# Combine
df = pd.concat([historical_data, Newdata], ignore_index=True)

# Remove duplicates
df = df.drop_duplicates(subset=["date"], keep="last")

# Current hour in Malaysia time
current_hour = (
    pd.Timestamp.now(tz="Asia/Kuala_Lumpur")
    .floor("h")
    .tz_localize(None)
)

print(f"Current hour: {current_hour}")
print("Dataset date:", df["date"].iloc[0])

# Separate current/historical and future data
current_data = df[df["date"] <= current_hour]
future_data = df[df["date"] > current_hour]

# Save historical/current data
current_data.to_csv("hourly_Weather_data.csv", index=False)
