import React, { useState } from "react";
import FilterDropdown from "./FilterDropdown";
import { FilterName, toSnakeCase } from "../constants/constants";
import FilterBadge from "./FilterBadge";
import { toast } from "react-toastify";
import SearchBar from "./SearchBar";

interface FiltersPanelProps {
  onEsolangsChanged: (esolangs: string[]) => void;
}

const FiltersPanel: React.FC<FiltersPanelProps> = ({ onEsolangsChanged }) => {
  const [searchInput, setSearchInput] = useState<string>("");
  const [selectedFilters, setSelectedFilters] = useState<{ [key: string]: string[]; }>({});

  const handleSearchInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchInput(e.target.value);
  };

  const clearSearchInput = () => {
    setSearchInput("");
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
          onEsolangsChanged([]);
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
        }
        onEsolangsChanged(data);
      }
    } catch (err: any) {
      toast.error(`Error: ${err.message}`, {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: true,
      });
    }
  };



  return (
    <div className="container-fluid mt-4 mb-4">
      <SearchBar
        searchInput={searchInput}
        onSearchInputChange={handleSearchInputChange}
        onClearSearch={clearSearchInput}
        onSearch={handleApplyFilters}
      />
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
