"""ECO opening data loading, search, and access.

Reads the curated Encyclopedia of Chess Openings sample data shipped
with this package. No external services, no network access.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "eco_openings.json")

_OPENINGS: Optional[dict] = None


@dataclass(frozen=True)
class Opening:
    code: str
    name: str
    moves: list[str]
    tags: list[str]

    @property
    def move_count(self) -> int:
        return len(self.moves)


def _load_openings() -> dict:
    global _OPENINGS
    if _OPENINGS is None:
        with open(DATA_FILE, "r", encoding="utf-8") as handle:
            _OPENINGS = json.load(handle)["openings"]
    return _OPENINGS


def list_openings() -> dict[str, Opening]:
    """Return every opening in the data file, keyed by ECO code."""
    raw = _load_openings()
    return {
        code: Opening(
            code=code,
            name=entry.get("name", ""),
            moves=list(entry.get("moves", [])),
            tags=list(entry.get("tags", [])),
        )
        for code, entry in raw.items()
    }


def get_opening(code: str) -> Optional[Opening]:
    """Return the opening for an ECO code, or None if not found."""
    code = code.strip().upper()
    raw = _load_openings()
    if code not in raw:
        return None
    entry = raw[code]
    return Opening(
        code=code,
        name=entry.get("name", ""),
        moves=list(entry.get("moves", [])),
        tags=list(entry.get("tags", [])),
    )


def search_openings(query: str) -> list[Opening]:
    """Search openings by ECO code or name (case-insensitive substring)."""
    q = query.strip().lower()
    if not q:
        return []
    matches: list[Opening] = []
    for opening in list_openings().values():
        if q in opening.code.lower() or q in opening.name.lower():
            matches.append(opening)
    matches.sort(key=lambda o: (not o.code.lower().startswith(q), o.code))
    return moves_sanitized(matches)


def moves_sanitized(openings: list[Opening]) -> list[Opening]:
    """Ensure move strings carry no trailing whitespace artifacts."""
    return [
        Opening(
            code=o.code,
            name=o.name,
            moves=[mv.strip() for mv in o.moves],
            tags=list(o.tags),
        )
        for o in openings
    ]


def all_codes() -> list[str]:
    """Return sorted ECO codes present in the data file."""
    return sorted(_load_openings().keys())
