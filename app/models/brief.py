from pydantic import BaseModel
from typing import List, Optional

class CampaignBrief(BaseModel):
    """
    Model representing a marketing campaign brief.
    """
    campaign_name: str
    business_objective: str
    target_audience: str
    key_message: str
    channels: List[str]
    budget: Optional[str] = None
    timeline: str
    success_metrics: str
    constraints: str
