import json
import os
from typing import Dict, Any
import anthropic

def opd_triage_agent(symptoms: str, age: int, history: str) -> Dict[str, Any]:
    """
    Triage patient based on symptoms, age, and medical history.
    Returns priority level and recommended department.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""You are a medical triage AI for an OPD (Outpatient Department).
Based on the following patient information, determine the priority level and recommended department.

Patient Age: {age}
Symptoms: {symptoms}
Medical History: {history}

Respond ONLY with valid JSON in this format:
{{
    "priority": "critical|high|medium|low",
    "department": "Cardiology|Orthopedics|Gastroenterology|Neurology|General|Pediatrics|Dermatology",
    "reasoning": "brief explanation"
}}"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(message.content[0].text)


def token_allocation_agent(priority: str, opd_load: int, doctor_availability: Dict[str, int]) -> Dict[str, Any]:
    """
    Allocate token and estimate visit time based on priority and current OPD load.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""You are an OPD token allocation system.
Based on current conditions, allocate a token and estimate wait time.

Patient Priority: {priority}
Current OPD Load: {opd_load} patients
Doctor Availability (department: available_slots): {json.dumps(doctor_availability)}

Respond ONLY with valid JSON in this format:
{{
    "token_number": 101,
    "estimated_wait_minutes": 30,
    "assigned_department": "department_name",
    "notes": "brief note"
}}"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(message.content[0].text)


def crowd_prediction_agent(historical_tokens: list, time_of_day: str, department: str) -> Dict[str, Any]:
    """
    Predict crowd risk and suggest actions based on historical data and time.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""You are an OPD crowd prediction AI.
Analyze historical patterns and predict crowd risk.

Historical Token Data (last 7 days): {json.dumps(historical_tokens)}
Current Time: {time_of_day}
Department: {department}

Respond ONLY with valid JSON in this format:
{{
    "crowd_risk": "low|medium|high|critical",
    "expected_patients": 45,
    "suggested_action": "open_additional_counter|call_backup_staff|implement_online_booking|none",
    "confidence": 0.85
}}"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(message.content[0].text)


def alert_exception_agent(opd_load: int, doctor_status: Dict[str, str], emergency_flag: bool) -> Dict[str, Any]:
    """
    Generate alerts for exceptional conditions and recommend actions.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""You are an OPD alert and exception handling system.
Analyze current conditions and generate alerts if necessary.

Current OPD Load: {opd_load} patients
Doctor Status (name: status): {json.dumps(doctor_status)}
Emergency Flag: {emergency_flag}

Respond ONLY with valid JSON in this format:
{{
    "alert_level": "none|warning|critical",
    "alert_message": "description of issue",
    "recommended_action": "specific action to take",
    "immediate_notify": true
}}"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(message.content[0].text)


def admin_insight_agent(daily_opd_stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate actionable insights for administrators based on daily OPD statistics.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""You are an OPD analytics and insights AI for administrators.
Analyze the daily statistics and provide 3 actionable insights.

Daily OPD Statistics: {json.dumps(daily_opd_stats)}

Respond ONLY with valid JSON in this format:
{{
    "insights": [
        {{"insight": "first actionable insight", "priority": "high|medium|low"}},
        {{"insight": "second actionable insight", "priority": "high|medium|low"}},
        {{"insight": "third actionable insight", "priority": "high|medium|low"}}
    ],
    "summary": "brief executive summary"
}}"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(message.content[0].text)