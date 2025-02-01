import React from 'react';

const FilterBadge = React.memo(({ filterName, value, onRemove }: any) => (
    <span className="badge bg-secondary m-1 text-truncate" style={{ maxWidth: "calc(100vw - 40px)" }} title={value}>
        <button
            className="btn-close me-1"
            onClick={() => onRemove(filterName, value)}
        />
        {value}
    </span>
));

export default FilterBadge;