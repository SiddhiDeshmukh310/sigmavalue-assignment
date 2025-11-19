import os
import pandas as pd
from django.conf import settings

EXCEL_PATH = os.path.join(settings.BASE_DIR, "data", "realestate.xlsx")

if os.path.exists(EXCEL_PATH):
    df = pd.read_excel(EXCEL_PATH, engine='openpyxl')
    df.columns = [col.strip().replace('\n', ' ') for col in df.columns]
    df["final location"] = df["final location"].astype(str).str.strip()
    print("Excel loaded! Areas:", df["final location"].unique())
else:
    df = pd.DataFrame()
    print("Excel file not found at:", EXCEL_PATH)

def get_area_data(area: str):
    if df.empty:
        return pd.DataFrame()
    mask = df["final location"].str.contains(area, case=False, na=False)
    return df[mask].copy()