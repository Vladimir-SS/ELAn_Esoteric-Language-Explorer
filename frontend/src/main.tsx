import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import { EsolangCompareProvider } from "./context/EsolangCompareContext";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <EsolangCompareProvider>
      <App />
    </EsolangCompareProvider>
  </StrictMode>
);
