# Chord Extractor - New Frontend

Modern, mobile-first React application for extracting and displaying guitar chords from YouTube videos.

## Features

- 🎵 Extract chords from any YouTube video URL
- 🎸 Real-time chord synchronization with video playback
- 📱 Fully responsive design (mobile-first)
- ⚡ Modern UI with Tailwind CSS
- 🎨 Beautiful gradient design inspired by Chordify
- 🎯 Auto-scrolling chord grid
- ⏯️ Video player controls with beat navigation

## Prerequisites

- Node.js 16+
- npm or yarn
- Backend server running (see `../autochord-backend/README.md`)

## Installation

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm start
```

The app will open at `http://localhost:3000`

## Usage

1. Make sure the backend server is running at `http://localhost:5000`
2. Paste a YouTube URL in the search bar
3. Click "Extract" to process the video
4. Watch the video while following along with the chord grid
5. Click on any chord to jump to that position in the video

## Build for Production

```bash
npm run build
```

The build folder will contain the optimized production build.

## Technologies Used

- React 18
- Tailwind CSS
- React Player (YouTube integration)
- Lucide React (icons)
- Modern ES6+ JavaScript
