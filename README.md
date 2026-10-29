# Chess Opening Explorer CLI

A local-first, dependency-free Python CLI for exploring chess openings:
search ECO codes, save favorite lines as local Markdown, and quiz move
order with local JSON progress tracking. Includes tests for parsing and
scoring. No game assets, no accounts, no network access, no secrets.

A fan project by **Asdale Dynamics, LLC** — beginner-friendly AI education,
books and guides, and practical tools the LLC can publish or sell.
Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC (Indiana, formed Oct 2026). His book *The Massive AI Manual*
and hub site dylanasdale.github.io explain AI "like a friend would": plain
English, step by step, never condescending.

## What it does

- **Search** ECO codes by code or opening name (`search`)
- **Show** an opening's recorded move sequence (`show`)
- **Save** favorite lines to a local Markdown file (`favorite add/list/remove`)
- **Quiz** move order interactively, with correctness scored per move and
  progress persisted to local JSON (`quiz`)
- **Tested**: unit tests cover ECO parsing/search and scoring logic

## Requirements

- Python 3.10+ (standard library only — nothing to install)

## Run it

```bash
# From the project folder
python -m chess_explorer --version
python -m chess_explorer search sicilian
python -m chess_explorer show C50
python -m chess_explorer show C89
python -m chess_explorer favorite add C50
python -m chess_explorer favorite list
python -m chess_explorer quiz C50
```

Quiz flow: you are shown the moves played so far and type the next move in
SAN (e.g. `e4`, `Nf3`, `O-O`). Each guess is scored, and results append to
`chess_explorer/user_data/progress.json`. Favorites live in
`chess_explorer/user_data/favorites.md`.

## Tests

```bash
python -m pytest tests
```

## Files

- `chess_explorer/data/eco_openings.json` — curated sample ECO data
  (codes, names, moves in SAN, tags). Not a complete ECO enumeration.
- `chess_explorer/user_data/favorites.md` — your saved favorite lines
- `chess_explorer/user_data/progress.json` — quiz progress history
- `tests/test_eco.py`, `tests/test_scoring.py` — parsing and scoring tests

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
