import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const TokenStatus = () => {
    const [tokenData, setTokenData] = useState(null);
    const location = useLocation();
    const patientId = new URLSearchParams(location.search).get('patient_id');

    useEffect(() => {
        const fetchTokenStatus = async () => {
            try {
                const response = await fetch(`/token-status/${patientId}`);
                const data = await response.json();
                setTokenData(data);
            } catch (error) {
                console.error('Error fetching token status:', error);
            }
        };

        if (patientId) {
            fetchTokenStatus();
        }
    }, [patientId]);

    if (!tokenData) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Token Status</h1>
            <p><strong>Token Number:</strong> {tokenData.token_number ?? tokenData.tokenNumber}</p>
            <p><strong>Triage Level:</strong> {tokenData.triage_level}</p>
            <p><strong>Status:</strong> {tokenData.status}</p>
            <p><strong>Department:</strong> {tokenData.department ?? 'N/A'}</p>
        </div>
    );
};

export default TokenStatus;