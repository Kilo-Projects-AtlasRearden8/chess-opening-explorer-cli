"""Command-line interface for the Chess Opening Explorer."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from . import __version__
from .eco import get_opening, list_openings, search_openings
from .quiz import quiz_open
from .scoring import SessionScore

FAVORITES_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "user_data", "favorites.md"
)
PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "user_data", "progress.json"
)


def _fmt_opening(opening) -> str:
    tags = f" [{', '.join(opening.tags)}]" if opening.tags else ""
    moves = f"\n  Moves: {' '.join(opening.moves)}" if opening.moves else "\n  Moves: (none recorded)"
    return f"{opening.code} {opening.name}{tags}{moves}"


def cmd_search(args: argparse.Namespace) -> int:
    results = search_openings(args.query)
    if not results:
        print(f"No openings matched '{args.query}'.")
        return 1
    print(f"Found {len(results)} opening(s):")
    for opening in results:
        print("  " + _fmt_opening(opening).replace("\n", "\n    "))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    opening = get_opening(args.code)
    if opening is None:
        print(f"Unknown ECO code: {args.code}")
        return 1
    print(_fmt_opening(opening))
    if not opening.moves:
        print("  No move sequence recorded for this code.")
    return 0


def _read_favorites() -> list[str]:
    if not os.path.exists(FAVORITES_FILE):
        return []
    codes: list[str] = []
    with open(FAVORITES_FILE, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line.startswith("- ") and " (" in line:
                code = line.split(" (", 1)[1].rstrip(")")
                if code:
                    codes.append(code)
    return codes


def _write_favorites(codes: list[str]) -> None:
    os.makedirs(os.path.dirname(FAVORITES_FILE) or ".", exist_ok=True)
    seen: list[str] = []
    for code in codes:
        if code not in seen:
            seen.append(code)
    with open(FAVORITES_FILE, "w", encoding="utf-8") as handle:
        handle.write("# Favorite Chess Openings\n\n")
        handle.write("Saved locally with the Chess Opening Explorer CLI.\n\n")
        for code in seen:
            opening = get_opening(code)
            if opening is None:
                handle.write(f"- {code} (data unavailable)\n")
            else:
                handle.write(f"- {opening.name} ({code})\n")
        handle.write("\n")


def cmd_favorite_add(args: argparse.Namespace) -> int:
    opening = get_opening(args.code)
    if opening is None:
        print(f"Unknown ECO code: {args.code}")
        return 1
    codes = _read_favorites()
    if args.code in codes:
        print(f"{args.code} ({opening.name}) is already a favorite.")
        return 0
    codes.append(args.code)
    _write_favorites(codes)
    print(f"Added {opening.name} ({args.code}) to favorites.")
    return 0


def cmd_favorite_list(args: argparse.Namespace) -> int:
    codes = _read_favorites()
    if not codes:
        print("No favorites yet. Add one with: favorite add <ECO>")
        return 0
    print("Favorite openings:")
    for code in codes:
        opening = get_opening(code)
        if opening is None:
            print(f"  {code} (data unavailable)")
        else:
            print(f"  {opening.name} ({code})")
    return 0


def cmd_favorite_remove(args: argparse.Namespace) -> int:
    codes = _read_favorites()
    opening = get_opening(args.code)
    if args.code not in codes:
        name = opening.name if opening else args.code
        print(f"{name} ({args.code}) is not in your favorites.")
        return 0
    codes = [c for c in codes if c != args.code]
    _write_favorites(codes)
    name = opening.name if opening else args.code
    print(f"Removed {name} ({args.code}) from favorites.")
    return 0


def cmd_quiz(args: argparse.Namespace) -> int:
    score: Optional[SessionScore] = quiz_open(args.code, PROGRESS_FILE, interactive=not args.stdin)
    if score is None:
        print(f"Cannot quiz unknown or empty opening: {args.code}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chess-openings",
        description="Explore chess openings locally: search ECO codes, save favorites, quiz move order.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Search openings by ECO code or name")
    p_search.add_argument("query", help="Search text (ECO code or opening name)")
    p_search.set_defaults(func=cmd_search)

    p_show = sub.add_parser("show", help="Show details for an ECO code")
    p_show.add_argument("code", help="ECO code (e.g. C50)")
    p_show.set_defaults(func=cmd_show)

    p_fav = sub.add_parser("favorite", help="Manage favorite opening lines (saved as Markdown)")
    fav_sub = p_fav.add_subparsers(dest="action", required=True)

    p_fav_add = fav_sub.add_parser("add", help="Add an opening to favorites")
    p_fav_add.add_argument("code", help="ECO code")
    p_fav_add.set_defaults(func=cmd_favorite_add)

    p_fav_list = fav_sub.add_parser("list", help="List favorite openings")
    p_fav_list.set_defaults(func=cmd_favorite_list)

    p_fav_rem = fav_sub.add_parser("remove", help="Remove an opening from favorites")
    p_fav_rem.add_argument("code", help="ECO code")
    p_fav_rem.set_defaults(func=cmd_favorite_remove)

    p_quiz = sub.add_parser("quiz", help="Quiz move order for an opening (progress saved to JSON)")
    p_quiz.add_argument("code", help="ECO code (e.g. C50)")
    p_quiz.add_argument(
        "--stdin",
        action="store_true",
        help="Read guesses from stdin (for testing/automation)",
    )
    p_quiz.set_defaults(func=cmd_quiz)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
