import { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  AlertTriangle,
  Shield,
  AlertCircle,
  Sprout,
  Loader2,
} from "lucide-react";
import Navbar from "@/components/Navbar";

const PestRadar = () => {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [threats, setThreats] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(
          "http://127.0.0.1:8000/agri-advisor/dashboard"
        );
        if (!res.ok) throw new Error("Failed to fetch data");
        const data = await res.json();

        setRecommendations(data.recommendations || []);
        setThreats(data.pest_alerts || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Map severity → badge/icon color
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return { badge: "destructive", text: "text-red-600" };
      case "medium":
        return { badge: "secondary", text: "text-yellow-500" };
      case "low":
        return { badge: "secondary", text: "text-green-600" };
      default:
        return { badge: "secondary", text: "text-muted-foreground" };
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "high":
        return AlertTriangle;
      case "medium":
        return AlertCircle;
      case "low":
        return Shield;
      default:
        return AlertCircle;
    }
  };

  return (
    <div className="min-h-screen dashboard-gradient">
      {/* ✅ Navbar always stays */}
      <Navbar />

      <main className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8 flex items-center space-x-3">
          <Sprout className="h-8 w-8 text-green-600" />
          <div>
            <h1 className="text-4xl font-bold text-foreground mb-2">
              Crop Recommendations
            </h1>
            <p className="text-muted-foreground text-lg">
              Best crop suggestions based on soil, weather, and season
            </p>
          </div>
        </div>

        {loading ? (
          // ✅ Loader
          <div className="flex justify-center items-center py-20">
            <Loader2 className="h-10 w-10 animate-spin text-primary" />
          </div>
        ) : error ? (
          // ✅ Error
          <p className="text-destructive text-center">❌ {error}</p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Crop Recommendations */}
            <div className="lg:col-span-2">
              <Card className="card-gradient">
                <CardHeader>
                  <CardTitle>Crop Recommendations</CardTitle>
                  <CardDescription>
                    Suggested crops to maximize yield and sustainability
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recommendations.map((rec, idx) => (
                      <div
                        key={idx}
                        className="border border-border/50 rounded-lg p-4 transition-smooth hover:glow-primary"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <Sprout className="h-4 w-4 text-green-600" />
                            <h4 className="font-medium text-sm">
                              {rec.crop}
                            </h4>
                          </div>
                          <Badge variant="secondary" className="text-xs">
                            Recommended
                          </Badge>
                        </div>

                        <p className="text-xs text-muted-foreground mb-2">
                          🌱 {rec.rationale || rec.reason}
                        </p>

                        <div className="bg-muted/30 rounded p-2">
                          <p className="text-xs font-medium text-green-600">
                            ✅ {rec.action || "Follow recommended practices"}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Pest Alerts */}
            <div>
              <Card className="card-gradient">
                <CardHeader>
                  <CardTitle>Active Pest Alerts</CardTitle>
                  <CardDescription>
                    Real-time pest and disease warnings
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {threats.map((threat, idx) => {
                      const severity = threat.risk || threat.severity || "low";
                      const { badge, text } = getSeverityColor(severity);
                      const SeverityIcon = getSeverityIcon(severity);

                      return (
                        <div
                          key={idx}
                          className="border border-border/50 rounded-lg p-4 transition-smooth hover:glow-primary"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              <SeverityIcon className={`h-4 w-4 ${text}`} />
                              <h4 className="font-medium text-sm">
                                {threat.pest || "Unknown Pest"}
                              </h4>
                            </div>
                            <Badge variant={badge as any} className="text-xs">
                              {severity.toUpperCase()}
                            </Badge>
                          </div>

                          <p className="text-xs text-foreground mb-3">
                            {threat.note || threat.description}
                          </p>

                          <div className="bg-muted/30 rounded p-2">
                            <p className="text-xs font-medium text-green-600">
                              💡{" "}
                              {threat.recommendation ||
                                "Monitor and apply preventive measures"}
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
        )}
      </main>
    </div>
  );
};

export default PestRadar;
