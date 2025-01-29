import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { Esolang } from "../constants/types";

const EsolangDetails: React.FC = () => {
    const { name } = useParams<{ name: string }>();

    const [language, setLanguage] = React.useState<Esolang>();
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState<string | null>(null);

    useEffect(() => {
        const fetchLanguage = async () => {
            try {
                console.log(name);
                const encodedName = encodeURIComponent(encodeURIComponent(name ?? ""));
                console.log(encodedName);
                const response = await fetch(`/api/esolangs/${encodedName}`);
                if (!response.ok) {
                    throw new Error("Language not found");
                }
                const data = await response.json();
                setLanguage(data);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchLanguage();
    }, [name]);

    if (loading) {
        return <div className="text-center mt-5">Loading...</div>;
    }

    if (error || !language) {
        return <div className="alert alert-danger text-center mt-5">{error ?? "Language not found"}</div>;
    }

    return (
      <div className="container mt-5">
        <div className="d-flex justify-content-between align-items-center">
          <h1>Esoteric Language Details</h1>
        </div>
        <div className="card">
          <div className="card-body">
            <h1 className="card-title">{decodeURIComponent(language.name)}</h1>

            <div className="mb-3">
              <strong>Data collected from:</strong>{" "}
              {language.url ? (
                <a href={language.url} className="link-primary">
                  {decodeURIComponent(language.url)}
                </a>
              ) : (
                "N/A"
              )}
            </div>

            {language.alias && (
              <div className="mb-3">
                <strong>Also known as:</strong> {language.alias}
              </div>
            )}

            <p className="mb-2">
              <strong>Created in:</strong>{" "}
              {language.yearCreated ? language.yearCreated : "N/A"}
            </p>
            <p className="mb-2">
              <strong>Designed by:</strong>{" "}
              {language.designedBy ? language.designedBy : "N/A"}
            </p>
            <p className="mb-2">
              <strong>Short Description:</strong>{" "}
              {language.shortDescription ? language.shortDescription : "N/A"}
            </p>
            {language.paradigms && language.paradigms.length > 0 && (
              <p className="mb-2">
                <strong>Paradigms:</strong>{" "}
                {language.paradigms.map((paradigm, index) => (
                  <a key={index} href={paradigm} className="link-primary me-2">
                    {decodeURIComponent(paradigm)}
                  </a>
                ))}
              </p>
            )}
            {language.influencedBy && language.influencedBy.length > 0 && (
              <p className="mb-2">
                <strong>Influenced by:</strong>{" "}
                {language.influencedBy.map((influencedBy, index) => (
                  <a
                    key={index}
                    href={influencedBy}
                    className="link-primary me-2"
                  >
                    {decodeURIComponent(influencedBy)}
                  </a>
                ))}
              </p>
            )}

            {language.influenced && language.influenced.length > 0 && (
              <p className="mb-2">
                <strong>Influenced:</strong>{" "}
                {language.influenced.map((influenced, index) => (
                  <a
                    key={index}
                    href={influenced}
                    className="link-primary me-2"
                  >
                    {decodeURIComponent(influenced)}
                  </a>
                ))}
              </p>
            )}

            {language.fileExtensions && language.fileExtensions.length > 0 && (
              <p className="mb-2">
                <strong>File Extensions:</strong>{" "}
                {language.fileExtensions.join(", ")}
              </p>
            )}

            {language.categories && language.categories.length > 0 && (
              <p className="mb-2">
                <strong>Has categories:</strong>{" "}
                {language.categories.map((category, index) => (
                  <a key={index} href={category} className="link-primary me-2">
                    {decodeURIComponent(category)}
                  </a>
                ))}
              </p>
            )}
          </div>
        </div>
      </div>
    );
};

export default EsolangDetails;