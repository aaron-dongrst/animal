import React, { useState } from "react";
import "./Enclosure.css";
import AnimalParameters from "./AnimalParameters";
import VideoUpload from "./VideoUpload";
import AnalysisResults from "./AnalysisResults";

const Enclosure = ({ enclosure, onUpdate, onRemove, canRemove }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const handleParameterChange = (field, value) => {
    onUpdate({
      animal: {
        ...enclosure.animal,
        [field]: value
      }
    });
  };

  const handleVideoChange = (file) => {
    onUpdate({ video: file, analysis: null, error: null });
  };

  const handleAnalyze = async () => {
    if (!enclosure.video) {
      onUpdate({ error: "Please upload a video first" });
      return;
    }

    if (!enclosure.animal.species) {
      onUpdate({ error: "Please enter the animal species" });
      return;
    }

    onUpdate({ loading: true, error: null, analysis: null });

    const formData = new FormData();
    formData.append("video", enclosure.video);
    formData.append("species", enclosure.animal.species);
    formData.append("age", enclosure.animal.age || "");
    formData.append("diet", enclosure.animal.diet || "");
    formData.append("health_conditions", enclosure.animal.healthConditions || "");

    try {
      const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Analysis failed");
      }

      const data = await response.json();
      onUpdate({ analysis: data, loading: false, error: null });
    } catch (error) {
      onUpdate({ 
        error: error.message || "Failed to analyze video. Please check if the backend is running.",
        loading: false 
      });
    }
  };

  return (
    <div className="enclosure-card">
      <div className="enclosure-header">
        <div className="enclosure-title-section">
          <h2 className="enclosure-title">{enclosure.name}</h2>
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
            aria-label="Remove enclosure"
          >
            ×
          </button>
        )}
      </div>

      {isExpanded && (
        <div className="enclosure-content">
          <AnimalParameters
            animal={enclosure.animal}
            onChange={handleParameterChange}
          />

          <VideoUpload
            video={enclosure.video}
            onChange={handleVideoChange}
          />

          <div className="analyze-section">
            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={enclosure.loading || !enclosure.video || !enclosure.animal.species}
            >
              {enclosure.loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                "🔍 Analyze Animal Health"
              )}
            </button>
          </div>

          {enclosure.error && (
            <div className="error-message">
              ⚠️ {enclosure.error}
            </div>
          )}

          {enclosure.analysis && (
            <AnalysisResults analysis={enclosure.analysis} />
          )}
        </div>
      )}
    </div>
  );
};

export default Enclosure;

