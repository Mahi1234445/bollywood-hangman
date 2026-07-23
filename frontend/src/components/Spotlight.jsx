const MAX_WRONG = 6;

export default function Spotlight({ livesLeft, status }) {
  const bulbs = Array.from({ length: MAX_WRONG }, (_, i) => i < livesLeft);
  const spotlightOpacity =
    status === "lost" ? 0.05 : 0.22 + (livesLeft / MAX_WRONG) * 0.15;
  const reelOpacity = Math.max(livesLeft / MAX_WRONG, 0.15);

  return (
    <>
      <div className="bulbs">
        {bulbs.map((lit, i) => (
          <div key={i} className={`bulb ${lit ? "lit" : "out"}`} />
        ))}
      </div>

      <div className="spotlight" style={{ "--sp-op": spotlightOpacity }}>
        <div className="reel" style={{ "--reel-op": reelOpacity }}>
          {Array.from({ length: Math.max(livesLeft, 1) }).map((_, i) => {
            const angle = (360 / MAX_WRONG) * i;
            return (
              <div
                key={i}
                className="spoke"
                style={{ transform: `rotate(${angle}deg) translate(38px, -9px)` }}
              />
            );
          })}
        </div>
      </div>
    </>
  );
}
