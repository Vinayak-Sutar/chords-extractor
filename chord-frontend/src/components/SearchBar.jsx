import React, { useRef, useEffect, Fragment, useState } from "react";
import YTSearch from "youtube-api-search";
import VideoCard from "./VideoCard";
import ChordGrid from "./ChordGrid";
import { chords, beatLength } from "../data/kehna";
import "./SearchBar.css";

function SearchBar() {
  const API_KEY = "AIzaSyAnKoIFOMcI8r-Gk61UdlwBNHVf5On_P5U";
  const kehnaUrl = "https://www.youtube.com/watch?v=dPaZNGRcPK4";

  const [videos, setVideos] = useState();
  const [term, setTerm] = useState("");
  const [showCards, setShowCards] = useState(false);
  const [chordData, setChordData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cachedVideos, setCachedVideos] = useState(new Set());

  const wrapperRef = useRef(null);

  const videoSearch = (searchTerm) => {
    YTSearch(
      { key: API_KEY, term: searchTerm, maxResults: 10 },
      async (videos) => {
        console.log(videos);
        setVideos(videos);

        // Check cache status for all videos
        await checkCacheStatus(videos);
      }
    );
  };

  // Check which videos are already cached
  const checkCacheStatus = async (videos) => {
    if (!videos || videos.length === 0) return;

    try {
      // Extract video IDs
      const videoIds = videos.map((v) => v.id.videoId);

      // Make single batch request to check all videos at once
      const response = await fetch("http://127.0.0.1:5000/cache/check-batch", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({ video_ids: videoIds }),
      });

      if (response.ok) {
        const data = await response.json();
        const cacheStatus = data.cache_status;

        // Create set of cached video IDs
        const cached = new Set();
        for (const [videoId, isCached] of Object.entries(cacheStatus)) {
          if (isCached) {
            cached.add(videoId);
          }
        }

        setCachedVideos(cached);
      }
    } catch (error) {
      // Silently fail - cache check is not critical
      console.log("Batch cache check failed:", error);
    }
  };

  const handleChange = (e) => {
    setTerm(e.target.value);
  };

  const handleSearchClick = () => {
    if (term.trim()) {
      setShowCards(true);
      videoSearch(term);
    }
  };

  const handleClickLink = async (videoId) => {
    setShowCards(false);
    setLoading(true);

    const linkpost = "https://www.youtube.com/watch?v=" + videoId;
    try {
      const body = { linkpost };
      const response = await fetch("http://127.0.0.1:5000/link", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await response.json();
      console.log("Backend response:", data); // Debug log

      // Only set chord data if it has valid chords
      if (
        data &&
        data.chords &&
        Array.isArray(data.chords) &&
        data.chords.length > 0
      ) {
        setChordData(data);
      } else {
        alert("Failed to extract chords from this video.");
      }
    } catch (error) {
      console.error(error.message);
      alert("Failed to extract chords. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  // Click outside to close dropdown
  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowCards(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // Load default Kehna song from database on mount
  useEffect(() => {
    const loadDefaultSong = async () => {
      console.log("🎵 Loading default Kehna song from database...");
      try {
        const body = { linkpost: kehnaUrl };
        const response = await fetch("http://127.0.0.1:5000/link", {
          method: "POST",
          headers: { "Content-type": "application/json" },
          body: JSON.stringify(body),
        });
        const data = await response.json();
        console.log("✅ Default song data loaded:", data);

        if (
          data &&
          data.chords &&
          Array.isArray(data.chords) &&
          data.chords.length > 0
        ) {
          setChordData(data);
          console.log("✅ Chord data set from database");
        }
      } catch (error) {
        console.error("Failed to load default song:", error);
        // Silently fail - will use hardcoded data as fallback
      }
    };

    loadDefaultSong();
  }, []);

  return (
    <Fragment>
      <div className="search-wrapper">
        <h1 className="title">🎸 Chords Extractor</h1>
        <p className="subtitle">Search for any song and learn chords</p>

        <div className="search-container">
          <input
            onChange={handleChange}
            value={term}
            type="text"
            className="search-input"
            placeholder="Search for a song..."
            autoFocus
            onKeyPress={(e) => e.key === "Enter" && handleSearchClick()}
          />
          <button className="search-button" onClick={handleSearchClick}>
            <i className="fa fa-search"></i> Search
          </button>
        </div>

        <div className="video-cards" ref={wrapperRef}>
          {videos &&
            showCards &&
            videos.map((v) => (
              <button
                key={v.id.videoId}
                className="video-card-button"
                onClick={() => handleClickLink(v.id.videoId)}
              >
                <VideoCard
                  title={v.snippet.title}
                  channel={v.snippet.channelTitle}
                  img={v.snippet.thumbnails.high.url}
                  isCached={cachedVideos.has(v.id.videoId)}
                />
              </button>
            ))}
        </div>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Extracting chords... This may take a minute.</p>
          </div>
        )}
      </div>

      {chordData && chordData.chords && chordData.chords.length > 0 ? (
        <ChordGrid
          chords={chordData.chords}
          beatLength={chordData.beat}
          url={chordData.url}
          bpm={chordData.bpm}
          musicKey={chordData.key}
          keyFlat={chordData.key_flat}
          keySharp={chordData.key_sharp}
          title={chordData.title}
          cached={chordData.cached}
        />
      ) : (
        <ChordGrid chords={chords} beatLength={beatLength} url={kehnaUrl} />
      )}
    </Fragment>
  );
}

export default SearchBar;
