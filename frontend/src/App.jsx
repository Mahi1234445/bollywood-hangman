import { useCallback, useEffect, useState } from "react";
import Marquee from "./components/Marquee";
import StickFigure from "./components/StickFigure";
import FaceUpload from "./components/FaceUpload";
import WordDisplay from "./components/WordDisplay";
import Keyboard from "./components/Keyboard";
import EndCard from "./components/EndCard";
import { startNewGame, guessLetter } from "./api/gameApi";
import "./styles/theme.css";

export default function App() {
  const [state, setState] = useState(null); // full state dict from backend
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [faceImage, setFaceImage] = useState(null);
  const [faceChoiceMade, setFaceChoiceMade] = useState(false);

  const newGame = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await startNewGame();
      setState(data);
    } catch (e) {
      setError("Couldn't reach the game server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    newGame();
  }, [newGame]);

  const onGuess = useCallback(
    async (letter) => {
      if (!state) return;
      const prevStatus = state.status;
      const updated = await guessLetter(state.game_id, letter);
      setState(updated);
      if (prevStatus === "playing" && updated.status === "won") {
        setScore((s) => s + Math.max(10 - updated.wrong_count, 4));
        setStreak((s) => s + 1);
      }
      if (prevStatus === "playing" && updated.status === "lost") {
        setStreak(0);
      }
    },
    [state]
  );

  return (
    <div className="stage">
      <Marquee score={score} streak={streak} />

      <div className={`theatre status-${state?.status || "loading"}`}>
        {loading && <div className="loading-wrap">Rolling the reel...</div>}
        {error && <div className="loading-wrap">{error}</div>}

        {!loading && !error && !faceChoiceMade && (
          <FaceUpload
            onFaceReady={(dataUrl) => {
              setFaceImage(dataUrl);
              setFaceChoiceMade(true);
            }}
            onSkip={() => setFaceChoiceMade(true)}
          />
        )}

        {!loading && !error && faceChoiceMade && state && (
          <>
            <StickFigure wrongCount={state.wrong_count} faceImage={faceImage} />

            {state.status === "playing" && (
              <>
                <WordDisplay display={state.display} hint={state.hint} />
                <Keyboard
                  guessedLetters={state.guessed_letters}
                  incorrectLetters={state.incorrect_letters}
                  onGuess={onGuess}
                  disabled={state.status !== "playing"}
                />
              </>
            )}

            {(state.status === "won" || state.status === "lost") && (
              <EndCard status={state.status} title={state.title} onPlayAgain={newGame} />
            )}
          </>
        )}
      </div>
    </div>
  );
}
