import { useState } from "react";

type Props = { 
  onSubmit: (text: string) => void; 
  loading?: boolean;
};

export default function MoodInput({ onSubmit, loading }: Props) {
  const [text, setText] = useState("");

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim().length === 0) return;
    onSubmit(text.trim());
  };

  return (
    <div className="flex flex-col gap-4 w-full">
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
        </div>
      </form>
    </div>
  );
}
