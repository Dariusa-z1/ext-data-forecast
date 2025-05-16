import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === Actual and predicted values for each month in 2024 ===
actual_values = np.array([
    14918, 14918, 14918,
    14168, 14168, 14168,
    12686, 12686, 12686,
    13392, 13392, 13392
])

predicted_values = np.array([
    14045.89870796, 14103.37515036, 14114.49594719,
    14516.96512213, 14625.04666821, 14620.06071729,
    14506.19129140, 14482.11201184, 14514.63391345,
    14756.63297095, 14859.81714626, 14843.14453241
])

# === Calculate Metrics ===
mae = np.mean(np.abs(predicted_values - actual_values))
mape = np.mean(np.abs((predicted_values - actual_values) / actual_values)) * 100
smape = np.mean(2 * np.abs(predicted_values - actual_values) / (np.abs(predicted_values) + np.abs(actual_values))) * 100

print("Forecast Accuracy for 2024:")
print(f"MAE: {mae:.2f} permits")
print(f"MAPE: {mape:.2f}%")
print(f"SMAPE: {smape:.2f}%")

# === Visualization ===
months_2024 = pd.date_range(start="2024-01-01", periods=12, freq="MS")
df_plot = pd.DataFrame({
    "Month": months_2024,
    "Actual": actual_values,
    "Predicted": predicted_values
})

plt.figure(figsize=(10, 5))
plt.plot(df_plot["Month"], df_plot["Actual"], marker='o', label="Actual", linewidth=2)
plt.plot(df_plot["Month"], df_plot["Predicted"], marker='x', linestyle='--', label="Predicted", linewidth=2)
plt.title("Monthly Building Permits: Actual vs Predicted by IBM AutoAI (2024)")
plt.xlabel("Month")
plt.ylabel("Number of Dwellings")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
