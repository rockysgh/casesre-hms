import React, { useEffect, useState } from 'react';

const AdminDashboard = () => {
    const [opdLoad, setOpdLoad] = useState({});
    const [doctors, setDoctors] = useState({});
    const [alerts, setAlerts] = useState(null);
    const [insights, setInsights] = useState(null);

    const fetchOpdLoad = async () => {
        const response = await fetch('/opd-load');
        const data = await response.json();
        setOpdLoad(data);
    };

    const fetchDoctors = async () => {
        const response = await fetch('/doctor-availability');
        const data = await response.json();
        setDoctors(data);
    };

    const fetchAlerts = async () => {
        const response = await fetch('/alerts');
        const data = await response.json();
        return data;
    };

    const fetchInsights = async () => {
        const response = await fetch('/insights');
        const data = await response.json();
        return data;
    }; 

    useEffect(() => {
        const interval = setInterval(async () => {
            fetchOpdLoad();
            fetchDoctors();
            const alerts = await fetchAlerts();
            const insights = await fetchInsights();
            setAlerts(alerts);
            setInsights(insights);
        }, 5000); // Poll every 5 seconds

        // initial fetch
        fetchOpdLoad();
        fetchDoctors();
        (async () => {
            setAlerts(await fetchAlerts());
            setInsights(await fetchInsights());
        })();

        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <h1>Admin Dashboard</h1>
            <h2>Live OPD Load</h2>
            <pre>{JSON.stringify(opdLoad, null, 2)}</pre>
            <h2>Doctor Availability</h2>
            <pre>{JSON.stringify(doctors, null, 2)}</pre>
            <h2>Alerts</h2>
            <pre>{JSON.stringify(alerts, null, 2)}</pre>
            <h2>AI Insights</h2>
            <pre>{JSON.stringify(insights, null, 2)}</pre>
        </div>
    );
};

export default AdminDashboard;