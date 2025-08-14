import { useState } from "react";

type Props = { onSubmit: (text: string)=>void; onListening?: (b:boolean)=>void; };

export default function MoodInput({ onSubmit, onListening }: Props) {
  const [text, setText] = useState("");

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

  return (
    <form onSubmit={submit} className="flex flex-col gap-3 w-full">
      <textarea
        className="w-full p-4 rounded-2xl shadow bg-white/80 focus:outline-none"
        rows={3}
        placeholder="Tell me how you feel..."
        value={text}
        onChange={e=>setText(e.target.value)}
      />
      <div className="flex items-center gap-3">
        <button type="submit" className="px-4 py-2 rounded-2xl shadow bg-black text-white">Analyze Mood</button>
        <button type="button" onClick={handleMic} className="px-3 py-2 rounded-2xl shadow bg-white">🎙️ Speak</button>
      </div>
    </form>
  );
}
