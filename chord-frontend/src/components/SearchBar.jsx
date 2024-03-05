import React, { useRef, useEffect, Fragment } from "react";
import { useState } from "react";
import YTSearch from "youtube-api-search";
import VideoCard from "./VideoCard";
import Chordgrid from "./Chordsgrid";

import { chords, beatLength } from "../data/kehna";

// api key hilariousheisnebrg youtube search AIzaSyDrWRvNPW4XqW3ZPJdInRIyQyEBqPmJsMQ
// api key iiitm AIzaSyAnKoIFOMcI8r-Gk61UdlwBNHVf5On_P5U
function SearchBar(props) {
  const kehnaUrl = "https://www.youtube.com/watch?v=dPaZNGRcPK4";

  let API_KEY = "AIzaSyAnKoIFOMcI8r-Gk61UdlwBNHVf5On_P5U";
  const [videos, SetVideos] = useState();
  const videoSearch = (term) => {
    // YTSearch({key: API_KEY, term: term,maxResultss:10}, (videos) => {
    YTSearch({ key: API_KEY, term: term, maxResultss: 10 }, (videos) => {
      console.log(videos);
      SetVideos(videos);
    });
  };
  const [term, setTerm] = useState("");
  // const [url, setUrl] = useState("hii");

  console.log(videos);

  const handleChange = (e) => {
    setTerm(e.target.value);
  };
  console.log(term);

  const [showCards, setShowCards] = useState(0);
  const handleClick = (e) => {
    setShowCards(1);
    videoSearch(term);
  };

  function useOutsideAlerter(ref) {
    useEffect(() => {
      /**
       * Alert if clicked on outside of element
       */
      function handleClickOutside(event) {
        if (ref.current && !ref.current.contains(event.target)) {
          setShowCards(0);
        }
      }
      // Bind the event listener
      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        // Unbind the event listener on clean up
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }, [ref]);
  }

  const [jso, setJso] = useState();
  const handleClickLink = async (link) => {
    // setUrl("https://www.youtube.com/watch?v=" + link);
    setShowCards(0);

    const linkpost = "https://www.youtube.com/watch?v=" + link;
    try {
      const body = { linkpost };
      // console.log(body);
      const response = await fetch("http://127.0.0.1:5000/link", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(body),
      });
      const js = await response.json();
      setJso(js);

      // console.log(js);
    } catch (error) {
      console.error(error.message);
    }
  };

  const wrapperRef = useRef(null);
  useOutsideAlerter(wrapperRef);
  return (
    <Fragment>
      <div className="wrap">
        <div className="search">
          <input
            onChange={handleChange}
            value={term}
            type="text"
            className="searchTerm"
            name="term"
            placeholder="Search any song..."
            autoFocus
          />
          <button type="submit" className="searchButton" onClick={handleClick}>
            <i className="fa fa-search"></i>
          </button>
        </div>
        <div className="cards" ref={wrapperRef}>
          {videos && showCards ? (
            videos.map((v) => (
              <button onClick={(e) => handleClickLink(v.id.videoId)}>
                <VideoCard
                  title={v.snippet.title}
                  channel={v.snippet.channelTitle}
                  img={v.snippet.thumbnails.high.url}
                />
              </button>
            ))
          ) : (
            <p></p>
          )}
        </div>
      </div>
      {jso ? (
        <Chordgrid chords={jso.chords} beatLength={jso.beat} url={jso.url} />
      ) : (
        <div>
          {/* <p>holaram</p> */}
          <Chordgrid chords={chords} beatLength={beatLength} url={kehnaUrl} />
        </div>
      )}
    </Fragment>
  );
}

export default SearchBar;
