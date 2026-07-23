import { useEffect } from "react";

const ROWS = ["1234567890", "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"];

export default function Keyboard({ guessedLetters, incorrectLetters, onGuess, disabled }) {
  useEffect(() => {
    function onKey(e) {
      const k = e.key.toUpperCase();
      if (/^[A-Z0-9]$/.test(k) && !disabled) onGuess(k);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onGuess, disabled]);

  return (
    <div className="keyboard">
      {ROWS.map((row, ri) => (
        <div key={ri} className="kb-row">
          {row.split("").map((L) => {
            const isGuessed = guessedLetters.includes(L);
            const isIncorrect = incorrectLetters.includes(L);
            const cls = isGuessed ? (isIncorrect ? "incorrect" : "correct") : "";
            return (
              <button
                key={L}
                className={`key ${cls}`}
                disabled={isGuessed || disabled}
                onClick={() => onGuess(L)}
              >
                {L}
              </button>
            );
          })}
        </div>
      ))}
    </div>
  );
}