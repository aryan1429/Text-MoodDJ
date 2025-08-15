import { useState } from "react";
import VoiceRecorder from "./VoiceRecorder";

type Props = { 
  onSubmit: (text: string) => void; 
  onVoiceSubmit: (audioBlob: Blob) => void;
  onListening?: (b: boolean) => void; 
  loading?: boolean;
};

export default function MoodInput({ onSubmit, onVoiceSubmit, onListening, loading }: Props) {
  const [text, setText] = useState("");
  const [mode, setMode] = useState<'text' | 'voice'>('text');

  const handleMic = async () => {
    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    
    if (!SpeechRecognition) {
      alert("SpeechRecognition not supported in this browser. Try Chrome.");
      return;
    }
    const rec = new SpeechRecognition();
    rec.lang = "en-US";
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    onListening?.(true);
    rec.onresult = (e: any) => {
      const transcript = e.results[0][0].transcript;
      setText(transcript);
      onListening?.(false);
    };
    rec.onerror = () => onListening?.(false);
    rec.onend = () => onListening?.(false);
    rec.start();
  };

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim().length === 0) return;
    onSubmit(text.trim());
  };

  const handleVoiceRecording = (audioBlob: Blob) => {
    onVoiceSubmit(audioBlob);
  };

  return (
    <div className="flex flex-col gap-4 w-full">
      {/* Mode Toggle */}
      <div className="flex justify-center gap-2">
        <button
          type="button"
          onClick={() => setMode('text')}
          className={`px-4 py-2 rounded-lg transition-colors ${
            mode === 'text' 
              ? 'bg-blue-500 text-white' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          ✏️ Type
        </button>
        <button
          type="button"
          onClick={() => setMode('voice')}
          className={`px-4 py-2 rounded-lg transition-colors ${
            mode === 'voice' 
              ? 'bg-blue-500 text-white' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          🎤 Voice
        </button>
      </div>

      {mode === 'text' ? (
        <form onSubmit={submit} className="flex flex-col gap-3 w-full">
          <textarea
            className="w-full p-4 rounded-2xl shadow bg-white/80 focus:outline-none"
            rows={3}
            placeholder="Tell me how you feel..."
            value={text}
            onChange={e => setText(e.target.value)}
            disabled={loading}
          />
          <div className="flex items-center gap-3">
            <button 
              type="submit" 
              disabled={loading || !text.trim()}
              className="px-4 py-2 rounded-2xl shadow bg-black text-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Analyze Mood'}
            </button>
            <button 
              type="button" 
              onClick={handleMic} 
              disabled={loading}
              className="px-3 py-2 rounded-2xl shadow bg-white disabled:opacity-50"
            >
              🎙️ Quick Speak
            </button>
          </div>
        </form>
      ) : (
        <div className="flex flex-col items-center gap-4 py-6">
          <VoiceRecorder 
            onRecordingComplete={handleVoiceRecording}
            disabled={loading}
          />
          {loading && (
            <div className="text-center text-blue-600 font-medium">
              🎯 Analyzing your voice and emotions...
            </div>
          )}
        </div>
      )}
    </div>
  );
}
