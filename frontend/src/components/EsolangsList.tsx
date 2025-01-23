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
        return <div>Loading languages...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h1>Esoteric Language List</h1>

            <div className="language-grid">
                {languages.length > 0 ? (
                    languages.map((language, index) => (
                        <div className="language-item" key={index}>
                            <Link to={`/esolangs/${decodeURIComponent(language)}`} className="language-link">
                                {decodeURIComponent(language)}
                            </Link>
                        </div>
                    ))
                ) : (
                    <div>No languages match the selected filters</div>
                )}
            </div>
        </div>
    );
};

export default EsolangsList;