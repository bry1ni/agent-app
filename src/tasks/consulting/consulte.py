from datetime import date, timedelta
import requests
from typing import Union, Tuple, Optional

from api.pydantic_models import StoreAnalyticsSchema
from src.tasks import API_BASE, EMAIL_AUTH, PASSWORD_AUTH, SHOP_ID
from src.tasks.utils import auth_hdr, get_token

def date_range(period: Union[str, int] = "week") -> Tuple[str, str]:
    """Return (start, end) ISO strings for the given period.

    • "week"  → last 7 full days (Mon‑Sun style)
    • "month" → last 30 days
    • int     → that many days back from today
    """
    today = date.today()
    if period == "week":
        delta = timedelta(days=7)
    elif period == "month":
        delta = timedelta(days=30)
    elif isinstance(period, int):
        delta = timedelta(days=period)
    else:
        raise ValueError("period must be 'week', 'month', or an int")
    start = today - delta
    return start.isoformat(), today.isoformat()

# ---------- fetchers -------------------------------------------------

def fetch_dashboard_stats(token: str):
    url = f"{API_BASE}/api/shops/{SHOP_ID}/dashboard-stats/"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def fetch_order_status(token: str):
    url = f"{API_BASE}/api/shops/{SHOP_ID}/order-status-count/"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def fetch_general_stats(token: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    if not (start_date and end_date):
        start_date, end_date = date_range("week")
    url = f"{API_BASE}/api/shops/{SHOP_ID}/analytics/general-stats/?start_date={start_date}&end_date={end_date}"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def fetch_top_sales(token: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    if not (start_date and end_date):
        start_date, end_date = date_range("week")
    url = f"{API_BASE}/api/shops/{SHOP_ID}/analytics/top-sales/?start_date={start_date}&end_date={end_date}"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def fetch_order_analytics(token: str):
    url = f"{API_BASE}/api/shops/{SHOP_ID}/analytics/orders/"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def get_complete_analytics(token: str = get_token(), period: Union[str, int] = "week") -> StoreAnalyticsSchema:
    """Fetch all analytics data and return in a structured format.
    
    Args:
        token: Authentication token
        period: Time period for analysis ("week", "month", or number of days)
    
    Returns:
        Complete analytics data in a structured format
    """
    # Get date range
    start_date, end_date = date_range(period)
    
    # Fetch all data
    dashboard = fetch_dashboard_stats(token)
    order_status = fetch_order_status(token)
    general_stats = fetch_general_stats(token, start_date, end_date)
    top_sales = fetch_top_sales(token, start_date, end_date)
    order_analytics = fetch_order_analytics(token)
    
    # Assemble complete response
    return {
        "dashboard_stats": dashboard,
        "order_status": order_status,
        "general_stats": general_stats,
        "top_sales": top_sales,
        "order_analytics": order_analytics,
        "time_period": {
            "start_date": start_date,
            "end_date": end_date
        }
    }