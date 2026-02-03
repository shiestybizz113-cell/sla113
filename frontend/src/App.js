import { useEffect, useState } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const EngineCard = ({ name, index }) => {
  const getEngineIcon = (engineName) => {
    if (engineName.includes('strategy')) return '🎯';
    if (engineName.includes('plan')) return '📋';
    if (engineName.includes('analysis')) return '🔍';
    if (engineName.includes('opportunity')) return '💡';
    if (engineName.includes('evaluator')) return '⚖️';
    if (engineName.includes('pricing')) return '💰';
    if (engineName.includes('blueprint')) return '🏗️';
    if (engineName.includes('persona')) return '👤';
    if (engineName.includes('anime')) return '🎨';
    if (engineName.includes('art')) return '🖼️';
    if (engineName.includes('money')) return '💵';
    if (engineName.includes('pipeline')) return '🔗';
    if (engineName.includes('canon')) return '📜';
    if (engineName.includes('drift')) return '📊';
    if (engineName.includes('error')) return '🛡️';
    if (engineName.includes('routing')) return '🔀';
    if (engineName.includes('hybrid') || engineName.includes('core')) return '🧠';
    return '⚙️';
  };

  const formatEngineName = (name) => {
    return name
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div 
      className="engine-card"
      style={{ animationDelay: `${index * 0.05}s` }}
      data-testid={`engine-card-${name}`}
    >
      <span className="engine-icon">{getEngineIcon(name)}</span>
      <span className="engine-name">{formatEngineName(name)}</span>
    </div>
  );
};

const ModelBadge = ({ name, status }) => (
  <div className={`model-badge ${status === 'available' ? 'available' : 'unavailable'}`} data-testid={`model-${name}`}>
    <span className="model-status-dot"></span>
    <span className="model-name">{name}</span>
  </div>
);

const Home = () => {
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchHealth = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/health`);
      setHealthData(response.data);
      setError(null);
    } catch (e) {
      console.error(e, 'Error fetching health data');
      setError('Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  if (loading) {
    return (
      <div className="dashboard" data-testid="loading-screen">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Connecting to Hybrid Intelligence Core...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard" data-testid="error-screen">
        <div className="error-container">
          <span className="error-icon">⚠️</span>
          <h2>Connection Error</h2>
          <p>{error}</p>
          <button onClick={fetchHealth} className="retry-button" data-testid="retry-button">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard" data-testid="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1 className="dashboard-title">
            <span className="title-icon">🧠</span>
            Hybrid Intelligence Core
          </h1>
          <div className={`status-badge ${healthData?.status === 'healthy' ? 'healthy' : 'unhealthy'}`} data-testid="status-badge">
            <span className="status-dot"></span>
            {healthData?.status?.toUpperCase() || 'UNKNOWN'}
          </div>
        </div>
        <p className="dashboard-subtitle">{healthData?.pipeline || 'AI Pipeline'}</p>
      </header>

      <section className="section models-section">
        <h2 className="section-title">Available Models</h2>
        <div className="models-grid" data-testid="models-grid">
          {healthData?.models && Object.entries(healthData.models).map(([name, status]) => (
            <ModelBadge key={name} name={name} status={status} />
          ))}
        </div>
      </section>

      <section className="section engines-section">
        <h2 className="section-title">
          Active Engines 
          <span className="engine-count" data-testid="engine-count">{healthData?.engines?.length || 0}</span>
        </h2>
        <div className="engines-grid" data-testid="engines-grid">
          {healthData?.engines?.map((engine, index) => (
            <EngineCard key={engine} name={engine} index={index} />
          ))}
        </div>
      </section>

      <section className="section raw-section">
        <h2 className="section-title">Raw Response</h2>
        <pre className="raw-json" data-testid="raw-json">
          {JSON.stringify(healthData, null, 2)}
        </pre>
      </section>

      <footer className="dashboard-footer">
        <p>Backend: <code>{BACKEND_URL}</code></p>
        <button onClick={fetchHealth} className="refresh-button" data-testid="refresh-button">
          ↻ Refresh
        </button>
      </footer>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
