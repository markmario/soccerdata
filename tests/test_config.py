"""Unittests for soccerdata._config."""

import json
import logging
from importlib import reload

from soccerdata import _config as conf


def test_env_soccerdata_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("SOCCERDATA_DIR", str(tmp_path))
    reload(conf)
    assert tmp_path == conf.BASE_DIR


def test_env_nocache(monkeypatch):
    monkeypatch.setenv("SOCCERDATA_NOCACHE", "t")
    reload(conf)
    assert conf.NOCACHE is True

    monkeypatch.setenv("SOCCERDATA_NOCACHE", "true")
    reload(conf)
    assert conf.NOCACHE is True

    monkeypatch.setenv("SOCCERDATA_NOCACHE", "f")
    reload(conf)
    assert conf.NOCACHE is False


def test_env_nostore(monkeypatch):
    monkeypatch.setenv("SOCCERDATA_NOSTORE", "t")
    reload(conf)
    assert conf.NOSTORE is True

    monkeypatch.setenv("SOCCERDATA_NOSTORE", "true")
    reload(conf)
    assert conf.NOSTORE is True

    monkeypatch.setenv("SOCCERDATA_NOSTORE", "f")
    reload(conf)
    assert conf.NOSTORE is False


def test_env_loglevel(monkeypatch):
    monkeypatch.setenv("SOCCERDATA_LOGLEVEL", "DEBUG")
    reload(conf)
    assert conf.logger.level == logging.DEBUG


def test_read_teamnname_replacements(monkeypatch, tmp_path):
    monkeypatch.setenv("SOCCERDATA_DIR", str(tmp_path))
    # no teamname_replacements.json
    reload(conf)
    assert conf.TEAMNAME_REPLACEMENTS == {}
    fp = tmp_path / "config" / "teamname_replacements.json"
    with fp.open("w", encoding="utf8") as outfile:
        json.dump({"Celta de Vigo": ["Celta Vigo", "Celta"]}, outfile)
    # correctly parse teamname_replacements.json
    reload(conf)
    assert conf.TEAMNAME_REPLACEMENTS == {
        "Celta Vigo": "Celta de Vigo",
        "Celta": "Celta de Vigo",
    }


def test_read_league_dict(monkeypatch, tmp_path):
    monkeypatch.setenv("SOCCERDATA_DIR", str(tmp_path))
    # no league_dict.json
    reload(conf)
    nb_default = len(conf.LEAGUE_DICT)
    fp = tmp_path / "config" / "league_dict.json"
    with fp.open("w", encoding="utf8") as outfile:
        json.dump({"ABC-Fake": {"WhoScored": "Fake"}}, outfile)
    # correctly parse league_dict.json
    reload(conf)
    assert len(conf.LEAGUE_DICT) == nb_default + 1
    assert conf.LEAGUE_DICT["ABC-Fake"] == {"WhoScored": "Fake"}


def test_whoscored_scrapingbee_consistency():
    """Test that leagues with WhoScored also have WhoScoredScrapingBee with matching values."""
    reload(conf)

    # Leagues that should have both WhoScored and WhoScoredScrapingBee with same values
    expected_leagues = [
        "ENG-Premier League",
        "ESP-La Liga",
        "ITA-Serie A",
        "GER-Bundesliga",
        "FRA-Ligue 1",
        "INT-World Cup",
        "INT-European Championship",
        "INT-Women's World Cup",
    ]

    for league in expected_leagues:
        assert league in conf.LEAGUE_DICT, f"{league} not found in LEAGUE_DICT"
        league_config = conf.LEAGUE_DICT[league]

        if "WhoScored" in league_config:
            assert "WhoScoredScrapingBee" in league_config, (
                f"{league} has WhoScored but missing WhoScoredScrapingBee"
            )
            assert league_config["WhoScored"] == league_config["WhoScoredScrapingBee"], (
                f"{league} WhoScored and WhoScoredScrapingBee values don't match"
            )


def test_international_tournaments_present():
    """Test that all required international tournament entries are present."""
    reload(conf)

    # New international tournaments that should be present
    expected_tournaments = [
        "INT-Africa Cup of Nations U20",
        "INT-EURO U-17",
        "INT-Friendly U-21",
        "INT-World Championship U-17",
        "INT-Confederations Cup",
        "INT-Club Friendlies",
        "INT-EURO U-19",
        "INT-Int. Friendly",
        "INT-Summer Olympics",
        "INT-Toulon Tournament",
        "INT-World Championship U-20",
        "INT-FIFA Club World Cup",
        "INT-Asian Cup",
        "INT-EURO U-21",
        "INT-World Cup Qualification AFC",
        "INT-World Cup Qualification CONCACAF",
        "INT-World Cup Qualification CAF",
        "INT-World Cup Qualification CONMEBOL",
        "INT-World Cup Qualification UEFA",
        "INT-Africa Cup of Nations",
        "INT-Copa America",
        "INT-EURO U21 Qualification",
        "INT-OFC U19 Championship",
        "INT-African Nations Championship",
        "INT-CONCACAF Nations League",
        "INT-UEFA Nations League B Qualification",
        "INT-UEFA Nations League A Qualification",
        "INT-UEFA Nations League D",
        "INT-UEFA Nations League C",
        "INT-UEFA Nations League B",
        "INT-UEFA Nations League A",
        "INT-UEFA Women's EURO",
    ]

    for tournament in expected_tournaments:
        assert tournament in conf.LEAGUE_DICT, f"{tournament} not found in LEAGUE_DICT"
        tournament_config = conf.LEAGUE_DICT[tournament]

        # Check that both WhoScored and WhoScoredScrapingBee are present
        assert "WhoScored" in tournament_config, f"{tournament} missing WhoScored"
        assert "WhoScoredScrapingBee" in tournament_config, (
            f"{tournament} missing WhoScoredScrapingBee"
        )

        # Check that values match
        assert tournament_config["WhoScored"] == tournament_config["WhoScoredScrapingBee"], (
            f"{tournament} WhoScored and WhoScoredScrapingBee values don't match"
        )

        # Verify value format (should start with "International - ")
        expected_value = f"International - {tournament.replace('INT-', '')}"
        assert tournament_config["WhoScored"] == expected_value, (
            f"{tournament} has incorrect WhoScored value. Expected: {expected_value}, "
            f"Got: {tournament_config['WhoScored']}"
        )
