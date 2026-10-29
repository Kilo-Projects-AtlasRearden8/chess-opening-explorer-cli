# STATUS

Chess Opening Explorer CLI — fan project credited to Asdale Dynamics, LLC.

## What was built

A local-first, dependency-free Python CLI for exploring chess openings:

- **ECO search** (`search <query>`): find openings by ECO code or name in the
  curated `chess_explorer/data/eco_openings.json` sample (55 openings across
  A–E codes, with SAN move sequences and tags).
- **Show** (`show <ECO>`): opening details and recorded move sequence.
- **Favorites** (`favorite add/list/remove <ECO>`): save favorite lines to a
  local Markdown file (`chess_explorer/user_data/favorites.md`).
- **Quiz** (`quiz <ECO>`): interactive move-order drill. You type each ply in
  SAN; every guess is scored and appended to local JSON progress
  (`chess_explorer/user_data/progress.json`) with accuracy, streak, and grade.
- **Tests**: `tests/test_eco.py` (parsing/search) and `tests/test_scoring.py`
  (accuracy, streaks, grading, session aggregation).
- Packaging: `pyproject.toml` (console script `chess-openings`), MIT `LICENSE`,
  `README.md`, `.gitignore`.

No game assets, no accounts, no network access, no secrets or personal data.

## How to run

```bash
python3 -m chess_explorer --version
python3 -m chess_explorer search sicilian
python3 -m chess_explorer show C50
python3 -m chess_explorer favorite add C50
python3 -m chess_explorer favorite list
python3 -m chess_explorer quiz C50
python3 -m pytest tests
```

Requires Python 3.10+ only (standard library). Also installable via
`pip install .` for the `chess-openings` console script.

## Verification results

- `python3 -m pytest tests`: 24 passed.
- CLI smoke tests all succeeded: `--version`, `search`, `show` (known and
  unknown code), `quiz` with piped stdin (progress JSON written correctly),
  `favorite add/list/remove`.

## Known gaps

- ECO data is a curated fan-project sample, not a complete ECO enumeration;
  move sequences are short illustrative lines in SAN, not full theory.
- SAN comparison is string-based normalization (no full move-legality
  validation; no chess library dependency).
- Quiz advances to the next ply after an incorrect guess rather than making
  you retry.
- No `python` binary on this image; use `python3`.
