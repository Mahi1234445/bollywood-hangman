import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import CORS_ORIGINS
from .game_logic import GameSession
from .models import GameStateResponse, GuessRequest
from .movies import fetch_random_movie

# Load backend/.env explicitly by path, regardless of which directory
# uvicorn was launched from.
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

app = FastAPI(title="Bollywood Hangman API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store. Swap for Redis/DB once this needs to survive
# restarts or scale past a single process.
GAMES: dict[str, GameSession] = {}

TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # unset until you wire up a real key


@app.on_event("startup")
def log_movie_source():
    if TMDB_API_KEY:
        masked = TMDB_API_KEY[:4] + "..." + TMDB_API_KEY[-4:]
        print(f"[bollywood-hangman] .env path checked: {ENV_PATH}")
        print(f"[bollywood-hangman] TMDB_API_KEY loaded: {masked} — live API is active.")
    else:
        print(f"[bollywood-hangman] .env path checked: {ENV_PATH}")
        print("[bollywood-hangman] No TMDB_API_KEY found — using local dictionary only.")


@app.post("/api/game/new", response_model=GameStateResponse)
async def new_game():
    movie = await fetch_random_movie(TMDB_API_KEY)
    game_id = str(uuid.uuid4())
    session = GameSession(game_id=game_id, movie=movie)
    GAMES[game_id] = session
    return session.to_state_dict()


@app.get("/api/game/{game_id}", response_model=GameStateResponse)
def get_game(game_id: str):
    session = GAMES.get(game_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return session.to_state_dict()


@app.post("/api/game/{game_id}/guess", response_model=GameStateResponse)
def guess_letter(game_id: str, body: GuessRequest):
    session = GAMES.get(game_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game not found")
    session.guess(body.letter)
    return session.to_state_dict()


@app.get("/api/health")
def health():
    return {"status": "ok"}