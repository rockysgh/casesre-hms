CARESRE – FULL EXECUTION PLAN (FROM SCRATCH)
WHAT YOU ARE BUILDING (1 LINE – REMEMBER THIS)
CareSRE is an AI-powered intelligence layer that sits on top of a basic Hospital Management System to manage OPD flow, crowd load, and operational decisions using multiple task-specific AI agents.
This sentence alone is judge-safe.

PHASE 0: DECIDE SCOPE (VERY IMPORTANT)
You are NOT building:
Full hospital software


Real medical diagnosis


Real-time government integration


You ARE building:
A working MVP


With visible OPD flow


AI agents making decisions


A clear real-world story



PHASE 1: TECH STACK (DO NOT CHANGE THIS)
This stack is beginner-friendly + IIT-acceptable.
Frontend
React (basic)


OR Next.js (optional)


UI library: Tailwind / simple CSS


Pages:


OPD Registration


Token Status


Admin Dashboard


Backend
Python + FastAPI


JSON-based APIs


No heavy DB needed (use SQLite / JSON)


AI Layer
OpenAI / Azure OpenAI / Gemini API


NO model training


Prompt-based agents


Deployment (Optional)
Localhost demo is enough


Bonus: Render / Vercel



PHASE 2: DEFINE THE HMS CORE (MINIMUM)
This is your base system.
Entities (Simple)
Patient


Doctor


OPD Department


Token


APIs (Backend)
POST /register-patient
GET /token-status/{patient_id}
GET /opd-load
GET /doctor-availability

⚠️ This alone is NOT special.
 The magic is what AI does on top of this.

PHASE 3: DEFINE YOUR MULTI-AI AGENTS (CORE OF CARESRE)
You will implement 5 AI agents.
 Each agent = one responsibility + one prompt.

🧠 Agent 1: OPD Triage Agent
Purpose: Decide urgency + department
Input:
Patient symptoms


Age


History (optional)


Output:
Priority: Low / Medium / High


Suggested OPD department


How you implement:
prompt = """
You are an OPD triage agent.
Given patient symptoms, classify urgency and department.
Return JSON only.
"""


⏱ Agent 2: Token & Time Allocation Agent (MOST IMPORTANT)
Purpose: Replace physical queue
Input:
OPD load


Doctor availability


Priority from Agent 1


Output:
Token number


Expected visit time window


This is your USP / MVP slide.

📊 Agent 3: Crowd Prediction Agent
Purpose: Predict OPD congestion
Input:
Historical token data


Time of day


Department


Output:
Crowd risk: Low / Medium / High


Suggested slot shifting


This shows intelligence, not automation.

🚨 Agent 4: Alert & Exception Agent
Purpose: Detect failures
Triggers:
Doctor absent


OPD overload


Emergency spike


Output:
Alert message


Suggested action (reroute patients)



🧾 Agent 5: Admin Insight Agent
Purpose: Decision support
Input:
Daily OPD stats


Output:
3 actionable insights (plain English)


Example:
“ENT OPD is overloaded between 9–11 AM. Consider adding one more doctor.”

PHASE 4: AGENT ORCHESTRATION (IMPORTANT)
This is where judges get impressed.
Flow (Simple):
Patient registers


Triage Agent runs


Token Agent assigns slot


Crowd Agent monitors load


Alert Agent intervenes if needed


Admin Agent summarizes data


You DO NOT run agents simultaneously.
 You run them step-by-step via backend logic.

PHASE 5: FRONTEND FLOW (WHAT JUDGES SEE)
Patient Side
Enter symptoms


Click “Generate OPD Token”


See:


Token number


Time window


Department


Admin Side
Live OPD load


Alerts


AI suggestions


💡 Even fake data + real AI decisions = valid MVP

PHASE 6: OPD WORKFLOW SLIDE (YOUR MVP SLIDE)
Before CareSRE
Physical queue


Manual slips


No predictability


After CareSRE
Home-based OPD token


AI time allocation


Controlled crowd entry


This is NOT sugarcoating.
 This is a real Indian public hospital problem.

PHASE 7: IMPLEMENTATION FEASIBILITY (JUDGE-SAFE)
Use this EXACT logic in PPT:
“CareSRE is implemented using existing hospital data, lightweight APIs, and pre-trained LLMs. No model training or hardware upgrades are required, making it deployable as a pilot within weeks.”

PHASE 8: WHAT EACH TEAM MEMBER DOES
UI/UX Person
Design OPD screens


Token display


Admin dashboard


Backend (IITM teammate)
APIs


Agent orchestration


Data handling


YOU (IMPORTANT)
Agent prompts


Workflow logic


OPD concept


Pitch explanation


You are NOT useless.
 You are the system thinker.

PHASE 9: WHAT MAKES THIS IIT-LEVEL
✔ Real government hospital pain
 ✔ Multi-agent AI (not chatbot)
 ✔ Decision-support, not diagnosis
 ✔ Deployable MVP
 ✔ Clear societal impact


