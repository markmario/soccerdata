"""Unittests for class soccerdata.WhoScored."""

import pandas as pd
import pytest

import soccerdata as sd

# Unittests -------------------------------------------------------------------


def test_whoscored_missing_players(whoscored):
    assert isinstance(whoscored.read_missing_players(1485184), pd.DataFrame)


def test_whoscored_events(whoscored):
    assert isinstance(whoscored.read_events(1485184), pd.DataFrame)


def test_whoscored_scrapingbee_structure():
    """Test that WhoScoredScrapingBee has the correct structure."""
    # Verify class exists
    assert hasattr(sd, "WhoScoredScrapingBee")

    # Verify inheritance
    assert issubclass(sd.WhoScoredScrapingBee, sd.whoscored.WhoScoredMixin)
    assert issubclass(sd.WhoScoredScrapingBee, sd._common.BaseScrapingBeeReader)

    # Verify shared methods are present
    assert hasattr(sd.WhoScoredScrapingBee, "read_leagues")
    assert hasattr(sd.WhoScoredScrapingBee, "read_seasons")
    assert hasattr(sd.WhoScoredScrapingBee, "read_schedule")
    assert hasattr(sd.WhoScoredScrapingBee, "read_missing_players")
    assert hasattr(sd.WhoScoredScrapingBee, "read_events")

    # Verify Selenium-specific methods are NOT present
    assert not hasattr(sd.WhoScoredScrapingBee, "_read_game_info")
    assert not hasattr(sd.WhoScoredScrapingBee, "_handle_banner")


def test_whoscored_backward_compatibility():
    """Test that WhoScored class retains all original methods."""
    # Verify class structure hasn't changed
    assert hasattr(sd, "WhoScored")

    # Verify shared methods are present
    assert hasattr(sd.WhoScored, "read_leagues")
    assert hasattr(sd.WhoScored, "read_seasons")
    assert hasattr(sd.WhoScored, "read_schedule")
    assert hasattr(sd.WhoScored, "read_missing_players")
    assert hasattr(sd.WhoScored, "read_events")

    # Verify Selenium-specific methods are present
    assert hasattr(sd.WhoScored, "_read_game_info")
    assert hasattr(sd.WhoScored, "_handle_banner")
