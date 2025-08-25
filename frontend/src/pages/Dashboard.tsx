import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BarChart3, Cloud, Radar, Droplets, TrendingUp, MessageSquare, User } from "lucide-react";
import { Link } from "react-router-dom";
import Navbar from "@/components/Navbar";

const Dashboard = () => {
  const features = [
    {
      title: "What-If Simulator",
      description: "Simulate crop growth scenarios with different conditions",
      icon: BarChart3,
      link: "/what-if-simulator",
      color: "success"
    },
    {
      title: "Pest Radar",
      description: "Monitor pest threats and disease risks in real-time",
      icon: Radar,
      link: "/pest-radar",
      color: "warning"
    },
    {
      title: "Smart Irrigation",
      description: "Optimize water usage with intelligent recommendations",
      icon: Droplets,
      link: "/smart-irrigation",
      color: "primary"
    },
    {
      title: "Risk & Income Forecasting",
      description: "Predict yields and forecast income potential",
      icon: TrendingUp,
      link: "/risk-forecast",
      color: "success"
    },
    {
      title: "AgriTwin Coach",
      description: "Get AI-powered farming advice and guidance",
      icon: MessageSquare,
      link: "/agritwin-coach",
      color: "primary"
    },
    {
      title: "Profile",
      description: "Manage your farm profile and notification settings",
      icon: User,
      link: "/profile", 
      color: "secondary"
    }
  ];

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">AgriTwin Dashboard</h1>
          <p className="text-muted-foreground text-lg">Your smart digital farm twin - manage all farming operations from one place</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="card-gradient border-border/50 hover:glow-primary transition-smooth group">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3 mb-2">
                  <div className={`p-2 rounded-lg bg-${feature.color}/10`}>
                    <feature.icon className={`h-6 w-6 text-${feature.color}`} />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </div>
                <CardDescription className="text-muted-foreground">
                  {feature.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Link to={feature.link}>
                  <Button variant="outline" className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-smooth">
                    Explore Feature
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;