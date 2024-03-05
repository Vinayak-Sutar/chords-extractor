import React from "react";
function VideoCard(props) {
  return (
    <div className="card-struct">
      <div className="image">
        {/* <img src={'https://i.redd.it/jbkai89vwyja1.jpg'} alt="Girl in a jacket" width={"200px"} heoght={"200px"} /> */}
        <img
          src={props.img}
          alt="Youtube thumbnail"
          width={"200px"}
          height={"100%"}
        />
        {/* <img src={props.img} alt="Girl in a jacket" width={"200px"} heoght={"200px"} /> */}
      </div>
      <div className="video-detail">
        <div className="video-title">
          {props.title}
          {/* MORE Elden Ring DLC Updates Just Dropped! | BIG FromSoftware News, Elden Ring Mobile, and more! */}
        </div>
        <div className="channel-name">
          {props.channel}
          {/* ZIOSTORM */}
        </div>
      </div>
    </div>
  );
}

export default VideoCard;
