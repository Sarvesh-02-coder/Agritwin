import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // change to your backend URL
});

// ✅ Interceptor to attach language param
api.interceptors.request.use((config) => {
  const lang = localStorage.getItem("agritwin-language") || "en";
  
  // Attach as query param
  config.params = { ...(config.params || {}), lang };

  // Or attach as header (if you prefer header-based)
  config.headers["X-Language"] = lang;

  return config;
});

export default api;
