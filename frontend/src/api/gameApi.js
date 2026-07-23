const BASE_URL = "";
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
