import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { Esolang } from "../constants/types";
import FieldList from "./FieldList";
import { useEsolangCompare } from "../context/EsolangCompareContext";
import Badge from "./Badge";
import { toast } from "react-toastify";

interface EsolangDetailsProps {
  name?: string;
}

const EsolangDetails: React.FC<EsolangDetailsProps> = (props) => {
  const { name: paramName } = useParams<{ name: string }>();
  const name = props.name ?? paramName;

  const [language, setLanguage] = React.useState<Esolang>();
  const [similarLanguages, setSimilarLanguages] = React.useState<string[]>();
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const { addLanguage } = useEsolangCompare();

  useEffect(() => {
    const fetchLanguage = async () => {
      try {
        const encodedName = encodeURIComponent(name ?? "");
        const response = await fetch(`/api/esolangs/${encodedName}`);
        if (!response.ok) {
          throw new Error("Language not found");
        }
        const data = await response.json();
        setLanguage(data);
      } catch (err: any) {
        setError(err.message);
      }
    };

    const fetchSimilarLanguages = async () => {
      try {
        const encodedName = encodeURIComponent(name ?? "");
        const response = await fetch(`/api/esolangs/similar/${encodedName}`);
        if (!response.ok) {
          if (response.status === 404) {
            toast.warn("No similar languages found", {
              position: "top-right",
              autoClose: 3000,
              hideProgressBar: true,
            });
            setSimilarLanguages([]);
            return;
          }
          throw new Error("Similar languages not found");
        }
        const data = await response.json();
        setSimilarLanguages(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLanguage();
    fetchSimilarLanguages();
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

  const inCompareMode = !!props.name;

  return (
    <div className="container-fluid mt-5">
      {!inCompareMode && (
        <div className="d-flex justify-content-between flex-wrap align-items-center">
          <h1 className="mb-4">Esoteric Language Details</h1>
          <button
            className="btn btn-sm btn-outline-primary mx-2"
            onClick={() => name && addLanguage(name)}
          >
            Compare
          </button>
        </div>
      )}
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

          <FieldList title="Paradigm(s)" items={language.paradigms ?? []} />
          <FieldList
            title="Influenced by"
            items={language.influencedBy ?? []}
          />
          <FieldList title="Influenced" items={language.influenced ?? []} />
          <FieldList
            title="File Extension(s)"
            items={language.fileExtensions ?? []}
            isLinkList={false}
          />
          <FieldList
            title="Computational Class(es)"
            items={language.computationalClasses ?? []}
          />
          <FieldList title="Type Systems" items={language.typeSystems ?? []} />
          <FieldList title="Dialects" items={language.dialects ?? []} />
          <FieldList title="Dimensions" items={language.dimensions ?? []} />
          <FieldList
            title="Memory System"
            items={language.memorySystem ?? []}
          />
          <FieldList title="Has categories" items={language.categories ?? []} />
        </div>
      </div>
      {!inCompareMode && (
        <div className="card mt-4">
          {similarLanguages && similarLanguages.length > 0 ? (
            <div className="card-body">
              <h3 className="card-title">Similar languages</h3>
              <div className="row">
                {similarLanguages.map((language) => (
                  <Badge
                    key={language}
                    title={language}
                    isEsolang
                  />
                ))}
              </div>
            </div>
          ) : (
            <div className="card-body">No similar languages found</div>
          )}
        </div>
      )}
    </div>
  );
};

export default EsolangDetails;
