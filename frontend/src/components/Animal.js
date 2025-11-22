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
      onUpdate({ error: "Please enter the animal species" });
      return;
    }

    onUpdate({ loading: true, error: null, analysis: null });

    const formData = new FormData();
    formData.append("video", animal.video);
    formData.append("species", animal.animal.species);
    formData.append("age", animal.animal.age || "");
    formData.append("diet", animal.animal.diet || "");
    formData.append("health_conditions", animal.animal.healthConditions || "");

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
                "Analyze Animal Health"
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

