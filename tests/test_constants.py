"""
Test suite for the constants module.
"""

import pytest

from src.constants import (
    AIRPORT_CODE_LENGTH,
    BEARING_MAX,
    BEARING_MIN,
    DECLINATION_MAX,
    DECLINATION_MIN,
    DISTANCE_MIN,
    FIX_FILE_IDENTIFIER_INDEX,
    FIX_FILE_LAT_INDEX,
    FIX_FILE_LON_INDEX,
    LARGE_DISTANCE_THRESHOLD_NM,
    LAT_MAX,
    LAT_MIN,
    LON_MAX,
    LON_MIN,
    METERS_PER_NAUTICAL_MILE,
    NAV_FILE_IDENTIFIER_INDEX,
    NAV_FILE_LAT_INDEX,
    NAV_FILE_LON_INDEX,
    NAV_FILE_TENTH_PART_INDEX,
    RADIUS_RANGES,
    RUNWAY_MAX,
    RUNWAY_MIN,
    VOR_IDENTIFIER_MAX_LENGTH,
    VOR_IDENTIFIER_MIN_LENGTH,
    FileType,
    FixType,
    FixUsage,
    NavAidType,
    OperationType,
)


class TestNumericConstants:
    """Tests for numeric constants."""

    def test_meters_per_nautical_mile(self):
        """Test meters per nautical mile constant."""
        assert METERS_PER_NAUTICAL_MILE == 1852.0

    def test_large_distance_threshold(self):
        """Test large distance threshold."""
        assert LARGE_DISTANCE_THRESHOLD_NM == 26.5

    def test_coordinate_ranges(self):
        """Test coordinate validation ranges."""
        assert LAT_MIN == -90.0
        assert LAT_MAX == 90.0
        assert LON_MIN == -180.0
        assert LON_MAX == 180.0

    def test_bearing_ranges(self):
        """Test bearing validation ranges."""
        assert BEARING_MIN == 0.0
        assert BEARING_MAX == 360.0

    def test_distance_ranges(self):
        """Test distance validation ranges."""
        assert DISTANCE_MIN == 0.0

    def test_declination_ranges(self):
        """Test declination validation ranges."""
        assert DECLINATION_MIN == -180.0
        assert DECLINATION_MAX == 180.0

    def test_runway_ranges(self):
        """Test runway code ranges."""
        assert RUNWAY_MIN == 0
        assert RUNWAY_MAX == 99

    def test_identifier_lengths(self):
        """Test identifier length constants."""
        assert AIRPORT_CODE_LENGTH == 4
        assert VOR_IDENTIFIER_MIN_LENGTH == 3
        assert VOR_IDENTIFIER_MAX_LENGTH == 4


class TestRadiusRanges:
    """Tests for radius ranges constant."""

    def test_radius_ranges_structure(self):
        """Test that radius ranges are properly structured."""
        assert isinstance(RADIUS_RANGES, list)
        assert len(RADIUS_RANGES) == 26  # A-Z

    def test_radius_ranges_letters(self):
        """Test that radius ranges contain all letters A-Z."""
        letters = [item[2] for item in RADIUS_RANGES]
        expected_letters = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        assert letters == expected_letters

    def test_radius_ranges_continuity(self):
        """Test that radius ranges are continuous."""
        for i in range(len(RADIUS_RANGES) - 1):
            current_high = RADIUS_RANGES[i][1]
            next_low = RADIUS_RANGES[i + 1][0]
            # Each range should be adjacent (high + 0.1 = next low)
            assert abs((current_high + 0.1) - next_low) < 0.01

    def test_radius_ranges_values(self):
        """Test specific radius range values."""
        # Check first range (A)
        assert RADIUS_RANGES[0] == (0.1, 1.4, "A")
        # Check last range (Z)
        assert RADIUS_RANGES[25] == (25.5, 26.4, "Z")


class TestFileFormatIndices:
    """Tests for file format index constants."""

    def test_nav_file_indices(self):
        """Test NAV file format indices."""
        assert NAV_FILE_LAT_INDEX == 1
        assert NAV_FILE_LON_INDEX == 2
        assert NAV_FILE_IDENTIFIER_INDEX == 7
        assert NAV_FILE_TENTH_PART_INDEX == 9

    def test_fix_file_indices(self):
        """Test FIX file format indices."""
        assert FIX_FILE_LAT_INDEX == 0
        assert FIX_FILE_LON_INDEX == 1
        assert FIX_FILE_IDENTIFIER_INDEX == 2


class TestOperationType:
    """Tests for OperationType enum."""

    def test_operation_type_values(self):
        """Test that all operation types exist."""
        assert OperationType.DEPARTURE
        assert OperationType.ARRIVAL
        assert OperationType.APPROACH

    def test_operation_type_labels(self):
        """Test operation type labels."""
        assert OperationType.DEPARTURE.label == "Departure"
        assert OperationType.ARRIVAL.label == "Arrival"
        assert OperationType.APPROACH.label == "Approach"

    def test_operation_type_codes(self):
        """Test operation type codes."""
        assert OperationType.DEPARTURE.code == "4464713"
        assert OperationType.ARRIVAL.code == "4530249"
        assert OperationType.APPROACH.code == "4595785"

    def test_operation_type_iteration(self):
        """Test that we can iterate over operation types."""
        types = list(OperationType)
        assert len(types) == 3


class TestFixType:
    """Tests for FixType enum."""

    def test_fix_type_values(self):
        """Test that all fix types exist."""
        assert FixType.VORDME
        assert FixType.VOR
        assert FixType.NDBDME
        assert FixType.NDB
        assert FixType.ILS
        assert FixType.RNP

    def test_fix_type_labels(self):
        """Test fix type labels."""
        assert FixType.VORDME.label == "VORDME"
        assert FixType.VOR.label == "VOR"
        assert FixType.NDBDME.label == "NDBDME"
        assert FixType.NDB.label == "NDB"
        assert FixType.ILS.label == "ILS"
        assert FixType.RNP.label == "RNP"

    def test_fix_type_codes(self):
        """Test fix type codes."""
        assert FixType.VORDME.code == "D"
        assert FixType.VOR.code == "V"
        assert FixType.NDBDME.code == "Q"
        assert FixType.NDB.code == "N"
        assert FixType.ILS.code == "I"
        assert FixType.RNP.code == "R"

    def test_fix_type_iteration(self):
        """Test that we can iterate over fix types."""
        types = list(FixType)
        assert len(types) == 6


class TestFixUsage:
    """Tests for FixUsage enum."""

    def test_fix_usage_values(self):
        """Test that all fix usage types exist."""
        assert FixUsage.FINAL_APPROACH
        assert FixUsage.INITIAL_APPROACH
        assert FixUsage.INTERMEDIATE_APPROACH
        assert FixUsage.FINAL_APPROACH_COURSE
        assert FixUsage.MISSED_APPROACH_POINT

    def test_fix_usage_labels(self):
        """Test fix usage labels."""
        assert FixUsage.FINAL_APPROACH.label == "Final approach fix"
        assert FixUsage.INITIAL_APPROACH.label == "Initial approach fix"
        assert FixUsage.INTERMEDIATE_APPROACH.label == "Intermediate approach fix"
        assert FixUsage.FINAL_APPROACH_COURSE.label == "Final approach course fix"
        assert FixUsage.MISSED_APPROACH_POINT.label == "Missed approach point fix"

    def test_fix_usage_codes(self):
        """Test fix usage codes."""
        assert FixUsage.FINAL_APPROACH.code == "F"
        assert FixUsage.INITIAL_APPROACH.code == "A"
        assert FixUsage.INTERMEDIATE_APPROACH.code == "I"
        assert FixUsage.FINAL_APPROACH_COURSE.code == "C"
        assert FixUsage.MISSED_APPROACH_POINT.code == "M"

    def test_fix_usage_iteration(self):
        """Test that we can iterate over fix usage types."""
        usages = list(FixUsage)
        assert len(usages) == 5


class TestNavAidType:
    """Tests for NavAidType enum."""

    def test_navaid_type_values(self):
        """Test that all navaid types exist."""
        assert NavAidType.VOR
        assert NavAidType.DME_VOR
        assert NavAidType.NDB
        assert NavAidType.DME
        assert NavAidType.OUTER_MARKER
        assert NavAidType.MIDDLE_MARKER
        assert NavAidType.INNER_MARKER

    def test_navaid_type_codes(self):
        """Test navaid type codes."""
        assert NavAidType.VOR.code == "3"
        assert NavAidType.DME_VOR.code == "12"
        assert NavAidType.NDB.code == "2"
        assert NavAidType.DME.code == "13"
        assert NavAidType.OUTER_MARKER.code == "7"
        assert NavAidType.MIDDLE_MARKER.code == "8"
        assert NavAidType.INNER_MARKER.code == "9"

    def test_navaid_type_labels(self):
        """Test navaid type labels."""
        assert NavAidType.VOR.label == "VOR"
        assert NavAidType.DME_VOR.label == "DME (VOR)"
        assert NavAidType.NDB.label == "NDB"
        assert NavAidType.DME.label == "DME"
        assert NavAidType.OUTER_MARKER.label == "OUTER MARKER"
        assert NavAidType.MIDDLE_MARKER.label == "MIDDLE MARKER"
        assert NavAidType.INNER_MARKER.label == "INNER MARKER"

    def test_navaid_type_iteration(self):
        """Test that we can iterate over navaid types."""
        types = list(NavAidType)
        assert len(types) == 7


class TestFileType:
    """Tests for FileType enum."""

    def test_file_type_values(self):
        """Test that all file types exist."""
        assert FileType.NAV
        assert FileType.FIX

    def test_file_type_values_content(self):
        """Test file type values."""
        assert FileType.NAV.value == "NAV"
        assert FileType.FIX.value == "FIX"

    def test_file_type_iteration(self):
        """Test that we can iterate over file types."""
        types = list(FileType)
        assert len(types) == 2
