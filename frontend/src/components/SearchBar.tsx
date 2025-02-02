import React from "react";

interface SearchBarProps {
  searchInput: string;
  onSearchInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onClearSearch: () => void;
  onSearch: () => void;
}

const SearchBar: React.FC<SearchBarProps> = ({
  searchInput,
  onSearchInputChange,
  onClearSearch,
  onSearch,
}) => {
  return (
    <div className="input-group mb-3 searchbar">
      <input
        type="text"
        className="form-control rounded-left border-end-0"
        value={searchInput}
        onChange={onSearchInputChange}
        placeholder="Search esolangs..."
      />
      {searchInput && (
        <button
          className="btn btn-outline-secondary"
          type="button"
          title="Clear search"
          onClick={onClearSearch}
        >
          ✕
        </button>
      )}
      <button className="btn btn-primary" type="button" onClick={onSearch}>
        Search
      </button>
    </div>
  );
};

export default SearchBar;
