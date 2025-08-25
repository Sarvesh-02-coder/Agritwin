import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu, Home, BarChart3, Radar, Droplets, TrendingUp, MessageSquare, User } from "lucide-react";

const Navbar = () => {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const navigationItems = [
    { name: "Dashboard", href: "/dashboard", icon: Home },
    { name: "What-If Simulator", href: "/what-if-simulator", icon: BarChart3 },
    { name: "Pest Radar", href: "/pest-radar", icon: Radar },
    { name: "Smart Irrigation", href: "/smart-irrigation", icon: Droplets },
    { name: "Risk Forecast", href: "/risk-forecast", icon: TrendingUp },
    { name: "AgriTwin Coach", href: "/agritwin-coach", icon: MessageSquare },
    { name: "Profile", href: "/profile", icon: User }
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-card/95 backdrop-blur-sm border-b border-border/50 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <img 
            src="/logo.png" 
            alt="AgriTwin Logo" 
            className="h-8 w-8 rounded-lg object-contain" 
            />
            <span className="text-xl font-bold text-foreground">AgriTwin</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link key={item.name} to={item.href}>
                  <Button
                    variant={isActive(item.href) ? "default" : "ghost"}
                    size="sm"
                    className={`transition-smooth ${
                      isActive(item.href) 
                        ? "glow-primary" 
                        : "hover:bg-primary/10"
                    }`}
                  >
                    <Icon className="h-4 w-4 mr-2" />
                    {item.name}
                  </Button>
                </Link>
              );
            })}
          </div>

          {/* Mobile Navigation */}
          <div className="lg:hidden">
            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon">
                  <Menu className="h-6 w-6" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-64">
                <div className="flex flex-col space-y-4 mt-8">
                  <Link to="/" className="flex items-center space-x-2 mb-4">
                    <div className="w-8 h-8 rounded-lg hero-gradient flex items-center justify-center glow-primary">
                      <span className="text-white font-bold text-sm">AT</span>
                    </div>
                    <span className="text-xl font-bold text-foreground">AgriTwin</span>
                  </Link>
                  
                  {navigationItems.map((item) => {
                    const Icon = item.icon;
                    return (
                      <Link 
                        key={item.name} 
                        to={item.href}
                        onClick={() => setIsOpen(false)}
                      >
                        <Button
                          variant={isActive(item.href) ? "default" : "ghost"}
                          className={`w-full justify-start transition-smooth ${
                            isActive(item.href) 
                              ? "glow-primary" 
                              : "hover:bg-primary/10"
                          }`}
                        >
                          <Icon className="h-4 w-4 mr-3" />
                          {item.name}
                        </Button>
                      </Link>
                    );
                  })}
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;