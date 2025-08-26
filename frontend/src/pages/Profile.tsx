import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { User, MapPin, Wheat, Phone } from "lucide-react";
import Navbar from "@/components/Navbar";

const API_BASE = "http://localhost:8000";

const Profile = () => {
  const { toast } = useToast();
  const [loading, setLoading] = useState(true);
  const [profiles, setProfiles] = useState<any[]>([]);
  const [selectedPhone, setSelectedPhone] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    crop: "",
    location: "",
    smsAlerts: false,
    farmArea: 0,
  });
  const refreshProfile = async () => {
    try {
      const res = await fetch(`${API_BASE}/profile/`);
      const data = await res.json();
      if (data.success && data.data.length > 0) {
        setProfiles(data.data);
        setFormData(data.data[0]); // 🔥 Always set to top profile
        setSelectedPhone(data.data[0].phone);
      }
    } catch (err) {
      console.error("Error refreshing profile:", err);
    }
  };


  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetch(`${API_BASE}/profile/`);
        const data = await res.json();

        if (data.success && data.data && data.data.length > 0) {
          setProfiles(data.data);
          const latestProfile = data.data[data.data.length - 1];
          setFormData(latestProfile);
          setSelectedPhone(latestProfile.phone);
        }
      } catch (err) {
        console.error("Error fetching profile:", err);
        toast({
          title: "Error",
          description: "Could not load profile",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [toast]);

  const handleInputChange = (field: string, value: string | boolean | number) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSave = async () => {
    try {
      if (!formData.phone) {
        toast({
          title: "Phone number required",
          description: "Please enter your phone number before saving",
          variant: "destructive",
        });
        return;
      }

      if (!/^\d{6}$/.test(formData.location)) {
        toast({
          title: "Invalid PIN Code",
          description: "Please enter a valid 6-digit Indian PIN code",
          variant: "destructive",
        });
        return;
      }

      if (formData.farmArea <= 0) {
        toast({
          title: "Invalid Farm Area",
          description: "Please enter a valid farm size greater than 0",
          variant: "destructive",
        });
        return;
      }

      const res = await fetch(`${API_BASE}/profile/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (!res.ok) {
        toast({
          title: "Error",
          description: data.detail || "Failed to save profile",
          variant: "destructive",
        });
        return;
      }

      if (data.action === "created") {
        toast({
          title: "Profile Created!",
          description: "Your profile has been saved successfully",
          variant: "default",
        });
      } else if (data.action === "updated") {
        toast({
          title: "Profile Updated!",
          description: "Your profile changes have been saved",
          variant: "default",
        });
      } else {
        toast({
          title: "No Update Needed",
          description: "No changes were detected in your profile",
          variant: "default",
        });
      }
    } catch (err) {
      console.error("Save error:", err);
      toast({
        title: "Error",
        description: "Failed to connect to server",
        variant: "destructive",
      });
    }
  };

  const handleSwitchProfile = async () => {
    if (!selectedPhone) return;

    try {
      const res = await fetch(`${API_BASE}/profile/switch/${selectedPhone}`, {
        method: "POST",
      });
      const data = await res.json();

      if (!res.ok) {
        toast({
          title: "Error",
          description: data.detail || "Failed to switch profile",
          variant: "destructive",
        });
        return;
      }

      // 🔥 After switching, refresh profile list so top one is active
      await refreshProfile();

      toast({
        title: "Profile Switched",
        description: `Active profile set to ${data.data.name || data.data.phone}`,
      });
    } catch (err) {
      console.error("Switch error:", err);
      toast({
        title: "Error",
        description: "Could not switch profile",
        variant: "destructive",
      });
    }
  };


  if (loading) {
    return (
      <div className="min-h-screen dashboard-gradient flex items-center justify-center">
        <p className="text-lg">Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen dashboard-gradient">
      <Navbar />

      {/* Switch Profile Section (top-right) */}
      <div className="flex justify-end items-center space-x-2 px-4 py-2">
        <Select
          value={selectedPhone}
          onValueChange={(value) => setSelectedPhone(value)}
        >
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Select a profile" />
          </SelectTrigger>
          <SelectContent>
            {profiles.map((p) => (
              <SelectItem key={p.phone} value={p.phone}>
                {p.name || p.phone}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Button onClick={handleSwitchProfile}>Switch</Button>
      </div>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">Profile</h1>
          <p className="text-muted-foreground text-lg">
            Manage your farm profile and notification preferences
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          <Card className="card-gradient glow-primary">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <User className="h-6 w-6 text-primary" />
                <span>Farm Profile</span>
              </CardTitle>
              <CardDescription>
                Keep your information updated to receive personalized recommendations
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Name Field */}
              <div className="space-y-2">
                <Label htmlFor="name" className="flex items-center space-x-2">
                  <User className="h-4 w-4 text-primary" />
                  <span>Full Name</span>
                </Label>
                <Input
                  id="name"
                  placeholder="Enter your full name"
                  value={formData.name}
                  onChange={(e) => handleInputChange("name", e.target.value)}
                  className="transition-smooth"
                />
              </div>

              {/* Phone Field */}
              <div className="space-y-2">
                <Label htmlFor="phone" className="flex items-center space-x-2">
                  <Phone className="h-4 w-4 text-primary" />
                  <span>Phone Number</span>
                </Label>
                <Input
                  id="phone"
                  placeholder="Enter your phone number"
                  value={formData.phone}
                  onChange={(e) => handleInputChange("phone", e.target.value)}
                  className="transition-smooth"
                />
              </div>

              {/* Location Field */}
              <div className="space-y-2">
                <Label htmlFor="location" className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4 text-primary" />
                  <span>PIN Code</span>
                </Label>
                <Input
                  id="location"
                  placeholder="Enter your 6-digit PIN code"
                  value={formData.location}
                  onChange={(e) => {
                    const value = e.target.value;
                    if (/^\d{0,6}$/.test(value)) {
                      handleInputChange("location", value);
                    }
                  }}
                  maxLength={6}
                  className="transition-smooth"
                />
              </div>

              {/* Crop Selection */}
              <div className="space-y-2">
                <Label className="flex items-center space-x-2">
                  <Wheat className="h-4 w-4 text-primary" />
                  <span>Primary Crop</span>
                </Label>
                <Select
                  value={formData.crop}
                  onValueChange={(value) => handleInputChange("crop", value)}
                >
                  <SelectTrigger className="transition-smooth">
                    <SelectValue placeholder="Select your primary crop" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="wheat">Wheat</SelectItem>
                    <SelectItem value="rice">Rice</SelectItem>
                    <SelectItem value="corn">Corn</SelectItem>
                    <SelectItem value="tomato">Tomato</SelectItem>
                    <SelectItem value="potato">Potato</SelectItem>
                    <SelectItem value="cotton">Cotton</SelectItem>
                    <SelectItem value="sugarcane">Sugarcane</SelectItem>
                    <SelectItem value="onion">Onion</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Farm Area Field */}
              <div className="space-y-2">
                <Label htmlFor="farmArea" className="flex items-center space-x-2">
                  <span>Farm Area (in acres)</span>
                </Label>
                <Input
                  id="farmArea"
                  type="number"
                  placeholder="Enter your farm size"
                  value={formData.farmArea}
                  onChange={(e) => handleInputChange("farmArea", parseFloat(e.target.value))}
                  className="transition-smooth"
                />
              </div>

              {/* SMS Alerts Checkbox */}
              <div className="flex items-center space-x-3 p-4 bg-muted/20 rounded-lg">
                <Checkbox
                  id="smsAlerts"
                  checked={formData.smsAlerts}
                  onCheckedChange={(checked) =>
                    handleInputChange("smsAlerts", checked as boolean)
                  }
                />
                <div className="flex-1">
                  <Label htmlFor="smsAlerts" className="text-sm font-medium cursor-pointer">
                    Send me SMS alerts 5-7 days before critical farming activities
                  </Label>
                  <p className="text-xs text-muted-foreground mt-1">
                    Get timely notifications for irrigation, pest control, and harvest reminders
                  </p>
                </div>
              </div>

              {/* Save Button */}
              <Button
                onClick={handleSave}
                className="w-full glow-primary transition-bounce"
                size="lg"
              >
                Save Profile
              </Button>
            </CardContent>
          </Card>

          {/* Additional Settings Card */}
          <Card className="card-gradient mt-6">
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>
                Customize how you receive updates from AgriTwin
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Weather Alerts</p>
                  <p className="text-xs text-muted-foreground">Receive severe weather warnings</p>
                </div>
                <Checkbox defaultChecked />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Market Price Updates</p>
                  <p className="text-xs text-muted-foreground">Get daily crop price notifications</p>
                </div>
                <Checkbox defaultChecked />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">Pest & Disease Warnings</p>
                  <p className="text-xs text-muted-foreground">Early warning system for crop threats</p>
                </div>
                <Checkbox defaultChecked />
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Profile;
