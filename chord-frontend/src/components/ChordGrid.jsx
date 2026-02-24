import React, { Fragment, useEffect, useState, useRef } from "react";
import ReactPlayer from "react-player";
import Chord from "./Chord";
import "./ChordGrid.css";

function ChordGrid({
  chords,
  beatLength,
  url,
  bpm,
  musicKey,
  keyFlat,
  keySharp,
  title,
  cached,
}) {
  // Convert chords array to beat-indexed array (exactly like original)
  const n = Math.ceil(chords[chords.length - 1][0] / beatLength);
  let arr = Array.from(" ".repeat(n));
  for (let i = 0; i < chords.length; i++) {
    arr[Math.round(chords[i][0] / beatLength)] = chords[i][2];
  }

  const [playing, setPlaying] = useState(false);
  const [currentBeat, setCurrentBeat] = useState(-1);
  const [width, setWidth] = useState(window.innerWidth);
  const [useFlat, setUseFlat] = useState(false); // Default to sharp notation
  const [capoFret, setCapoFret] = useState(0); // Capo position (0 = no capo)
  const playerRef = useRef(null);

  // Chromatic scale for transposition
  const chromaticScale = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
  ];
  const chromaticScaleFlat = [
    "C",
    "Db",
    "D",
    "Eb",
    "E",
    "F",
    "Gb",
    "G",
    "Ab",
    "A",
    "Bb",
    "B",
  ];

  // Function to transpose a chord based on capo position
  const transposeChord = (chord, semitones) => {
    if (!chord || chord === "N" || chord === " " || semitones === 0)
      return chord;

    // Extract root note (first 1-2 characters)
    let rootNote = chord[0];
    let restOfChord = "";

    if (chord.length > 1 && (chord[1] === "#" || chord[1] === "b")) {
      rootNote = chord.substring(0, 2);
      restOfChord = chord.substring(2);
    } else {
      restOfChord = chord.substring(1);
    }

    // Find the note in chromatic scale
    let scale = useFlat ? chromaticScaleFlat : chromaticScale;
    let noteIndex = scale.indexOf(rootNote);

    // If not found, try the other scale
    if (noteIndex === -1) {
      scale = useFlat ? chromaticScale : chromaticScaleFlat;
      noteIndex = scale.indexOf(rootNote);
    }

    if (noteIndex === -1) return chord; // Return original if not found

    // Transpose by semitones (capo moves notes down, so we subtract)
    let newIndex = (noteIndex - semitones + 12) % 12;

    // Get transposed note from preferred scale
    scale = useFlat ? chromaticScaleFlat : chromaticScale;
    return scale[newIndex] + restOfChord;
  };

  // Function to convert chord notation between flat and sharp
  const convertChordNotation = (chord, toFlat) => {
    if (!chord || chord === "N" || chord === " ") return chord;

    // Remove chord quality suffixes (minor, major, 7th, etc.) - keep only root note
    // Remove: -, m, min, maj, 7, 9, 11, 13, sus, dim, aug, add, etc.
    let rootNote = chord
      .replace(/:(maj|min|sus|dim|aug|add)\d*/g, "") // Remove :maj, :min, etc.
      .replace(/-(maj|min)?\d*/g, "") // Remove - and any following text
      .replace(/(maj|min|sus|dim|aug|add)\d*/g, "") // Remove maj, min, etc.
      .replace(/\d+/g, "") // Remove any numbers (7, 9, 11, 13)
      .replace(/[()]/g, "") // Remove parentheses
      .trim();

    if (toFlat) {
      // Convert sharp to flat notation
      return rootNote
        .replace(/C#/g, "Db")
        .replace(/D#/g, "Eb")
        .replace(/F#/g, "Gb")
        .replace(/G#/g, "Ab")
        .replace(/A#/g, "Bb");
    } else {
      // Convert flat to sharp notation
      return rootNote
        .replace(/Db/g, "C#")
        .replace(/Eb/g, "D#")
        .replace(/Gb/g, "F#")
        .replace(/Ab/g, "G#")
        .replace(/Bb/g, "A#");
    }
  };

  // Convert all chords in the array based on toggle and capo
  const displayChords = arr.map((chord) => {
    let processedChord = convertChordNotation(chord, useFlat);
    return transposeChord(processedChord, capoFret);
  });

  // Determine which key to display based on toggle and transpose for capo
  const baseKey = useFlat ? keyFlat || musicKey : keySharp || musicKey;
  const displayKey = transposeChord(baseKey, capoFret);

  function startPlaying() {
    if (currentBeat === -1) {
      setCurrentBeat(0);
      setPlaying(true);
    } else {
      setPlaying(true);
    }
  }

  function pausePlaying() {
    setPlaying(false);
  }

  const handleChordClick = (i) => {
    playerRef.current.seekTo(i * beatLength);
    setCurrentBeat(i);
    setPlaying(true);
  };

  const handlePlay = () => {
    setPlaying(!playing);
  };

  const currentTime = (e) => {
    setCurrentBeat(Math.floor(e.playedSeconds / beatLength));
  };

  // Auto-scroll to current beat
  useEffect(() => {
    let scrollId;
    if (window.innerWidth <= 700) {
      scrollId = currentBeat >= 8 ? currentBeat - 8 : 0;
      document
        .getElementById(`chord-${scrollId}`)
        ?.scrollIntoView({ behavior: "smooth" });
    } else {
      scrollId = Math.floor(currentBeat / 4) * 4 - 3;
      document
        .getElementById(`chord-${scrollId}`)
        ?.scrollIntoView({ behavior: "smooth", inline: "start" });
    }
  }, [currentBeat]);

  useEffect(() => {
    setWidth(window.innerWidth);
  }, [width]);

  return (
    <Fragment>
      <div className="chord-player-container">
        <div className="player-content">
          {/* Video Player Section */}
          <div className="player-section">
            <div className="video-player">
              <ReactPlayer
                progressInterval={beatLength * 1000}
                playing={playing}
                url={url}
                onPlay={startPlaying}
                onPause={pausePlaying}
                onProgress={currentTime}
                controls={true}
                ref={playerRef}
                width="100%"
                height="100%"
              />
            </div>

            <div className="player-controls">
              <button className="play-button" onClick={handlePlay}>
                {playing ? "⏸ Pause" : "▶ Play"}
              </button>
              <div className="player-info">
                <div className="beat-info">
                  Beat: {currentBeat >= 0 ? currentBeat : 0} / {arr.length}
                </div>
                <div className="song-metadata">
                  {displayKey && displayKey !== "Unknown" && (
                    <div className="key-display">
                      <span className="key-badge">🎼 Key: {displayKey}</span>
                      <button
                        className="notation-toggle"
                        onClick={() => setUseFlat(!useFlat)}
                        title={
                          useFlat ? "Switch to Sharp (♯)" : "Switch to Flat (♭)"
                        }
                      >
                        {useFlat ? "♭" : "♯"}
                      </button>
                    </div>
                  )}
                  <div className="capo-control">
                    <label className="capo-label">🎸 Capo:</label>
                    <select
                      className="capo-select"
                      value={capoFret}
                      onChange={(e) => setCapoFret(parseInt(e.target.value))}
                    >
                      <option value="0">No Capo</option>
                      <option value="1">1st Fret</option>
                      <option value="2">2nd Fret</option>
                      <option value="3">3rd Fret</option>
                      <option value="4">4th Fret</option>
                      <option value="5">5th Fret</option>
                      <option value="6">6th Fret</option>
                      <option value="7">7th Fret</option>
                      <option value="8">8th Fret</option>
                      <option value="9">9th Fret</option>
                      <option value="10">10th Fret</option>
                      <option value="11">11th Fret</option>
                    </select>
                  </div>
                  <span className="bpm-badge">
                    ♩ {bpm ? bpm.toFixed(1) : (60 / beatLength).toFixed(1)} BPM
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Chord Grid Section */}
          <div className="chord-grid-container">
            <h2 className="grid-title">🎸 Chords</h2>
            <div className="chord-grid">
              {displayChords.map((chord, i) => (
                <Chord
                  key={i}
                  id={`chord-${i}`}
                  chord={chord}
                  colored={currentBeat === i}
                  onClick={() => handleChordClick(i)}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </Fragment>
  );
}

export default ChordGrid;
