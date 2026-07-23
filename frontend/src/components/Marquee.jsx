export default function Marquee({ score, streak }) {
  return (
    <>
      <div className="marquee-wrap">
        <h1 className="marquee-title">Bollywood Hangman</h1>
        <div className="marquee-sub">Ek dialogue, ek movie, chaar galtiyaan</div>
      </div>
      <div className="scoreboard">
        <div className="chip">Score <b>{score}</b></div>
        <div className="chip">Streak <b>{streak}</b></div>
      </div>
    </>
  );
}
