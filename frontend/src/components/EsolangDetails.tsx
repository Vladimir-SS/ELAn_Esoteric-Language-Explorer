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
        return <div>Loading...</div>;
    }

    if (error || !language) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Esoteric Language Details for {decodeURIComponent(language.name)}</h1>

            <div>
                <div>
                    <strong>Data collected from:</strong> {language.url ? <a href={
                        language.url
                    }
                    >{decodeURIComponent(language.url)}</a> : "N/A"}
                </div>
                {language.alias ? <div><strong>Also known as:</strong> {language.alias}</div> : null}
                <p className="year"><strong>Created in:</strong> {language.yearCreated ? language.yearCreated : "N/A"}</p>
                <p><strong>Designed by:</strong> {language.designedBy ? language.designedBy : "N/A"}</p>
                <p><strong>Short Description:</strong> {language.shortDescription ? language.shortDescription : "N/A"}</p>
                {language.influencedBy && language.influencedBy.length > 0 &&
                    <p>
                        <strong>Influenced by:</strong>
                        {language.influencedBy.map((influencedBy, index) => (
                            <a key={index} href={influencedBy}>
                                {decodeURIComponent(influencedBy)}
                            </a>
                        ))}
                    </p>
                }

                {language.influenced && language.influenced.length > 0 &&
                    <p>
                        <strong>Influenced:</strong>
                        {language.influenced.map((influenced, index) => (
                            <a key={index} href={influenced}>
                                {decodeURIComponent(influenced)}
                            </a>
                        ))}
                    </p>
                }

                {language.fileExtensions && language.fileExtensions.length > 0 &&
                    <p>
                        <strong>File Extensions:</strong> {language.fileExtensions.join(", ")}
                    </p>
                }

                {language.categories && language.categories.length > 0 &&
                    <p>
                        <strong>Has categories:</strong>
                        {language.categories.map((category, index) => (
                            <a key={index} href={category}>
                                {decodeURIComponent(category)}
                            </a>
                        ))}
                    </p>
                }
            </div>
        </div>
    );
};

export default EsolangDetails;