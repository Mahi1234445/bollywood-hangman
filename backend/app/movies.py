"""
Movie data source.

fetch_random_movie() is the single entry point the game logic calls.
It tries a live API first; if that fails for ANY reason (no key configured
yet, network error, timeout, bad response), it transparently falls back to
the local MOVIES dictionary below. Nothing upstream needs to know which
path was used.
"""

import logging
import random
from dataclasses import dataclass

import httpx

logger = logging.getLogger("bollywood_hangman.movies")

# ---------------------------------------------------------------------------
# Local fallback dictionary. This is the source of truth until a real API
# key is wired up, and stays as the safety net afterwards.
# Each entry carries year / genre / storyline as separate fields so the
# frontend can offer them as independent, clickable hints.
# ---------------------------------------------------------------------------
MOVIES: list[dict] = [
    {"title": "SHOLAY", "year": "1975", "genre": "Action/Drama",
     "storyline": "Two small-time crooks are hired by a retired police officer to capture the ruthless bandit who destroyed his family."},
    {"title": "DILWALE DULHANIA LE JAYENGE", "year": "1995", "genre": "Romance",
     "storyline": "A carefree young man falls for a woman promised to someone else back home, and follows her across countries to win her family over."},
    {"title": "LAGAAN", "year": "2001", "genre": "Sports/Drama",
     "storyline": "Villagers under colonial rule wager their crushing tax burden on the outcome of a cricket match against their rulers."},
    {"title": "KABHI KHUSHI KABHIE GHAM", "year": "2001", "genre": "Family Drama",
     "storyline": "A wealthy family fractures when the elder son marries against his father's wishes, and the years-long rift threatens to break them apart for good."},
    {"title": "ZINDAGI NA MILEGI DOBARA", "year": "2011", "genre": "Road Trip",
     "storyline": "Three childhood friends take a bachelor road trip through Spain, each confronting a fear and a truth about their own life along the way."},
    {"title": "GULLY BOY", "year": "2019", "genre": "Musical Drama",
     "storyline": "A young man from Mumbai's slums discovers rap as a way to voice his frustrations and claw his way toward a bigger life."},
    {"title": "ANDHADHUN", "year": "2018", "genre": "Thriller",
     "storyline": "A blind pianist becomes an unwitting witness to a murder, and must decide how much to reveal to survive what he's stumbled into."},
    {"title": "QUEEN", "year": "2013", "genre": "Comedy Drama",
     "storyline": "Left at the altar days before her wedding, a sheltered woman goes on her planned honeymoon alone and discovers who she is outside her old life."},
    {"title": "DANGAL", "year": "2016", "genre": "Sports/Biopic",
     "storyline": "A former wrestler trains his daughters to become championship wrestlers, defying small-town expectations of what girls are allowed to become."},
    {"title": "BAAHUBALI", "year": "2015", "genre": "Epic Action",
     "storyline": "A young man raised outside his kingdom uncovers a buried royal legacy and a betrayal that shaped his family's fate."},
    {"title": "OM SHANTI OM", "year": "2007", "genre": "Reincarnation Drama",
     "storyline": "A junior actor killed while trying to save his secret love is reborn decades later, drawn back toward the people who wronged him."},
    {"title": "3 IDIOTS", "year": "2009", "genre": "Comedy Drama",
     "storyline": "Two friends search for their long-lost college roommate, whose free-spirited approach to learning once upended their rigid engineering school."},
    {"title": "SWADES", "year": "2004", "genre": "Drama",
     "storyline": "A NASA scientist returns to his childhood village in India and is quietly transformed by the community he thought he'd left behind for good."},
    {"title": "CHAK DE INDIA", "year": "2007", "genre": "Sports Drama",
     "storyline": "A disgraced former hockey captain gets a second chance by coaching the women's national team, and has to earn their trust from zero."},
    {"title": "BARFI", "year": "2012", "genre": "Romance",
     "storyline": "A deaf-mute young man's playful charm draws in two very different women, and his story becomes tangled with a missing-persons mystery years later."},
    {"title": "TAARE ZAMEEN PAR", "year": "2007", "genre": "Drama",
     "storyline": "A struggling young boy with dyslexia is written off by everyone until a new art teacher notices what his family and school have missed."},
    {"title": "PIKU", "year": "2015", "genre": "Comedy Drama",
     "storyline": "A stubborn elderly father, obsessed with his health, drags his exasperated daughter on a road trip that tests both their patience and their bond."},
    {"title": "RANG DE BASANTI", "year": "2006", "genre": "Drama",
     "storyline": "A group of carefree college friends are shaken out of their apathy while filming a documentary, and drift toward an act of real consequence."},
    {"title": "KAL HO NAA HO", "year": "2003", "genre": "Romance",
     "storyline": "A dying man secretly orchestrates a romance between his neighbor and her best friend, choosing to give away the happiness he can't keep."},
    {"title": "MASAAN", "year": "2015", "genre": "Drama",
     "storyline": "Two strangers in a small town on the Ganges each carry private shame and grief, their lives quietly intersecting against the weight of tradition."},
    {"title": "PYAAR KA PUNCHNAMA", "year": "2011", "genre": "Comedy",
     "storyline": "Three roommates' relationships slowly unravel, building to a legendary rant about the everyday absurdities of modern dating."},
    {"title": "GOLMAAL", "year": "2006", "genre": "Comedy",
     "storyline": "A group of friends' web of lies to their strict guardian spirals into escalating chaos neither they nor he can keep straight."},
    {"title": "DIL CHAHTA HAI", "year": "2001", "genre": "Coming of Age",
     "storyline": "Three lifelong friends drift apart over love and ego after college, and slowly find their way back to what held them together."},
    {"title": "PADMAAVAT", "year": "2018", "genre": "Period Drama",
     "storyline": "A queen's fabled beauty draws the obsession of a ruthless sultan, setting a proud kingdom on a collision course with siege and war."},
    {"title": "ARTICLE 15", "year": "2019", "genre": "Crime Drama",
     "storyline": "A city-raised police officer posted to a rural district uncovers a case that forces him to confront a caste divide he never had to see before."},
]

# TMDb genre_ids are numeric and not included by name in the discover
# response — this is the standard, stable movie-genre list TMDb uses.
TMDB_GENRE_MAP: dict[int, str] = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western",
}

# TMDb discover endpoint, filtered to Hindi-language originals.
# Set TMDB_API_KEY as an environment variable to activate this path.
TMDB_URL = "https://api.themoviedb.org/3/discover/movie"


@dataclass
class Movie:
    title: str
    year: str
    genre: str
    storyline: str


def _genre_names(genre_ids: list[int]) -> str:
    names = [TMDB_GENRE_MAP.get(gid) for gid in genre_ids]
    names = [n for n in names if n]
    return "/".join(names[:2]) if names else "Unknown"


async def _fetch_from_tmdb(api_key: str | None) -> Movie | None:
    if not api_key:
        return None
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(
                TMDB_URL,
                params={
                    "api_key": api_key,
                    "with_original_language": "hi",
                    "sort_by": "popularity.desc",
                    "page": random.randint(1, 20),
                },
            )
            resp.raise_for_status()
            results = resp.json().get("results", [])
            if not results:
                logger.warning("TMDb returned no results — falling back to dictionary.")
                return None
            choice = random.choice(results)
            year = (choice.get("release_date") or "----")[:4]
            genre = _genre_names(choice.get("genre_ids", []))
            storyline = choice.get("overview") or "No storyline available for this one."
            logger.info("TMDb pick: %s (%s)", choice["title"], year)
            return Movie(
                title=choice["title"].upper(),
                year=year,
                genre=genre,
                storyline=storyline,
            )
    except (httpx.HTTPError, KeyError, ValueError) as e:
        logger.warning(
            "TMDb call failed (%s: %s) — falling back to dictionary.",
            type(e).__name__,
            e,
        )
        return None


def _fetch_from_dictionary() -> Movie:
    choice = random.choice(MOVIES)
    return Movie(
        title=choice["title"],
        year=choice["year"],
        genre=choice["genre"],
        storyline=choice["storyline"],
    )


async def fetch_random_movie(tmdb_api_key: str | None = None) -> Movie:
    """Try the live API, fall back to the local dictionary on any failure."""
    movie = await _fetch_from_tmdb(tmdb_api_key)
    if movie is not None:
        return movie
    return _fetch_from_dictionary()
