import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import { TrendingUp, DollarSign, Calendar, Target } from "lucide-react";
import Navbar from "@/components/Navbar";

const RiskForecast = () => {
  const yieldForecast = [
    { month: 'Jan', yield: 85, income: 42500 },
    { month: 'Feb', yield: 92, income: 46000 },
    { month: 'Mar', yield: 88, income: 44000 },
    { month: 'Apr', yield: 95, income: 47500 },
    { month: 'May', yield: 100, income: 50000 },
    { month: 'Jun', yield: 105, income: 52500 }
  ];

  const riskFactors = [
    { factor: 'Weather', risk: 35 },
    { factor: 'Market Price', risk: 20 },
    { factor: 'Pest/Disease', risk: 15 },
    { factor: 'Input Costs', risk: 25 },
    { factor: 'Labor', risk: 12 }
  ];

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">Risk & Income Forecasting</h1>
          <p className="text-muted-foreground text-lg">Predict yields and analyze income potential with risk assessment</p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="card-gradient glow-success">
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <Target className="h-8 w-8 text-success" />
                <div>
                  <p className="text-2xl font-bold text-success">95%</p>
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
                  <p className="text-2xl font-bold text-primary">₹47.5K</p>
                  <p className="text-sm text-muted-foreground">Monthly Income</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="card-gradient glow-success">
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <Calendar className="h-8 w-8 text-success" />
                <div>
                  <p className="text-2xl font-bold text-success">Apr 15</p>
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
                  <p className="text-2xl font-bold text-warning">Medium</p>
                  <p className="text-sm text-muted-foreground">Risk Level</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

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
                    <XAxis 
                      dataKey="month" 
                      stroke="hsl(var(--muted-foreground))"
                    />
                    <YAxis 
                      yAxisId="yield"
                      orientation="left"
                      stroke="hsl(var(--muted-foreground))"
                    />
                    <YAxis 
                      yAxisId="income"
                      orientation="right"
                      stroke="hsl(var(--muted-foreground))"
                    />
                    <Tooltip 
                      contentStyle={{
                        backgroundColor: 'hsl(var(--popover))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '0.5rem'
                      }}
                    />
                    <Line 
                      yAxisId="yield"
                      type="monotone" 
                      dataKey="yield" 
                      stroke="hsl(var(--success))" 
                      strokeWidth={3}
                      name="Yield %"
                      dot={{ fill: 'hsl(var(--success))', strokeWidth: 0, r: 4 }}
                    />
                    <Line 
                      yAxisId="income"
                      type="monotone" 
                      dataKey="income" 
                      stroke="hsl(var(--primary))" 
                      strokeWidth={3}
                      name="Income ₹"
                      dot={{ fill: 'hsl(var(--primary))', strokeWidth: 0, r: 4 }}
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
                  <BarChart data={riskFactors} layout="horizontal">
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis 
                      type="number"
                      domain={[0, 40]}
                      stroke="hsl(var(--muted-foreground))"
                    />
                    <YAxis 
                      dataKey="factor"
                      type="category"
                      width={80}
                      stroke="hsl(var(--muted-foreground))"
                    />
                    <Tooltip 
                      contentStyle={{
                        backgroundColor: 'hsl(var(--popover))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '0.5rem'
                      }}
                    />
                    <Bar 
                      dataKey="risk" 
                      fill="hsl(var(--warning))"
                      name="Risk Level %"
                      radius={[0, 4, 4, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              
              <div className="mt-6 space-y-3">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Overall Risk Score:</span>
                  <span className="font-medium text-warning">21.4% (Medium)</span>
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
      </main>
    </div>
  );
};

export default RiskForecast;