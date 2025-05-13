# ext-data-forecast

**External data and scripts to support forecasting and predictive modeling.**

This repository contains reusable code and datasets to generate features for forecasting tasks using external, publicly available data — starting with holiday-based features for Italy.

---

## 📁 Contents

- `get-it-holidays.py`  
  Generates Italian holidays for 2023–2025 using the `holidays` package and classifies them as Religious or Civil.

- `generate-holiday-features.py`  
  Aggregates holiday data into monthly features like counts and binary indicators (e.g., any/civil/religious holidays).

- `italy_holidays.csv`  
  Output from `get-it-holidays.py` — holiday names and types.

- `italy_monthly_holiday_features.csv`  
  Output from `generate-holiday-features.py` — monthly holiday features for modeling.

---

## 📦 Dependencies

- `pandas`
- `holidays`

Install them with:

```bash
pip install pandas holidays
