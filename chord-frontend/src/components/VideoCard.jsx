import React from "react";
import "./VideoCard.css";

function VideoCard({ title, channel, img, isCached }) {
  return (
    <div className="video-card">
      {isCached && <div className="cache-badge">✓</div>}
      <img src={img} alt={title} className="video-thumbnail" />
      <div className="video-info">
        <div className="video-title">{title}</div>
        <div className="channel-name">{channel}</div>
      </div>
    </div>
  );
}

export default VideoCard;
