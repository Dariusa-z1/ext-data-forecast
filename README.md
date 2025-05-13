# ext-data-forecast

Developed as part of the **IBM watsonx Gen AI Challenge 2025** — a cross-university course focused on solving real-world business problems. Students worked in teams to build end-to-end solutions using AI tools and cloud services, combining academic knowledge with hands-on development.

---

## 📌 Overview

**ext-data-forecast** is a growing repository of external data sources and feature engineering scripts designed to support time series forecasting and predictive modeling.

The project currently includes tools to process and classify holidays in Italy and generate features for forecasting models.

---

## 📁 Contents

- `get-it-holidays.py`  
  Generates Italian holidays for 2023–2025 using the `holidays` package and classifies them as *Religious*, *Civil*, or *Unknown*.

- `generate-holiday-features.py`  
  Aggregates holiday data into monthly features (e.g., counts, binary indicators) for modeling.

- `italy_holidays.csv`  
  Generated holiday list with classification.

- `italy_monthly_holiday_features.csv`  
  Aggregated monthly features including total number of holidays and holiday type indicators.

---

## 📦 Dependencies

Install required Python packages:

```bash
pip install pandas holidays
```

---

## 🚀 Usage

1. Generate holidays and classify them:
   ```bash
   python get-it-holidays.py
   ```

2. Aggregate into monthly features:
   ```bash
   python generate-holiday-features.py
   ```

CSV outputs will be saved in the project directory.

---

## 🛠️ Roadmap

Planned future additions:

- Weather-based feature extraction
- Economic indicators and sentiment data
- External event calendars

---

## 🤝 Contributing

Pull requests, suggestions, and improvements are welcome!
