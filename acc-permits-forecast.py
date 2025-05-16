import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === Step 1: Ground truth and IBM AutoAI predictions ===
actual_values = np.array([
    14918, 14918, 14918,
    14168, 14168, 14168,
    12686, 12686, 12686,
    13392, 13392, 13392
])

autoai_predicted = np.array([
    14045.89870796, 14103.37515036, 14114.49594719,
    14516.96512213, 14625.04666821, 14620.06071729,
    14506.19129140, 14482.11201184, 14514.63391345,
    14756.63297095, 14859.81714626, 14843.14453241
])

# === Step 2: Load Prophet forecast from CSV ===
prophet_df = pd.read_csv("forecasted_permits_2024.csv", parse_dates=["Month"])
prophet_df = prophet_df.sort_values("Month").reset_index(drop=True)
prophet_predicted = prophet_df["Forecasted_Dwellings"].values[:12]

# === Step 3: Evaluate Metrics ===
def evaluate(predicted, actual):
    mae = np.mean(np.abs(predicted - actual))
    mape = np.mean(np.abs((predicted - actual) / actual)) * 100
    smape = np.mean(2 * np.abs(predicted - actual) / (np.abs(predicted) + np.abs(actual))) * 100
    return mae, mape, smape

mae_ibm, mape_ibm, smape_ibm = evaluate(autoai_predicted, actual_values)
mae_prophet, mape_prophet, smape_prophet = evaluate(prophet_predicted, actual_values)

# === Step 4: Print Metrics ===
print("Forecast Accuracy for 2024:")
print(f"[IBM AutoAI]     MAE: {mae_ibm:.2f}, MAPE: {mape_ibm:.2f}%, SMAPE: {smape_ibm:.2f}%")
print(f"[Prophet]        MAE: {mae_prophet:.2f}, MAPE: {mape_prophet:.2f}%, SMAPE: {smape_prophet:.2f}%")

# === Step 5: Plot Comparison ===
months_2024 = pd.date_range(start="2024-01-01", periods=12, freq="MS")
df_plot = pd.DataFrame({
    "Month": months_2024,
    "Actual": actual_values,
    "IBM AutoAI": autoai_predicted,
    "Prophet": prophet_predicted
})

plt.figure(figsize=(10, 5))
plt.plot(df_plot["Month"], df_plot["Actual"], marker='o', label="Actual", linewidth=2)
plt.plot(df_plot["Month"], df_plot["IBM AutoAI"], marker='x', linestyle='--', label="IBM AutoAI", linewidth=2)
plt.plot(df_plot["Month"], df_plot["Prophet"], marker='s', linestyle='--', label="Prophet", linewidth=2)
plt.title("Monthly Building Permits: Actual vs Forecasts (2024)")
plt.xlabel("Month")
plt.ylabel("Number of Dwellings")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
