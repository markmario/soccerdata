"""Configurations."""

import json
import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Dict

from rich.logging import RichHandler

# Configuration
NOCACHE = os.environ.get("SOCCERDATA_NOCACHE", "False").lower() in ("true", "1", "t")
NOSTORE = os.environ.get("SOCCERDATA_NOSTORE", "False").lower() in ("true", "1", "t")
MAXAGE = None
if os.environ.get("SOCCERDATA_MAXAGE") is not None:
    MAXAGE = int(os.environ.get("SOCCERDATA_MAXAGE", 0))
LOGLEVEL = os.environ.get("SOCCERDATA_LOGLEVEL", "INFO").upper()

# Directories
BASE_DIR = Path(os.environ.get("SOCCERDATA_DIR", Path.home() / "soccerdata"))
LOGS_DIR = Path(BASE_DIR, "logs")
DATA_DIR = Path(BASE_DIR, "data")
CONFIG_DIR = Path(BASE_DIR, "config")

# Create dirs
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Logger
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"  # noqa: E501
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "info", "error"],
            "level": LOGLEVEL,
            "propagate": True,
        },
    },
}
logging.config.dictConfig(logging_config)
logging.captureWarnings(True)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)

# Team name replacements
TEAMNAME_REPLACEMENTS: Dict[str, str] = {}
_f_custom_teamnname_replacements = CONFIG_DIR / "teamname_replacements.json"
if _f_custom_teamnname_replacements.is_file():
    with _f_custom_teamnname_replacements.open(encoding="utf8") as json_file:
        for team, to_replace_list in json.load(json_file).items():
            for to_replace in to_replace_list:
                TEAMNAME_REPLACEMENTS[to_replace] = team
    logger.info(
        "Custom team name replacements loaded from %s.",
        _f_custom_teamnname_replacements,
    )
else:
    logger.info(
        "No custom team name replacements found. You can configure these in %s.",
        _f_custom_teamnname_replacements,
    )


# League dict
LEAGUE_DICT = {
    "ENG-Premier League": {
        "ClubElo": "ENG_1",
        "MatchHistory": "E0",
        "FiveThirtyEight": "premier-league",
        "FBref": "Premier League",
        "ESPN": "eng.1",
        "Sofascore": "Premier League",
        "SoFIFA": "[England] Premier League",
        "Understat": "EPL",
        "WhoScored": "England - Premier League",
        "WhoScoredScrapingBee": "England - Premier League",
        "season_start": "Aug",
        "season_end": "May",
    },
    "ESP-La Liga": {
        "ClubElo": "ESP_1",
        "MatchHistory": "SP1",
        "FiveThirtyEight": "la-liga",
        "FBref": "La Liga",
        "ESPN": "esp.1",
        "Sofascore": "LaLiga",
        "SoFIFA": "[Spain] La Liga",
        "Understat": "La liga",
        "WhoScored": "Spain - LaLiga",
        "WhoScoredScrapingBee": "Spain - LaLiga",
        "season_start": "Aug",
        "season_end": "May",
    },
    "ITA-Serie A": {
        "ClubElo": "ITA_1",
        "MatchHistory": "I1",
        "FiveThirtyEight": "serie-a",
        "FBref": "Serie A",
        "ESPN": "ita.1",
        "Sofascore": "Serie A",
        "SoFIFA": "[Italy] Serie A",
        "Understat": "Serie A",
        "WhoScored": "Italy - Serie A",
        "WhoScoredScrapingBee": "Italy - Serie A",
        "season_start": "Aug",
        "season_end": "May",
    },
    "GER-Bundesliga": {
        "ClubElo": "GER_1",
        "MatchHistory": "D1",
        "FiveThirtyEight": "bundesliga",
        "FBref": "Fußball-Bundesliga",
        "ESPN": "ger.1",
        "Sofascore": "Bundesliga",
        "SoFIFA": "[Germany] Bundesliga",
        "Understat": "Bundesliga",
        "WhoScored": "Germany - Bundesliga",
        "WhoScoredScrapingBee": "Germany - Bundesliga",
        "season_start": "Aug",
        "season_end": "May",
    },
    "FRA-Ligue 1": {
        "ClubElo": "FRA_1",
        "MatchHistory": "F1",
        "FiveThirtyEight": "ligue-1",
        "FBref": "Ligue 1",
        "ESPN": "fra.1",
        "Sofascore": "Ligue 1",
        "SoFIFA": "[France] Ligue 1",
        "Understat": "Ligue 1",
        "WhoScored": "France - Ligue 1",
        "WhoScoredScrapingBee": "France - Ligue 1",
        "season_start": "Aug",
        "season_end": "May",
    },
    "INT-World Cup": {
        "FBref": "FIFA World Cup",
        "WhoScored": "International - FIFA World Cup",
        "WhoScoredScrapingBee": "International - FIFA World Cup",
        "season_code": "single-year",
    },
    "INT-European Championship": {
        "FBref": "UEFA European Football Championship",
        "Sofascore": "EURO",
        "WhoScored": "International - European Championship",
        "WhoScoredScrapingBee": "International - European Championship",
        "season_start": "Jun",
        "season_end": "Jul",
        "season_code": "single-year",
    },
    "INT-Women's World Cup": {
        "FBref": "FIFA Women's World Cup",
        "WhoScored": "International - FIFA Women's World Cup",
        "WhoScoredScrapingBee": "International - FIFA Women's World Cup",
        "season_code": "single-year",
    },
    "INT-Africa Cup of Nations U20": {
        "WhoScored": "International - Africa Cup of Nations U20",
        "WhoScoredScrapingBee": "International - Africa Cup of Nations U20",
    },
    "INT-EURO U-17": {
        "WhoScored": "International - EURO U-17",
        "WhoScoredScrapingBee": "International - EURO U-17",
    },
    "INT-Friendly U-21": {
        "WhoScored": "International - Friendly U-21",
        "WhoScoredScrapingBee": "International - Friendly U-21",
    },
    "INT-World Championship U-17": {
        "WhoScored": "International - World Championship U-17",
        "WhoScoredScrapingBee": "International - World Championship U-17",
    },
    "INT-Confederations Cup": {
        "WhoScored": "International - Confederations Cup",
        "WhoScoredScrapingBee": "International - Confederations Cup",
    },
    "INT-Club Friendlies": {
        "WhoScored": "International - Club Friendlies",
        "WhoScoredScrapingBee": "International - Club Friendlies",
    },
    "INT-EURO U-19": {
        "WhoScored": "International - EURO U-19",
        "WhoScoredScrapingBee": "International - EURO U-19",
    },
    "INT-Int. Friendly": {
        "WhoScored": "International - Int. Friendly",
        "WhoScoredScrapingBee": "International - Int. Friendly",
    },
    "INT-Summer Olympics": {
        "WhoScored": "International - Summer Olympics",
        "WhoScoredScrapingBee": "International - Summer Olympics",
    },
    "INT-Toulon Tournament": {
        "WhoScored": "International - Toulon Tournament",
        "WhoScoredScrapingBee": "International - Toulon Tournament",
    },
    "INT-World Championship U-20": {
        "WhoScored": "International - World Championship U-20",
        "WhoScoredScrapingBee": "International - World Championship U-20",
    },
    "INT-FIFA Club World Cup": {
        "WhoScored": "International - FIFA Club World Cup",
        "WhoScoredScrapingBee": "International - FIFA Club World Cup",
    },
    "INT-Asian Cup": {
        "WhoScored": "International - Asian Cup",
        "WhoScoredScrapingBee": "International - Asian Cup",
    },
    "INT-EURO U-21": {
        "WhoScored": "International - EURO U-21",
        "WhoScoredScrapingBee": "International - EURO U-21",
    },
    "INT-World Cup Qualification AFC": {
        "WhoScored": "International - World Cup Qualification AFC",
        "WhoScoredScrapingBee": "International - World Cup Qualification AFC",
    },
    "INT-World Cup Qualification CONCACAF": {
        "WhoScored": "International - World Cup Qualification CONCACAF",
        "WhoScoredScrapingBee": "International - World Cup Qualification CONCACAF",
    },
    "INT-World Cup Qualification CAF": {
        "WhoScored": "International - World Cup Qualification CAF",
        "WhoScoredScrapingBee": "International - World Cup Qualification CAF",
    },
    "INT-World Cup Qualification CONMEBOL": {
        "WhoScored": "International - World Cup Qualification CONMEBOL",
        "WhoScoredScrapingBee": "International - World Cup Qualification CONMEBOL",
    },
    "INT-World Cup Qualification UEFA": {
        "WhoScored": "International - World Cup Qualification UEFA",
        "WhoScoredScrapingBee": "International - World Cup Qualification UEFA",
    },
    "INT-Africa Cup of Nations": {
        "WhoScored": "International - Africa Cup of Nations",
        "WhoScoredScrapingBee": "International - Africa Cup of Nations",
    },
    "INT-Copa America": {
        "WhoScored": "International - Copa America",
        "WhoScoredScrapingBee": "International - Copa America",
    },
    "INT-EURO U21 Qualification": {
        "WhoScored": "International - EURO U21 Qualification",
        "WhoScoredScrapingBee": "International - EURO U21 Qualification",
    },
    "INT-OFC U19 Championship": {
        "WhoScored": "International - OFC U19 Championship",
        "WhoScoredScrapingBee": "International - OFC U19 Championship",
    },
    "INT-African Nations Championship": {
        "WhoScored": "International - African Nations Championship",
        "WhoScoredScrapingBee": "International - African Nations Championship",
    },
    "INT-CONCACAF Nations League": {
        "WhoScored": "International - CONCACAF Nations League",
        "WhoScoredScrapingBee": "International - CONCACAF Nations League",
    },
    "INT-UEFA Nations League B Qualification": {
        "WhoScored": "International - UEFA Nations League B Qualification",
        "WhoScoredScrapingBee": "International - UEFA Nations League B Qualification",
    },
    "INT-UEFA Nations League A Qualification": {
        "WhoScored": "International - UEFA Nations League A Qualification",
        "WhoScoredScrapingBee": "International - UEFA Nations League A Qualification",
    },
    "INT-UEFA Nations League D": {
        "WhoScored": "International - UEFA Nations League D",
        "WhoScoredScrapingBee": "International - UEFA Nations League D",
    },
    "INT-UEFA Nations League C": {
        "WhoScored": "International - UEFA Nations League C",
        "WhoScoredScrapingBee": "International - UEFA Nations League C",
    },
    "INT-UEFA Nations League B": {
        "WhoScored": "International - UEFA Nations League B",
        "WhoScoredScrapingBee": "International - UEFA Nations League B",
    },
    "INT-UEFA Nations League A": {
        "WhoScored": "International - UEFA Nations League A",
        "WhoScoredScrapingBee": "International - UEFA Nations League A",
    },
    "INT-UEFA Women's EURO": {
        "WhoScored": "International - UEFA Women's EURO",
        "WhoScoredScrapingBee": "International - UEFA Women's EURO",
    },
}
_f_custom_league_dict = CONFIG_DIR / "league_dict.json"
if _f_custom_league_dict.is_file():
    with _f_custom_league_dict.open(encoding="utf8") as json_file:
        LEAGUE_DICT = {**LEAGUE_DICT, **json.load(json_file)}
    logger.info("Custom league dict loaded from %s.", _f_custom_league_dict)
else:
    logger.info(
        "No custom league dict found. You can configure additional leagues in %s.",
        _f_custom_league_dict,
    )
