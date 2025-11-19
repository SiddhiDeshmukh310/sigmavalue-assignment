# backend/api/utils.py
import math

import numpy as np
import pandas as pd

def _clean_numeric(val):
    if pd.isna(val) or val in ["", "-", None]:
        return 0.0
    try:
        return float(str(val).replace(",", "").replace("₹", "").strip())
    except:
        return 0.0


def extract_areas(query: str):
    q = query.lower().strip()

    found = set()

    if "wakad" in q:
        found.add("Wakad")
    if "aundh" in q:
        found.add("Aundh")
    if "akurdi" in q or "chinchwad" in q:
        found.add("Akurdi")
    if any(x in q for x in ["ambegaon", "ambegao", "ambegaon budruk", "ambegaonbk", "ambegaon bk"]):
        found.add("Ambegaon Budruk")

    found_list = list(found)

    # 🏆 Best-investment query keywords
    best_keywords = ["best", "investment", "top", "winner", "highest", "good investment"]

    # 🔥 FIX: ANY best-investment query → return all areas
    if any(k in q for k in best_keywords):
        return ["Wakad", "Aundh", "Akurdi", "Ambegaon Budruk"]

    # Compare query or multiple areas mentioned
    if "compare" in q or len(found_list) > 1:
        return found_list or ["Wakad", "Aundh", "Akurdi", "Ambegaon Budruk"]

    # Single-area analysis
    if len(found_list) == 1:
        return found_list

    # Generic real estate question → default to all areas
    if any(w in q for w in ["area", "pune", "rate", "price", "property", "analysis", "analyze", "flat"]):
        return ["Wakad", "Aundh", "Akurdi", "Ambegaon Budruk"]

    return []



# Keep the rest exactly as before — they were already perfect
def generate_summary(areas, data_dict):
    if not areas:
        return "No data found for that area.\n\nAvailable areas:\n• Wakad\n• Aundh\n• Akurdi\n• Ambegaon Budruk"

    if len(areas) >= 3:  # best investment mode
        summary = "**Best Investment Area (2020–2024)**\n\n"
        best_area = None
        best_growth = -999
        for area in areas:
            df = data_dict[area]
            p2020 = _clean_numeric(df[df["year"] == 2020]["flat - weighted average rate"].iloc[0])
            p2024 = _clean_numeric(df[df["year"] == 2024]["flat - weighted average rate"].iloc[0])
            growth = round((p2024 - p2020) / p2020 * 100, 1) if p2020 > 0 else 0
            units = int(_clean_numeric(df["total sold - igr"].sum()))
            summary += f"• **{area}**: +{growth}% growth | {units:,} units sold\n"
            if growth > best_growth:
                best_growth = growth
                best_area = area
        summary += f"\n🏆 **WINNER: {best_area}** (+{best_growth}%)\nStrong demand & highest returns!"
        return summary

    if len(areas) == 1:
        area = areas[0]
        df = data_dict[area]
        p2020 = _clean_numeric(df[df["year"] == 2020]["flat - weighted average rate"].iloc[0])
        p2024 = _clean_numeric(df[df["year"] == 2024]["flat - weighted average rate"].iloc[0])
        growth = round((p2024 - p2020) / p2020 * 100, 1)
        units = int(_clean_numeric(df["total sold - igr"].sum()))
        return f"**{area} – 2020-2024**\n\n📈 Price: ₹{int(p2020):,} → ₹{int(p2024):,}/sqft (+{growth}%)\n🏗️ Units sold: {units:,}\n\nVery strong growth!"

    # Comparison (2 areas)
    summary = "**Comparison**\n\n"
    best, best_g = None, -999
    for area in areas:
        df = data_dict[area]
        p2020 = _clean_numeric(df[df["year"] == 2020]["flat - weighted average rate"].iloc[0])
        p2024 = _clean_numeric(df[df["year"] == 2024]["flat - weighted average rate"].iloc[0])
        growth = round((p2024 - p2020) / p2020 * 100, 1)
        units = int(_clean_numeric(df["total sold - igr"].sum()))
        summary += f"• {area}: +{growth}% | {units:,} units\n"
        if growth > best_g:
            best_g = growth
            best = area
    summary += f"\n🏆 **Best: {best}** (+{best_g}%)"
    return summary


def build_chart_data(areas, data_dict):
    chart = []
    for year in [2020, 2021, 2022, 2023, 2024]:
        entry = {"year": str(year)}
        for area in areas:
            df = data_dict.get(area, pd.DataFrame())
            row = df[df["year"] == year]
            price = int(_clean_numeric(row["flat - weighted average rate"].iloc[0])) if not row.empty else 0
            units = int(_clean_numeric(row["total sold - igr"].iloc[0])) if not row.empty else 0
            entry[f"{area} Price"] = price
            entry[f"{area} Units"] = units
        chart.append(entry)
    return chart


def make_json_safe(obj):
    """Recursively convert NaN/inf and numpy types to JSON-safe Python types."""
    # Handle numpy scalar types first
    if isinstance(obj, (np.generic,)):
        obj = obj.item()

    # Primitives
    if obj is None or isinstance(obj, (str, bool, int)):
        return obj

    if isinstance(obj, float):
        # Replace NaN/inf with None
        if not math.isfinite(obj):
            return None
        return obj

    # Containers
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [make_json_safe(v) for v in obj]

    # Fallback for other numpy / pandas objects: convert to string
    return str(obj)
