import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [dashboard, setDashboard] = useState([]);

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://127.0.0.1:8000/upload-pdf", formData);
    setResult(res.data);
  };

  const approve = async () => {
    await axios.post("http://127.0.0.1:8000/approve", result);
    alert("Approved!");
    loadDashboard();
  };

  const loadDashboard = async () => {
    const res = await axios.get("http://127.0.0.1:8000/dashboard");
    setDashboard(res.data);
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const getColor = (level) => {
    if (!level) return "black";
    if (level.includes("HIGH")) return "red";
    if (level.includes("MEDIUM")) return "orange";
    return "green";
  };

  return (
    <div style={{ fontFamily: "Arial", background: "#b4bfed", minHeight: "100vh", padding: "20px" }}>

      <h1 style={{ textAlign: "center", color: "#2f3640" }}>
        ⚖️ Judgment AI Dashboard
      </h1>

      {/* Upload Section */}
      <div style={{
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        marginBottom: "20px"
      }}>
        <h3>Upload Court Judgment</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadFile} style={{ marginLeft: "10px", padding: "6px 12px" }}>
          Upload
        </button>
      </div>

      {/* Result Section */}
      {result && (
        <div style={{
          display: "flex",
          gap: "20px",
          marginBottom: "20px"
        }}>

          {/* Extracted Data */}
          <div style={{
            flex: 1,
            background: "white",
            padding: "15px",
            borderRadius: "10px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
          }}>
            <h3>Extracted Data</h3>
            <pre style={{ fontSize: "12px", overflow: "auto" }}>
              {JSON.stringify(result.extracted_data, null, 2)}
            </pre>
          </div>

          {/* Action Plan */}
          <div style={{
            flex: 1,
            background: "white",
            padding: "15px",
            borderRadius: "10px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
          }}>
            <h3>Action Plan</h3>

            <p><b>Action:</b> {result.action_plan?.action_required}</p>
            <p>
              <b>Urgency:</b>{" "}
              <span style={{ color: getColor(result.action_plan?.urgency_level) }}>
                {result.action_plan?.urgency_level}
              </span>
            </p>
            <p><b>Deadline:</b> {result.action_plan?.deadline}</p>
            <p><b>Department:</b> {result.action_plan?.responsible_department}</p>

            <h4>Steps:</h4>
            <ul>
              {result.action_plan?.recommended_steps?.map((step, i) => (
                <li key={i}>{step}</li>
              ))}
            </ul>

            <button onClick={approve} style={{
              marginTop: "10px",
              padding: "8px 14px",
              background: "green",
              color: "white",
              border: "none",
              borderRadius: "5px"
            }}>
              Approve
            </button>
          </div>

        </div>
      )}

      {/* Dashboard */}
      <div style={{
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
      }}>
        <h3>Approved Cases Dashboard</h3>

        {dashboard.length === 0 && <p>No approved cases yet.</p>}

        {dashboard.map((item, index) => (
          <div key={index} style={{
            border: "1px solid #ddd",
            margin: "10px 0",
            padding: "10px",
            borderRadius: "8px"
          }}>
            <p><b>Action:</b> {item.action_plan?.action_required}</p>
            <p>
              <b>Urgency:</b>{" "}
              <span style={{ color: getColor(item.action_plan?.urgency_level) }}>
                {item.action_plan?.urgency_level}
              </span>
            </p>
            <p><b>Deadline:</b> {item.action_plan?.deadline}</p>
          </div>
        ))}
      </div>

    </div>
  );
}

export default App;


