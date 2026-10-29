"""Tests for quiz scoring helpers."""

import pytest

from chess_explorer.scoring import (
    MoveResult,
    SessionScore,
    accuracy,
    compute_streak,
    grade_from_accuracy,
    score_session,
)


def test_accuracy_perfect():
    assert accuracy(10, 10) == 100.0


def test_accuracy_zero_attempts():
    assert accuracy(0, 0) == 0.0


def test_accuracy_half():
    assert accuracy(3, 4) == 75.0


def test_accuracy_rounding():
    assert accuracy(1, 3) == 33.33


def test_grade_boundaries():
    assert grade_from_accuracy(100.0) == "A"
    assert grade_from_accuracy(90.0) == "A"
    assert grade_from_accuracy(89.99) == "B"
    assert grade_from_accuracy(80.0) == "B"
    assert grade_from_accuracy(70.0) == "C"
    assert grade_from_accuracy(60.0) == "D"
    assert grade_from_accuracy(0.0) == "F"


def test_compute_streak_all_correct():
    assert compute_streak([True, True, True]) == (3, 3)


def test_compute_streak_all_wrong():
    assert compute_streak([False, False]) == (0, 0)


def test_compute_streak_mixed():
    assert compute_streak([True, True, False, True, True, True, False, True]) == (1, 3)


def test_compute_streak_empty():
    assert compute_streak([]) == (0, 0)


def test_score_session():
    results = [
        MoveResult(eco="C50", move_index=0, expected="1. e4", guessed="e4", correct=True),
        MoveResult(eco="C50", move_index=1, expected="2. Nf3", guessed="Nf3", correct=True),
        MoveResult(eco="C50", move_index=2, expected="3. Bc4", guessed="Bc5", correct=False),
    ]
    score = score_session("C50", "Italian Game", results)
    assert isinstance(score, SessionScore)
    assert score.attempts == 3
    assert score.correct == 2
    assert score.accuracy == 66.67
    assert score.streak == 0
    assert score.best_streak == 2
    assert score.grade == "D"
    assert score.total_moves == 3


def test_score_session_empty():
    score = score_session("B20", "Sicilian Defense", [])
    assert score.attempts == 0
    assert score.correct == 0
    assert score.accuracy == 0.0
    assert score.grade == "F"
