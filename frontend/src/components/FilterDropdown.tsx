import React, { useEffect, useState } from "react";
import { toKebabCase } from "../constants/constants";

interface Props {
  filterName: string;
  onFilterChange: (filterName: string, value: string) => void;
}

const FilterDropdown: React.FC<Props> = ({ filterName, onFilterChange }) => {
  const [options, setOptions] = useState<string[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const filterEndpoint = toKebabCase(filterName);
        const response = await fetch(`/api/${filterEndpoint}`);
        if (!response.ok) {
          throw new Error("Options not found");
        }
        const data = await response.json();
        console.log(data);
        setOptions(data.map((option: string) => decodeURIComponent(option).split("/").pop()));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchOptions();
    console.log("Fetched Options");
  }, [filterName]);

  const handleSelectionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOption = event.target.value;
    onFilterChange(filterName, selectedOption);
  };

  return (
    <div className="form-group me-2 small-badge">
      <label htmlFor={filterName} className="text-truncate" title={filterName}>
        {filterName}
      </label>
      <select
        className="form-control rounded-2"
        id={filterName}
        onChange={handleSelectionChange}
      >
        {loading && <option value="">Loading...</option>}
        {error && <option value="">{error}</option>}
        <option value="">Select options</option>
        {options &&
          options.map((option, index) => (
            <option
              key={`${option}-${index}`}
              value={option}
              title={option}
              className="text-truncate"
            >
              {option}
            </option>
          ))}
      </select>
    </div>
  );
};

export default FilterDropdown;
