import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
const heroBackground = "/lovable-uploads/c887d4e8-7945-4192-8ee5-451037ceaae2.png";
import LanguageSelector from "@/components/LanguageSelector";

const Index = () => {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Language Selector */}
      <LanguageSelector />
      
      {/* Hero Background */}
      <div 
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: `url(${heroBackground})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center center',
          backgroundRepeat: 'no-repeat',
          imageRendering: 'crisp-edges',
          filter: 'contrast(1.05) saturate(1.1)'
        }}
      >
      </div>

      {/* Floating Particles */}
      <div className="absolute inset-0 z-10">
        <div className="particle-drift absolute top-20 left-10 w-2 h-2 bg-primary-glow rounded-full opacity-60"></div>
        <div className="particle-drift absolute top-40 right-20 w-3 h-3 bg-primary-glow rounded-full opacity-40" style={{ animationDelay: '2s' }}></div>
        <div className="particle-drift absolute bottom-40 left-20 w-2 h-2 bg-primary-glow rounded-full opacity-50" style={{ animationDelay: '4s' }}></div>
        <div className="particle-drift absolute bottom-60 right-10 w-1 h-1 bg-primary-glow rounded-full opacity-70" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Main Content */}
      <div className="relative z-20 min-h-screen flex items-center justify-center px-4">
        <div className="text-center max-w-4xl mx-auto">
          {/* Main Heading */}
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            AgriTwin
            <div className="text-3xl md:text-4xl font-normal text-white/90 mt-2">
              Your Smart Digital Farm Twin
            </div>
          </h1>

          {/* Subheading */}
          <p className="text-xl md:text-2xl text-white/80 mb-12 max-w-2xl mx-auto leading-relaxed">
            Transform your farming with AI-powered insights, real-time monitoring, and intelligent recommendations for optimal crop management.
          </p>

          {/* CTA Button */}
          <Link to="/dashboard">
            <Button 
              size="lg" 
              className="text-lg px-12 py-6 bg-white/10 text-white border border-white/20 hover:bg-white/20 glow-primary transition-bounce backdrop-blur-sm"
            >
              Explore Dashboard
            </Button>
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="absolute bottom-0 w-full z-20 bg-black/20 backdrop-blur-sm border-t border-white/10">
        <div className="container mx-auto px-4 py-4">
          <p className="text-center text-white/60 text-sm">
            © 2025 AgriTwin. Empowering farmers with smart agriculture technology.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
