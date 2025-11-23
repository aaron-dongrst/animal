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

    try {
      const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5001";
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 300000);
      
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
        errorMessage = "Cannot connect to backend. Please make sure the backend is running on http://localhost:5001";
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
          <div className="animal-number-badge">{animal.name.replace(/^(Animal|Subject) /, '')}</div>
          <h2 className="animal-title">{animal.name}</h2>
          <button
            className="expand-button"
            onClick={() => setIsExpanded(!isExpanded)}
            aria-label={isExpanded ? "Collapse" : "Expand"}
          >
            <svg 
              viewBox="0 0 24 24" 
              fill="none" 
              xmlns="http://www.w3.org/2000/svg"
              className={isExpanded ? 'expanded' : ''}
            >
              <path d="M6 9L12 15L18 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
        {canRemove && (
          <button
            className="remove-button"
            onClick={onRemove}
            aria-label="Remove animal"
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        )}
      </div>

      <div className={`animal-content-wrapper ${isExpanded ? 'expanded' : 'collapsed'}`}>
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
                  <div className="spinner"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Analyze Behavior</span>
                </>
              )}
            </button>
          </div>

          {animal.error && (
            <div className="error-message">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 8V12M12 16H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <div className="error-text">{animal.error}</div>
            </div>
          )}

          {animal.analysis && (
            <AnalysisResults analysis={animal.analysis} />
          )}
        </div>
      </div>
    </div>
  );
};

export default Animal;
