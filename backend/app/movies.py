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
# ---------------------------------------------------------------------------
MOVIES: list[dict] = [
    {"title": "SHOLAY", "hint": "1975 · Action/Drama"},
    {"title": "DILWALE DULHANIA LE JAYENGE", "hint": "1995 · Romance"},
    {"title": "LAGAAN", "hint": "2001 · Sports/Drama"},
    {"title": "KABHI KHUSHI KABHIE GHAM", "hint": "2001 · Family Drama"},
    {"title": "ZINDAGI NA MILEGI DOBARA", "hint": "2011 · Road Trip"},
    {"title": "GULLY BOY", "hint": "2019 · Musical Drama"},
    {"title": "ANDHADHUN", "hint": "2018 · Thriller"},
    {"title": "QUEEN", "hint": "2013 · Comedy Drama"},
    {"title": "DANGAL", "hint": "2016 · Sports/Biopic"},
    {"title": "BAAHUBALI", "hint": "2015 · Epic Action"},
    {"title": "OM SHANTI OM", "hint": "2007 · Reincarnation Drama"},
    {"title": "3 IDIOTS", "hint": "2009 · Comedy Drama"},
    {"title": "SWADES", "hint": "2004 · Drama"},
    {"title": "CHAK DE INDIA", "hint": "2007 · Sports Drama"},
    {"title": "BARFI", "hint": "2012 · Romance"},
    {"title": "TAARE ZAMEEN PAR", "hint": "2007 · Drama"},
    {"title": "PIKU", "hint": "2015 · Comedy Drama"},
    {"title": "RANG DE BASANTI", "hint": "2006 · Drama"},
    {"title": "KAL HO NAA HO", "hint": "2003 · Romance"},
    {"title": "MASAAN", "hint": "2015 · Drama"},
    {"title": "PYAAR KA PUNCHNAMA", "hint": "2011 · Comedy"},
    {"title": "GOLMAAL", "hint": "2006 · Comedy"},
    {"title": "DIL CHAHTA HAI", "hint": "2001 · Coming of Age"},
    {"title": "PADMAAVAT", "hint": "2018 · Period Drama"},
    {"title": "ARTICLE 15", "hint": "2019 · Crime Drama"},
]

# TMDb discover endpoint, filtered to Hindi-language originals.
# Set TMDB_API_KEY as an environment variable to activate this path.
TMDB_URL = "https://api.themoviedb.org/3/discover/movie"


@dataclass
class Movie:
    title: str
    hint: str


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
            logger.info("TMDb pick: %s (%s)", choice["title"], year)
            return Movie(
                title=choice["title"].upper(),
                hint=f"{year} · TMDb pick",
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
    return Movie(title=choice["title"], hint=choice["hint"])


async def fetch_random_movie(tmdb_api_key: str | None = None) -> Movie:
    """Try the live API, fall back to the local dictionary on any failure."""
    movie = await _fetch_from_tmdb(tmdb_api_key)
    if movie is not None:
        return movie
    return _fetch_from_dictionary()