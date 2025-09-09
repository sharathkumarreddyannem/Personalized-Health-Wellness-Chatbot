const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
export async function sendMessage(userId, text) {
  const res = await fetch(`${API_BASE}/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, text })
  });
  return res.json();
}
export async function saveProfile(profile) {
  const res = await fetch(`${API_BASE}/profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile)
  });
  return res.json();
}
