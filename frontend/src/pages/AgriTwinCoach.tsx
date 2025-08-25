import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { MessageSquare, Mic, Send, Bot } from "lucide-react";
import Navbar from "@/components/Navbar";

const AgriTwinCoach = () => {
  const [message, setMessage] = useState("");

  const sampleMessages = [
    {
      type: "bot",
      message: "Hello! I'm your AgriTwin Coach. I can help you with farming advice, crop recommendations, and answer any agricultural questions you have.",
      time: "10:30 AM"
    },
    {
      type: "user", 
      message: "What's the best time to plant tomatoes in my region?",
      time: "10:32 AM"
    },
    {
      type: "bot",
      message: "For optimal tomato growing, I recommend planting after the last frost date in your region. Based on your location, the ideal planting window is between March 15-30. Make sure soil temperature is consistently above 60°F (15°C).",
      time: "10:33 AM"
    }
  ];

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">AgriTwin Coach</h1>
          <p className="text-muted-foreground text-lg">Get AI-powered farming advice and guidance</p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card className="card-gradient h-[600px] flex flex-col">
            <CardHeader className="border-b border-border/50">
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-full bg-primary/10">
                  <Bot className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <CardTitle>AgriTwin Assistant</CardTitle>
                  <CardDescription>Your intelligent farming companion</CardDescription>
                </div>
              </div>
            </CardHeader>
            
            {/* Chat Messages */}
            <CardContent className="flex-1 overflow-y-auto p-6">
              <div className="space-y-4">
                {sampleMessages.map((msg, index) => (
                  <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] rounded-lg p-4 ${
                      msg.type === 'user' 
                        ? 'bg-primary text-primary-foreground' 
                        : 'bg-muted/50 text-foreground'
                    }`}>
                      <p className="text-sm">{msg.message}</p>
                      <p className={`text-xs mt-2 ${
                        msg.type === 'user' 
                          ? 'text-primary-foreground/70' 
                          : 'text-muted-foreground'
                      }`}>
                        {msg.time}
                      </p>
                    </div>
                  </div>
                ))}
                
                {/* Typing indicator placeholder */}
                <div className="flex justify-start">
                  <div className="bg-muted/30 rounded-lg p-4 max-w-[80%]">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-pulse"></div>
                      <div className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
            
            {/* Message Input */}
            <div className="border-t border-border/50 p-4">
              <div className="flex items-center space-x-2">
                <Input
                  placeholder="Ask me anything about farming..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  className="flex-1"
                  disabled
                />
                <Button size="icon" variant="outline" disabled>
                  <Mic className="h-4 w-4" />
                </Button>
                <Button size="icon" disabled>
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              
              <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-2">
                <Button variant="outline" size="sm" disabled className="text-left justify-start">
                  <MessageSquare className="h-3 w-3 mr-2" />
                  "How to prevent crop diseases?"
                </Button>
                <Button variant="outline" size="sm" disabled className="text-left justify-start">
                  <MessageSquare className="h-3 w-3 mr-2" />
                  "Best fertilizer for wheat?"
                </Button>
                <Button variant="outline" size="sm" disabled className="text-left justify-start">
                  <MessageSquare className="h-3 w-3 mr-2" />
                  "Weather impact on crops?"
                </Button>
              </div>
              
              <p className="text-xs text-muted-foreground mt-3 text-center">
                💡 This is a UI mockup. Chat functionality will be available once integrated with AI services.
              </p>
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default AgriTwinCoach;