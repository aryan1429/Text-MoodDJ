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

export async function analyzeVoice(audioBlob: Blob) {
  const sid = await ensureSession();
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");
  
  const res = await api.post("/analyze-voice", formData, {
    headers: { 
      "X-Session-Id": sid,
      "Content-Type": "multipart/form-data"
    }
  });
  return res.data;
}

export async function transcribeAudio(audioBlob: Blob) {
  const sid = await ensureSession();
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");
  
  const res = await api.post("/transcribe", formData, {
    headers: { 
      "X-Session-Id": sid,
      "Content-Type": "multipart/form-data"
    }
  });
  return res.data;
}

export async function getSpeech(emotion: string, confidence: number = 0.8) {
  const res = await api.get(`/speak/${emotion}?confidence=${confidence}`, {
    responseType: 'blob'
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
