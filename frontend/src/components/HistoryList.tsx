import { getEmotionTheme } from '../utils/emotionThemes';

type Item = { id:number; text:string; emotion:string; created_at:string; };

export default function HistoryList({ items }:{items: Item[]}) {
  if (!items?.length) return null;
  
  return (
    <div className="space-y-3">
      {items.map((item, index) => {
        const theme = getEmotionTheme(item.emotion);
        const timeAgo = new Date(item.created_at).toLocaleTimeString([], { 
          hour: '2-digit', 
          minute: '2-digit' 
        });
        
        return (
          <div 
            key={item.id}
            className="flex items-center gap-4 p-4 rounded-xl shadow-md hover:scale-105 transition-all duration-300 animate-slideIn"
            style={{ 
              backgroundColor: theme.secondary,
              borderLeft: `4px solid ${theme.primary}`,
              animationDelay: `${index * 0.1}s`
            }}
          >
            {/* Emotion indicator */}
            <div className="flex items-center gap-2 min-w-0">
              <div className="text-2xl">{theme.emoji}</div>
              <div className="flex flex-col min-w-0">
                <div 
                  className="font-medium capitalize text-sm"
                  style={{ color: theme.accent }}
                >
                  {item.emotion}
                </div>
                <div className="text-xs opacity-70" style={{ color: theme.text }}>
                  {timeAgo}
                </div>
              </div>
            </div>
            
            {/* Text preview */}
            <div 
              className="flex-1 text-sm truncate"
              style={{ color: theme.text }}
              title={item.text}
            >
              "{item.text}"
            </div>
          </div>
        );
      })}
    </div>
  );
}
