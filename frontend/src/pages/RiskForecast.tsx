import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import { TrendingUp, DollarSign, Calendar, Target } from "lucide-react";
import Navbar from "@/components/Navbar";

interface YieldForecast {
  month: string;
  yield: number;
  income: number;
}

interface RiskFactor {
  factor: string;
  risk: number;
}

interface ForecastSummary {
  expected_yield_qtl: number;
  expected_income_inr: number;
  harvest_date_label: string;
  risk_level: string;
  overall_risk_pct: number;
}

const RiskForecast = () => {
  const [summary, setSummary] = useState<ForecastSummary | null>(null);
  const [yieldForecast, setYieldForecast] = useState<YieldForecast[]>([]);
  const [riskFactors, setRiskFactors] = useState<RiskFactor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const res = await fetch("http://localhost:8000/forecast/");
        if (!res.ok) throw new Error(`Error: ${res.status}`);
        const json = await res.json();

        if (json.success && json.data && json.data.forecast) {
          setSummary(json.data.forecast.summary);
          setYieldForecast(json.data.forecast.yieldForecast);
          setRiskFactors(json.data.forecast.riskFactors);
        } else {
          throw new Error("Invalid response structure");
        }
      } catch (err: any) {
        setError(err.message || "Failed to fetch forecast");
      } finally {
        setLoading(false);
      }
    };

    fetchForecast();
  }, []);

  return (
    <div className="min-h-screen dashboard-gradient">
      {/* ✅ Navbar always visible */}
      <Navbar />

      <main className="container mx-auto px-4 py-8">
        {loading ? (
          <div className="min-h-[60vh] flex items-center justify-center">
            <p className="text-lg text-muted-foreground">Loading forecast...</p>
          </div>
        ) : error || !summary ? (
          <div className="min-h-[60vh] flex items-center justify-center">
            <p className="text-lg text-red-500">{error || "No forecast data available"}</p>
          </div>
        ) : (
          <>
            {/* ✅ Your original content goes here (unchanged) */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-foreground mb-2">Risk & Income Forecasting</h1>
              <p className="text-muted-foreground text-lg">
                Predict yields and analyze income potential with risk assessment
              </p>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card className="card-gradient glow-success">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-2">
                    <Target className="h-8 w-8 text-success" />
                    <div>
                      <p className="text-2xl font-bold text-success">
                        {summary.expected_yield_qtl.toFixed(1)} qtl
                      </p>
                      <p className="text-sm text-muted-foreground">Expected Yield</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-gradient glow-primary">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-2">
                    <DollarSign className="h-8 w-8 text-primary" />
                    <div>
                      <p className="text-2xl font-bold text-primary">
                        ₹{(summary.expected_income_inr / 1000).toFixed(1)}K
                      </p>
                      <p className="text-sm text-muted-foreground">Expected Income</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-gradient glow-success">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-2">
                    <Calendar className="h-8 w-8 text-success" />
                    <div>
                      <p className="text-2xl font-bold text-success">{summary.harvest_date_label}</p>
                      <p className="text-sm text-muted-foreground">Harvest Date</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-gradient glow-warning">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-2">
                    <TrendingUp className="h-8 w-8 text-warning" />
                    <div>
                      <p className="text-2xl font-bold text-warning">{summary.risk_level}</p>
                      <p className="text-sm text-muted-foreground">Risk Level</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Yield & Income Forecast */}
              <Card className="card-gradient">
                <CardHeader>
                  <CardTitle>Yield & Income Forecast</CardTitle>
                  <CardDescription>6-month projection based on current conditions</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 w-full chart-enter">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={yieldForecast}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
                        <YAxis yAxisId="yield" orientation="left" stroke="hsl(var(--muted-foreground))" />
                        <YAxis yAxisId="income" orientation="right" stroke="hsl(var(--muted-foreground))" />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: "hsl(var(--popover))",
                            border: "1px solid hsl(var(--border))",
                            borderRadius: "0.5rem",
                          }}
                        />
                        <Line
                          yAxisId="yield"
                          type="monotone"
                          dataKey="yield"
                          stroke="hsl(var(--success))"
                          strokeWidth={3}
                          name="Yield (qtl)"
                          dot={{ fill: "hsl(var(--success))", r: 4 }}
                        />
                        <Line
                          yAxisId="income"
                          type="monotone"
                          dataKey="income"
                          stroke="hsl(var(--primary))"
                          strokeWidth={3}
                          name="Income (₹)"
                          dot={{ fill: "hsl(var(--primary))", r: 4 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Risk Analysis */}
              <Card className="card-gradient">
                <CardHeader>
                  <CardTitle>Risk Factor Analysis</CardTitle>
                  <CardDescription>Key risks that could impact your farm's performance</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 w-full chart-enter">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={riskFactors} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis type="number" domain={[0, 100]} stroke="hsl(var(--muted-foreground))" />
                        <YAxis
                          dataKey="factor"
                          type="category"
                          width={100}
                          stroke="hsl(var(--muted-foreground))"
                        />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: "hsl(var(--popover))",
                            border: "1px solid hsl(var(--border))",
                            borderRadius: "0.5rem",
                          }}
                        />
                        <Bar dataKey="risk" fill="#f59e0b" name="Risk Level %" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  <div className="mt-6 space-y-3">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-muted-foreground">Overall Risk Score:</span>
                      <span className="font-medium text-warning">
                        {summary.overall_risk_pct.toFixed(1)}% ({summary.risk_level})
                      </span>
                    </div>
                    <div className="bg-muted/30 rounded p-3">
                      <p className="text-xs text-success font-medium">
                        💡 Weather monitoring and crop insurance recommended for risk mitigation.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </>
        )}
      </main>
    </div>
  );
};

export default RiskForecast;
