import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import OPDRegistration from './pages/OPDRegistration';
import TokenStatus from './pages/TokenStatus';
import AdminDashboard from './pages/AdminDashboard';
import './app.css';

function App() {
    return (
        <BrowserRouter>
            <div className="app-container">
                <nav className="navbar">
                    <Link to="/">OPD Registration</Link>
                    <Link to="/token-status">Token Status</Link>
                    <Link to="/admin">Admin Dashboard</Link>
                </nav>

                <main className="content">
                    <Routes>
                        <Route path="/" element={<OPDRegistration />} />
                        <Route path="/token-status" element={<TokenStatus />} />
                        <Route path="/admin" element={<AdminDashboard />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    );
}

// Mount the app when loaded from index.html
const rootEl = document.getElementById('root');
if (rootEl) {
    ReactDOM.createRoot(rootEl).render(<App />);
}

export default App;