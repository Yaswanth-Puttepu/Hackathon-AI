from fastapi import APIRouter
from app.models.brief import CampaignBrief
from app.services.planner_service import generate_plan

router = APIRouter()

@router.post("/brief")
async def create_brief(brief: CampaignBrief):
    """
    Endpoint to receive a campaign brief and return a generated execution plan.
    """
    plan = generate_plan(brief)
    
    return {
        "message": "Brief processed successfully",
        "brief": brief,
        "plan": plan
    }
