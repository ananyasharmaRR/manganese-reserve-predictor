"""
generate_data.py
-----------------
WHAT THIS FILE DOES:
Creates a sample dataset that looks like it came from combining:
  1. Satellite data (vegetation index, soil moisture, land temperature)
  2. Mine production records (ore extracted, equipment downtime, blasting delays)

WHY WE'RE DOING THIS:
In a real MOIL deployment, satellite numbers would come live from Google Earth
Engine, and production numbers would come from MOIL's internal systems. Neither
of those is available to us in a hackathon. So we generate realistic sample data
based on the REAL locations of MOIL's actual mines and REAL ranges these
satellite indices take in nature. This is a completely normal and accepted
hackathon practice -- explain this openly to judges, don't hide it. It shows
you understood the data pipeline even without having access to the real feeds.

HOW TO RUN THIS FILE:
In your terminal, inside this project folder, type:
    python generate_data.py
It will create a file at: data/manganese_data.csv
"""

import numpy as np
import pandas as pd

# Setting a "seed" makes the random numbers reproducible -- if you run this
# script again, you get the exact same data. Useful so your results don't
# change randomly right before your presentation.
np.random.seed(42)

# ---------------------------------------------------------------------------
# STEP 1: Define real MOIL mine locations (these are real, public coordinates)
# ---------------------------------------------------------------------------
MINES = [
    {"name": "Balaghat Mine",   "lat": 21.8046, "lon": 80.1867},
    {"name": "Nagpur Mine",     "lat": 21.1458, "lon": 79.0882},
    {"name": "Ukwa Mine",       "lat": 21.4478, "lon": 79.9040},
    {"name": "Gumgaon Mine",    "lat": 21.0350, "lon": 79.2500},
]

N_DAYS = 365          # one year of daily records
records = []

for mine in MINES:
    # Each mine gets its own "baseline" ore output so mines don't look identical
    base_output = np.random.uniform(180, 260)   # tons/day baseline

    for day in range(N_DAYS):
        # --- Simulated satellite indices ---
        # NDVI (vegetation index) realistically ranges -1 to 1; bare mining
        # land usually sits low, around 0.1 to 0.4
        vegetation_index = np.clip(np.random.normal(0.25, 0.08), -1, 1)

        # Soil moisture as a percentage (0-100)
        soil_moisture = np.clip(np.random.normal(22, 6), 0, 100)

        # Land surface temperature in Celsius (central India ranges roughly 15-45C)
        land_temperature = np.clip(np.random.normal(29, 6), 10, 48)

        # --- Simulated operational data ---
        equipment_downtime_hours = max(0, np.random.exponential(1.5))
        blasting_delay_hours = max(0, np.random.exponential(1.0))
        # Heavy rain (high soil moisture) tends to cause more weather delays
        weather_delay_hours = max(0, np.random.exponential(0.5 + soil_moisture / 60))

        # --- The "answer" we want our AI to learn to predict ---
        # More downtime/delays => lower ore output. This mimics a real
        # cause-and-effect relationship the model can actually learn.
        disruption_penalty = (
            equipment_downtime_hours * 6
            + blasting_delay_hours * 4
            + weather_delay_hours * 5
        )
        ore_extracted_tons = max(
            0, base_output - disruption_penalty + np.random.normal(0, 8)
        )

        # A day counts as a "shortfall risk" if output drops more than 20%
        # below that mine's baseline -- this becomes our risk label
        shortfall_flag = int(ore_extracted_tons < 0.8 * base_output)

        records.append({
            "date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=day),
            "mine_name": mine["name"],
            "latitude": mine["lat"],
            "longitude": mine["lon"],
            "vegetation_index": round(vegetation_index, 3),
            "soil_moisture_pct": round(soil_moisture, 2),
            "land_temperature_c": round(land_temperature, 2),
            "equipment_downtime_hours": round(equipment_downtime_hours, 2),
            "blasting_delay_hours": round(blasting_delay_hours, 2),
            "weather_delay_hours": round(weather_delay_hours, 2),
            "ore_extracted_tons": round(ore_extracted_tons, 2),
            "shortfall_flag": shortfall_flag,
        })

df = pd.DataFrame(records)
df.to_csv("data/manganese_data.csv", index=False)

print(f"Done! Created data/manganese_data.csv with {len(df)} rows "
      f"across {len(MINES)} mines.")
print(df.head(3).to_string(index=False))
