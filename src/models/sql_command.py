from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SQLCommand(BaseModel):
    """Represents the SQL command(s) that implement a business recommendation."""
    sql: str = Field(..., description="The SQL command to execute ONLY, do not include any other text")