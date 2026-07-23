export default function EndCard({ status, title, onPlayAgain }) {
  const won = status === "won";
  return (
    <div className="end-card">
      <div className={`end-title ${won ? "win" : "lose"}`}>
        {won ? "Houseful!" : "The End"}
      </div>
      <div className="reveal-title">
        {won ? title : `It was — ${title}`}
      </div>
      <button className="play-btn" onClick={onPlayAgain}>
        {won ? "Next Show →" : "Roll Again →"}
      </button>
    </div>
  );
}
