"""
Test suite for the formatters module.
"""

import pytest

from src.formatters import FixFormatter, NavAidFormatter, WaypointFormatter
from src.models import Coordinates, FixResult, NavAidEntry, WaypointResult


class TestWaypointFormatter:
    """Tests for WaypointFormatter class."""

    def test_format_small_distance_with_vor(self):
        """Test formatting waypoint with small distance and VOR identifier."""
        coords = Coordinates(latitude=37.621300000, longitude=-122.379000000)
        result = WaypointResult(
            coordinates=coords,
            radius_letter="D",
            airport_code="KSFO",
            operation_code="A",
            vor_identifier="SFO",
            magnetic_bearing=90.5,
            distance_nm=3.7,
        )

        formatted = WaypointFormatter.format(result)

        # Check coordinate precision
        assert "37.621300000" in formatted
        assert "-122.379000000" in formatted
        # Check radius designator format (D090D for bearing 90, radius D)
        assert "D090D" in formatted
        # Check airport code
        assert "KSFO" in formatted
        assert "KS" in formatted  # Airport region
        # Check operation code
        assert "A" in formatted
        # Check VOR identifier with bearing and distance (SFO090004)
        assert "SFO090004" in formatted  # Bearing 90, distance rounded to 4

    def test_format_small_distance_without_vor(self):
        """Test formatting waypoint with small distance and no VOR identifier."""
        coords = Coordinates(latitude=37.621300000, longitude=-122.379000000)
        result = WaypointResult(
            coordinates=coords,
            radius_letter="D",
            airport_code="KSFO",
            operation_code="A",
            vor_identifier="",
            magnetic_bearing=90.0,
            distance_nm=3.7,
        )

        formatted = WaypointFormatter.format(result)

        # Check basic components
        assert "37.621300000" in formatted
        assert "-122.379000000" in formatted
        assert "D090D" in formatted
        assert "KSFO" in formatted
        assert "KS" in formatted
        assert "A" in formatted
        # Should not have VOR bearing/distance suffix (e.g., SFO090004)
        # Note: Airport code KSFO will contain "SFO", so we check for the absence of the suffix pattern
        assert "090004" not in formatted  # No VOR-specific bearing/distance code

    def test_format_large_distance_with_vor(self):
        """Test formatting waypoint with large distance (>26.5 NM)."""
        coords = Coordinates(latitude=38.000000000, longitude=-122.000000000)
        result = WaypointResult(
            coordinates=coords,
            radius_letter="Z",  # Not used for large distances
            airport_code="KSFO",
            operation_code="D",
            vor_identifier="SFO",
            magnetic_bearing=45.7,
            distance_nm=30.2,
        )

        formatted = WaypointFormatter.format(result)

        # Check coordinates
        assert "38.000000000" in formatted
        assert "-122.000000000" in formatted
        # Check VOR+distance format (SFO30)
        assert "SFO30" in formatted
        # Check airport code
        assert "KSFO" in formatted
        assert "KS" in formatted
        # Check operation code
        assert "D" in formatted
        # Check VOR identifier with bearing and distance (SFO045030)
        assert "SFO045030" in formatted

    def test_format_large_distance_without_vor(self):
        """Test formatting waypoint with large distance and no VOR identifier."""
        coords = Coordinates(latitude=38.000000000, longitude=-122.000000000)
        result = WaypointResult(
            coordinates=coords,
            radius_letter="Z",
            airport_code="KSFO",
            operation_code="D",
            vor_identifier="",
            magnetic_bearing=45.0,
            distance_nm=30.0,
        )

        formatted = WaypointFormatter.format(result)

        # Check coordinates
        assert "38.000000000" in formatted
        assert "-122.000000000" in formatted
        # Check airport code
        assert "KSFO" in formatted
        assert "KS" in formatted
        # Check operation code
        assert "D" in formatted
        # Should not have VOR bearing/distance suffix
        # Note: Airport code KSFO will contain "SFO", so we check for the absence of the suffix pattern
        assert "045030" not in formatted  # No VOR-specific bearing/distance code

    def test_format_bearing_padding(self):
        """Test that bearing is zero-padded to 3 digits."""
        coords = Coordinates(latitude=37.621300000, longitude=-122.379000000)
        result = WaypointResult(
            coordinates=coords,
            radius_letter="B",
            airport_code="KSFO",
            operation_code="A",
            vor_identifier="SFO",
            magnetic_bearing=5.0,
            distance_nm=2.0,
        )

        formatted = WaypointFormatter.format(result)

        # Check that bearing is padded (005)
        assert "D005B" in formatted
        assert "SFO005002" in formatted

    def test_format_distance_rounding(self):
        """Test that distance is rounded for display."""
        coords = Coordinates(latitude=37.621300000, longitude=-122.379000000)
        result = WaypointResult(
            coordinates=coords,
            radius_letter="D",
            airport_code="KSFO",
            operation_code="A",
            vor_identifier="SFO",
            magnetic_bearing=90.0,
            distance_nm=3.4,  # Should round to 3
        )

        formatted = WaypointFormatter.format(result)
        assert "SFO090003" in formatted

        result2 = WaypointResult(
            coordinates=coords,
            radius_letter="D",
            airport_code="KSFO",
            operation_code="A",
            vor_identifier="SFO",
            magnetic_bearing=90.0,
            distance_nm=3.6,  # Should round to 4
        )

        formatted2 = WaypointFormatter.format(result2)
        assert "SFO090004" in formatted2


class TestFixFormatter:
    """Tests for FixFormatter class."""

    def test_format_basic_fix(self):
        """Test formatting basic fix result."""
        coords = Coordinates(latitude=37.621300000, longitude=-122.379000000)
        result = FixResult(
            coordinates=coords,
            fix_code="V",
            usage_code="F",
            runway_code="28",
            airport_code="KSFO",
            operation_code="A",
        )

        formatted = FixFormatter.format(result)

        # Check coordinates
        assert "37.621300000" in formatted
        assert "-122.379000000" in formatted
        # Check usage+fix+runway format (FV28)
        assert "FV28" in formatted
        # Check airport code
        assert "KSFO" in formatted
        assert "KS" in formatted  # Airport region
        # Check operation code
        assert "A" in formatted

    def test_format_runway_padding(self):
        """Test that runway code is zero-padded to 2 digits."""
        coords = Coordinates(latitude=37.621300000, longitude=-122.379000000)
        result = FixResult(
            coordinates=coords,
            fix_code="V",
            usage_code="F",
            runway_code="9",
            airport_code="KSFO",
            operation_code="A",
        )

        formatted = FixFormatter.format(result)

        # Check that runway is padded (09)
        assert "FV09" in formatted

    def test_format_different_fix_types(self):
        """Test formatting with different fix codes."""
        coords = Coordinates(latitude=37.621300000, longitude=-122.379000000)

        # VOR
        result_vor = FixResult(
            coordinates=coords,
            fix_code="V",
            usage_code="F",
            runway_code="28",
            airport_code="KSFO",
            operation_code="A",
        )
        assert "FV28" in FixFormatter.format(result_vor)

        # ILS
        result_ils = FixResult(
            coordinates=coords,
            fix_code="I",
            usage_code="F",
            runway_code="28",
            airport_code="KSFO",
            operation_code="A",
        )
        assert "FI28" in FixFormatter.format(result_ils)

        # NDB
        result_ndb = FixResult(
            coordinates=coords,
            fix_code="N",
            usage_code="I",
            runway_code="28",
            airport_code="KSFO",
            operation_code="A",
        )
        assert "IN28" in FixFormatter.format(result_ndb)

    def test_format_different_usage_codes(self):
        """Test formatting with different usage codes."""
        coords = Coordinates(latitude=37.621300000, longitude=-122.379000000)

        # Final approach
        result_final = FixResult(
            coordinates=coords,
            fix_code="V",
            usage_code="F",
            runway_code="28",
            airport_code="KSFO",
            operation_code="A",
        )
        assert "FV28" in FixFormatter.format(result_final)

        # Initial approach
        result_initial = FixResult(
            coordinates=coords,
            fix_code="V",
            usage_code="A",
            runway_code="28",
            airport_code="KSFO",
            operation_code="A",
        )
        assert "AV28" in FixFormatter.format(result_initial)

        # Intermediate approach
        result_intermediate = FixResult(
            coordinates=coords,
            fix_code="V",
            usage_code="I",
            runway_code="28",
            airport_code="KSFO",
            operation_code="A",
        )
        assert "IV28" in FixFormatter.format(result_intermediate)


class TestNavAidFormatter:
    """Tests for NavAidFormatter class."""

    def test_format_navaid_with_name(self):
        """Test formatting navigation aid entry with name."""
        entry = NavAidEntry(
            type_code="3",  # VOR
            latitude=37.6213,
            longitude=-122.3790,
            identifier="SFO",
            name="San Francisco",
        )

        formatted = NavAidFormatter.format_for_display(entry)

        # Check type label
        assert "VOR" in formatted
        # Check identifier
        assert "SFO" in formatted
        # Check name
        assert "San Francisco" in formatted
        # Check format
        assert formatted == "VOR - SFO - San Francisco"

    def test_format_navaid_without_name(self):
        """Test formatting navigation aid entry without name."""
        entry = NavAidEntry(
            type_code="3",  # VOR
            latitude=37.6213,
            longitude=-122.3790,
            identifier="SFO",
            name=None,
        )

        formatted = NavAidFormatter.format_for_display(entry)

        # Check type label
        assert "VOR" in formatted
        # Check identifier
        assert "SFO" in formatted
        # Check placeholder for missing name
        assert "[No name]" in formatted

    def test_format_different_navaid_types(self):
        """Test formatting different navigation aid types."""
        # VOR
        entry_vor = NavAidEntry(
            type_code="3", latitude=37.6213, longitude=-122.3790, identifier="SFO", name="Test"
        )
        formatted_vor = NavAidFormatter.format_for_display(entry_vor)
        assert "VOR" in formatted_vor

        # DME (VOR)
        entry_dme = NavAidEntry(
            type_code="12", latitude=37.6213, longitude=-122.3790, identifier="SFO", name="Test"
        )
        formatted_dme = NavAidFormatter.format_for_display(entry_dme)
        assert "DME (VOR)" in formatted_dme

        # NDB
        entry_ndb = NavAidEntry(
            type_code="2", latitude=37.6213, longitude=-122.3790, identifier="SFO", name="Test"
        )
        formatted_ndb = NavAidFormatter.format_for_display(entry_ndb)
        assert "NDB" in formatted_ndb

        # DME
        entry_dme_standalone = NavAidEntry(
            type_code="13", latitude=37.6213, longitude=-122.3790, identifier="SFO", name="Test"
        )
        formatted_dme_standalone = NavAidFormatter.format_for_display(entry_dme_standalone)
        assert "DME" in formatted_dme_standalone

    def test_format_unknown_navaid_type(self):
        """Test formatting navigation aid with unknown type code."""
        entry = NavAidEntry(
            type_code="99",  # Unknown type
            latitude=37.6213,
            longitude=-122.3790,
            identifier="SFO",
            name="Test",
        )

        formatted = NavAidFormatter.format_for_display(entry)

        # Should show "Unknown" for unrecognized type
        assert "Unknown" in formatted
        assert "SFO" in formatted
