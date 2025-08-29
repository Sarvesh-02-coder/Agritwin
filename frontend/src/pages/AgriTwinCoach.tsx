import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot } from "lucide-react";
import Navbar from "@/components/Navbar";

type ChatMessage = {
  type: "user" | "bot";
  message: string;
  time: string;
  detectedLanguage?: string;
};

// ✅ Use environment variable for API URL
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const AgriTwinCoach = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      type: "bot",
      message:
        "Hello! I'm your AgriTwin Coach. I can help you with farming advice, crop recommendations, and answer any agricultural questions you have.",
      time: new Date().toLocaleTimeString(),
    },
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim() || loading) return; // ✅ prevent empty / duplicate sends

    const userMsg: ChatMessage = {
      type: "user",
      message,
      time: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: message }), // ✅ matches FastAPI schema
      });

      const data = await res.json();

      const botMsg: ChatMessage = {
        type: "bot",
        message: data.answer || "Sorry, I couldn’t understand that.",
        time: new Date().toLocaleTimeString(),
        detectedLanguage: data.detected_language,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          message: "⚠️ Error connecting to server.",
          time: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">AgriTwin Coach</h1>
          <p className="text-muted-foreground text-lg">
            Get AI-powered farming advice and guidance
          </p>
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
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-4 ${
                        msg.type === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted/50 text-foreground"
                      }`}
                    >
                      <p className="text-sm">{msg.message}</p>
                      {msg.type === "bot" && msg.detectedLanguage && (
                        <p className="text-xs text-muted-foreground mt-1">
                          🌐 Detected language: {msg.detectedLanguage}
                        </p>
                      )}
                      <p
                        className={`text-xs mt-2 ${
                          msg.type === "user"
                            ? "text-primary-foreground/70"
                            : "text-muted-foreground"
                        }`}
                      >
                        {msg.time}
                      </p>
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-muted/30 rounded-lg p-4 max-w-[80%]">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-pulse"></div>
                        <div
                          className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-pulse"
                          style={{ animationDelay: "0.2s" }}
                        ></div>
                        <div
                          className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-pulse"
                          style={{ animationDelay: "0.4s" }}
                        ></div>
                      </div>
                    </div>
                  </div>
                )}
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
                  onKeyDown={(e) => e.key === "Enter" && handleSend()}
                  disabled={loading} // ✅ prevent typing during send
                />
                <Button size="icon" variant="outline" onClick={handleSend} disabled={loading}>
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default AgriTwinCoach;
