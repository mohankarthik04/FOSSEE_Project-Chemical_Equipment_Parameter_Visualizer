import React, { useState, useEffect } from "react";
import axios from "axios";
import Charts from "./Charts";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/history/", auth);
      setHistory(res.data);
    } catch {
      console.log("History load failed");
    }
  };

  const USERNAME = "sri";         // Django username
  const PASSWORD = "Sri@0407";    // password

  const auth = {
  headers: {
    Authorization: "Basic " + btoa(USERNAME + ":" + PASSWORD),
  },
};


  const handleUpload = async () => {
    if (!file) return alert("Select CSV first");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      await axios.post("http://127.0.0.1:8000/upload/", formData, auth);
      const res = await axios.get("http://127.0.0.1:8000/summary/", auth);

      setSummary(res.data);
      fetchHistory();
    } catch {
      alert("Error connecting to server");
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/generate-pdf/", {
      responseType: "blob",
      headers: auth.headers,
  });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "equipment_report.pdf");
      document.body.appendChild(link);
      link.click();
    } catch {
      alert("PDF generation failed");
    }
  };

  const loadHistoryItem = (item) => setSummary(item.summary);

  const format = (val, unit) =>
    val !== undefined && val !== null ? `${Number(val).toFixed(3)} ${unit}` : "-";

  return (
    <div className="container my-5">
      <h1 className="text-center mb-4 fw-bold">
        ⚙ Equipment Data Analytics Dashboard
      </h1>

      <div className="card shadow-lg p-4 mb-4">
        <input
          type="file"
          className="form-control mb-3"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button className="btn btn-primary w-100" onClick={handleUpload}>
          {loading ? "Uploading..." : "📂 Upload CSV File"}
        </button>
      </div>

      {summary && (
        <>
          <div className="card shadow-sm p-4 mb-3 text-center bg-light">
            <h5>
              <strong>Total:</strong> {summary.total_count} |{" "}
              <strong>Avg. Flow:</strong> {format(summary.avg_flowrate, "m³/s")} |{" "}
              <strong>Avg. Pressure:</strong> {format(summary.avg_pressure, "Pa")} |{" "}
              <strong>Avg. Temp:</strong> {format(summary.avg_temperature, "°C")}
            </h5>
          </div>

          <div className="text-center mb-4">
            <button className="btn btn-success px-4 py-2" onClick={downloadPDF}>
              📄 Download PDF Report
            </button>
          </div>
        </>
      )}

      <Charts data={summary} />

      {summary?.type_distribution && (
        <div className="card shadow-lg p-4 mt-4">
          <h4 className="mb-3">Type Distribution Table</h4>
          <table className="table table-bordered table-striped text-center">
            <thead className="table-dark">
              <tr>
                <th>Equipment Type</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(summary.type_distribution).map(([key, value]) => (
                <tr key={key}>
                  <td>{key}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="card shadow-lg p-4 mt-5">
        <h4 className="mb-3">🕒 History</h4>
        <ul className="list-group">
          {history.map((item, index) => (
            <li
              key={index}
              className="list-group-item list-group-item-action"
              style={{ cursor: "pointer" }}
              onClick={() => loadHistoryItem(item)}
            >
              <strong>{item.time}</strong> — Total: {item.summary.total_count} |
              Flow: {format(item.summary.avg_flowrate, "m³/s")} |
              Pressure: {format(item.summary.avg_pressure, "Pa")} |
              Temp: {format(item.summary.avg_temperature, "°C")}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
