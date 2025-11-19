# backend/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .excel_loader import get_area_data
from .utils import extract_areas, generate_summary, build_chart_data, make_json_safe
import pandas as pd

@api_view(['POST'])
def analyze_query(request):
    query = request.data.get('query', '').strip()
    if not query:
        return Response({"summary": "Please send a query", "chart": [], "tables": {}, "areas": []})

    areas = extract_areas(query)
    data_dict = {}
    for area in areas:
        df = get_area_data(area)
        if not df.empty:
            data_dict[area] = df

    if not data_dict:
        return Response({
            "summary": "❌ No data found for that area.\n\nAvailable areas:\n• Wakad\n• Aundh\n• Akurdi\n• Ambegaon Budruk",
            "chart": [],
            "tables": {},
            "areas": []
        })

    summary = generate_summary(list(data_dict.keys()), data_dict)
    chart = build_chart_data(list(data_dict.keys()), data_dict)

    # Convert DataFrames to plain Python types and replace NaN/NaT with None
    tables = {
        area: df.where(pd.notna(df), None).to_dict(orient="records")
        for area, df in data_dict.items()
    }

    response_data = {
        "summary": summary,
        "chart": chart,
        "tables": tables,
        "areas": list(data_dict.keys()),
    }

    # Ensure everything in the response is JSON-serializable (no NaN/inf or numpy types)
    return Response(make_json_safe(response_data))
