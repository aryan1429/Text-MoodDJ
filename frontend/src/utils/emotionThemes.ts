// Emotion-based color themes and styling
export const emotionThemes = {
  joy: {
    primary: '#FFD700',      // Golden yellow
    secondary: '#FFF8DC',    // Cream
    accent: '#FF6347',       // Tomato red
    background: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
    text: '#8B4513',         // Saddle brown
    emoji: '😊',
    icon: '☀️',
    music: '🎵',
    description: 'Bright and cheerful'
  },
  sadness: {
    primary: '#4682B4',      // Steel blue
    secondary: '#E6F3FF',    // Light blue
    accent: '#191970',       // Midnight blue
    background: 'linear-gradient(135deg, #87CEEB 0%, #4682B4 100%)',
    text: '#2F4F4F',         // Dark slate gray
    emoji: '😢',
    icon: '🌧️',
    music: '🎻',
    description: 'Calm and reflective'
  },
  anger: {
    primary: '#DC143C',      // Crimson
    secondary: '#FFE4E1',    // Misty rose
    accent: '#8B0000',       // Dark red
    background: 'linear-gradient(135deg, #FF6B6B 0%, #DC143C 100%)',
    text: '#8B0000',         // Dark red
    emoji: '😠',
    icon: '🔥',
    music: '🎸',
    description: 'Intense and powerful'
  },
  fear: {
    primary: '#483D8B',      // Dark slate blue
    secondary: '#F8F8FF',    // Ghost white
    accent: '#2F2F2F',       // Dark gray
    background: 'linear-gradient(135deg, #9370DB 0%, #483D8B 100%)',
    text: '#2F2F2F',         // Dark gray
    emoji: '😰',
    icon: '⚡',
    music: '🎭',
    description: 'Mysterious and tense'
  },
  surprise: {
    primary: '#FF69B4',      // Hot pink
    secondary: '#FFF0F5',    // Lavender blush
    accent: '#FF1493',       // Deep pink
    background: 'linear-gradient(135deg, #FF69B4 0%, #FF1493 100%)',
    text: '#8B008B',         // Dark magenta
    emoji: '😲',
    icon: '✨',
    music: '🎪',
    description: 'Vibrant and unexpected'
  },
  disgust: {
    primary: '#6B8E23',      // Olive drab
    secondary: '#F5F5DC',    // Beige
    accent: '#556B2F',       // Dark olive green
    background: 'linear-gradient(135deg, #9ACD32 0%, #6B8E23 100%)',
    text: '#2F4F2F',         // Dark green
    emoji: '🤢',
    icon: '🚫',
    music: '🎵',
    description: 'Earthy and grounded'
  },
  love: {
    primary: '#FF69B4',      // Hot pink
    secondary: '#FFF0F5',    // Lavender blush
    accent: '#DC143C',       // Crimson
    background: 'linear-gradient(135deg, #FF1493 0%, #FF69B4 100%)',
    text: '#8B008B',         // Dark magenta
    emoji: '😍',
    icon: '💖',
    music: '💕',
    description: 'Warm and romantic'
  },
  neutral: {
    primary: '#708090',      // Slate gray
    secondary: '#F5F5F5',    // White smoke
    accent: '#2F4F4F',       // Dark slate gray
    background: 'linear-gradient(135deg, #B0C4DE 0%, #708090 100%)',
    text: '#2F4F4F',         // Dark slate gray
    emoji: '😐',
    icon: '⚖️',
    music: '🎶',
    description: 'Balanced and calm'
  }
};

export const getEmotionTheme = (emotion: string) => {
  const normalizedEmotion = emotion.toLowerCase();
  return emotionThemes[normalizedEmotion as keyof typeof emotionThemes] || emotionThemes.neutral;
};

export const emotionAnimations = {
  joy: 'animate-bounce',
  sadness: 'animate-pulse',
  anger: 'animate-ping',
  fear: 'animate-pulse',
  surprise: 'animate-bounce',
  disgust: 'animate-pulse',
  love: 'animate-pulse',
  neutral: 'animate-none'
};

export const getEmotionAnimation = (emotion: string) => {
  const normalizedEmotion = emotion.toLowerCase();
  return emotionAnimations[normalizedEmotion as keyof typeof emotionAnimations] || 'animate-none';
};
