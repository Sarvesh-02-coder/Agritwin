import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

// ✅ Import i18n config (this initializes translations)
import "./i18n";

createRoot(document.getElementById("root")!).render(
  <App />
);
