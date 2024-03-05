import React, { Fragment, useEffect, useState, useRef } from "react";
// import ReactAudioPlayer from "react-audio-player";
import ReactPlayer from "react-player";
import Dropdown from "react-dropdown";
import "react-dropdown/style.css";

import Chord from "./Chord";
// import { chords, beatLength  } from "../data/kehna";
// import kehna from "../data/kehna.wav";
import play from "../images/play.svg";
import pause from "../images/pause.svg";

// const kehnaUrl = "https://www.youtube.com/watch?v=dPaZNGRcPK4";

function Chordgrid(props) {
  const beatsPerRow = 8;
  let n = Math.ceil(
    props.chords[props.chords.length - 1][0] / props.beatLength
  );
  let arr = Array.from(" ".repeat(n));
  for (let i = 0; i < props.chords.length; i++) {
    arr[Math.round(props.chords[i][0] / props.beatLength)] = props.chords[i][2];
  }
  // let [firstStart,setFirstStart] = useState(true);
  const [playing, setPlaying] = useState(false);
  const [currentBeat, setCurrentBeat] = useState(-1);
  const [width, setWidth] = useState(window.innerWidth);
  const playerRef = useRef(null);
  const gridRef = useRef(null);

  function startPlaying() {
    if (currentBeat === -1) {
      setCurrentBeat(0);
      setPlaying(true);
      // setFirstStart(false);
    } else {
      setPlaying(true);
    }
  }

  function pausePlaying() {
    setPlaying(false);
  }

  const handleClick = (i) => {
    playerRef.current.seekTo(i * props.beatLength);
    // console.log("current time 2 ",playerRef.current.getCurrentTime());
    setCurrentBeat(i);
    setPlaying(true);
  };

  const myRefs = useRef([]);
  myRefs.current = arr.map(
    (element, i) => myRefs.current[i] ?? React.createRef()
  );

  useEffect(() => {
    let scrollId;
    // console.log(window.innerWidth);
    if (window.innerWidth <= 700) {
      scrollId = currentBeat >= beatsPerRow ? currentBeat - beatsPerRow : 0;
      document
        .getElementById(`${scrollId}`)
        ?.scrollIntoView({ behavior: "smooth" });
    } else {
      scrollId = Math.floor(currentBeat / 4) * 4 - 3;
      // scrollId = Math.floor(currentBeat / 4) * 4 ;
      console.log(scrollId + " " + currentBeat);
      document
        .getElementById(`${scrollId}`)
        ?.scrollIntoView({ behavior: "smooth", inline: "start" });
    }
  }, [currentBeat]);

  useEffect(() => {
    console.log(width);
    setWidth(window.innerWidth);
  }, [width]);

  const currentTime = (e) => {
    setCurrentBeat(Math.floor(e.playedSeconds / props.beatLength));
    // console.log(e.playedSeconds);
  };

  const handlePlay = () => {
    if (playing) {
      setPlaying(false);
    } else {
      setPlaying(true);
    }
  };

  // console.log("player width", playerRef.current);

  const options = [
    "1st fret",
    "2nd fret",
    "3rd fret",
    "4th fret",
    "5th fret",
    "6th fret",
    "7th fret",
    "8th fret",
    "9th fret",
    "10th fret",
    "11th fret",
    "none",
  ];
  // const defaultOption = options[0];

  return (
    <Fragment>
      <div className="chordflex">
        <div className="container" width={width}>
          <div className="controller">
            <img
              src={playing ? pause : play}
              alt="play/pause"
              className="controller-image"
              onClick={handlePlay}
            />
            <div className="capo">
              <div>Capo</div>
              <Dropdown
                options={options}
                value={0}
                placeholder="None"
                width="100%"
              />
            </div>
          </div>

          <div className="audioBox">
            <ReactPlayer
              progressInterval={props.beatLength * 1000}
              playing={playing}
              url={props.url}
              autoPlay
              onPlay={startPlaying}
              onPause={pausePlaying}
              onProgress={currentTime}
              controls={true}
              ref={playerRef}
              width={width <= 700 ? "100%" : "800px"}
              height={width <= 700 ? "100%" : "450px"}
            />
          </div>
        </div>
          <div className="chordGrid" ref={gridRef} width="window.innerWidth">
            {arr.map((a, i) => {
              return (
                <Chord
                  chord={a}
                  id={i}
                  key={i}
                  ref={myRefs.current[i]}
                  colored={currentBeat === i}
                  onClick={() => handleClick(i)}
                  width={width / 8}
                />
              );
            })}
          </div>
      </div>
    </Fragment>
  );
}

export default Chordgrid;
