import os
import json
from openai import AzureOpenAI

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

def run_qa_agent(brief: dict, plan: dict):
    try:
        client, deployment_name = get_azure_client()

        prompt = f"""
You are an expert marketing QA agent. Your task is to check an execution plan against its originating brief and surface misalignments before launch.
Do not check for spelling or formatting; focus strictly on SEMANTIC CONSISTENCY (e.g., audience mismatches, missing budget, tone divergence, missing constraints).

You MUST return your response as a valid JSON object containing an array called "issues". 
Each issue must have the following keys: "type", "severity" (High, Medium, Low), "description", and "suggestion".

Campaign Brief:
{json.dumps(brief)}

Execution Plan:
{json.dumps(plan)}
"""

        response = client.chat.completions.create(
            model=deployment_name,
            response_format={"type": "json_object"}, # Force JSON output
            messages=[
                {"role": "system", "content": "You are a precise JSON-generating QA agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_completion_tokens=800
        )

        content = response.choices[0].message.content.strip()
        print("🔍 RAW QA OUTPUT:", content)

        try:
            parsed_data = json.loads(content)
            issues = parsed_data.get("issues", [])
        except json.JSONDecodeError:
            issues = []

        if not issues:
            issues = [
                {
                    "type": "Model Failure",
                    "severity": "High",
                    "description": "Failed to parse QA output as JSON.",
                    "suggestion": "Check model response or prompt"
                }
            ]
            return {"score": 0, "blocking_issues": True, "summary": "QA generation failed.", "issues": issues}

        # 🎯 SCORING
        score = 100
        blocking = False

        for issue in issues:
            severity = issue.get("severity", "").lower()
            if severity == "high":
                score -= 15
                blocking = True
            elif severity == "medium":
                score -= 8
            elif severity == "low":
                score -= 3

        score = max(score, 0)

        # 🧠 SUMMARY
        if blocking:
            summary = "High risk: critical issues must be resolved before launch"
        elif score >= 80:
            summary = "Low risk: campaign is well aligned"
        elif score >= 60:
            summary = "Moderate risk: some improvements needed"
        else:
            summary = "High risk: major gaps in campaign execution"

        return {
            "score": score,
            "blocking_issues": blocking,
            "summary": summary,
            "issues": issues
        }

    except Exception as e:
        return {"error": f"Error running QA agent: {str(e)}"}


def generate_llm_fix_plan(brief: dict, plan: dict, issues: list):
    try:
        client, deployment_name = get_azure_client()

        prompt = f"""
You are a senior marketing strategist.
Create an improved execution plan based on the QA issues provided. 

You MUST return the output as a valid JSON object representing the fixed execution plan. 
Do not include markdown blocks or any text outside the JSON object.

Campaign Brief:
{json.dumps(brief)}

Original Execution Plan:
{json.dumps(plan)}

QA Issues:
{json.dumps(issues)}
"""

        response = client.chat.completions.create(
            model=deployment_name,
            response_format={"type": "json_object"}, # Force JSON output
            messages=[
                {"role": "system", "content": "You output valid JSON execution plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_completion_tokens=4000  # 👈 Increased token limit!
        )

        content = response.choices[0].message.content.strip()
        print("🔧 LLM FIX PLAN OUTPUT:", content)

        return json.loads(content) 

    except Exception as e:
        return {"error": f"LLM fix plan error: {str(e)}"}