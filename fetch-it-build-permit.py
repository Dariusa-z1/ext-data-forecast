"""
Script to download, process, and engineer features from ISTAT's SDMX API on new dwelling permits.
Final output is a monthly-aligned time series dataset with engineered indicators.
Data source: https://esploradati.istat.it/databrowser/#/en/dw/categories/IT1,Z0600IND,1.0/DCSC_PERM_RAP1/IT1,111_111_DF_DCSC_PERM_RAP1_1,1.0
"""

import requests
import pandas as pd
from lxml import etree

# === Step 1: API Request ===
# Define the ISTAT SDMX endpoint URL for construction permits dataset
sdmx_url = (
    "https://esploradati.istat.it/SDMXWS/rest/data/"
    "IT1,111_111_DF_DCSC_PERM_RAP1_1,1.0/all/ALL/"
    "?detail=full&startPeriod=2023-09-01&endPeriod=2024-12-31"
    "&dimensionAtObservation=TIME_PERIOD"
)
# Make the HTTP GET request to the ISTAT SDMX API
response = requests.get(sdmx_url)
raw_xml = response.content # Get raw XML response


# === Step 2: Parse and Filter XML ===
# Parse XML content using lxml and extract relevant data points
root = etree.fromstring(raw_xml)
ns = {"generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}

data = []
# Loop through all Series elements
for series in root.findall(".//generic:Series", namespaces=ns):
    keys = {el.attrib["id"]: el.attrib["value"] for el in series.find("generic:SeriesKey", namespaces=ns)}
    if keys.get("DATA_TYPE") == "NUMDW" and keys.get("ADJUSTMENT") == "N":
        for obs in series.findall("generic:Obs", namespaces=ns):
            time = obs.find("generic:ObsDimension", namespaces=ns).attrib["value"]
            value = int(obs.find("generic:ObsValue", namespaces=ns).attrib["value"])
            data.append((time, value))

# Create DataFrame from extracted data
df = pd.DataFrame(data, columns=["Quarter", "Dwellings"]).sort_values("Quarter")

# === Step 3: Feature Engineering ===
# Convert 'Quarter' to datetime format
# Map quarters to starting months
quarter_to_month = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}
df["Quarter"] = pd.to_datetime(
    df["Quarter"].str.replace(r"(Q[1-4])", lambda m: quarter_to_month[m.group(1)], regex=True),
    format="%Y-%m"
)

# Add lag features and indicators
df["permits_lag1"] = df["Dwellings"].shift(1) # Previous quarter's value
df["permits_change"] = df["Dwellings"].diff() # Absolute change
df["permits_pct_change"] = df["Dwellings"].pct_change() # Percentage change
df["permits_rolling2"] = df["Dwellings"].rolling(2).mean() # Rolling average (2 quarters)
df["is_growth_quarter"] = (df["permits_change"] > 0).astype(int) # Binary growth indicator

# === Step 4: Convert to Monthly Format (for time series alignment) ===
# Generate monthly date range covering the same time span
monthly = pd.DataFrame({"Month": pd.date_range(df["Quarter"].min(), df["Quarter"].max() + pd.offsets.QuarterEnd(0), freq="MS")})

# Map each month to its corresponding quarter's start date
monthly["Quarter"] = monthly["Month"].dt.to_period("Q").dt.start_time

# Merge quarterly features into monthly dataframe and forward-fill
monthly = monthly.merge(df, on="Quarter", how="left").drop(columns=["Quarter"])
monthly = monthly.ffill()

# === Step 5: Save Final Dataset ===
monthly.to_csv("monthly_demand_features_from_istat.csv", index=False)
print(monthly.head(12))
