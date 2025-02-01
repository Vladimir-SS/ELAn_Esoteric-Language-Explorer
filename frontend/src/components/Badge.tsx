
import React from "react";

interface BadgeProps {
  title: string;
  isEsolang?: boolean;
}

const Badge: React.FC<BadgeProps> = ({ title, isEsolang }) => (
  <div className="col-md-3 mx-1 my-2">
    <div className="card">
      <div
        className="card-body"
        style={{ display: "flex", flexDirection: "column" }}
      >
        <h5
          className="card-title text-truncate mb-3"
          title={decodeURIComponent(title)}
        >
          {decodeURIComponent(title).split("/").pop()}
        </h5>
        <button
          className="btn btn-sm btn-primary"
          style={{ width: "fit-content", alignSelf: "end" }}
          onClick={() => (window.location.href = isEsolang ? `/esolangs/${title}` :  `${title}`)}
        >
            {isEsolang ? "See more" : "See languages"}
        </button>
      </div>
    </div>
  </div>
);

export default Badge;