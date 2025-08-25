import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, Shield, AlertCircle } from "lucide-react";
import Navbar from "@/components/Navbar";

const PestRadar = () => {
  const threats = [
    {
      id: 1,
      name: "Aphid Infestation",
      severity: "high",
      location: "North Field",
      description: "High aphid population detected in tomato crops",
      recommendation: "Apply neem oil spray immediately"
    },
    {
      id: 2,
      name: "Fungal Disease Risk",
      severity: "medium",
      location: "Greenhouse 2",
      description: "Humidity levels increasing fungal disease risk",
      recommendation: "Improve ventilation and reduce watering frequency"
    },
    {
      id: 3,
      name: "Beneficial Insects",
      severity: "low",
      location: "South Field",
      description: "Good population of ladybugs providing natural pest control",
      recommendation: "Continue current practices to maintain balance"
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'destructive';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'secondary';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high': return AlertTriangle;
      case 'medium': return AlertCircle;
      case 'low': return Shield;
      default: return AlertCircle;
    }
  };

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">Pest Radar</h1>
          <p className="text-muted-foreground text-lg">Monitor pest threats and disease risks across your farm</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Heatmap */}
          <div className="lg:col-span-2">
            <Card className="card-gradient">
              <CardHeader>
                <CardTitle>Risk Heatmap</CardTitle>
                <CardDescription>Visual representation of pest and disease risks across farm zones</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="relative h-64 bg-muted/20 rounded-lg overflow-hidden">
                  {/* Simulated heatmap zones */}
                  <div className="absolute inset-4 grid grid-cols-4 grid-rows-3 gap-2">
                    {/* High risk zone */}
                    <div className="bg-destructive/30 glow-danger rounded-lg flex items-center justify-center text-sm font-medium">
                      North<br/>HIGH
                    </div>
                    {/* Medium risk zones */}
                    <div className="bg-warning/30 glow-warning rounded-lg flex items-center justify-center text-sm font-medium">
                      East<br/>MED
                    </div>
                    <div className="bg-success/30 glow-success rounded-lg flex items-center justify-center text-sm font-medium">
                      Center<br/>LOW
                    </div>
                    <div className="bg-success/30 glow-success rounded-lg flex items-center justify-center text-sm font-medium">
                      West<br/>LOW
                    </div>
                    {/* Additional zones */}
                    <div className="bg-warning/30 glow-warning rounded-lg flex items-center justify-center text-sm font-medium">
                      GH2<br/>MED
                    </div>
                    <div className="bg-success/30 glow-success rounded-lg flex items-center justify-center text-sm font-medium">
                      GH1<br/>LOW
                    </div>
                    <div className="bg-success/30 glow-success rounded-lg flex items-center justify-center text-sm font-medium">
                      South<br/>LOW
                    </div>
                    <div className="bg-success/30 glow-success rounded-lg flex items-center justify-center text-sm font-medium">
                      Storage<br/>LOW
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between mt-4 text-sm text-muted-foreground">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-success rounded"></div>
                      <span>Low Risk</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-warning rounded"></div>
                      <span>Medium Risk</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-destructive rounded"></div>
                      <span>High Risk</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Alerts Panel */}
          <div>
            <Card className="card-gradient">
              <CardHeader>
                <CardTitle>Active Alerts</CardTitle>
                <CardDescription>Real-time pest and disease warnings</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {threats.map((threat) => {
                    const SeverityIcon = getSeverityIcon(threat.severity);
                    return (
                      <div key={threat.id} className="border border-border/50 rounded-lg p-4 transition-smooth hover:glow-primary">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <SeverityIcon className={`h-4 w-4 text-${getSeverityColor(threat.severity)}`} />
                            <h4 className="font-medium text-sm">{threat.name}</h4>
                          </div>
                          <Badge variant={getSeverityColor(threat.severity) as any} className="text-xs">
                            {threat.severity.toUpperCase()}
                          </Badge>
                        </div>
                        
                        <p className="text-xs text-muted-foreground mb-2">
                          📍 {threat.location}
                        </p>
                        
                        <p className="text-xs text-foreground mb-3">
                          {threat.description}
                        </p>
                        
                        <div className="bg-muted/30 rounded p-2">
                          <p className="text-xs font-medium text-success">
                            💡 {threat.recommendation}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PestRadar;