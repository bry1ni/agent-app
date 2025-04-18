import json

from typing import List, Tuple
from datetime import datetime
from agno.agent import RunResponse

from api.pydantic_models import BusinessData, ConsultationOutput
from src.agents.consultant import consultant
from src.tools.utils import render_email, send as send_mail, split_recs_and_tasks
from src.tools.consultant import competitor_analysis_tool  

DASHBOARD_URL = "https://app.ayor.com/agents/executor?run=latest"


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
            f"Orders up **{order_delta:.0f} %** but revenue only **{rev_delta:+.0f} %**",
            "Raise AOV by nudging hoodie price to €49" if order_delta > rev_delta else
            "Monitor pricing — revenue is keeping pace with orders"
        ))

        if "conversion_rate" in a["general_stats"]:
            conv = a["general_stats"]["conversion_rate"]
            if conv < 0.02:
                insights.append((
                    f"Conversion rate is only **{conv*100:.1f} %**",
                    "Add urgency banner to /home to boost conversions"
                ))

    except KeyError:
        insights.append(("Could not parse analytics JSON", "Review API payload"))

    return insights


DASHBOARD_URL = "https://dashboard.ayorservices.com"

async def consulte(request: BusinessData) -> ConsultationOutput:
    """
    1. Pass merchant‑supplied business data to the agent
    (the agent will call competitor_analysis_tool to fetch KPIs).
    2. Post‑process the response to produce an HTML+TXT email.
    """
    run_resp: RunResponse = consultant.run(
    business_data=request.model_dump(mode="json")
    )

    output: ConsultationOutput = run_resp.content
    clean_recs, tasks_json_line = split_recs_and_tasks(output.recommendations)
    output.recommendations = clean_recs   

    insight_table = [("Last‑month revenue", request.last_month_revenue)]
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

    clean_recs, tasks_json_line = split_recs_and_tasks(output.recommendations)

    insight_table: List[Tuple[str, str]] = [
        ("Last‑month revenue", request.last_month_revenue),
    ]

    html_body, text_body = render_email(
        first_name="Patrick",                    
        insight_table=insight_table,
        recs=clean_recs,
        dashboard_url=DASHBOARD_URL,
        tasks_line=tasks_json_line,
    )

    output.email_template = html_body
    return output