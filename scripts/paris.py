"""Date du jour à Paris : une seule fonction pour tous les scripts (le cloud tourne en UTC, le Mac à Paris).

Information et apprentissage, pas un conseil en investissement.
"""
from datetime import date, datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")


def aujourdhui() -> date:
    """Le jour actuel à Paris (jamais `date.today()`, qui dépend du fuseau de la machine)."""
    return datetime.now(PARIS).date()
