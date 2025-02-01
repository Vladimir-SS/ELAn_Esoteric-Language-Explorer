import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Pagination from "./Pagination";
import FiltersPanel from "./FiltersPanel";

const EsolangsList: React.FC = () => {
    const [languages, setLanguages] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [currentPage, setCurrentPage] = useState<number>(1);
    const itemsPerPage = 15;

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

    const onEsolangsChanged = (data: string[]) => {
        setLanguages(data);
    }

    if (loading) {
        return <div className="text-center mt-5">Loading...</div>;
    }

    if (error || !languages) {
        return <div className="alert alert-danger text-center mt-5">{error ?? "Language not found"}</div>;
    }

    // Pagination logic
    const totalPages = Math.ceil(languages.length / itemsPerPage);
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentLanguages = languages.slice(indexOfFirstItem, indexOfLastItem);

    const handlePageChange = (page: number) => {
        setCurrentPage(page);
    };

    return (
        <div className="container-fluid mt-4">
            <h1 className="mb-4">Esoteric Language List ({languages.length} languages)</h1>
            <FiltersPanel onEsolangsChanged={onEsolangsChanged} />
            <div className="row d-flex flex-wrap justify-content-start g-3">
                {currentLanguages.length > 0 ? (
                    <div className="row">
                        {currentLanguages.map((language, index) => {
                            const decodedName = decodeURIComponent(language);
                            return (
                                <div className="col-md-4" key={index}>
                                    <div className="card">
                                        <div className="card-body">
                                            <h5 className="card-title text-truncate" title={decodedName}>
                                                <Link to={`/esolangs/${language}`} className="stretched-link">
                                                    {decodedName}
                                                </Link>
                                            </h5>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                ) : (
                    <div className="col-12">
                        <div className="alert alert-info">No languages match the selected filters.</div>
                    </div>
                )}
            </div>

            {/* Pagination Component */}
            <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
                visiblePages={5}
            />
        </div>);
};

export default EsolangsList;