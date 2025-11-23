import React, { useState } from "react";
import "./Animal.css";
import AnimalParameters from "./AnimalParameters";
import VideoUpload from "./VideoUpload";
import AnalysisResults from "./AnalysisResults";

const Animal = ({ animal, onUpdate, onRemove, canRemove }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const handleParameterChange = (field, value) => {
    onUpdate({
      animal: {
        ...animal.animal,
        [field]: value
      }
    });
  };

  const handleVideoChange = (file) => {
    onUpdate({ video: file, analysis: null, error: null });
  };

  const handleAnalyze = async () => {
    if (!animal.video) {
      onUpdate({ error: "Please upload a video first" });
      return;
    }

    if (!animal.animal.species) {
      onUpdate({ error: "Please enter the pig breed or species" });
      return;
    }

    onUpdate({ loading: true, error: null, analysis: null });

    const formData = new FormData();
    formData.append("video", animal.video);
    formData.append("species", animal.animal.species || "Pig");
    formData.append("age", animal.animal.age || "");
    formData.append("diet", animal.animal.diet || "");
    formData.append("health_conditions", animal.animal.healthConditions || "");
    
    // Debug: Log what we're sending
    console.log("Sending request with:", {
      video: animal.video ? animal.video.name : "no video",
      species: animal.animal.species,
      age: animal.animal.age,
      diet: animal.animal.diet
    });

    try {
      const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5001";
      
      // Make the request with timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minute timeout
      
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);

      if (!response.ok) {
        let errorMessage = "Analysis failed";
        try {
          const errorData = await response.json();
          errorMessage = errorData.error || errorMessage;
        } catch (e) {
          errorMessage = `Server error: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      onUpdate({ analysis: data, loading: false, error: null });
    } catch (error) {
      let errorMessage = error.message;
      if (error.name === "AbortError") {
        errorMessage = "Request timed out. The video might be too large or processing is taking too long.";
      } else if (error.message.includes("Failed to fetch") || 
                 error.message.includes("NetworkError") ||
                 error.message.includes("Network request failed") ||
                 error.message.includes("fetch")) {
        errorMessage = "Cannot connect to backend. Please make sure:\n1. Backend is running (./START_BACKEND.sh)\n2. Backend is on http://localhost:5000\n3. No firewall is blocking the connection";
      }
      onUpdate({ 
        error: errorMessage,
        loading: false 
      });
    }
  };

  return (
    <div className="animal-card">
      <div className="animal-header">
        <div className="animal-title-section">
          <h2 className="animal-title">{animal.name}</h2>
          <button
            className="expand-button"
            onClick={() => setIsExpanded(!isExpanded)}
            aria-label={isExpanded ? "Collapse" : "Expand"}
          >
            {isExpanded ? "▼" : "▶"}
          </button>
        </div>
        {canRemove && (
          <button
            className="remove-button"
            onClick={onRemove}
            aria-label="Remove animal"
          >
            ×
          </button>
        )}
      </div>

      {isExpanded && (
        <div className="animal-content">
          <AnimalParameters
            animal={animal.animal}
            onChange={handleParameterChange}
          />

          <VideoUpload
            video={animal.video}
            onChange={handleVideoChange}
          />

          <div className="analyze-section">
            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={animal.loading || !animal.video || !animal.animal.species}
            >
              {animal.loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                "Analyze Pig Behavior"
              )}
            </button>
          </div>

          {animal.error && (
            <div className="error-message">
              {animal.error}
            </div>
          )}

          {animal.analysis && (
            <AnalysisResults analysis={animal.analysis} />
          )}
        </div>
      )}
    </div>
  );
};

export default Animal;

