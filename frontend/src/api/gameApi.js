// - If VITE_API_URL is explicitly set, that always wins.
// - Otherwise: in local dev (`npm run dev`), Vite sets import.meta.env.DEV
//   to true, so we default to the standalone backend on :8000.
// - In a production build (`npm run build`, including the Docker build),
//   DEV is false, so we default to "" — a relative path, correct for the
//   single-service setup where FastAPI serves the built frontend itself
//   and both live on the same origin.
const BASE_URL =
  import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV ? "http://localhost:8000" : "");

async function request(path, options) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

export function startNewGame() {
  return request("/api/game/new", { method: "POST" });
}

export function guessLetter(gameId, letter) {
  return request(`/api/game/${gameId}/guess`, {
    method: "POST",
    body: JSON.stringify({ letter }),
  });
}

export function getGameState(gameId) {
  return request(`/api/game/${gameId}`);
}