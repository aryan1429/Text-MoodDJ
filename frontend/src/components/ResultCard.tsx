type Props = {
  emotion: string;
  confidence: number;
  track?: { track_name: string; artist: string; preview_url?: string; external_url: string; image?: string; };
  meme_url?: string;
};

export default function ResultCard({ emotion, confidence, track, meme_url }: Props) {
  return (
    <div className="rounded-2xl shadow p-4 bg-white/80 flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="text-xl font-semibold capitalize">Mood: {emotion}</div>
        <div className="text-sm opacity-70">Confidence: {(confidence*100).toFixed(1)}%</div>
      </div>

      {track && (
        <div className="flex items-center gap-4">
          {track.image && <img src={track.image} alt="album" className="w-16 h-16 rounded-xl object-cover" />}
          <div className="flex flex-col">
            <div className="font-medium">{track.track_name}</div>
            <div className="text-sm opacity-70">{track.artist}</div>
            <div className="mt-2 flex items-center gap-3">
              {track.preview_url && (
                <audio controls src={track.preview_url} className="w-64" />
              )}
              <a href={track.external_url} target="_blank" className="text-blue-600 underline">Open in Spotify</a>
            </div>
          </div>
        </div>
      )}

      {meme_url && (
        <img src={meme_url} alt="meme" className="w-full rounded-xl" />
      )}
    </div>
  );
}
