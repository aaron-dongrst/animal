import React from "react";
import "./AnalysisResults.css";

const AnalysisResults = ({ analysis }) => {
  if (!analysis) return null;

  const isHealthy = analysis.is_healthy;
  const healthStatusClass = isHealthy === true ? "healthy" : isHealthy === false ? "unhealthy" : "unknown";

  return (
    <div className="analysis-results">
      <h3 className="section-title">Analysis Results</h3>
      
      <div className="results-grid">
        <div className="result-card">
          <div className="result-label">Species</div>
          <div className="result-value">{analysis.species || "N/A"}</div>
        </div>

        <div className="result-card">
          <div className="result-label">Behavior Observed</div>
          <div className="result-value">{analysis.behavior_observed || "N/A"}</div>
        </div>

        <div className="result-card">
          <div className="result-label">Duration</div>
          <div className="result-value">
            {analysis.length_seconds ? `${analysis.length_seconds}s (${analysis.length_minutes}min)` : "N/A"}
          </div>
        </div>

        <div className="result-card">
          <div className="result-label">Pattern</div>
          <div className="result-value">
            {analysis.is_repeating ? "Repetitive" : "Normal"}
          </div>
        </div>

        <div className="result-card">
          <div className="result-label">Confidence</div>
          <div className="result-value">
            {analysis.confidence ? `${(analysis.confidence * 100).toFixed(1)}%` : "N/A"}
          </div>
        </div>

        <div className={`result-card health-status ${healthStatusClass}`}>
          <div className="result-label">Health Status</div>
          <div className="result-value-large">
            {isHealthy === true ? "Healthy" : isHealthy === false ? "Unhealthy" : "Unknown"}
          </div>
        </div>
      </div>

      {analysis.reasoning && (
        <div className="reasoning-section">
          <h4 className="reasoning-title">Assessment Reasoning</h4>
          <p className="reasoning-text">{analysis.reasoning}</p>
        </div>
      )}

      {analysis.recommendations && (
        <div className="recommendations-section">
          <h4 className="recommendations-title">Recommendations</h4>
          <div className="recommendations-text">
            {analysis.recommendations.split('\n').map((rec, index) => (
              rec.trim() && (
                <div key={index} className="recommendation-item">
                  {rec.trim()}
                </div>
              )
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;

