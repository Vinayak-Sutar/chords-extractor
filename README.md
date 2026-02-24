# 🎸 Chord Extractor

Extract and play guitar chords from any YouTube video! This application uses audio analysis to detect chords from YouTube videos and displays them in a synchronized, scrollable grid for easy learning while the song plays.

**Inspired by Chordify mobile app**

## 🌟 Features

- 🎵 Extract chords from any YouTube video URL
- 🎸 Real-time chord synchronization with video playback
- 📱 Fully responsive, mobile-first design
- ⚡ Modern UI with beautiful gradients
- 🎯 Auto-scrolling chord grid
- ⏯️ Video player with chord navigation controls
- 🎼 Automatic beat detection and tempo analysis

## 📁 Project Structure

```
chords-project/
├── autochord-backend/          # Flask API for chord extraction
│   ├── app.py                  # Main API server
│   ├── extract_chords.py       # Chord extraction logic
│   ├── database.py             # PostgreSQL caching layer
│   ├── download_audio_from_youtube.py
│   ├── requirements.txt        # Python dependencies
│   └── venv/                   # Virtual environment
│
└── chord-frontend/             # Modern React frontend
    ├── src/
    │   ├── components/
    │   │   ├── SearchBar.jsx   # YouTube URL input
    │   │   ├── ChordPlayer.jsx # Video player + controls
    │   │   └── ChordGrid.jsx   # Scrollable chord display
    │   ├── App.jsx
    │   └── index.css           # Tailwind CSS
    ├── package.json
    └── README.md
```

## 🚀 Quick Start

### Backend Setup

1. Navigate to backend directory:

```bash
cd autochord-backend
```

2. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd chord-frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The app will open at `http://localhost:3000`

## 💻 Usage

1. **Start the backend server** (make sure it's running on port 5000)
2. **Open the frontend** in your browser
3. **Paste a YouTube URL** in the search bar (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
4. **Click "Extract"** and wait for chord processing (may take 30-60 seconds)
5. **Watch the video** while following the synchronized chord grid
6. **Click any chord** to jump to that position in the video
7. **Use player controls** to skip forward/backward by beats

## 🛠️ Technology Stack

### Backend

- **Flask** - Python web framework
- **librosa** - Audio analysis and beat detection
- **autochord** - Chord recognition
- **pytube** - YouTube video downloading
- **moviepy** - Audio extraction

### Frontend

- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **React Player** - YouTube integration
- **Lucide React** - Icons
- **Modern ES6+** JavaScript

## 📱 Mobile Support

The new frontend is built with a mobile-first approach and works seamlessly on:

- 📱 Smartphones (iOS & Android)
- 💻 Tablets
- 🖥️ Desktop browsers

## 🎯 How It Works

1. **User Input**: Paste YouTube URL
2. **Backend Processing**:
   - Downloads audio from YouTube video
   - Analyzes audio with librosa for beat detection
   - Extracts chords using autochord algorithm
   - Returns chord timeline with beat information
3. **Frontend Display**:
   - Embeds YouTube video with controls
   - Maps chords to beat-indexed grid
   - Syncs current beat with video playback
   - Auto-scrolls to active chord

## 🐛 Troubleshooting

**Backend Issues:**

- Make sure Python virtual environment is activated
- Check that all dependencies are installed: `pip list`
- Verify Flask is running on port 5000
- Check for FFmpeg installation (required by moviepy)

**Frontend Issues:**

- Make sure Node.js 16+ is installed
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that backend is running and accessible
- Verify CORS is enabled on backend

**Chord Extraction Issues:**

- YouTube video must be publicly accessible
- Processing time varies with song length (30-90 seconds typical)
- Some videos may be blocked due to copyright restrictions

## 📝 API Documentation

### POST /link

Extract chords from a YouTube video.

**Request:**

```json
{
  "linkpost": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**

```json
{
  "beat": 0.510839,
  "chords": [
    [7.848, 9.891, "G#"],
    [9.891, 11.888, "C#"],
    ...
  ],
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Inspired by **Chordify** mobile app
- Built with love for guitar players 🎸
- Audio analysis powered by librosa and autochord

---

**Made with ❤️ for guitar players everywhere 🎸**
