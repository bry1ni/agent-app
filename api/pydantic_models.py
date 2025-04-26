from pydantic import BaseModel, Field

class Query(BaseModel):
    query: str = Field(..., description="The query to be answered")

class Answer(BaseModel):
    answer: str = Field(..., description="The answer to the query")

