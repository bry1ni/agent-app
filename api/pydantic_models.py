from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Delivery(BaseModel):
    delivery_id: str = Field(..., description="Unique identifier for the delivery")
    order_id: str = Field(..., description="Reference to the associated order")
    customer_id: str = Field(..., description="ID of the customer receiving the delivery")
    delivery_date: datetime = Field(..., description="Scheduled delivery date")
    delivery_address: str = Field(..., description="Shipping address for the delivery")
    status: str = Field(..., description="Current status of the delivery (e.g., 'pending', 'in_transit', 'delivered')")
    items: List[str] = Field(..., description="List of product IDs in this delivery")
    delivery_notes: Optional[str] = Field(None, description="Additional notes about the delivery")

class OrderedDeliveryList(BaseModel):
    date: datetime = Field(..., description="Date for which deliveries are scheduled")
    deliveries: List[Delivery] = Field(..., description="List of deliveries scheduled for this date")
    total_deliveries: int = Field(..., description="Total number of deliveries for this date")
    status: str = Field(..., description="Overall status of the delivery list (e.g., 'pending', 'in_progress', 'completed')")
    priority_zone: Optional[str] = Field(None, description="Priority delivery zone for this list")

class BusinessData(BaseModel):
    last_month_revenue: str = Field(..., description="Progress on last month revenue")

class Recommendation(BaseModel):
    """Represents a business recommendation that needs to be implemented in the database."""
    id: Optional[str] = None
    description: str = Field(..., description="Natural language description of the recommendation")
    target_table: str = Field(..., description="The primary table affected by this recommendation")
    additional_context: Optional[dict] = None

class ConsultationOutput(BaseModel):
    summary_report: str = Field(..., description="Summary of the consultation's report content")
    recommendations: List[Recommendation] = Field(..., description="List of TODO recommendation")

class SQLCommand(BaseModel):
    """Represents the SQL command(s) that implement a business recommendation."""
    recommendation_id: Optional[str] = None
    sql: str = Field(..., description="The SQL command to execute")
    pre_checks: Optional[List[str]] = None  # Optional verification queries to run before
    post_checks: Optional[List[str]] = None  # Optional verification queries to run after
    use_transaction: bool = True
    created_at: datetime = Field(default_factory=datetime.now)