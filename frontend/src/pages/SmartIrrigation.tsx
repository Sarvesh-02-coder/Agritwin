import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Droplets, CloudRain, Thermometer } from "lucide-react";
import Navbar from "@/components/Navbar";

const SmartIrrigation = () => {
  const [waterUsage, setWaterUsage] = useState(65);

  const weeklyData = [
    { day: 'Mon', rainfall: 5, irrigation: 15 },
    { day: 'Tue', rainfall: 0, irrigation: 20 },
    { day: 'Wed', rainfall: 12, irrigation: 8 },
    { day: 'Thu', rainfall: 0, irrigation: 18 },
    { day: 'Fri', rainfall: 3, irrigation: 12 },
    { day: 'Sat', rainfall: 0, irrigation: 20 },
    { day: 'Sun', rainfall: 8, irrigation: 10 }
  ];

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">Smart Irrigation</h1>
          <p className="text-muted-foreground text-lg">Optimize water usage with intelligent recommendations</p>
        </div>

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
                  <div className="text-4xl font-bold text-primary">20mm</div>
                  <p className="text-lg text-foreground">Irrigate your crops today</p>
                  <Badge variant="outline" className="bg-success/10 text-success border-success/20">
                    Optimal timing: 6:00 AM - 8:00 AM
                  </Badge>
                  
                  <div className="grid grid-cols-2 gap-4 mt-6">
                    <div className="text-center">
                      <CloudRain className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                      <div className="text-2xl font-semibold">2mm</div>
                      <div className="text-sm text-muted-foreground">Expected Rainfall</div>
                    </div>
                    <div className="text-center">
                      <Thermometer className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                      <div className="text-2xl font-semibold">28°C</div>
                      <div className="text-sm text-muted-foreground">Max Temperature</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="card-gradient">
              <CardHeader>
                <CardTitle>Water Usage Tracker</CardTitle>
                <CardDescription>Monitor your water consumption efficiency</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Weekly Usage</span>
                    <span className="text-sm text-muted-foreground">{waterUsage}% of recommended</span>
                  </div>
                  <Progress value={waterUsage} className="h-3" />
                  
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="text-center">
                      <div className="text-xl font-semibold text-primary">103L</div>
                      <div className="text-xs text-muted-foreground">Used This Week</div>
                    </div>
                    <div className="text-center">
                      <div className="text-xl font-semibold text-success">47L</div>
                      <div className="text-xs text-muted-foreground">Saved vs Target</div>
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
              <CardDescription>Rainfall vs irrigation comparison for the week</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-64 w-full chart-enter">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={weeklyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis 
                      dataKey="day" 
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
      </main>
    </div>
  );
};

export default SmartIrrigation;