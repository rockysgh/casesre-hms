from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Patient(BaseModel):
    id: str
    name: str
    age: int
    symptoms: str
    priority: Priority
    department: str


class Doctor(BaseModel):
    id: str
    name: str
    department: str
    available: bool


class OPDDepartment(BaseModel):
    name: str
    current_load: int


class Token(BaseModel):
    patient_id: str
    token_number: int
    expected_time_window: str