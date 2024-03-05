import { react, useState } from "react";
import Chordgrid from "./components/Chordsgrid.jsx";
// import bg from "../src/images/guit.png"
import SearchBar from "./components/SearchBar.jsx";

function App() {
  const [show, setShow] = useState(1);
  const handleClick = (e) => {
    setShow(0);
  };
  return (
    // <div className="app" style={{backgroundImage:bg}}>

    <div className="app" onClick={handleClick}>
      <SearchBar show={show} />
      {/* <Chordgrid /> */}
    </div>
  );
}

export default App;
