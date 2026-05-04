import streamlit as st
import requests
import json
import pandas as pd

# 🎨 1. Page Configuration & Custom CSS
st.set_page_config(page_title="AI Campaign Copilot", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .score-high { color: #28a745; font-size: 55px; font-weight: 800; text-align: center; }
    .score-med { color: #ffc107; font-size: 55px; font-weight: 800; text-align: center; }
    .score-low { color: #dc3545; font-size: 55px; font-weight: 800; text-align: center; }
    .stProgress > div > div > div > div { background-color: #007bff; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 AI Campaign Manager Copilot")
st.markdown("Transform vague campaign ideas into precise execution plans, and automatically QA agency deliverables.")

# Using tabs to separate the two directions for the demo
tab1, tab2 = st.tabs(["1️⃣ Brief-to-Plan Generator", "2️⃣ QA & Misalignment Checker"])

# --- TAB 1: DIRECTION 1 ---
with tab1:
    st.header("Turn Aspirational Briefs into Execution Plans")
    
    with st.form("planner_form"):
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name", "Q3 Enterprise Trial-to-Paid Push")
            target_audience = st.text_input("Audience", "Trial users at companies with 1000+ employees.")
            channels = st.text_input("Channels", "Email, LinkedIn, social")
            budget = st.text_input("Budget", "Not specified")
            timeline = st.text_input("Timeline", "Live by July 1")
            success_metrics = st.text_input("Success Metrics", "Conversion rate to 22%") 
        with col2:
            business_objective = st.text_area("Objective", "Convert 200 enterprise trial accounts to paid contracts.", height=110)
            key_message = st.text_area("Key Message", "Stop leaving hours of manual work on the table.", height=110)
            constraints = st.text_area("Constraints / Brand Rules", "No competitor names.", height=110)
        
        submit_plan = st.form_submit_button("✨ Generate AI Execution Plan", use_container_width=True)

    if submit_plan:
        payload = {
            "campaign_name": campaign_name, "business_objective": business_objective,
            "target_audience": target_audience, "key_message": key_message,
            "channels": [c.strip() for c in channels.split(",")], "budget": budget,
            "timeline": timeline, "success_metrics": success_metrics, "constraints": constraints
        }
        
        with st.spinner("🧠 AI is analyzing the brief and structuring the plan..."):
            res = requests.post("http://localhost:8000/generate-plan", json=payload)
            if res.status_code == 200:
                st.session_state['original_brief'] = payload
                st.session_state['generated_plan'] = res.json()["data"]
                # 👇 FIX: Clear out any old answers if we start a brand new campaign
                st.session_state.pop('user_refinements', None)
                st.session_state.pop('refined_plan', None)
            else:
                st.error(f"Failed to connect to API. Error Code: {res.status_code}. Is your FastAPI backend running?")

    if 'generated_plan' in st.session_state:
        data = st.session_state['generated_plan']
        
        # --- MISSING INFO / CLARIFYING QUESTIONS ---
        if data.get("clarifying_questions"):
            st.divider()
            st.subheader("⚠️ Missing Information (Clarifying Questions)")
            st.markdown("The AI detected the following ambiguities in your brief that must be resolved:")
            
            for q in data.get("clarifying_questions", []):
                st.warning(f"**❓ {q.get('question', 'Question')}** \n*Context:* {q.get('reason', '')}")
            
            st.divider()
            with st.expander("🗣️ Refine Plan with Human Context", expanded=True):
                st.markdown("Provide answers to the AI's questions below to generate a highly accurate, final execution plan.")
                
                with st.form("refinement_form"):
                    user_refinements = {}
                    # 👇 FIX: Retrieve saved answers so the text boxes don't empty out!
                    saved_refinements = st.session_state.get('user_refinements', {})
                    
                    for i, q in enumerate(data["clarifying_questions"]):
                        q_text = q.get('question', f"Question {i+1}")
                        # 👇 FIX: Pass the saved answer into the 'value' parameter
                        user_refinements[q_text] = st.text_input(q_text, value=saved_refinements.get(q_text, ""))
                    
                    submit_refinements = st.form_submit_button("✨ Finalize Execution Plan", use_container_width=True)

                if submit_refinements:
                    # Save the user's answers instantly
                    st.session_state['user_refinements'] = user_refinements
                    
                    refine_payload = {
                        "original_brief": st.session_state['original_brief'],
                        "refinements": user_refinements
                    }
                    with st.spinner("🧠 AI is absorbing your answers and finalizing the execution plan..."):
                        res_refine = requests.post("http://localhost:8000/refine-plan", json=refine_payload)
                        if res_refine.status_code == 200:
                            # 👇 FIX: Save the new plan separately so we don't delete the questions!
                            st.session_state['refined_plan'] = res_refine.json()["data"]
                            st.rerun() 
                        else:
                            st.error("Failed to connect to Refinement API.")

        # --- RENDER THE EXECUTION PLAN ---
        st.divider()
        
        # 👇 FIX: Check if we have a refined plan. If yes, show that one. If no, show the original one.
        if 'refined_plan' in st.session_state:
            st.success("✅ Execution Plan successfully updated with your human constraints!")
            display_data = st.session_state['refined_plan']
        else:
            display_data = data
            
        st.subheader("📋 Generated Execution Plan")
        
        st.markdown("### 🎯 Target Segments")
        for aud in display_data.get("audience_segments", []):
            st.markdown(f"- ✅ {aud}")
        
        st.markdown("### 📢 Channel Strategy")
        try:
            df_channels = pd.DataFrame(display_data.get("channels", []))
            st.dataframe(df_channels, use_container_width=True, hide_index=True)
        except:
            st.json(display_data.get("channels", [])) 
        
        st.markdown("### 📅 Timeline & Milestones")
        for step in display_data.get("timeline", []):
            st.info(f"⏳ {step}")
        
        with st.expander("Show Raw Developer JSON Output"):
            st.json(display_data)

# --- TAB 2: DIRECTION 2 ---
with tab2:
    st.header("Campaign QA & Semantic Alignment")
    st.markdown("Check an agency's execution plan against your brief for semantic consistency.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Campaign Brief (Your Rules)")
        brief_json = st.text_area("Brief Input", '{"audience": "Enterprise users", "budget": "10000"}', height=200, label_visibility="collapsed")
    with col2:
        st.caption("Flawed Execution Plan (Agency's Homework)")
        plan_json = st.text_area("Plan Input", '{"audience": "Small businesses", "budget_allocated": "15000"}', height=200, label_visibility="collapsed")
        
    if st.button("🔍 Run AI Semantic QA Agent", use_container_width=True):
        try:
            qa_payload = {"brief": json.loads(brief_json), "plan": json.loads(plan_json)}
            with st.spinner("🤖 AI is hunting for misalignments..."):
                res = requests.post("http://localhost:8000/qa-plan", json=qa_payload)
                if res.status_code == 200:
                    result = res.json()["data"]
                    qa_eval = result["qa_evaluation"]
                    
                    st.divider()
                    
                    score = qa_eval.get("score", 0)
                    score_class = "score-high" if score >= 80 else ("score-med" if score >= 60 else "score-low")
                    
                    score_col, summary_col = st.columns([1, 3])
                    with score_col:
                        st.markdown("<p style='text-align: center; margin-bottom: 0px;'>Health Score</p>", unsafe_allow_html=True)
                        st.markdown(f"<div class='{score_class}'>{score}/100</div>", unsafe_allow_html=True)
                        st.progress(score / 100)
                    with summary_col:
                        st.subheader("AI QA Summary")
                        st.write(qa_eval.get("summary", ""))
                    
                    st.markdown("### 🚨 Identified Issues:")
                    for issue in qa_eval.get("issues", []):
                        severity = issue.get("severity", "Low").lower()
                        issue_text = f"**{issue.get('type', 'Issue')}** - {issue.get('description', '')} \n\n 👉 **Fix:** {issue.get('suggestion', '')}"
                        
                        if severity == "high":
                            st.error(issue_text, icon="🚨")
                        elif severity == "medium":
                            st.warning(issue_text, icon="⚠️")
                        else:
                            st.info(issue_text, icon="ℹ️")
                    
                    if "fixed_plan" in result:
                        st.divider()
                        st.success("### ✨ AI Auto-Corrected Execution Plan")
                        st.markdown("The AI rewrote the plan to align perfectly with the original brief.")
                        st.json(result["fixed_plan"])
                        
        except json.JSONDecodeError:
            st.error("Please enter valid JSON in both text areas.")