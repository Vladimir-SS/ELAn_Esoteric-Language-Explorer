import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const EsolangsList: React.FC = () => {
    const [languages, setLanguages] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchLanguages = async () => {
            try {

                const response = await fetch(`/api/esolangs`);
                if (!response.ok) {
                    throw new Error("Failed to fetch languages");
                }
                const data = await response.json();
                setLanguages(data);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchLanguages();
    }, []);

    if (loading) {
        return <div className="text-center mt-5">Loading...</div>;
    }

    if (error || !languages) {
        return <div className="alert alert-danger text-center mt-5">{error ?? "Language not found"}</div>;
    }

    return (
        <div className="container mt-4">
            <h1 className="mb-4">Esoteric Language List ({languages.length} languages)</h1>

            <div className="row d-flex flex-wrap justify-content-start g-3">
                {languages.length > 0 ? (
                    languages.map((language, index) => (
                        <div className="col-auto" key={index}>
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">
                                        <Link to={`/esolangs/${language}`} className="stretched-link">
                                            {decodeURIComponent(language)}
                                        </Link>
                                    </h5>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="col-12">
                        <div className="alert alert-info" role="alert">
                            No languages match the selected filters.
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EsolangsList;