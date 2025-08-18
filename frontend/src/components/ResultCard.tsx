import { getEmotionTheme } from '../utils/emotionThemes';

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
  const theme = getEmotionTheme(emotion);

  return (
    <div 
      className="rounded-2xl shadow-lg p-6 flex flex-col gap-4 transition-all duration-500"
      style={{ 
        background: theme.background,
        borderLeft: `6px solid ${theme.accent}`,
        color: theme.text
      }}
    >
      {/* Emotion Header with Enhanced Styling */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="text-4xl">{theme.emoji}</div>
          <div>
            <div className="text-2xl font-bold capitalize" style={{ color: theme.accent }}>
              {theme.icon} {emotion}
            </div>
            <div className="text-sm opacity-80">{theme.description}</div>
          </div>
        </div>
        <div 
          className="px-3 py-1 rounded-full text-sm font-medium shadow-md"
          style={{ 
            backgroundColor: theme.accent, 
            color: theme.secondary 
          }}
        >
          {(confidence*100).toFixed(1)}% confident
        </div>
      </div>

      {track && (
        <div className="flex flex-col gap-4">
          {/* Music Section Header */}
          <div className="flex items-center gap-2">
            <div className="text-2xl">{theme.music}</div>
            <div className="text-lg font-semibold" style={{ color: theme.accent }}>
              Perfect Music Match
            </div>
          </div>
          
          {/* Video thumbnail and info */}
          <div 
            className="flex items-center gap-4 p-4 rounded-xl shadow-md"
            style={{ backgroundColor: theme.secondary }}
          >
            {track.thumbnail && (
              <img 
                src={track.thumbnail} 
                alt="video thumbnail" 
                className="w-24 h-18 rounded-xl object-cover shadow-md" 
              />
            )}
            <div className="flex flex-col">
              <div className="font-bold text-lg" style={{ color: theme.accent }}>
                {track.track_name}
              </div>
              <div className="opacity-80" style={{ color: theme.text }}>
                {track.artist}
              </div>
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
          
          {/* Action buttons with theme colors */}
          <div className="flex items-center gap-3 flex-wrap">
            {track.youtube_url && (
              <a 
                href={track.youtube_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="px-6 py-3 rounded-xl font-medium transition-all duration-300 hover:shadow-lg"
                style={{ 
                  backgroundColor: '#FF0000', 
                  color: 'white' 
                }}
              >
                🎵 Open in YouTube
              </a>
            )}
            {track.youtube_music_url && (
              <a 
                href={track.youtube_music_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="px-6 py-3 rounded-xl font-medium transition-all duration-300 hover:shadow-lg"
                style={{ 
                  backgroundColor: '#FF6600', 
                  color: 'white' 
                }}
              >
                🎧 Open in YouTube Music
              </a>
            )}
          </div>
        </div>
      )}

      {meme_url && (
        <div className="mt-4">
          <div className="flex items-center gap-2 mb-3">
            <div className="text-2xl">😂</div>
            <div className="text-lg font-semibold" style={{ color: theme.accent }}>
              Mood Meme
            </div>
          </div>
          <div 
            className="rounded-xl overflow-hidden shadow-lg"
            style={{ borderColor: theme.primary }}
          >
            <img 
              src={meme_url} 
              alt="mood meme" 
              className="w-full max-h-96 object-contain" 
            />
          </div>
        </div>
      )}
    </div>
  );
}
