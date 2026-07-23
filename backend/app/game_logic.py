"""
Pure game logic, kept separate from the API layer so it's independently
testable and doesn't know anything about HTTP.
"""

from dataclasses import dataclass, field

from .config import MAX_WRONG_GUESSES
from .movies import Movie


@dataclass
class GameSession:
    game_id: str
    movie: Movie
    guessed_letters: set[str] = field(default_factory=set)
    wrong_count: int = 0

    @property
    def unique_letters(self) -> set[str]:
        # Includes digits too, so titles like "Khiladi 786" require
        # guessing each number just like a letter — nothing auto-reveals.
        return {c for c in self.movie.title if c.isalnum()}

    @property
    def lives_left(self) -> int:
        return max(MAX_WRONG_GUESSES - self.wrong_count, 0)

    @property
    def status(self) -> str:
        if self.unique_letters.issubset(self.guessed_letters):
            return "won"
        if self.wrong_count >= MAX_WRONG_GUESSES:
            return "lost"
        return "playing"

    def display_pattern(self) -> list[str]:
        """Returns the title as a list of chars, blanked unless guessed
        (or unless the game has ended, in which case it's fully revealed)."""
        reveal_all = self.status in ("won", "lost")
        out = []
        for ch in self.movie.title:
            if ch == " ":
                out.append(" ")
            elif ch in self.guessed_letters or reveal_all:
                out.append(ch)
            else:
                out.append("_")
        return out

    def guess(self, letter: str) -> None:
        letter = letter.upper()
        if self.status != "playing":
            return
        if letter in self.guessed_letters:
            return
        self.guessed_letters.add(letter)
        if letter not in self.movie.title:
            self.wrong_count += 1

    def to_state_dict(self) -> dict:
        incorrect = sorted(l for l in self.guessed_letters if l not in self.movie.title)
        return {
            "game_id": self.game_id,
            "display": self.display_pattern(),
            "year": self.movie.year,
            "genre": self.movie.genre,
            "storyline": self.movie.storyline,
            "guessed_letters": sorted(self.guessed_letters),
            "incorrect_letters": incorrect,
            "wrong_count": self.wrong_count,
            "lives_left": self.lives_left,
            "max_wrong": MAX_WRONG_GUESSES,
            "status": self.status,
            # Title is only ever sent once the game is over.
            "title": self.movie.title if self.status in ("won", "lost") else None,
        }
