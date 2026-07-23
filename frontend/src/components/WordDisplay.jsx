import { useState } from "react";

export default function WordDisplay({ display, year, genre, storyline }) {
  const [showGenre, setShowGenre] = useState(false);
  const [showStory, setShowStory] = useState(false);

  return (
    <>
      <div className="hints-row">
        <button
          className="hint-toggle"
          onClick={() => setShowGenre(true)}
          disabled={showGenre}
        >
          {showGenre ? `🎬 ${year} · ${genre}` : "🎬 Year & Genre"}
        </button>
        <button
          className="hint-toggle"
          onClick={() => setShowStory(true)}
          disabled={showStory}
        >
          📖 Storyline
        </button>
      </div>

      {showStory && <div className="storyline-box">{storyline}</div>}

      <div className="word-row">
        {display.map((ch, i) =>
          ch === " " ? (
            <div key={i} className="letter-box space" />
          ) : (
            <div key={i} className="letter-box">
              {ch === "_" ? "" : ch}
            </div>
          )
        )}
      </div>
    </>
  );
}