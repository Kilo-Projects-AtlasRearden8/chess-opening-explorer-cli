"""Interactive move-order quiz.

The user is shown the moves played so far and must type the next move in
SAN. Results are scored and appended to a local JSON progress file.
"""

from __future__ import annotations

import re
import datetime as _dt
import json
import os
from typing import Optional

from .eco import Opening, get_opening
from .scoring import MoveResult, SessionScore, score_session, session_to_dict


MOVE_NUMBER_RE = re.compile(r"\d+\.\.\.?|\d+\.")


def normalize_move(text: str) -> str:
    """Normalize a user's move guess for comparison: strip numbers/dots/spaces."""
    cleaned = "".join(ch for ch in text if ch.isalnum() or ch in "+#=!?").strip()
    return cleaned.lower()


def split_plies(move_strings: list[str]) -> list[str]:
    """Split stored SAN strings into individual ply tokens.

    "1. e4 e5 2. Nf3" -> ["e4", "e5", "Nf3"]
    """
    tokens: list[str] = []
    for entry in move_strings:
        cleaned = MOVE_NUMBER_RE.sub(" ", entry)
        for part in cleaned.split():
            tokens.append(part)
    return tokens


def quiz_open(eco: str, progress_path: str, interactive: bool = True) -> Optional[SessionScore]:
    """Run a quiz session for an opening.

    When ``interactive`` is False, reads guesses from stdin line by line
    (useful for automated smoke tests) and still writes progress.
    Returns the SessionScore, or None if the opening was not found.
    """
    opening: Optional[Opening] = get_opening(eco)
    if opening is None or not opening.moves:
        return None

    tokens = split_plies(opening.moves)
    results: list[MoveResult] = []
    move_index = 0

    print(f"Quiz: {opening.code} {opening.name}")
    print(f"Moves to learn ({len(tokens)} plies): {' '.join(opening.moves)}")
    print("Type each move in SAN (e.g. e4, Nf3, O-O). Type 'quit' to stop.\n")

    shown = ""
    while move_index < len(tokens):
        prefix = " ".join(opening.moves[:move_index])
        prompt = f"Move {move_index + 1}/{len(tokens)} [{prefix}] > " if prefix else f"Move {move_index + 1}/{len(tokens)} > "
        if interactive:
            try:
                guess = input(prompt)
            except (EOFError, KeyboardInterrupt):
                print("\nQuiz interrupted.")
                break
        else:
            guess = input(prompt)  # stdin is redirected in non-interactive mode too
        guess = guess.strip()
        if guess.lower() in {"quit", "q", "exit"}:
            print("Quiz ended early.")
            break

        correct = normalize_move(guess) == tokens[move_index]
        results.append(
            MoveResult(
                eco=opening.code,
                move_index=move_index,
                expected=tokens[move_index],
                guessed=guess,
                correct=correct,
            )
        )
        if correct:
            print("  Correct!")
        else:
            print(f"  Not quite. Expected: {tokens[move_index]}")
        move_index += 1

    score = score_session(opening.code, opening.name, results)
    _save_progress(progress_path, score, results)
    print(f"\nSession complete: {score.correct}/{score.attempts} correct  "
          f"({score.accuracy}%)  Grade {score.grade}  Best streak: {score.best_streak}")
    return score


def _load_progress(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_progress(path: str, score: SessionScore, results: list[MoveResult]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    data = _load_progress(path)
    entry = session_to_dict(score)
    entry["last_played"] = _dt.datetime.now().isoformat(timespec="seconds")
    per_move: dict[str, dict] = {}
    for r in results:
        key = f"{r.move_index}:{r.expected}"
        slot = per_move.setdefault(key, {"attempts": 0, "correct": 0})
        slot["attempts"] += 1
        if r.correct:
            slot["correct"] += 1
    entry["moves"] = per_move

    previous = data.get(score.eco, {})
    if previous:
        # Merge with history: simple running tally.
        prev_attempts = previous.get("attempts", 0)
        prev_correct = previous.get("correct", 0)
        entry["attempts"] = prev_attempts + score.attempts
        entry["correct"] = prev_correct + score.correct
        entry["accuracy"] = round(100.0 * entry["correct"] / entry["attempts"], 2) if entry["attempts"] else 0.0
        entry["grade"] = _grade(entry["accuracy"])
        old_best = previous.get("best_streak", 0)
        entry["best_streak"] = max(score.best_streak, old_best)

    data[score.eco] = entry
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
    os.replace(tmp, path)


def _grade(value: float) -> str:
    if value >= 90.0:
        return "A"
    if value >= 80.0:
        return "B"
    if value >= 70.0:
        return "C"
    if value >= 60.0:
        return "D"
    return "F"
