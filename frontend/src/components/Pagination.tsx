import React, { useEffect, useState } from "react";

interface PaginationProps {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    visiblePages?: number;
}

const Pagination: React.FC<PaginationProps> = ({ currentPage, totalPages, onPageChange, visiblePages = 5 }) => {
    const [dynamicVisiblePages, setDynamicVisiblePages] = useState<number>(visiblePages);
    const [showIcons, setShowIcons] = useState<boolean>(false);

    const updateVisiblePages = () => {
        if (window.innerWidth < 768) {
            setDynamicVisiblePages(2);
            setShowIcons(true);
        } else {
            setDynamicVisiblePages(visiblePages);
            setShowIcons(false);
        }
    };

    useEffect(() => {
        updateVisiblePages();

        window.addEventListener("resize", updateVisiblePages);

        return () => window.removeEventListener("resize", updateVisiblePages);
    }, [visiblePages]);


    const getPaginationItems = () => {
        let pages: (number | string)[] = [];
        const startPage = Math.max(1, currentPage - Math.floor(dynamicVisiblePages / 2));
        const endPage = Math.min(totalPages, startPage + dynamicVisiblePages - 1);

        if (startPage > 1) {
            pages.push(1);
            if (startPage > 2) pages.push("...");
        }

        for (let i = startPage; i <= endPage; i++) {
            pages.push(i);
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) pages.push("...");
            pages.push(totalPages);
        }

        return pages;
    };

    return (
        <nav className="mt-4">
            <ul className="pagination justify-content-center">
                <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
                    {showIcons ? (
                        <button className="page-link" onClick={() => onPageChange(1)} aria-label="First">
                            <span aria-hidden="true">&laquo;&laquo;</span>
                        </button>
                    ) : (
                        <button className="page-link" onClick={() => onPageChange(1)}>First</button>
                    )}
                </li>
                <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
                    {showIcons ? (
                        <button className="page-link" onClick={() => onPageChange(currentPage - 1)} aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </button>
                    ) : (
                        <button className="page-link" onClick={() => onPageChange(currentPage - 1)}>Previous</button>
                    )}
                </li>

                {getPaginationItems().map((page, index) => (
                    <li key={index} className={`page-item ${currentPage === page ? "active" : ""}`}>
                        {page === "..." ? (
                            <span className="page-link">...</span>
                        ) : (
                            <button className="page-link" onClick={() => onPageChange(page as number)}>
                                {page}
                            </button>
                        )}
                    </li>
                ))}

                <li className={`page-item ${currentPage === totalPages ? "disabled" : ""}`}>
                    {showIcons ? (
                        <button className="page-link" onClick={() => onPageChange(currentPage + 1)} aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </button>
                    ) : (
                        <button className="page-link" onClick={() => onPageChange(currentPage + 1)}>Next</button>
                    )}
                </li>
                <li className={`page-item ${currentPage === totalPages ? "disabled" : ""}`}>
                    {showIcons ? (
                        <button className="page-link" onClick={() => onPageChange(totalPages)} aria-label="Last">
                            <span aria-hidden="true">&raquo;&raquo;</span>
                        </button>
                    ) : (
                        <button className="page-link" onClick={() => onPageChange(totalPages)}>Last</button>
                    )}
                </li>
            </ul>
        </nav>
    );
};

export default Pagination;