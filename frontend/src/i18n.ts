import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import HttpBackend from "i18next-http-backend";

i18n
  .use(HttpBackend) // ✅ load translations from public/locales
  .use(LanguageDetector) // ✅ detect language (localStorage, browser, etc.)
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    interpolation: {
      escapeValue: false,
    },
    backend: {
      loadPath: "/locales/{{lng}}/translation.json", // ✅ path to translation files
    },
    detection: {
      order: ["localStorage", "navigator"], // ✅ check localStorage first
      caches: ["localStorage"], // ✅ save preference in localStorage
      lookupLocalStorage: "agritwin-language", // ✅ custom key name
    },
  });

export default i18n;
