import json

from typing import List, Tuple, Union
from datetime import datetime
from agno.agent import RunResponse

from src.agents.utils import extract_response_from_agent
from api.pydantic_models import BusinessData, ConsultationOutput, StoreAnalyticsSchema
from src.agents.consultant import consultant
from src.tools.utils import render_email, send as send_mail, split_recs_and_tasks
from src.tools.consultant import competitor_analysis_tool  

DASHBOARD_URL = "https://dashboard.ayorservices.com"


def analytics_to_insights(a: dict) -> List[Tuple[str, str]]:
    insights: List[Tuple[str, str]] = []

    try:
        cur_orders = a["dashboard_stats"]["order_count"]
        cur_rev    = a["dashboard_stats"]["revenue"]
        prev_orders = a["general_stats"]["prev_order_count"]
        prev_rev    = a["general_stats"]["prev_revenue"]

        order_delta = (cur_orders - prev_orders) / max(prev_orders, 1) * 100
        rev_delta   = (cur_rev    - prev_rev)    / max(prev_rev,    1) * 100

        insights.append((
            f"Orders up **{order_delta:.0f} %** but revenue only **{rev_delta:+.0f} %**",
            "Raise AOV by nudging hoodie price to €49" if order_delta > rev_delta else
            "Monitor pricing — revenue is keeping pace with orders"
        ))

        if "conversion_rate" in a["general_stats"]:
            conv = a["general_stats"]["conversion_rate"]
            if conv < 0.02:
                insights.append((
                    f"Conversion rate is only **{conv*100:.1f} %**",
                    "Add urgency banner to /home to boost conversions"
                ))

    except KeyError:
        insights.append(("Could not parse analytics JSON", "Review API payload"))

    return insights

async def consulte(request: Union[StoreAnalyticsSchema, dict]) -> ConsultationOutput:
    """
    1. Pass merchant‑supplied business data to the agent
    (the agent will call competitor_analysis_tool to fetch KPIs).
    2. Post‑process the response to produce an HTML+TXT email.
    """
    analytics_data = request

    # Simplify analytics data for the agent
    simplified_data = {
        "current_period": {
            "orders": analytics_data["dashboard_stats"]["order_count"],
            "revenue": analytics_data["dashboard_stats"]["revenue"],
            "order_change": analytics_data["dashboard_stats"]["order_percentage_change"],
            "revenue_change": analytics_data["dashboard_stats"]["revenue_percentage_change"]
        },
        "order_status": {
            "pending": analytics_data["order_status"]["status_pending"],
            "confirmed": analytics_data["order_status"]["status_confirmed"],
            "cancelled": analytics_data["order_status"]["status_cancelled"]
        },
        "time_period": analytics_data["time_period"]
    }

    response = consultant.run(simplified_data)

    result = extract_response_from_agent(response, "consultant")
    output = ConsultationOutput(**result)
      
    clean_recs, tasks_json_line = split_recs_and_tasks(output.recommendations)
    output.recommendations = clean_recs   

    insight_table = [
        ("Current Period Revenue", f"${analytics_data['dashboard_stats']['revenue']}"),
        ("Order Change", f"{analytics_data['dashboard_stats']['order_percentage_change']}%"),
        ("Revenue Change", f"{analytics_data['dashboard_stats']['revenue_percentage_change']}%")
    ]
    
    html_body, text_body = render_email(
        first_name="Patrick",
        insight_table=insight_table,
        recs=clean_recs,
        dashboard_url=DASHBOARD_URL,
        tasks_line=tasks_json_line,
    )
    
    print(f"Consultation output: {output}")
    print(f"Recommendations: {output.recommendations}")
    print(f"Summary report: {output.summary_report}")   

    return output