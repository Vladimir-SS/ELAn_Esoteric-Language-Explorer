export enum FilterName {
  Paradigm = "Paradigm",
  Category = "Category",
  YearCreated = "Year Created",
  MemorySystem = "Memory System",
  Dimension = "Dimension",
  ComputationalClass = "Computational Class",
  FileExtension = "File Extension",
  TypeSystem = "Type System",
  Dialect = "Dialect",
}

export const toKebabCase = (str: string): string => {
  return str
    .trim()
    .replace(/([a-z])([A-Z])/g, "$1-$2")
    .replace(/\s+/g, "-")
    .toLowerCase();
};

export const toSnakeCase = (str: string): string => {
    return str
        .trim()
        .replace(/([a-z])([A-Z])/g, "$1_$2")
        .replace(/\s+/g, "_")
        .toLowerCase();
    }