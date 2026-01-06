# Hospital Management System - Data Storage

# Store patients information
patients = []

# Store doctors information
doctors = []

# Store departments information
departments = []

# Store authentication tokens
tokens = {}

# Store OPD (Out Patient Department) load
opd_load = {
    "total_patients": 0,
    "department_wise": {}
}


def add_patient(patient_id, name, age, department, doctor_id):
    """Add a new patient to the system"""
    patient = {
        "id": patient_id,
        "name": name,
        "age": age,
        "department": department,
        "doctor_id": doctor_id,
        "status": "active"
    }
    patients.append(patient)
    update_opd_load(department, 1)
    return patient


def add_doctor(doctor_id, name, department, specialization):
    """Add a new doctor to the system"""
    doctor = {
        "id": doctor_id,
        "name": name,
        "department": department,
        "specialization": specialization
    }
    doctors.append(doctor)
    return doctor


def add_department(dept_id, name, capacity):
    """Add a new department to the system"""
    department = {
        "id": dept_id,
        "name": name,
        "capacity": capacity
    }
    departments.append(department)
    opd_load["department_wise"][name] = 0
    return department


def update_opd_load(department, count):
    """Update OPD load for a department"""
    if department in opd_load["department_wise"]:
        opd_load["department_wise"][department] += count
        opd_load["total_patients"] += count
    return opd_load


def get_opd_load():
    """Retrieve current OPD load"""
    return opd_load


def get_department_load(department):
    """Get OPD load for a specific department"""
    return opd_load["department_wise"].get(department, 0)


def add_token(user_id, token_value):
    """Store authentication token"""
    tokens[user_id] = token_value
    return True


def validate_token(user_id, token_value):
    """Validate authentication token"""
    return tokens.get(user_id) == token_value