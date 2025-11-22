import React from "react";
import "./AnimalParameters.css";

const AnimalParameters = ({ animal, onChange }) => {
  const handleChange = (field, value) => {
    onChange(field, value);
  };

  return (
    <div className="animal-parameters">
      <h3 className="section-title">Animal Information</h3>
      
      <div className="parameters-grid">
        <div className="parameter-group">
          <label htmlFor="species" className="parameter-label">
            Species <span className="required">*</span>
          </label>
          <input
            id="species"
            type="text"
            className="parameter-input"
            placeholder="e.g., Bear, Gorilla, Rabbit"
            value={animal.species}
            onChange={(e) => handleChange("species", e.target.value)}
            required
          />
        </div>

        <div className="parameter-group">
          <label htmlFor="age" className="parameter-label">
            Age
          </label>
          <input
            id="age"
            type="text"
            className="parameter-input"
            placeholder="e.g., 5 years, 2 months"
            value={animal.age}
            onChange={(e) => handleChange("age", e.target.value)}
          />
        </div>

        <div className="parameter-group">
          <label htmlFor="diet" className="parameter-label">
            Diet
          </label>
          <select
            id="diet"
            className="parameter-input"
            value={animal.diet}
            onChange={(e) => handleChange("diet", e.target.value)}
          >
            <option value="">Select diet...</option>
            <option value="herbivore">Herbivore</option>
            <option value="carnivore">Carnivore</option>
            <option value="omnivore">Omnivore</option>
            <option value="insectivore">Insectivore</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="parameter-group full-width">
          <label htmlFor="healthConditions" className="parameter-label">
            Existing Health Conditions
          </label>
          <textarea
            id="healthConditions"
            className="parameter-input parameter-textarea"
            placeholder="e.g., Arthritis, Previous injury, None"
            value={animal.healthConditions}
            onChange={(e) => handleChange("healthConditions", e.target.value)}
            rows="3"
          />
        </div>
      </div>
    </div>
  );
};

export default AnimalParameters;

