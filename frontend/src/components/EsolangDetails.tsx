import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { Esolang } from "../constants/types";
import FieldList from "./FieldList";

const EsolangDetails: React.FC = () => {
  const { name } = useParams<{ name: string }>();

  const [language, setLanguage] = React.useState<Esolang>();
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  useEffect(() => {
    const fetchLanguage = async () => {
      try {
        console.log(name);
        const encodedName = encodeURIComponent(name ?? "");
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
    return (
      <div className="alert alert-danger text-center mt-5">
        {error ?? "Language not found"}
      </div>
    );
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
                {decodeURIComponent(language.url).split("/").pop()}
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

          <FieldList
            title="Paradigm(s)"
            items={language.paradigms ?? []}
          />
          <FieldList
            title="Influenced by"
            items={language.influencedBy ?? []}
          />
          <FieldList
            title="Influenced"
            items={language.influenced ?? []}
          />
          <FieldList
            title="File Extension(s)"
            items={language.fileExtensions ?? []}
            isLinkList={false}
          />
          <FieldList
            title="Computational Class(es)"
            items={language.computationalClasses ?? []}
          />
          <FieldList
            title="Type Systems"
            items={language.typeSystems ?? []}
          />
          <FieldList
            title="Dialects"
            items={language.dialects ?? []}
          />
          <FieldList
            title="Dimensions"
            items={language.dimensions ?? []}
          />
          <FieldList
            title="Memory System"
            items={language.memorySystem ?? []}
          />
          <FieldList
            title="Has categories"
            items={language.categories ?? []}
          />
        </div>
      </div>
    </div>
  );
};

export default EsolangDetails;