# 🚀 AI Campaign Manager Copilot

**Bridging the gap between aspirational ideas and operational execution.**

## 📌 The Problem: The "Brief-to-Execution" Gap
In enterprise marketing, stakeholders often submit campaign briefs that are incomplete, vague, or "aspirational." Translating these rough ideas into launch-ready execution plans usually requires weeks of kick-off meetings, Slack threads, and painful agency revision cycles. Mistakes made here cost companies thousands of dollars in wasted ad spend and brand safety violations.

## 💡 The Solution
**AI Campaign Manager Copilot** is a Human-in-the-Loop workflow engine that transforms ambiguous campaign briefs into hyper-precise, structured execution plans in seconds, and automatically audits agency deliverables for semantic alignment.

### ✨ Core Features

#### 1. AI Audit & Clarifying Questions
Instead of blindly generating a generic plan (hallucinating), our AI acts as a Senior Strategist. It scans the initial brief for missing constraints (e.g., missing budgets, vague audiences) and pauses to ask the user Enterprise-grade clarifying questions.

#### 2. Human-in-the-Loop Refinement Layer
We believe in "AI proposes, Humans dispose." Users can iteratively answer the AI's questions, dynamically updating budgets, constraints, and sales SLAs. The AI uses this human-provided ground truth to finalize the strategy, completely eliminating AI hallucination.

#### 3. Structured Execution Playbook
The Copilot translates the finalized strategy into a strictly formatted JSON execution plan, featuring:
* **Target Segments:** Buying-committee specific segmentation.
* **Channel Strategy:** Precise format specifications and copywriter guidance.
* **Timeline:** Week-by-week operational milestones.

#### 4. Semantic QA Agent
Users can input an external agency's proposed execution plan to check against their original rules. The QA Agent surfaces a Health Score, flags severe misalignments (like budget overages or illegal copy), and dynamically auto-corrects the flawed JSON.

## 🛠️ Technical Architecture
* **Frontend:** Streamlit (Dynamic state management for iterative UI)
* **Backend API:** FastAPI (RESTful routing, Pydantic validation)
* **LLM Engine:** Azure OpenAI
* **Orchestration:** Advanced System Prompting and strict JSON Schema enforcement (`response_format={"type": "json_object"}`) to ensure API-ready, deterministic outputs.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Yaswanth-Puttepu/Hackathon-AI.git](https://github.com/Yaswanth-Puttepu/Hackathon-AI.git)
   cd Hackathon-AI
