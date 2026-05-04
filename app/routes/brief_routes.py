from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from app.models.brief import CampaignBrief
# 👇 FIX: Imported the new refine_plan function here
from app.services.planner_service import generate_plan, refine_plan 
from app.services.qa_service import run_qa_agent, generate_llm_fix_plan

router = APIRouter()

# -----------------
# DIRECTION 1: PLANNER
# -----------------
@router.post("/generate-plan")
async def api_generate_plan(brief: CampaignBrief):
    """Takes a campaign brief and generates an execution plan + clarifying questions."""
    plan = generate_plan(brief)
    return {"status": "success", "data": plan}

# 👇 NEW: Data model for the Refinement API request
class RefineRequest(BaseModel):
    original_brief: Dict[str, Any]
    refinements: Dict[str, str]

# 👇 NEW: The endpoint that connects the UI's Magic Button to the AI Brain
@router.post("/refine-plan")
async def api_refine_plan(payload: RefineRequest):
    """Takes the original brief and human clarifications to finalize the plan."""
    final_plan = refine_plan(payload.original_brief, payload.refinements)
    return {"status": "success", "data": final_plan}

# -----------------
# DIRECTION 2: QA AGENT
# -----------------
class QARequest(BaseModel):
    brief: Dict[str, Any]
    plan: Dict[str, Any]

@router.post("/qa-plan")
async def api_qa_plan(payload: QARequest):
    """Evaluates an existing plan against a brief and generates a fix if needed."""
    qa_results = run_qa_agent(payload.brief, payload.plan)
    
    response_data = {"qa_evaluation": qa_results}
    
    # If there are issues, generate a fixed plan automatically
    if qa_results.get("issues") and qa_results.get("score", 100) < 100:
        fixed_plan = generate_llm_fix_plan(payload.brief, payload.plan, qa_results["issues"])
        response_data["fixed_plan"] = fixed_plan
        
    return {"status": "success", "data": response_data}