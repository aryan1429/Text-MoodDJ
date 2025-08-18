import { useEffect, useState } from "react";
import { analyze, history } from "./api";
import MoodInput from "./components/MoodInput";
import ResultCard from "./components/ResultCard";
import HistoryList from "./components/HistoryList";
import { getEmotionTheme } from "./utils/emotionThemes";

type AnalyzeRes = {
  session_id: string;
  emotion: string;
  confidence: number;
  track?: { 
    track_name: string; 
    artist: string; 
    youtube_url?: string; 
    youtube_music_url?: string;
    embed_url?: string;
    thumbnail?: string;
    video_id?: string;
  };
  meme_url?: string;
};

export default function App() {
  const [loading, setLoading] = useState(false);
  const [res, setRes] = useState<AnalyzeRes|null>(null);
  const [hist, setHist] = useState<Array<{id: number; text: string; emotion: string; created_at: string}>>([]);
  const [currentEmotion, setCurrentEmotion] = useState<string>('neutral');

  async function runAnalyze(text: string) {
    setLoading(true);
    setRes(null); // Clear previous result immediately
    try {
      const data = await analyze(text);
      setRes(data);
      setCurrentEmotion(data.emotion);
      const h = await history();
      setHist(h.items || []);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    history().then((h)=> setHist(h.items || []));
  }, []);

  const theme = getEmotionTheme(currentEmotion);

  return (
    <div 
      className="min-h-screen transition-all duration-1000"
      style={{ 
        backgroundImage: theme.background,
        backgroundAttachment: 'fixed',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover'
      }}
    >
      <div className="max-w-4xl mx-auto p-6 flex flex-col gap-6">
        {/* Enhanced Header */}
        <header className="pt-8 text-center">
          <div className="flex items-center justify-center gap-4 mb-4">
            <div className="text-6xl">{theme.icon}</div>
            <div>
              <h1 
                className="text-4xl font-bold"
                style={{ color: theme.text }}
              >
                TextMood DJ 🎧
              </h1>
              <p 
                className="text-lg opacity-80"
                style={{ color: theme.text }}
              >
                {theme.description} vibes detected ✨
              </p>
            </div>
          </div>
          <div 
            className="text-base opacity-90 max-w-2xl mx-auto"
            style={{ color: theme.text }}
          >
            Tell me how you feel through text; I'll analyze your emotions and find the perfect music & memes! 🎵😂
          </div>
        </header>

        {/* Input Section */}
        <div 
          className="bg-white/20 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-white/30"
          style={{ 
            backgroundColor: `${theme.secondary}20`,
            borderColor: `${theme.primary}30`
          }}
        >
          <MoodInput 
            onSubmit={runAnalyze} 
            loading={loading}
          />
        </div>

        {/* Status Messages */}
        {loading && (
          <div 
            className="text-center p-4 rounded-xl shadow-md"
            style={{ 
              backgroundColor: theme.secondary,
              color: theme.accent 
            }}
          >
            <div className="flex items-center justify-center gap-3">
              <div className="animate-spin">🎯</div>
              <span>Analyzing your emotions and finding the perfect vibe...</span>
            </div>
          </div>
        )}

        {/* Results Section */}
        {res && !loading && (
          <div className="transform transition-all duration-500 animate-fadeIn">
            <ResultCard
              emotion={res.emotion}
              confidence={res.confidence}
              track={res.track}
              meme_url={res.meme_url}
            />
          </div>
        )}

        {/* History Section */}
        {hist.length > 0 && (
          <div 
            className="bg-white/10 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-white/20"
            style={{ 
              backgroundColor: `${theme.secondary}15`,
              borderColor: `${theme.primary}25`
            }}
          >
            <div 
              className="text-xl font-bold mb-4 flex items-center gap-2"
              style={{ color: theme.accent }}
            >
              📊 Your Mood Journey
            </div>
            <HistoryList items={hist} />
          </div>
        )}

        {/* Footer */}
        <footer 
          className="py-8 text-center text-sm opacity-70"
          style={{ color: theme.text }}
        >
          <div className="space-y-2">
            <div>🔒 Sessions are device-based and private</div>
            <div>💡 Powered by AI emotion detection & YouTube Music</div>
          </div>
        </footer>
      </div>
    </div>
  );
}
