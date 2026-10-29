"""Tests for quiz move parsing and normalization."""

import pytest

from chess_explorer.quiz import normalize_move, split_plies


@pytest.mark.parametrize(
    "guess,expected",
    [
        ("e4", "e4"),
        ("E4", "e4"),
        ("Nf3", "nf3"),
        ("O-O", "oo"),
        ("0-0", "00"),
        ("e5!", "e5!"),
        ("  Nc6  ", "nc6"),
        ("exd5 e.p.", "exd5ep"),
    ],
)
def test_normalize_move(guess, expected):
    assert normalize_move(guess) == expected


def test_split_plies_single_entry():
    assert split_plies(["1. e4 e5 2. Nf3 Nc6 3. Bc4"]) == [
        "e4",
        "e5",
        "Nf3",
        "Nc6",
        "Bc4",
    ]


def test_split_plies_multiple_entries():
    assert split_plies(["1. e4 c5", "2. Nf3 d6", "3. d4 cxd4"]) == [
        "e4",
        "c5",
        "Nf3",
        "d6",
        "d4",
        "cxd4",
    ]


def test_split_plies_black_move_dots():
    assert split_plies(["1... e5 2. Nf3 Nc6"]) == ["e5", "Nf3", "Nc6"]


def test_split_plies_empty():
    assert split_plies([]) == []
    assert split_plies([""]) == []
