# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**soccerdata** is a Python library of web scrapers for soccer data from sites like FBref, ESPN, Sofascore, WhoScored, Understat, ClubElo, SoFIFA, and Football-Data.co.uk. It returns pandas DataFrames with standardized column names and league/team identifiers across data sources. Downloaded data is cached locally.

## Development Commands

Uses **uv** as package manager and **hatch** as build backend.

```bash
# Setup
uv venv && uv sync

# Run all tests (requires DVC test data, see below)
SOCCERDATA_DIR=tests/appdata pytest --cov=soccerdata

# Run a single test file or test
SOCCERDATA_DIR=tests/appdata pytest tests/test_FBref.py
SOCCERDATA_DIR=tests/appdata pytest tests/test_FBref.py -k "test_name"

# Lint and format
ruff check --config pyproject.toml soccerdata
ruff format --config pyproject.toml soccerdata

# Type checking
mypy --install-types --non-interactive --config-file pyproject.toml soccerdata tests

# Pre-commit hooks (ruff, pyupgrade, prettier, uv lock/export)
pre-commit run --all-files

# Build package
uv build
```

The `SOCCERDATA_DIR` env var is **required** for tests — it points test fixtures at `tests/appdata` instead of the default `~/soccerdata`. Test data is managed with DVC (stored in a GCS remote), so `dvc pull` is needed to get cached HTML fixtures before running tests.

## Architecture

### Class Hierarchy (`soccerdata/_common.py`)

```
BaseReader (ABC)
├── BaseRequestsReader    — HTTP via tls_requests (most scrapers)
├── BaseScrapingBeeReader — ScrapingBee API proxy
└── BaseSeleniumReader    — browser automation via SeleniumBase
```

Each scraper inherits from one of these:

| Scraper | Base Class | Source |
|---------|-----------|--------|
| `ClubElo` | `BaseRequestsReader` | clubelo.com |
| `ESPN` | `BaseRequestsReader` | espn.com |
| `FBref` | `BaseRequestsReader` | fbref.com |
| `MatchHistory` | `BaseRequestsReader` | football-data.co.uk |
| `Sofascore` | `BaseRequestsReader` | sofascore.com |
| `SoFIFA` | `BaseRequestsReader` | sofifa.com |
| `Understat` | `BaseRequestsReader` | understat.com |
| `WhoScored` | `BaseSeleniumReader` | whoscored.com |

### Key Concepts

- **`LEAGUE_DICT`** (`_config.py`): Central registry mapping canonical league IDs (e.g., `"ENG-Premier League"`) to source-specific IDs for each scraper. Users can extend this via `config/league_dict.json`.
- **`SeasonCode`** (`_common.py`): Handles season format normalization — some leagues use single-year (`"2021"`) and others use multi-year (`"2122"`) formats.
- **Caching**: `BaseReader.get()` handles download-and-cache logic. Files are stored under `DATA_DIR/<ScraperName>/`. Cache age controlled via `MAXAGE` config or `max_age` parameter.
- **Team name standardization**: `TEAMNAME_REPLACEMENTS` dict unifies team names across sources. Users can customize via `config/teamname_replacements.json`.

### Configuration (`soccerdata/_config.py`)

All config is driven by environment variables:
- `SOCCERDATA_DIR` — base directory (default: `~/soccerdata`)
- `SOCCERDATA_NOCACHE` / `SOCCERDATA_NOSTORE` — disable caching
- `SOCCERDATA_MAXAGE` — max cache age in seconds
- `SOCCERDATA_LOGLEVEL` — log level

### Code Style

- **Ruff** for linting and formatting, line length 99, target Python 3.9
- **numpy-style** docstrings
- Type annotations required on all function definitions (enforced by mypy with `disallow_untyped_defs`)
- Tests follow pattern `tests/test_<ScraperName>.py` with fixtures in `tests/conftest.py`
