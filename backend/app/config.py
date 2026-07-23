"""Central config/constants for the game backend."""

MAX_WRONG_GUESSES = 6

# Frontend dev server origin(s) allowed to call this API.
# Add your deployed frontend URL here once you host it.
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
