import React, { useState, useEffect } from "react";
import FilterDropdown from "./FilterDropdown";
import { FilterName, toSnakeCase } from "../constants/constants";

interface FiltersPanelProps {
  onEsolangsChanged: (esolangs: string[]) => void;
}

const FiltersPanel: React.FC<FiltersPanelProps> = ({ onEsolangsChanged }) => {
  const [searchInput, setSearchInput] = useState<string>("");
  const [selectedFilters, setSelectedFilters] = useState<{ [key: string]: string[]; }>({});
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const handleSearchInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchInput(e.target.value);
  };

  const handleFilterChange = (filterName: string, value: string) => {
    setSelectedFilters((prevFilters) => {
      const currentFilterValues = prevFilters[filterName] ?? [];

      if (!currentFilterValues.includes(value)) {
        return {
          ...prevFilters,
          [filterName]: [...currentFilterValues, value],
        };
      }

      return prevFilters;
    });
  };

  const removeFilter = (filterName: string, value: string) => {
    setSelectedFilters((prevFilters) => {
      const currentFilterValues = prevFilters[filterName] ?? [];
      const updatedFilterValues = currentFilterValues.filter(
        (filterValue) => filterValue !== value
      );
      return {
        ...prevFilters,
        [filterName]: updatedFilterValues,
      };
    });
  };

  const createQueryParams = () => {
    const queryParams = Object.entries(selectedFilters)
      .map(([key, values]) =>
        values.map((value) => `${toSnakeCase(key)}=${encodeURIComponent(value)}`))
      .flat()
      .join("&");

    if (!searchInput) {
      return queryParams;
    }

    return queryParams + `&search_term=${encodeURIComponent(searchInput)}`;
  };

  const handleApplyFilters = async () => {
    try {
      const queryParams = createQueryParams();
      const url = `/api/esolangs/search/?${queryParams}`;
      console.log(url);
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error("Languages not found");
      }
      const data = await response.json();
      console.log(data);

      onEsolangsChanged(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const FilterBadge = React.memo(({ filterName, value, onRemove }: any) => (
    <span className="badge bg-secondary m-1 text-truncate" title={value}>
      <button
        className="btn-close me-1"
        onClick={() => onRemove(filterName, value)}
      />
      {value}
    </span>
  ));

  return (
    <div className="container mt-4 mb-4">
      <div className="input-group w-50 mb-3">
        <input
          type="text"
          className="form-control rounded-left border-end-0"
          value={searchInput}
          onChange={handleSearchInputChange}
          placeholder="Search esolangs..."
        />
        <button
          className="btn btn-primary"
          type="button"
          onClick={handleApplyFilters}
        >
          Search
        </button>
      </div>
      <div className="mb-3" style={{ display: "flex" }}>
        <FilterDropdown
          filterName={FilterName.YearCreated}
          onFilterChange={handleFilterChange}
        />
        <FilterDropdown
          filterName={FilterName.Paradigm}
          onFilterChange={handleFilterChange}
        />
        <FilterDropdown
          filterName={FilterName.Category}
          onFilterChange={handleFilterChange}
        />
        <FilterDropdown
          filterName={FilterName.MemorySystem}
          onFilterChange={handleFilterChange}
        />
        <FilterDropdown
          filterName={FilterName.Dimension}
          onFilterChange={handleFilterChange}
        />
        <FilterDropdown
          filterName={FilterName.ComputationalClass}
          onFilterChange={handleFilterChange}
        />
        <FilterDropdown
          filterName={FilterName.FileExtension}
          onFilterChange={handleFilterChange}
        />
        <FilterDropdown
          filterName={FilterName.TypeSystem}
          onFilterChange={handleFilterChange}
        />
        <FilterDropdown
          filterName={FilterName.Dialect}
          onFilterChange={handleFilterChange}
        />
      </div>
      <div>
        <div className="mb-3">
          {Object.keys(selectedFilters).length > 0 && (
            <div>
              <strong className="me-2">Selected Filters:</strong>
              <div style={{ display: "flex", flexWrap: "wrap" }}>
                {Object.entries(selectedFilters).map(([filterName, values]) =>
                  values.map((value) => (
                    <FilterBadge
                      key={`${filterName}-${value}`}
                      filterName={filterName}
                      value={value}
                      onRemove={removeFilter}
                    />
                  ))
                )}
              </div>
            </div>
          )}
        </div>
        <div>
          <button className="btn btn-primary" onClick={handleApplyFilters}>
            Filter Esolangs
          </button>
        </div>
      </div>
    </div>
  );
};

export default FiltersPanel;
