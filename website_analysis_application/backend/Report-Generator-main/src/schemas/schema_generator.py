from pydantic import BaseModel, Field


class GenerateReportRequest(BaseModel):
    url: str = Field(default="https://www.berkshirehathaway.com/")
