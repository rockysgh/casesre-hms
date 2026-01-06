import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const OPDRegistration = () => {
    const [name, setName] = useState('');
    const [age, setAge] = useState('');
    const [symptoms, setSymptoms] = useState('');
    const [contact, setContact] = useState('');
    const [history, setHistory] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const patientData = { name, age: Number(age), symptoms, contact, history };

        try {
            const response = await fetch('/register-patient', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(patientData),
            });

            if (response.ok) {
                const data = await response.json();
                // Navigate to Token Status page with patient_id
                navigate(`/token-status?patient_id=${data.patient_id}`);
            } else {
                // Handle error
                console.error('Failed to register patient');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h1>OPD Registration</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name:</label>
                    <input 
                        type="text" 
                        value={name} 
                        onChange={(e) => setName(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Age:</label>
                    <input 
                        type="number" 
                        value={age} 
                        onChange={(e) => setAge(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Contact:</label>
                    <input
                        type="text"
                        value={contact}
                        onChange={(e) => setContact(e.target.value)}
                    />
                </div>
                <div>
                    <label>Medical History (optional):</label>
                    <textarea 
                        value={history} 
                        onChange={(e) => setHistory(e.target.value)} 
                    />
                </div>
                <div>
                    <label>Symptoms:</label>
                    <textarea 
                        value={symptoms} 
                        onChange={(e) => setSymptoms(e.target.value)} 
                        required 
                    />
                </div>
                <button type="submit">Generate OPD Token</button>
            </form>
        </div>
    );
};

export default OPDRegistration;