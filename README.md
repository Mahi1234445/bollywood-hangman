# Bollywood Hangman

A Hangman game themed around Bollywood movies. Game logic lives entirely in
the FastAPI backend; the React frontend is a pure view layer that renders
whatever state the API sends.

```
bollywood-hangman/
├── backend/                 FastAPI app — owns all game state and rules
│   └── app/
│       ├── main.py          Routes + in-memory session store
│       ├── game_logic.py    GameSession class (pure logic, no HTTP)
│       ├── movies.py        Movie source: live API first, dict fallback
│       ├── models.py        Pydantic request/response schemas
│       └── config.py        Constants (max wrong guesses, CORS origins)
└── frontend/                React + Vite — renders backend state, no game rules
    └── src/
        ├── App.jsx          Orchestrates API calls + top-level state
        ├── api/gameApi.js   fetch wrapper for the backend
        ├── components/      Marquee, Spotlight, WordDisplay, Keyboard, EndCard
        └── styles/theme.css Bollywood cinema visual theme
```

## Why the letter is never sent to the browser

The backend only ever reveals the movie title once the game is `won` or
`lost`. Every guess response is derived server-side, so there's no way to
peek at the answer via devtools — the browser genuinely doesn't know it
until the game ends.

## Running locally

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # optional: add a TMDB_API_KEY later
uvicorn app.main:app --reload --port 8000
```

Check it's alive: open `http://localhost:8000/api/health` — should return
`{"status": "ok"}`. Interactive API docs: `http://localhost:8000/docs`.

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173`.

## Enabling the live movie API

Right now `movies.py` always falls back to the local dictionary because no
`TMDB_API_KEY` is set. To go live:

1. Get a free API key from https://www.themoviedb.org/settings/api
2. Put it in `backend/.env` as `TMDB_API_KEY=your_key_here`
3. Restart the backend — `fetch_random_movie()` will now try TMDb first and
   only fall back to the dictionary if that call fails.

## Where the data/analytics layer plugs in later

`GAMES` in `main.py` is currently an in-memory dict — fine for one process,
gone on restart. When you're ready for the analytics layer:

- Swap `GAMES` for a real store (Postgres/SQLite to start)
- Log each `guess()` call with a timestamp, movie, and outcome to a
  separate `events` table
- Build aggregate queries on top (hardest movies, average guesses per win,
  most active hours) — that's the actual data engineering piece, sitting
  cleanly behind the existing API without touching the frontend at all.
