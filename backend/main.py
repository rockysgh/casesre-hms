from fastapi import FastAPI, HTTPException
from models import PatientRegister, PatientResponse
from agents import opd_triage_agent, token_allocation_agent, alert_exception_agent, admin_insight_agent, crowd_prediction_agent
from pydantic import BaseModel
from typing import Dict, List
import json
from datetime import datetime
import uvicorn

app = FastAPI(title="CareSRE HMS API", version="1.0.0")

# In-memory storage
patients_db: Dict = {}
tokens_db: Dict = {}
opd_load_db: Dict = {"current": 0, "capacity": 100}
doctors_db: Dict = {
    "Dr. Smith": {"available": True, "patients": 0},
    "Dr. Johnson": {"available": True, "patients": 0},
}

# Pydantic models
class PatientRegister(BaseModel):
    name: str
    age: int
    symptoms: str
    contact: str
    history: str = ""

class PatientResponse(BaseModel):
    patient_id: str
    name: str
    triage_level: str
    token_number: int

# Helper functions
def generate_patient_id() -> str:
    return f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"

def run_triage_agent(symptoms: str, age: int, history: str):
    # Use the OPD triage agent for better triage decisions
    try:
        resp = opd_triage_agent(symptoms, age, history)
        priority = resp.get("priority", "low")
        department = resp.get("department", "General")
    except Exception:
        priority = "low"
        department = "General"
    triage_level = "High" if priority in ("critical", "high") else "Normal"
    return triage_level, priority, department

def run_token_allocation_agent(patient_id: str, priority: str, triage_level: str) -> int:
    # Use the token allocation agent and fallback to local counter
    doctor_availability = {name: (1 if info.get("available") else 0) for name, info in doctors_db.items()}
    try:
        resp = token_allocation_agent(priority, opd_load_db["current"], doctor_availability)
        token_number = resp.get("token_number")
    except Exception:
        token_number = None
    if not token_number:
        token_number = tokens_db.get("counter", 0) + 1
        tokens_db["counter"] = token_number
    return token_number

# API Endpoints
@app.post("/register-patient")

@app.post("/register-patient", response_model=PatientResponse)
def register_patient(patient: PatientRegister):
    patient_id = generate_patient_id()
    
    # Run triage agent
    triage_level, priority, department = run_triage_agent(patient.symptoms, patient.age, patient.history)
    
    # Run token allocation agent
    token_number = run_token_allocation_agent(patient_id, priority, triage_level)
    
    # Store patient data
    patients_db[patient_id] = {
        "name": patient.name,
        "age": patient.age,
        "symptoms": patient.symptoms,
        "contact": patient.contact,
        "history": patient.history,
        "triage_level": triage_level,
        "department": department,
        "registered_at": datetime.now().isoformat()
    }
    
    tokens_db[patient_id] = token_number
    opd_load_db["current"] += 1
    
    return PatientResponse(
        patient_id=patient_id,
        name=patient.name,
        triage_level=triage_level,
        token_number=token_number
    )

@app.get("/token-status/{patient_id}")
def get_token_status(patient_id: str):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "patient_id": patient_id,
        "token_number": tokens_db.get(patient_id),
        "triage_level": patients_db[patient_id]["triage_level"],
        "status": "Waiting"
    }

@app.get("/opd-load")
def get_opd_load():
    return {
        "current_patients": opd_load_db["current"],
        "capacity": opd_load_db["capacity"],
        "utilization": f"{(opd_load_db['current'] / opd_load_db['capacity']) * 100:.1f}%"
    }

@app.get("/doctor-availability")
def get_doctor_availability():
    return {
        "doctors": doctors_db,
        "available_count": sum(1 for doc in doctors_db.values() if doc["available"])
    }

@app.get("/alerts")
def get_alerts():
    # Prepare inputs for alert agent
    doctor_status = {name: ("available" if info.get("available") else "unavailable") for name, info in doctors_db.items()}
    emergency_flag = any(p.get("triage_level") == "High" for p in patients_db.values())
    try:
        resp = alert_exception_agent(opd_load_db["current"], doctor_status, emergency_flag)
    except Exception:
        # Fallback simple logic
        if opd_load_db["current"] / opd_load_db["capacity"] > 0.9 or emergency_flag:
            resp = {
                "alert_level": "critical",
                "alert_message": "High load or emergency cases detected",
                "recommended_action": "open_additional_counter",
                "immediate_notify": True
            }
        else:
            resp = {"alert_level": "none", "alert_message": "All good", "recommended_action": "none", "immediate_notify": False}
    return resp

@app.get("/insights")
def get_insights():
    # Assemble daily stats for insight agent
    daily_stats = {
        "total_registered": len(patients_db),
        "current_patients": opd_load_db["current"],
        "capacity": opd_load_db["capacity"],
        "triage_counts": {
            "High": sum(1 for p in patients_db.values() if p.get("triage_level") == "High"),
            "Normal": sum(1 for p in patients_db.values() if p.get("triage_level") == "Normal")
        },
        "doctor_summary": {name: info for name, info in doctors_db.items()}
    }
    try:
        resp = admin_insight_agent(daily_stats)
    except Exception:
        resp = {"insights": [{"insight": "Not enough data", "priority": "low"}], "summary": "No insights available"}
    return resp

@app.get("/crowd-prediction")
def get_crowd_prediction(department: str = "General"):
    historical_tokens = list(tokens_db.values())[:50]
    time_of_day = datetime.now().strftime("%H:%M")
    try:
        resp = crowd_prediction_agent(historical_tokens, time_of_day, department)
    except Exception:
        resp = {"crowd_risk": "low", "expected_patients": 0, "suggested_action": "none", "confidence": 0.5}
    return resp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)