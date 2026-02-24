import React from "react";
import "./Chord.css";

function Chord({ id, chord, colored, onClick }) {
  return (
    <div
      id={id}
      className={`chord-box ${colored ? "active" : ""}`}
      onClick={onClick}
    >
      {chord || "—"}
    </div>
  );
}

export default Chord;
