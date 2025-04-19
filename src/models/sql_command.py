from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SQLCommand(BaseModel):
    """Represents the SQL command(s) that implement a business recommendation."""
    sql: str = Field(..., description="The SQL command to execute ONLY, do not include any other text")
    action: str = Field(..., description="Natural language description of what the SQL command does")
    action_type: str = Field(..., description="Type of the operation to be performed")
    target: str = Field(..., description="The primary table or entity being modified")
    preview: Optional[str] = Field(None, description="Preview of the changes that will be made")