import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const api = axios.create({
  baseURL: `${API_BASE}/api`,
  withCredentials: true
});

export async function ensureSession(): Promise<string> {
  const existing = localStorage.getItem("session_id");
  if (existing) return existing;
  const res = await api.get("/session");
  const sid = res.data.session_id as string;
  localStorage.setItem("session_id", sid);
  return sid;
}

export async function analyze(text: string) {
  const sid = await ensureSession();
  const res = await api.post("/analyze", { text }, {
    headers: { "X-Session-Id": sid }
  });
  return res.data;
}

export async function history() {
  const sid = await ensureSession();
  const res = await api.get("/history", {
    headers: { "X-Session-Id": sid }
  });
  return res.data;
}
