import React from "react";
import { useEsolangCompare } from "../context/EsolangCompareContext";
import { useNavigate } from "react-router-dom";

interface BadgeProps {
  title: string;
  isEsolang?: boolean;
  onCompare?: () => void;
}

const Badge: React.FC<BadgeProps> = ({ title, isEsolang }) => {
  const { addLanguage } = useEsolangCompare();
  const navigate = useNavigate();

  const decodedTitle = isEsolang ? decodeURIComponent(title) : decodeURIComponent(title).split("/").pop();

  return (
    <div className="col-md-3 mx-1 my-2">
      <div className="card">
        <div
          className="card-body"
          style={{ display: "flex", flexDirection: "column" }}
        >
          <h5 className="card-title text-truncate mb-3" title={decodedTitle}>
            {decodedTitle}
          </h5>
          <div style={{ alignSelf: "flex-end" }}>
            {isEsolang && (
              <button
                className="btn btn-sm btn-outline-primary mx-2"
                onClick={() => addLanguage(decodedTitle ?? "")}
              >
                Compare
              </button>
            )}
            <button
              className="btn btn-sm btn-primary"
              onClick={() =>
                navigate(isEsolang ? `/esolangs/${title}` : `${title}`)
              }
            >
              {isEsolang ? "See more" : "See languages"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Badge;
