"""
VOR-FIX Coordinate Calculator Package

A Python package for calculating aviation navigation waypoints and approach fixes
using geodesic calculations based on VOR/DME/NDB data.
"""

__version__ = "1.0.0"
__author__ = "Justin"
__email__ = "epa6643@gmail.com"
__license__ = "MIT"

from src.models import Coordinates, FixInput, FixResult, NavAidEntry, WaypointInput, WaypointResult

__all__ = [
    "Coordinates",
    "WaypointInput",
    "WaypointResult",
    "FixInput",
    "FixResult",
    "NavAidEntry",
]
