import React, { useState, useEffect } from 'react';
import '../app.css';

export default function App() {
  const [page, setPage] = useState('home');
  const [loading, setLoading] = useState(false);

  return (
    <div className="app">
      <nav className="navbar">
        <h1>CareSRE</h1>
        <div className="nav-links">
          <button onClick={() => setPage('home')}>Home</button>
          <button onClick={() => setPage('registration')}>OPD Register</button>
          <button onClick={() => setPage('token')}>Token Status</button>
          <button onClick={() => setPage('admin')}>Admin</button>
        </div>
      </nav>

      <main className="content">
        {page === 'home' && <HomePage setPage={setPage} />}
        {page === 'registration' && <OPDRegistration />}
        {page === 'token' && <TokenStatus />}
        {page === 'admin' && <AdminDashboard />}
      </main>
    </div>
  );
}

function HomePage({ setPage }) {
  return (
    <div className="page">
      <h2>Welcome to CareSRE</h2>
      <p>Care SRE - Smart Resource Management for Emergency</p>
      <button className="btn-primary" onClick={() => setPage('registration')}>
        Register for OPD
      </button>
    </div>
  );
}

function OPDRegistration() {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    symptoms: '',
  });
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('/register-patient', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setToken(data.token);
      setFormData({ name: '', age: '', symptoms: '' });
    } catch (error) {
      alert('Registration failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h2>OPD Registration</h2>
      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          placeholder="Name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Age"
          value={formData.age}
          onChange={(e) => setFormData({ ...formData, age: e.target.value })}
          required
        />
        <textarea
          placeholder="Describe your symptoms"
          value={formData.symptoms}
          onChange={(e) => setFormData({ ...formData, symptoms: e.target.value })}
          required
        />
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      {token && (
        <div className="success-box">
          <p>Registration Successful!</p>
          <p className="token">Your Token: <strong>{token}</strong></p>
        </div>
      )}
    </div>
  );
}

function TokenStatus() {
  const [token, setToken] = useState('');
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const response = await fetch(`/token-status/${token}`);
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      alert('Error fetching status: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h2>Check Token Status</h2>
      <div className="form">
        <input
          type="text"
          placeholder="Enter your token"
          value={token}
          onChange={(e) => setToken(e.target.value)}
        />
        <button onClick={handleCheck} className="btn-primary" disabled={loading}>
          {loading ? 'Checking...' : 'Check Status'}
        </button>
      </div>
      {status && (
        <div className="status-box">
          <p><strong>Position:</strong> {status.position}</p>
          <p><strong>Estimated Wait:</strong> {status.wait_time} mins</p>
          <p><strong>Status:</strong> {status.status}</p>
        </div>
      )}
    </div>
  );
}

function AdminDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const [opdRes, docRes, insightsRes] = await Promise.all([
          fetch('/opd-load'),
          fetch('/doctor-availability'),
          fetch('/insights')
        ]);
        const [opdData, docData, insightsData] = await Promise.all([opdRes.json(), docRes.json(), insightsRes.json()]);
        setDashboard({
          opd_load: opdData,
          doctors: docData,
          insights: insightsData
        });
      } catch (error) {
        console.error('Error fetching dashboard:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
    const interval = setInterval(fetchDashboard, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="page"><p>Loading...</p></div>;

  return (
    <div className="page">
      <h2>Admin Dashboard</h2>
      {dashboard && (
        <div className="dashboard-grid">
          <div className="card">
            <h3>OPD Load</h3>
            <p className="metric">{dashboard.opd_load}</p>
          </div>
          <div className="card">
            <h3>Total Patients</h3>
            <p className="metric">{dashboard.total_patients}</p>
          </div>
          <div className="card">
            <h3>Avg Wait Time</h3>
            <p className="metric">{dashboard.avg_wait_time} min</p>
          </div>
          {dashboard.alerts && dashboard.alerts.length > 0 && (
            <div className="card alert">
              <h3>⚠️ Alerts</h3>
              <ul>
                {dashboard.alerts.map((alert, i) => (
                  <li key={i}>{alert}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}