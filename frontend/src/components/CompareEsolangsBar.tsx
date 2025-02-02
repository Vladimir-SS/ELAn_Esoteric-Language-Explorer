import React, { useState } from "react";
import { useEsolangCompare } from "../context/EsolangCompareContext";
import { useNavigate } from "react-router-dom";

const CompareEsolangsBar: React.FC = () => {
  const { selectedLanguages, removeLanguage } = useEsolangCompare();
  const navigate = useNavigate();
  const [isAtBottom, setIsAtBottom] = useState(true);

  const togglePosition = () => {
    setIsAtBottom(!isAtBottom);
  };

  if (selectedLanguages.length === 0) return;

  return (
    <div
      className={`sticky-language-bar medium-badge ${
        isAtBottom ? "bottom" : "top"
      }`}
    >
      <div className="drag-button-container mt-2">
        <button
          className="btn btn-outline"
          type="button"
          onClick={togglePosition}
        >
          ↕
        </button>
      </div>

      {selectedLanguages.map((language) => (
        <div
          className="badge bg-secondary my-1 me-4 d-flex justify-content-between align-items-center"
          key={language}
        >
          <p className="card-title text-truncate">{language}</p>
          <button
            className="btn btn-outline"
            type="button"
            onClick={() => removeLanguage(language)}
          >
            ✕
          </button>
        </div>
      ))}
      {selectedLanguages.length === 2 && (
        <button
          className="btn btn-primary mt-1 me-4"
          onClick={() => navigate("/compare")}
        >
          Compare
        </button>
      )}
    </div>
  );
};

export default CompareEsolangsBar;
