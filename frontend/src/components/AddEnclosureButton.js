import React from "react";
import "./AddEnclosureButton.css";

const AddEnclosureButton = ({ onAdd }) => {
  return (
    <button className="add-enclosure-button" onClick={onAdd}>
      <span className="add-icon">+</span>
      <span className="add-text">Add New Enclosure</span>
    </button>
  );
};

export default AddEnclosureButton;

