export default function StickFigure({ wrongCount, faceImage, status }) {
  const isLost = status === "lost";
  const isWon = status === "won";
  const show = (n) => isWon || wrongCount >= n;

  return (
    <div className="gallows-wrap">
      <svg viewBox="0 0 200 260" className="gallows-svg">
        {/* Gallows structure - always visible, never falls */}
        <line x1="20" y1="240" x2="150" y2="240" className="gallows-line" />
        <line x1="55" y1="240" x2="55" y2="20" className="gallows-line" />
        <line x1="55" y1="20" x2="130" y2="20" className="gallows-line" />
        <line x1="130" y1="20" x2="130" y2="50" className="gallows-line rope" />

        {/* Everything in this group falls over together when the game is lost,
            or drops down to the floor when the game is won */}
        <g className={isLost ? "figure-fall" : isWon ? "figure-drop" : ""} style={{ transformOrigin: "130px 205px" }}>
          {/* This inner group handles the continuous dance groove separately
              from the one-time drop above, so they don't fight over transform */}
          <g className={isWon ? "figure-dance" : ""} style={{ transformOrigin: "130px 165px" }}>
            {show(1) && (
              <g className="reveal-part">
                {faceImage ? (
                  <>
                    <defs>
                      <clipPath id="faceClip">
                        <circle cx="130" cy="72" r="22" />
                      </clipPath>
                    </defs>
                    <image
                      href={faceImage}
                      x="108"
                      y="50"
                      width="44"
                      height="44"
                      preserveAspectRatio="xMidYMid slice"
                      clipPath="url(#faceClip)"
                    />
                    <circle cx="130" cy="72" r="22" className="face-ring" fill="none" />
                  </>
                ) : (
                  <>
                    <circle cx="130" cy="72" r="22" className="default-head" />
                    <circle cx="123" cy="68" r="2.2" fill="#240609" />
                    <circle cx="137" cy="68" r="2.2" fill="#240609" />
                    <path d="M122 80 Q130 75 138 80" stroke="#240609" strokeWidth="2" fill="none" />
                  </>
                )}
              </g>
            )}

            {show(2) && (
              <line x1="130" y1="94" x2="130" y2="165" className="gallows-line body reveal-part" />
            )}
            {show(3) && (
              <line
                x1="130" y1="105" x2="102" y2="135"
                className={`gallows-line body reveal-part ${isWon ? "arm-left-dance" : ""}`}
                style={isWon ? { transformOrigin: "130px 105px" } : undefined}
              />
            )}
            {show(4) && (
              <line
                x1="130" y1="105" x2="158" y2="135"
                className={`gallows-line body reveal-part ${isWon ? "arm-right-dance" : ""}`}
                style={isWon ? { transformOrigin: "130px 105px" } : undefined}
              />
            )}
            {show(5) && (
              <line
                x1="130" y1="165" x2="108" y2="205"
                className={`gallows-line body reveal-part ${isWon ? "leg-left-dance" : ""}`}
                style={isWon ? { transformOrigin: "130px 165px" } : undefined}
              />
            )}
            {show(6) && (
              <line
                x1="130" y1="165" x2="152" y2="205"
                className={`gallows-line body reveal-part ${isWon ? "leg-right-dance" : ""}`}
                style={isWon ? { transformOrigin: "130px 165px" } : undefined}
              />
            )}
          </g>
        </g>

        {isLost && (
          <g className="comic-car">
            <g transform="translate(0,-360) scale(2.5)">
              <rect x="0" y="222" width="46" height="16" rx="4" className="car-body" />
              <rect x="8" y="212" width="24" height="14" rx="3" className="car-body" />
              <circle cx="10" cy="238" r="6" className="car-wheel" />
              <circle cx="36" cy="238" r="6" className="car-wheel" />
            </g>
          </g>
        )}
      </svg>

      {wrongCount === 1 && !isLost && !isWon && (
        <div className="gallows-caption">that's... uncomfortably accurate 😬</div>
      )}
      {isLost && (
        <div className="gallows-caption">well, that escalated quickly 🚗</div>
      )}
      {isWon && (
        <div className="gallows-caption">🕺 free at last, and dancing about it</div>
      )}
    </div>
  );
}