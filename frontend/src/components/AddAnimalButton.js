import React from "react";
import "./AddAnimalButton.css";

const AddAnimalButton = ({ onAdd }) => {
  return (
    <button className="add-animal-button" onClick={onAdd}>
      <div className="add-button-content">
        <div className="add-icon-wrapper">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M5 12H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <span className="add-text">Add New Animal</span>
      </div>
    </button>
  );
};

export default AddAnimalButton;
