import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import Navbar from "@/components/Navbar";

const WhatIfSimulator = () => {
  const [sowingDelay, setSowingDelay] = useState([0]);
  const [irrigationDelay, setIrrigationDelay] = useState([0]);

  // Generate chart data based on slider values
  const generateChartData = () => {
    const baseYield = 100;
    const sowingImpact = sowingDelay[0] * -0.5;
    const irrigationImpact = irrigationDelay[0] * -0.3;
    
    return [
      { week: 'Week 1', yield: Math.max(20, baseYield * 0.2 + sowingImpact + irrigationImpact) },
      { week: 'Week 2', yield: Math.max(35, baseYield * 0.35 + sowingImpact + irrigationImpact) },
      { week: 'Week 3', yield: Math.max(50, baseYield * 0.5 + sowingImpact + irrigationImpact) },
      { week: 'Week 4', yield: Math.max(70, baseYield * 0.7 + sowingImpact + irrigationImpact) },
      { week: 'Week 5', yield: Math.max(85, baseYield * 0.85 + sowingImpact + irrigationImpact) },
      { week: 'Week 6', yield: Math.max(60, baseYield + sowingImpact + irrigationImpact) }
    ];
  };

  const chartData = generateChartData();

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">What-If Simulator</h1>
          <p className="text-muted-foreground text-lg">Simulate different farming scenarios and see their impact on crop yield</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Controls */}
          <div className="space-y-6">
            <Card className="card-gradient">
              <CardHeader>
                <CardTitle>Scenario Parameters</CardTitle>
                <CardDescription>Adjust the sliders to simulate different conditions</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <label className="text-sm font-medium text-foreground mb-3 block">
                    Sowing Delay: {sowingDelay[0]} days
                  </label>
                  <Slider
                    value={sowingDelay}
                    onValueChange={setSowingDelay}
                    max={30}
                    step={1}
                    className="w-full"
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium text-foreground mb-3 block">
                    Irrigation Delay: {irrigationDelay[0]} days
                  </label>
                  <Slider
                    value={irrigationDelay}
                    onValueChange={setIrrigationDelay}
                    max={15}
                    step={1}
                    className="w-full"
                  />
                </div>
              </CardContent>
            </Card>

            <Card className="card-gradient">
              <CardHeader>
                <CardTitle>Impact Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Expected Yield Impact:</span>
                    <span className={`font-medium ${(sowingDelay[0] + irrigationDelay[0]) > 10 ? 'text-destructive' : 'text-success'}`}>
                      {(sowingDelay[0] + irrigationDelay[0]) > 10 ? '-' : '+'}{Math.abs((sowingDelay[0] * 0.5 + irrigationDelay[0] * 0.3)).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Risk Level:</span>
                    <span className={`font-medium ${(sowingDelay[0] + irrigationDelay[0]) > 15 ? 'text-destructive' : (sowingDelay[0] + irrigationDelay[0]) > 7 ? 'text-warning' : 'text-success'}`}>
                      {(sowingDelay[0] + irrigationDelay[0]) > 15 ? 'High' : (sowingDelay[0] + irrigationDelay[0]) > 7 ? 'Medium' : 'Low'}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Chart */}
          <Card className="card-gradient">
            <CardHeader>
              <CardTitle>Crop Growth Simulation</CardTitle>
              <CardDescription>Projected yield over time based on your scenario</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-64 w-full chart-enter">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis 
                      dataKey="week" 
                      stroke="hsl(var(--muted-foreground))"
                    />
                    <YAxis 
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
                      type="monotone" 
                      dataKey="yield" 
                      stroke="hsl(var(--primary))" 
                      strokeWidth={3}
                      dot={{ fill: 'hsl(var(--primary))', strokeWidth: 0, r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default WhatIfSimulator;