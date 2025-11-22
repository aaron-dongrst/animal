import React, { useState } from "react";
import axios from "axios";

function App() {
  const [video, setVideo] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleVideoUpload = (event) => {
    setVideo(event.target.files[0]);
    setResults(null);
    setError("");
  };

  const handleSubmit = async () => {
    if (!video) {
      setError("Please upload a video first.");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("video", video);

    try {
      const response = await axios.post("http://localhost:5000/classify", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(response.data);
    } catch (err) {
      setError("Failed to classify the video. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>FaunaVision</h1>
      <p>Upload a video of an animal to classify its action and health status.</p>

      <input type="file" accept="video/*" onChange={handleVideoUpload} />
      <button onClick={handleSubmit} disabled={loading} style={{ marginLeft: "10px" }}>
        {loading ? "Processing..." : "Classify Video"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {results && (
        <div style={{ marginTop: "20px" }}>
          <h2>Classification Results</h2>
          <p><strong>Action:</strong> {results.action}</p>
          <p><strong>Health Status:</strong> {results.health_status}</p>
          <h3>Recommendations</h3>
          <p>{results.recommendations}</p>
        </div>
      )}
    </div>
  );
}

export default App;
