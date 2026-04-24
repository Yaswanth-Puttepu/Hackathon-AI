from app.models.brief import CampaignBrief

def generate_plan(brief: CampaignBrief) -> dict:
    """
    Generate a structured execution plan based on the campaign brief.
    Currently returns a mock response.
    """
    # Mock structured response
    plan = {
        "audience_segments": [
            {"segment": brief.target_audience, "priority": "High"}
        ],
        "channels": brief.channels,
        "messaging": f"Focus on: {brief.key_message}",
        "timeline": brief.timeline,
        "tasks": [
            {"task": "Identify specific media placements", "status": "Pending"},
            {"task": "Develop creative assets", "status": "Pending"},
            {"task": "Setup tracking and attribution", "status": "Pending"}
        ]
    }
    return plan
