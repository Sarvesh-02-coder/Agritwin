import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Languages } from "lucide-react";

type Language = {
  code: string;
  name: string;
  flag: string;
};

const languages: Language[] = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
  { code: 'mr', name: 'मराठी', flag: '🇮🇳' }
];

const LanguageSelector = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState<Language>(languages[0]);

  useEffect(() => {
    // Check if user has visited before
    const hasVisited = localStorage.getItem('agritwin-language-selected');
    if (!hasVisited) {
      setIsOpen(true);
    } else {
      const savedLanguage = localStorage.getItem('agritwin-language');
      if (savedLanguage) {
        const lang = languages.find(l => l.code === savedLanguage);
        if (lang) setSelectedLanguage(lang);
      }
    }
  }, []);

  const handleLanguageSelect = (language: Language) => {
    setSelectedLanguage(language);
    localStorage.setItem('agritwin-language', language.code);
    localStorage.setItem('agritwin-language-selected', 'true');
    setIsOpen(false);
  };

  return (
    <>
      {/* Language Toggle Button */}
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setIsOpen(true)}
        className="fixed top-4 right-4 z-50 bg-card/90 backdrop-blur-sm border border-border/50 hover:glow-primary transition-smooth"
      >
        <Languages className="h-4 w-4 mr-2" />
        {selectedLanguage.flag} {selectedLanguage.name}
      </Button>

      {/* Language Selection Modal */}
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-md card-gradient glow-primary">
          <DialogHeader className="text-center">
            <DialogTitle className="text-2xl font-bold mb-2">
              Welcome to AgriTwin
            </DialogTitle>
            <DialogDescription className="text-lg">
              Choose your preferred language
              <br />
              अपनी पसंदीदा भाषा चुनें
              <br />
              तुमची आवडती भाषा निवडा
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-3 mt-6">
            {languages.map((language) => (
              <Button
                key={language.code}
                variant={selectedLanguage.code === language.code ? "default" : "outline"}
                size="lg"
                className={`w-full justify-start text-left transition-smooth ${
                  selectedLanguage.code === language.code ? "glow-primary" : "hover:glow-primary"
                }`}
                onClick={() => handleLanguageSelect(language)}
              >
                <span className="text-2xl mr-3">{language.flag}</span>
                <span className="text-lg font-medium">{language.name}</span>
              </Button>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default LanguageSelector;