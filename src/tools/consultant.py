from agno.tools import tool
from typing import Optional

from src.tasks.consulting.consulte import date_range, get_token, fetch_dashboard_stats, fetch_order_status, fetch_general_stats, fetch_top_sales, fetch_order_analytics

@tool
def competitor_analysis_tool(business_data: Optional[dict] = None) -> dict:
    token = get_token()

    this_start, today         = date_range("week")
    last_start, last_end      = date_range(14)           # 8‑14 days ago

    this_week = {
        "dashboard":   fetch_dashboard_stats(token),
        "order_stats": fetch_order_status(token),
        "general":     fetch_general_stats(token, this_start, today),
        "top_sales":   fetch_top_sales(token,  this_start, today),
        "orders_tl":   fetch_order_analytics(token),
    }
    last_week = {
        "general":     fetch_general_stats(token, last_start, last_end),
        "top_sales":   fetch_top_sales(token,  last_start, last_end),
    }

    return {
        "json_data": {
            "this_week":     this_week,
            "last_week":     last_week,
            "business_data": business_data or {},
            "meta": {
                "this_week_start": this_start,
                "last_week_start": last_start,
                "today": today,
            },
        }
    }