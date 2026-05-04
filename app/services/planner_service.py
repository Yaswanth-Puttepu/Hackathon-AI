import os
import json
from openai import AzureOpenAI
from app.models.brief import CampaignBrief

def get_azure_client():
    # Helper to initialize Azure OpenAI client
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not all([api_key, endpoint, deployment_name, api_version]):
        raise ValueError("Missing Azure OpenAI configuration in .env file.")

    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version
    )
    return client, deployment_name

def generate_plan(brief: CampaignBrief) -> dict:
    try:
        client, deployment_name = get_azure_client()

        # 🔥 The Prompt: Notice how we explicitly ask it to find missing info
        prompt = f"""
You are an expert Marketing Campaign Manager. Your task is to take an aspirational campaign brief and convert it into a structured, launch-ready execution plan.

CRITICAL INSTRUCTIONS:
1. Briefs are often incomplete. Identify unstated assumptions or missing information (e.g., missing budget, vague target audience, unspecified channels).
2. Generate specific 'clarifying_questions' that the campaign manager MUST answer to resolve these ambiguities.
3. Generate a structured execution plan based on what IS provided.

You MUST return your response as a valid JSON object with the following schema:
{{
  "clarifying_questions": [
    {{"question": "Specific question about ambiguity", "reason": "Why this needs clarification"}}
  ],
  "audience_segments": ["Segment 1", "Segment 2"],
  "channels": [
    {{"channel": "Name", "specifications": "Format/Placement", "copy_guidance": "Instructions for copywriter"}}
  ],
  "timeline": ["Milestone 1", "Milestone 2"]
}}

Campaign Brief:
{brief.model_dump_json()}
"""

        response = client.chat.completions.create(
            model=deployment_name,
            response_format={"type": "json_object"}, # Force structured JSON output
            messages=[
                {"role": "system", "content": "You are a precise JSON-generating campaign planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4, # Slightly higher temperature for creative planning
            max_completion_tokens=4000
        )

        content = response.choices[0].message.content.strip()
        print("💡 PLANNER AI OUTPUT:", content)

        return json.loads(content)

    except Exception as e:
        return {"error": f"Failed to generate plan: {str(e)}"}

# 👇 NEW FUNCTION: The Human-in-the-Loop Refinement Engine 👇
def refine_plan(original_brief: dict, refinements: dict) -> dict:
    try:
        client, deployment_name = get_azure_client()

        prompt = f"""
You are an expert Marketing Campaign Manager. You previously reviewed a rough brief and asked clarifying questions.
Now, use the Original Brief AND the specific Human-Provided Clarifications below to build the final, highly-accurate execution plan. 
Do not ignore the human input; it is the absolute source of truth. If the human provided a budget, timeline, or specific constraint, you must strictly adhere to it.

You MUST return your response as a valid JSON object with the following schema. (Notice there are no clarifying_questions here—this is the final plan!):
{{
  "audience_segments": ["Segment 1", "Segment 2"],
  "channels": [
    {{"channel": "Name", "specifications": "Format/Placement", "copy_guidance": "Instructions for copywriter"}}
  ],
  "timeline": ["Milestone 1", "Milestone 2"]
}}

Original Campaign Brief:
{json.dumps(original_brief)}

Human-Provided Clarifications:
{json.dumps(refinements)}
"""

        response = client.chat.completions.create(
            model=deployment_name,
            response_format={"type": "json_object"}, 
            messages=[
                {"role": "system", "content": "You are a precise JSON-generating campaign planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, # Slightly lower temperature for strict adherence to the human's rules
            max_completion_tokens=4000
        )

        content = response.choices[0].message.content.strip()
        print("✨ REFINED PLANNER AI OUTPUT:", content)

        return json.loads(content)

    except Exception as e:
        return {"error": f"Failed to refine plan: {str(e)}"}