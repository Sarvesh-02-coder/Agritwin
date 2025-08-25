// src/lib/api.ts
const API_BASE = "http://localhost:8000"; // FastAPI default port

export async function saveProfile(profile: any) {
  const res = await fetch(`${API_BASE}/profile/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "Failed to save profile");
  }

  return res.json();
}

export async function getProfile() {
  const res = await fetch(`${API_BASE}/profile/`, { method: "GET" });
  if (!res.ok) throw new Error("Failed to fetch profile");
  return res.json();
}
