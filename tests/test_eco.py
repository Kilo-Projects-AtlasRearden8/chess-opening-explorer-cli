"""Tests for ECO opening data parsing and access."""

import pytest

from chess_explorer.eco import get_opening, list_openings, search_openings


def test_list_openings_returns_all_codes():
    openings = list_openings()
    assert len(openings) >= 10
    assert "C50" in openings
    assert "B01" in openings


def test_get_opening_known_code():
    opening = get_opening("C50")
    assert opening is not None
    assert opening.code == "C50"
    assert "Italian" in opening.name
    assert opening.move_count > 0


def test_get_opening_case_insensitive():
    assert get_opening("c50") is not None
    assert get_opening(" C50 ") is not None


def test_get_opening_unknown_code():
    assert get_opening("Z99") is None
    assert get_opening("") is None


def test_search_by_name():
    results = search_openings("sicilian")
    codes = {o.code for o in results}
    assert "B20" in codes
    assert all("Sicilian" in o.name for o in results)


def test_search_by_code_prefix():
    results = search_openings("C5")
    codes = {o.code for o in results}
    assert "C50" in codes
    assert "C53" in codes


def test_search_returns_none_for_empty():
    assert search_openings("") == []
    assert search_openings("   ") == []


def test_search_unknown_returns_empty():
    assert search_openings("zzzzz") == []


@pytest.mark.parametrize(
    "code,expected_name_fragment",
    [
        ("B01", "Scandinavian"),
        ("C65", "Berlin"),
        ("C89", "Marshall"),
        ("E50", "Rubinstein"),
    ],
)
def test_search_finds_famous_opening(code, expected_name_fragment):
    opening = get_opening(code)
    assert opening is not None
    assert expected_name_fragment in opening.name


def test_opening_moves_are_strings():
    opening = get_opening("C74")
    assert opening is not None
    assert all(isinstance(mv, str) and mv for mv in opening.moves)
