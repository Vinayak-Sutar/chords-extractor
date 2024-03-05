import { Fragment } from "react";

function Chord({ id, chord, colored, onClick }){
    return <div id={id} className="chordBox" style={{"backgroundColor": colored ? "gray" : "rgb(211, 235, 254)"}} onClick={onClick} >
            {chord}
    </div>
}

export default Chord;