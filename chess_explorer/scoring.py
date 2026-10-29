"""Scoring helpers for the move-order quiz.

Pure functions with no side effects: easy to unit test, easy to reason
about. All scores are computed locally and persisted as JSON.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class MoveResult:
    eco: str
    move_index: int
    expected: str
    guessed: str
    correct: bool
    hint_used: bool = False


@dataclass(frozen=True)
class SessionScore:
    eco: str
    name: str
    total_moves: int
    attempts: int
    correct: int
    accuracy: float
    streak: int
    best_streak: int
    grade: str


def accuracy(correct: int, attempts: int) -> float:
    """Percentage of correct guesses, 0-100. Zero attempts yields 0.0."""
    if attempts <= 0:
        return 0.0
    return round(100.0 * correct / attempts, 2)


def grade_from_accuracy(value: float) -> str:
    """Letter grade for an accuracy percentage."""
    if value >= 90.0:
        return "A"
    if value >= 80.0:
        return "B"
    if value >= 70.0:
        return "C"
    if value >= 60.0:
        return "D"
    return "F"


def compute_streak(results: Iterable[bool]) -> tuple[int, int]:
    """Return (current_streak, best_streak) from a sequence of booleans."""
    current = 0
    best = 0
    for ok in results:
        if ok:
            current += 1
            if current > best:
                best = current
        else:
            current = 0
    return current, best


def score_session(eco: str, name: str, results: list[MoveResult]) -> SessionScore:
    """Aggregate a finished quiz session into a SessionScore."""
    total_moves = len({r.move_index for r in results}) if results else 0
    attempts = len(results)
    correct = sum(1 for r in results if r.correct)
    acc = accuracy(correct, attempts)
    streak, best = compute_streak([r.correct for r in results])
    return SessionScore(
        eco=eco,
        name=name,
        total_moves=total_moves,
        attempts=attempts,
        correct=correct,
        accuracy=acc,
        streak=streak,
        best_streak=best,
        grade=grade_from_accuracy(acc),
    )


def session_to_dict(score: SessionScore) -> dict:
    return {
        "eco": score.eco,
        "name": score.name,
        "total_moves": score.total_moves,
        "attempts": score.attempts,
        "correct": score.correct,
        "accuracy": score.accuracy,
        "streak": score.streak,
        "best_streak": score.best_streak,
        "grade": score.grade,
    }
