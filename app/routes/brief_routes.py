from fastapi import APIRouter
from app.models.brief import CampaignBrief

router = APIRouter()

@router.post("/brief")
async def create_brief(brief: CampaignBrief):
    """
    Endpoint to receive a campaign brief and return a confirmation.
    """
    return {
        "message": "Brief received successfully",
        "data": brief
    }
