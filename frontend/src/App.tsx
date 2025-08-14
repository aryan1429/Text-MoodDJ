import { useEffect, useState } from "react";
import { analyze, history } from "./api";
import MoodInput from "./components/MoodInput";
import ResultCard from "./components/ResultCard";
import HistoryList from "./components/HistoryList";

type AnalyzeRes = {
  session_id: string;
  emotion: string;
  confidence: number;
  track?: { track_name:string; artist:string; preview_url?:string; external_url:string; image?:string; };
  meme_url?: string;
};

export default function App() {
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [res, setRes] = useState<AnalyzeRes|null>(null);
  const [hist, setHist] = useState<any[]>([]);

  async function runAnalyze(text: string) {
    setLoading(true);
    try {
      const data = await analyze(text);
      setRes(data);
      const h = await history();
      setHist(h.items || []);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    history().then((h)=> setHist(h.items || []));
  }, []);

  return (
    <div className="min-h-screen bg-gradient">
      <div className="max-w-3xl mx-auto p-6 flex flex-col gap-6">
        <header className="pt-8">
          <h1 className="text-3xl font-bold">TextMood DJ 🎧</h1>
          <p className="opacity-70">Tell me how you feel; I'll play the vibe & show a meme.</p>
        </header>

        <MoodInput onSubmit={runAnalyze} onListening={setListening} />

        {listening && <div className="text-sm">Listening… 🎙️</div>}
        {loading && <div className="text-sm">Finding your vibe… 🎵</div>}

        {res && (
          <ResultCard
            emotion={res.emotion}
            confidence={res.confidence}
            track={res.track}
            meme_url={res.meme_url}
          />
        )}

        <HistoryList items={hist} />

        <footer className="py-8 text-xs opacity-60">
          Sessions are device-based. Your session ID lives in localStorage.
        </footer>
      </div>
    </div>
  );
}
