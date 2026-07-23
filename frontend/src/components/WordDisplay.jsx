import { useState } from "react";

export default function WordDisplay({ display, hint }) {
  const [hintShown, setHintShown] = useState(false);

  return (
    <>
      <button
        className="hint-toggle"
        onClick={() => setHintShown(true)}
        disabled={hintShown}
      >
        {hintShown ? `CLUE · ${hint}` : "🎬 Tap for a clue"}
      </button>
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
