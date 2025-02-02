import React, { createContext, useContext, useState, ReactNode } from "react";

interface LanguageContextType {
  selectedLanguages: string[];
  addLanguage: (language: string) => void;
  removeLanguage: (language: string) => void;
}

const EsolangCompareContext = createContext<LanguageContextType | undefined>(undefined);

interface LanguageProviderProps {
  children: ReactNode;
}

export const EsolangCompareProvider: React.FC<LanguageProviderProps> = ({ children }) => {
  const [selectedLanguages, setSelectedLanguages] = useState<string[]>([]);

  const addLanguage = (language: string) => {
    const decodedLanguage = decodeURIComponent(language);
    setSelectedLanguages((prev) =>
      [...new Set([...prev, decodedLanguage])].slice(0, 2)
    );
  };

  const removeLanguage = (language: string) => {
    setSelectedLanguages((prev) => prev.filter((l) => l !== language));
  };

  return (
    <EsolangCompareContext.Provider
      value={{ selectedLanguages, addLanguage, removeLanguage }}
    >
      {children}
    </EsolangCompareContext.Provider>
  );
};

export const useEsolangCompare = () => {
  const context = useContext(EsolangCompareContext);
  if (context === undefined) {
    throw new Error("useEsolangCompare must be used within a LanguageProvider");
  }
  return context;
};
