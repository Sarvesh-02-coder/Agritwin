import { useState, useEffect, useMemo } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Droplets, CloudRain, Thermometer, AlertCircle } from "lucide-react";
import Navbar from "@/components/Navbar";

const SmartIrrigation = () => {
  const [waterUsage, setWaterUsage] = useState(65);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [profile, setProfile] = useState<any>(null); // ✅ active profile

  const refreshProfile = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/profile/");
      if (res.data.success && res.data.data.length > 0) {
        const active = res.data.data.find((p: any) => p.active);
        if (active) setProfile(active);
      }
    } catch (err) {
      console.error("Error refreshing profile:", err);
    }
  };

  // ✅ Step 1: fetch profile first
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/profile/");
        if (res.data.success && res.data.data.length > 0) {
          const active = res.data.data.find((p: any) => p.active);
          if (active) setProfile(active);
        }
      } catch (err) {
        console.error("Profile fetch error:", err);
        setError("Failed to fetch profile");
      }
    };

    fetchProfile();
  }, []);

  // ✅ Step 2: fetch irrigation after profile is loaded
  useEffect(() => {
    const fetchIrrigation = async () => {
      try {
        console.log("Fetching irrigation data...");
        const res = await axios.get("http://127.0.0.1:8000/irrigation/"); // 🔥 GET
        console.log("Irrigation API response:", res.data);
        setData(res.data);
      } catch (err: any) {
        console.error("Irrigation API error:", err);
        setError("Failed to fetch irrigation data");
      } finally {
        setLoading(false);
      }
    };

    if (profile) {
      fetchIrrigation();
    }
  }, [profile]);

  // ✅ build chart data with memo
  const weeklyData = useMemo(
    () =>
      data?.weather_weekly?.map((d: any) => ({
        day: d.day_name,
        rainfall: d.rainfall_mm,
        irrigation: d.irrigation_mm,
      })) || [],
    [data]
  );

  // ✅ calculate saved liters dynamically (fallback to demo value)
  const savedLiters =
    (data?.recommended_liters || 100) - (data?.actual_liters_used || 53);

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            Smart Irrigation
          </h1>
          <p className="text-muted-foreground text-lg">
            Optimize water usage with intelligent recommendations
          </p>
        </div>

        {loading && (
          <p className="text-center text-muted-foreground">
            Loading irrigation data...
          </p>
        )}

        {error && (
          <Card className="border-red-500 bg-red-50/10 text-red-600 mb-6">
            <CardHeader className="flex flex-row items-center space-x-2">
              <AlertCircle className="h-5 w-5" />
              <CardTitle>Error</CardTitle>
            </CardHeader>
            <CardContent>{error}</CardContent>
          </Card>
        )}

        {!loading && !error && data && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Daily Recommendation */}
            <div className="space-y-6">
              <Card className="card-gradient glow-primary">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Droplets className="h-6 w-6 text-primary" />
                    <span>Today's Recommendation</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center space-y-4">
                    <div className="text-4xl font-bold text-primary">
                      {data?.water_needed_mm?.toFixed(1) ?? "0.0"}mm
                    </div>
                    <p className="text-lg text-foreground">
                      {data?.rationale ?? "No recommendation available."}
                    </p>
                    <Badge
                      variant="outline"
                      className="bg-success/10 text-success border-success/20"
                    >
                      Optimal timing: 6:00 AM - 8:00 AM
                    </Badge>

                    <div className="grid grid-cols-2 gap-4 mt-6">
                      <div className="text-center">
                        <CloudRain className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                        <div className="text-2xl font-semibold">
                          {data?.weather_summary?.rainfall_7d_total?.toFixed(1) ??
                            "0.0"}
                          mm
                        </div>
                        <div className="text-sm text-muted-foreground">
                          7-Day Rainfall
                        </div>
                      </div>
                      <div className="text-center">
                        <Thermometer className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                        <div className="text-2xl font-semibold">
                          {data?.weather_summary?.temp_7d_avg?.toFixed(1) ??
                            "0.0"}
                          °C
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Avg Temp
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-gradient">
                <CardHeader>
                  <CardTitle>Water Usage Tracker</CardTitle>
                  <CardDescription>
                    Monitor your water consumption efficiency
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium">Weekly Usage</span>
                      <span className="text-sm text-muted-foreground">
                        {waterUsage}% of recommended
                      </span>
                    </div>
                    <Progress value={waterUsage} className="h-3" />

                    <div className="grid grid-cols-2 gap-4 pt-4">
                      <div className="text-center">
                        <div className="text-xl font-semibold text-primary">
                          {data?.water_needed_liters?.toLocaleString() ?? "0"}L
                        </div>
                        <div className="text-xs text-muted-foreground">
                          Required This Week
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="text-xl font-semibold text-success">
                          {savedLiters.toLocaleString()}L
                        </div>
                        <div className="text-xs text-muted-foreground">
                          Saved vs Target
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Weekly Comparison Chart */}
            <Card className="card-gradient">
              <CardHeader>
                <CardTitle>Weekly Water Analysis</CardTitle>
                <CardDescription>
                  Rainfall vs irrigation comparison for the week
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 w-full chart-enter">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={weeklyData}>
                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke="hsl(var(--border))"
                      />
                      <XAxis
                        dataKey="day"
                        stroke="hsl(var(--muted-foreground))"
                      />
                      <YAxis stroke="hsl(var(--muted-foreground))" />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "hsl(var(--popover))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: "0.5rem",
                        }}
                      />
                      <Bar
                        dataKey="rainfall"
                        fill="hsl(var(--accent))"
                        name="Rainfall (mm)"
                        radius={[2, 2, 0, 0]}
                      />
                      <Bar
                        dataKey="irrigation"
                        fill="hsl(var(--primary))"
                        name="Irrigation (mm)"
                        radius={[2, 2, 0, 0]}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="flex items-center justify-center space-x-6 mt-4 text-sm">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-accent rounded"></div>
                    <span>Rainfall</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-primary rounded"></div>
                    <span>Irrigation</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
};

export default SmartIrrigation;
