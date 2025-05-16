import pandas as pd
from prophet import Prophet

# === Load historical monthly permits ===
df = pd.read_csv("permits-till-23.csv", parse_dates=["Month"])

# Prepare data for Prophet: only use columns Prophet expects
df_prophet = df[["Month", "Dwellings"]].rename(columns={"Month": "ds", "Dwellings": "y"})

# === Fit Prophet model ===
model = Prophet(yearly_seasonality=True)
model.fit(df_prophet)

# === Make future dataframe for 12 months (Jan–Dec 2024) ===
future = model.make_future_dataframe(periods=12, freq="MS")

# === Predict ===
forecast = model.predict(future)

# === Extract and save only the 2024 forecast ===
forecast_2024 = forecast[forecast["ds"].dt.year == 2024][["ds", "yhat"]]
forecast_2024.columns = ["Month", "Forecasted_Dwellings"]
forecast_2024.to_csv("forecasted_permits_2024.csv", index=False)

print("Forecast saved to forecasted_permits_2024.csv")
