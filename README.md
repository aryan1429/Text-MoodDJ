# 🎧 TextMood DJ

**Detect your emotion from text or voice and get matching music + memes!**

An emotional assistant that analyzes your mood and responds with:
- 🎵 **YouTube Music** recommendations 
- 😂 **Animated GIFs/memes** from GIPHY
- 🎙️ **Voice input** support
- 📱 **Device-specific sessions**

## ✨ Features

- **Emotion Detection**: Uses AI to analyze sentiment from text
- **YouTube Integration**: Finds songs matching your mood (no Spotify Premium needed!)
- **Voice Input**: Speak your feelings using browser speech recognition
- **Meme Generator**: Gets mood-appropriate GIFs from GIPHY
- **Session Management**: Each device maintains its own history
- **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (or use the simple HTML version)
- YouTube Data API key
- GIPHY API key

### Backend Setup

1. **Clone and navigate:**
   ```bash
   git clone https://github.com/aryan1429/Text-MoodDJ.git
   cd Text-MoodDJ/backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Get API Keys:**
   
   **YouTube Data API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create project → Enable "YouTube Data API v3" → Create API Key
   
   **GIPHY API:**
   - Go to [GIPHY Developers](https://developers.giphy.com/)
   - Create account → Create app → Copy API key

5. **Run backend:**
   ```bash
   uvicorn app:app --reload --port 8000
   ```

### Frontend Options

#### Option 1: Simple HTML (Recommended for quick testing)
Open `test.html` in your browser - it works immediately!

#### Option 2: React App
```bash
cd ../frontend
npm install
npm run dev
```

## 🔧 API Endpoints

- `GET /api/session` - Create new session
- `POST /api/analyze` - Analyze mood from text
- `GET /api/history` - Get mood history

## 🌐 Deployment

### Backend (Render/Railway/Heroku)
1. Push to GitHub
2. Connect repository to hosting platform
3. Set environment variables:
   - `YOUTUBE_API_KEY`
   - `GIPHY_API_KEY` 
   - `ALLOWED_ORIGIN=https://your-frontend-domain.com`
4. Deploy with: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel/Netlify)
1. Set `VITE_API_BASE=https://your-backend-url.com`
2. Deploy from GitHub

## 📱 Usage

1. **Type or speak** how you're feeling
2. **Get instant** emotion analysis
3. **Enjoy** YouTube music recommendations
4. **Laugh** at mood-appropriate memes
5. **Track** your mood history

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Transformers
- **Frontend**: React + TypeScript, Tailwind CSS
- **APIs**: YouTube Data API, GIPHY API
- **AI/ML**: HuggingFace Transformers for sentiment analysis
- **Database**: SQLite (dev), PostgreSQL (production)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- HuggingFace for emotion detection models
- YouTube Data API for music search
- GIPHY for endless meme possibilities

---

**Made with ❤️ for music and mood lovers everywhere!**
