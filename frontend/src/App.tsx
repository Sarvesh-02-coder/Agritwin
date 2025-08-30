import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Dashboard from "./pages/Dashboard";
import WhatIfSimulator from "./pages/WhatIfSimulator";
import PestRadar from "./pages/PestRadar";
import SmartIrrigation from "./pages/SmartIrrigation";
import RiskForecast from "./pages/RiskForecast";
import AgriTwinCoach from "./pages/AgriTwinCoach";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";
import LanguageSelector from "@/components/LanguageSelector"; // ✅ import
import "./i18n"; // ✅ initialize i18n once at root

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        {/* ✅ Global Language Selector */}
        <LanguageSelector />

        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/what-if-simulator" element={<WhatIfSimulator />} />
          <Route path="/pest-radar" element={<PestRadar />} />
          <Route path="/smart-irrigation" element={<SmartIrrigation />} />
          <Route path="/risk-forecast" element={<RiskForecast />} />
          <Route path="/agritwin-coach" element={<AgriTwinCoach />} />
          <Route path="/profile" element={<Profile />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
