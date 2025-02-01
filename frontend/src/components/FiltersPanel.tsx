import React, { useState } from "react";
import FilterDropdown from "./FilterDropdown";
import { FilterName, toSnakeCase } from "../constants/constants";
import FilterBadge from "./FilterBadge";
import { toast } from "react-toastify";

interface FiltersPanelProps {
  onEsolangsChanged: (esolangs: string[]) => void;
}

const FiltersPanel: React.FC<FiltersPanelProps> = ({ onEsolangsChanged }) => {
  const [searchInput, setSearchInput] = useState<string>("");
  const [selectedFilters, setSelectedFilters] = useState<{ [key: string]: string[]; }>({});
  const [loading, setLoading] = React.useState(true);

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
      toast.info("Request is being processed...", {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: false,
        pauseOnHover: false,
        draggable: false,
        progress: undefined,
      });
      const queryParams = createQueryParams();
      const url = `/api/esolangs/search/?${queryParams}`;
      console.log(url);
      const response = await fetch(url);

      if (!response.ok) {
        if (response.status === 404) {
          toast.warn("No results found", {
            position: "top-right",
            autoClose: 3000,
            hideProgressBar: true,
          });
        } else {
          throw new Error("Languages not found");
        }
      } else {
        const data = await response.json();
        console.log(data);

        toast.success("Search successful", {
          position: "top-right",
          autoClose: 3000,
          hideProgressBar: true,
        });

        if (data.length === 0) {
          toast.warn("No results found", {
            position: "top-right",
            autoClose: 3000,
            hideProgressBar: true,
          });
        } else {
          onEsolangsChanged(data);
        }
      }
    } catch (err: any) {
      toast.error(`Error: ${err.message}`, {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: true,
      });
    } finally {
      setLoading(false);
    }
  };



  return (
    <div className="container-fluid mt-4 mb-4">
      <div className="input-group mb-3 searchbar">
        <input
          type="text"
          className="form-control rounded-left border-end-0"

          value={searchInput}
          onChange={handleSearchInputChange}
          placeholder="Search esolangs..."
        />
        {searchInput && (
          <button
            className="btn btn-outline-secondary"
            type="button"
            title="Clear search"
            onClick={() => setSearchInput("")}
          >
            ✕
          </button>
        )}
        <button
          className="btn btn-primary"
          type="button"
          onClick={handleApplyFilters}
        >
          Search
        </button>
      </div>
      <div className="mb-3 d-flex flex-wrap gap-2">
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
              <div className="d-flex flex-wrap">
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
      </div>
    </div>
  );
};

export default FiltersPanel;
