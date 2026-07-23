export default function StickFigure({ wrongCount, faceImage }) {
  const show = (n) => wrongCount >= n;

  return (
    <div className="gallows-wrap">
      <svg viewBox="0 0 200 260" className="gallows-svg">
        {/* Gallows structure - always visible */}
        <line x1="20" y1="240" x2="150" y2="240" className="gallows-line" />
        <line x1="55" y1="240" x2="55" y2="20" className="gallows-line" />
        <line x1="55" y1="20" x2="130" y2="20" className="gallows-line" />
        <line x1="130" y1="20" x2="130" y2="50" className="gallows-line rope" />

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
          <line x1="130" y1="105" x2="102" y2="135" className="gallows-line body reveal-part" />
        )}
        {show(4) && (
          <line x1="130" y1="105" x2="158" y2="135" className="gallows-line body reveal-part" />
        )}
        {show(5) && (
          <line x1="130" y1="165" x2="108" y2="205" className="gallows-line body reveal-part" />
        )}
        {show(6) && (
          <line x1="130" y1="165" x2="152" y2="205" className="gallows-line body reveal-part" />
        )}
      </svg>

      {wrongCount === 1 && (
        <div className="gallows-caption">that's... uncomfortably accurate 😬</div>
      )}
    </div>
  );
}
