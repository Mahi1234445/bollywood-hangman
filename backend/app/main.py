import os
import uuid
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
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
    allow_credentials=False,
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
# ---------------- Serve React in production ----------------
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Docker location
FRONTEND_DIR = Path("/app/frontend/dist")

print("=" * 60)
print("Initial FRONTEND_DIR:", FRONTEND_DIR)
print("Exists:", FRONTEND_DIR.exists())

# Local development fallback
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path(__file__).resolve().parents[3] / "frontend" / "dist"
    print("Using fallback path:", FRONTEND_DIR)
    print("Fallback exists:", FRONTEND_DIR.exists())

print("Final FRONTEND_DIR:", FRONTEND_DIR)

if FRONTEND_DIR.exists():
    print("Contents:", list(FRONTEND_DIR.iterdir()))
    assets_dir = FRONTEND_DIR / "assets"
    print("Assets exists:", assets_dir.exists())

    if assets_dir.exists():
        print("Asset files:", list(assets_dir.iterdir()))

        app.mount(
            "/assets",
            StaticFiles(directory=assets_dir),
            name="assets",
        )

    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        return FileResponse(FRONTEND_DIR / "index.html")

print("=" * 60)