"""
Title: Generate Italian Public Holidays (2023-2025)

Description:
    Generates official public holidays in Italy for the years 2023–2025 using the `holidays` package.
    Classifies each holiday as 'Religious', 'Civil', or 'Unknown' based on keyword matching.
    Outputs a structured CSV file with date, holiday name, and classification.

Output:
    - italy_holidays.csv: A CSV file with columns [Date, Holiday, Type].
"""


import holidays
import pandas as pd

# Generate Italian holidays for 2023 to 2025
it_holidays = holidays.country_holidays('IT', years=[2023, 2024, 2025])

# Convert to DataFrame
holiday_df = pd.DataFrame(list(it_holidays.items()), columns=['Date', 'Holiday'])

# Sort by date
holiday_df = holiday_df.sort_values(by='Date').reset_index(drop=True)

# Define classification rules
religious_keywords = [
    "Epifania", "Pasqua", "Angelo", "Assunzione", 
    "Tutti i Santi", "Immacolata", "Natale", "Santo Stefano"
]
civil_keywords = [
    "Capodanno", "Liberazione", "Lavoratori", "Repubblica"
]

# Function to classify the holiday type
def classify_holiday(name):
    if any(word in name for word in religious_keywords):
        return "Religious"
    elif any(word in name for word in civil_keywords):
        return "Civil"
    else:
        return "Unknown"

# Apply classification
holiday_df["Type"] = holiday_df["Holiday"].apply(classify_holiday)

# Save to CSV
holiday_df.to_csv('italy_holidays.csv', index=False)

print("Saved: italy_holidays.csv")
