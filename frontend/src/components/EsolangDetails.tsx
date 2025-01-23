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
                const response = await fetch(`/api/esolangs/${name}`);
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
        return <div>Loading...</div>;
    }

    if (error || !language) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Esoteric Language Details for {language.name}</h1>

            <div>
                <div>
                    <strong>Data collected from:</strong> {language.url ? <a href={
                        language.url
                    }
                    >{language.url}</a> : "N/A"}
                </div>
                {language.alias ? <div><strong>Also known as:</strong> {language.alias}</div> : null}
                <p className="year"><strong>Created in:</strong> {language.yearCreated ? language.yearCreated : "N/A"}</p>
                <p><strong>Designed by:</strong> {language.designedBy ? language.designedBy : "N/A"}</p>
                <p><strong>Short Description:</strong> {language.shortDescription ? language.shortDescription : "N/A"}</p>
                <p><strong>Categories:</strong> {language.categories ? language.categories.join(", ") : "N/A"}</p>
            </div>
        </div>
    );
};

export default EsolangDetails;