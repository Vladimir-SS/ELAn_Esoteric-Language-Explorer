import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Badge from "./Badge";

type PropertyDetailsProps = {
    propertyPath: string;
};

const PropertyDetails: React.FC<PropertyDetailsProps> = ({ propertyPath }) => {
  const { name } = useParams<{ name: string }>();
  const [languages, setLanguages] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPropertyLanguages = async () => {
      try {
        const encodedName = encodeURIComponent(name ?? "");
        const url = `/api/esolangs/search/?${propertyPath}=${encodedName}`;
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error("Languages not found");
        }
        const data = await response.json();
        setLanguages(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPropertyLanguages();
  }, [name]);

  if (loading) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  if (error || !languages) {
    return (
      <div className="alert alert-danger text-center mt-5">
        {error ?? "Languages not found"}
      </div>
    );
  }

  return (
    <div className="container-fluid mt-5">
      <h1 className="mb-4">
        List of languages having {decodeURIComponent(name ?? "")} {decodeURIComponent(propertyPath).replace("-", " ")}
      </h1>
      <div className="row d-flex flex-wrap justify-content-start g-3">
        {languages.length > 0 && (
          <div className="row">
            {languages.map((language, index) => {
              return <Badge key={index} title={language} isEsolang/>;
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default PropertyDetails;
