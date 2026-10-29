# Chess Opening Explorer CLI

A friendly, local-first Python CLI for exploring chess openings. Search ECO
codes, save your favorite lines as local Markdown, and quiz yourself on move
order — with progress saved to a local JSON file. No accounts, no network,
no game assets, no secrets.

A fan project by **Asdale Dynamics, LLC** — beginner-friendly AI education,
books and guides, and practical tools the LLC can publish or sell.
Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC (Indiana, formed Oct 2026). His book *The Massive AI Manual*
and hub site dylanasdale.github.io explain AI "like a friend would": plain
English, step by step, never condescending.

## What it does

| Command | What it does |
|---------|--------------|
| `search <text>` | Find openings by ECO code or opening name |
| `show <ECO>` | Show an opening's name, tags, and move sequence |
| `favorite add <ECO>` | Save an opening to your local Markdown favorites |
| `favorite list` | List your saved favorite openings |
| `favorite remove <ECO>` | Remove an opening from your favorites |
| `quiz <ECO>` | Practice move order; each guess is scored and saved locally |

Everything runs on your machine. Your favorites live in
`chess_explorer/user_data/favorites.md` and your quiz progress in
`chess_explorer/user_data/progress.json`.

## Requirements

- Python 3.10 or newer (standard library only — nothing to install)

## Run it step by step

From the project folder:

```bash
# See the version
python3 -m chess_explorer --version

# Search for openings by name or ECO code
python3 -m chess_explorer search sicilian
python3 -m chess_explorer search C50

# Look at one opening in detail
python3 -m chess_explorer show C50
python3 -m chess_explorer show C89

# Save a favorite line
python3 -m chess_explorer favorite add C50
python3 -m chess_explorer favorite list
python3 -m chess_explorer favorite remove C50

# Quiz yourself on move order
python3 -m chess_explorer quiz C50
```

During a quiz you're shown the moves played so far and type the next move
in SAN (for example `e4`, `Nf3`, `O-O`). Each guess is scored right away,
and when you finish your accuracy, streak, and grade are saved to
`progress.json` so you can watch yourself improve over time.

## Run the tests

```bash
python3 -m pytest tests
```

Tests cover ECO parsing/search and quiz scoring. There are no network calls
and no external packages required.

## Files

- `chess_explorer/data/eco_openings.json` — curated sample ECO data (codes,
  names, moves in SAN, tags). A fan-project sample, not a complete ECO
  enumeration.
- `chess_explorer/user_data/favorites.md` — your saved favorite lines
- `chess_explorer/user_data/progress.json` — your quiz progress history
- `tests/test_eco.py`, `tests/test_scoring.py`, `tests/test_quiz.py` — tests
- `pyproject.toml` — packaging (defines the `chess-openings` console script)
- `LICENSE` — MIT License

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
