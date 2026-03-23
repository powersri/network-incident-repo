import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [incidents, setIncidents] = useState([]);

  const [deviceName, setDeviceName] = useState("");
  const [location, setLocation] = useState("");
  const [incidentType, setIncidentType] = useState("");
  const [severity, setSeverity] = useState("low");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("open");

  const [message, setMessage] = useState("");

  const fetchIncidents = async () => {
    try {
      const response = await fetch(`${API_URL}/incidents`);
      const data = await response.json();

      if (response.ok) {
        setIncidents(data);
      } else {
        setMessage("Failed to load incidents.");
      }
    } catch (error) {
      setMessage("Error connecting to backend.");
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch(`${API_URL}/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.access_token);
        setToken(data.access_token);
        setMessage("Login successful.");
      } else {
        setMessage(data.detail || "Login failed.");
      }
    } catch (error) {
      setMessage("Error connecting to backend.");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
    setMessage("Logged out.");
  };

  const handleCreateIncident = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/incidents`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          device_name: deviceName,
          location,
          incident_type: incidentType,
          severity,
          description,
          status,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Incident created successfully.");
        setDeviceName("");
        setLocation("");
        setIncidentType("");
        setSeverity("low");
        setDescription("");
        setStatus("open");
        fetchIncidents();
      } else {
        setMessage(data.detail || "Failed to create incident.");
      }
    } catch (error) {
      setMessage("Error connecting to backend.");
    }
  };

  const handleDeleteIncident = async (incidentId) => {
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/incidents/${incidentId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Incident deleted successfully.");
        fetchIncidents();
      } else {
        setMessage(data.detail || "Failed to delete incident.");
      }
    } catch (error) {
      setMessage("Error connecting to backend.");
    }
  };

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Network Incident Reporting System</h1>

      {message && <p><strong>{message}</strong></p>}

      <section style={{ marginBottom: "30px" }}>
        <h2>Login</h2>
        {!token ? (
          <form onSubmit={handleLogin}>
            <div style={{ marginBottom: "10px" }}>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div style={{ marginBottom: "10px" }}>
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit">Login</button>
          </form>
        ) : (
          <button onClick={handleLogout}>Logout</button>
        )}
      </section>

      <section style={{ marginBottom: "30px" }}>
        <h2>Create Incident</h2>
        <form onSubmit={handleCreateIncident}>
          <div style={{ marginBottom: "10px" }}>
            <input
              type="text"
              placeholder="Device Name"
              value={deviceName}
              onChange={(e) => setDeviceName(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: "10px" }}>
            <input
              type="text"
              placeholder="Location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: "10px" }}>
            <input
              type="text"
              placeholder="Incident Type"
              value={incidentType}
              onChange={(e) => setIncidentType(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: "10px" }}>
            <select value={severity} onChange={(e) => setSeverity(e.target.value)}>
              <option value="low">low</option>
              <option value="medium">medium</option>
              <option value="high">high</option>
              <option value="critical">critical</option>
            </select>
          </div>

          <div style={{ marginBottom: "10px" }}>
            <textarea
              placeholder="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: "10px" }}>
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option value="open">open</option>
              <option value="investigating">investigating</option>
              <option value="resolved">resolved</option>
            </select>
          </div>

          <button type="submit" disabled={!token}>
            Create Incident
          </button>
        </form>
        {!token && <p>Log in first to create or delete incidents.</p>}
      </section>

      <section>
        <h2>Incident List</h2>
        {incidents.length === 0 ? (
          <p>No incidents found.</p>
        ) : (
          <ul>
            {incidents.map((incident) => (
              <li key={incident.id} style={{ marginBottom: "15px", border: "1px solid #ccc", padding: "10px" }}>
                <p><strong>Device:</strong> {incident.device_name}</p>
                <p><strong>Location:</strong> {incident.location}</p>
                <p><strong>Type:</strong> {incident.incident_type}</p>
                <p><strong>Severity:</strong> {incident.severity}</p>
                <p><strong>Status:</strong> {incident.status}</p>
                <p><strong>Description:</strong> {incident.description}</p>
                {token && (
                  <button onClick={() => handleDeleteIncident(incident.id)}>
                    Delete
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default App;