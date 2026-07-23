from pydantic import BaseModel, Field


class GuessRequest(BaseModel):
    letter: str = Field(..., min_length=1, max_length=1)


class GameStateResponse(BaseModel):
    game_id: str
    display: list[str]
    year: str
    genre: str
    storyline: str
    guessed_letters: list[str]
    incorrect_letters: list[str]
    wrong_count: int
    lives_left: int
    max_wrong: int
    status: str
    title: str | None = None
