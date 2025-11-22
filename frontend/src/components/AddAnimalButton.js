import React from "react";
import "./AddAnimalButton.css";

const AddAnimalButton = ({ onAdd }) => {
  return (
    <button className="add-animal-button" onClick={onAdd}>
      <span className="add-icon">+</span>
      <span className="add-text">Add New Animal</span>
    </button>
  );
};

export default AddAnimalButton;

