type Props = {
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

export default function ResultCard({ emotion, confidence, track, meme_url }: Props) {
  return (
    <div className="rounded-2xl shadow p-4 bg-white/80 flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="text-xl font-semibold capitalize">Mood: {emotion}</div>
        <div className="text-sm opacity-70">Confidence: {(confidence*100).toFixed(1)}%</div>
      </div>

      {track && (
        <div className="flex flex-col gap-4">
          {/* Video thumbnail and info */}
          <div className="flex items-center gap-4">
            {track.thumbnail && (
              <img src={track.thumbnail} alt="video thumbnail" className="w-24 h-18 rounded-xl object-cover" />
            )}
            <div className="flex flex-col">
              <div className="font-medium">{track.track_name}</div>
              <div className="text-sm opacity-70">{track.artist}</div>
            </div>
          </div>
          
          {/* YouTube embed player */}
          {track.embed_url && (
            <div className="w-full">
              <iframe
                width="100%"
                height="200"
                src={track.embed_url}
                title="YouTube video player"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="rounded-xl"
              ></iframe>
            </div>
          )}
          
          {/* Action buttons */}
          <div className="flex items-center gap-3 flex-wrap">
            {track.youtube_url && (
              <a 
                href={track.youtube_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                🎵 Open in YouTube
              </a>
            )}
            {track.youtube_music_url && (
              <a 
                href={track.youtube_music_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
              >
                🎧 Open in YouTube Music
              </a>
            )}
          </div>
        </div>
      )}

      {meme_url && (
        <div className="mt-4">
          <img src={meme_url} alt="meme" className="w-full rounded-xl max-h-96 object-contain" />
        </div>
      )}
    </div>
  );
}
