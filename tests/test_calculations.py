"""
Test suite for the calculations module.
"""

import pytest

from src.calculations import (
    calculate_destination_point,
    calculate_waypoint,
    get_radius_designator,
    magnetic_to_true_bearing,
)
from src.models import Coordinates


class TestMagneticToTrueBearing:
    """Tests for magnetic_to_true_bearing function."""

    def test_positive_declination(self):
        """Test conversion with positive declination."""
        result = magnetic_to_true_bearing(90.0, 15.0)
        assert result == 105.0

    def test_negative_declination(self):
        """Test conversion with negative declination."""
        result = magnetic_to_true_bearing(90.0, -15.0)
        assert result == 75.0

    def test_zero_declination(self):
        """Test conversion with zero declination."""
        result = magnetic_to_true_bearing(90.0, 0.0)
        assert result == 90.0

    def test_wrapping_over_360(self):
        """Test that result wraps around at 360 degrees."""
        result = magnetic_to_true_bearing(350.0, 20.0)
        assert result == 10.0

    def test_wrapping_below_zero(self):
        """Test that result wraps around below 0."""
        result = magnetic_to_true_bearing(10.0, -20.0)
        assert result == 350.0


class TestGetRadiusDesignator:
    """Tests for get_radius_designator function."""

    def test_letter_a_low(self):
        """Test lower bound of letter A range."""
        assert get_radius_designator(0.1) == "A"

    def test_letter_a_high(self):
        """Test upper bound of letter A range."""
        assert get_radius_designator(1.4) == "A"

    def test_letter_a_middle(self):
        """Test middle of letter A range."""
        assert get_radius_designator(0.8) == "A"

    def test_letter_b(self):
        """Test letter B range."""
        assert get_radius_designator(2.0) == "B"

    def test_letter_d(self):
        """Test letter D range."""
        assert get_radius_designator(4.0) == "D"

    def test_letter_m(self):
        """Test letter M range."""
        assert get_radius_designator(13.0) == "M"

    def test_letter_z_in_range(self):
        """Test letter Z within range."""
        assert get_radius_designator(26.0) == "Z"

    def test_distance_over_max_returns_z(self):
        """Test that distances over max range return Z."""
        assert get_radius_designator(30.0) == "Z"
        assert get_radius_designator(100.0) == "Z"

    def test_distance_below_min_returns_z(self):
        """Test that distances below min range return Z."""
        assert get_radius_designator(0.05) == "Z"


class TestCalculateDestinationPoint:
    """Tests for calculate_destination_point function."""

    def test_north_direction(self):
        """Test calculation going due north."""
        origin = Coordinates(latitude=37.0, longitude=-122.0)
        result = calculate_destination_point(origin, azimuth=0.0, distance_nm=60.0)

        # Going north should increase latitude, keep longitude similar
        assert result.latitude > origin.latitude
        assert abs(result.longitude - origin.longitude) < 0.1

    def test_east_direction(self):
        """Test calculation going due east."""
        origin = Coordinates(latitude=37.0, longitude=-122.0)
        result = calculate_destination_point(origin, azimuth=90.0, distance_nm=60.0)

        # Going east should increase longitude, keep latitude similar
        assert result.longitude > origin.longitude
        assert abs(result.latitude - origin.latitude) < 0.1

    def test_south_direction(self):
        """Test calculation going due south."""
        origin = Coordinates(latitude=37.0, longitude=-122.0)
        result = calculate_destination_point(origin, azimuth=180.0, distance_nm=60.0)

        # Going south should decrease latitude, keep longitude similar
        assert result.latitude < origin.latitude
        assert abs(result.longitude - origin.longitude) < 0.1

    def test_west_direction(self):
        """Test calculation going due west."""
        origin = Coordinates(latitude=37.0, longitude=-122.0)
        result = calculate_destination_point(origin, azimuth=270.0, distance_nm=60.0)

        # Going west should decrease longitude, keep latitude similar
        assert result.longitude < origin.longitude
        assert abs(result.latitude - origin.latitude) < 0.1

    def test_zero_distance(self):
        """Test calculation with zero distance returns same point."""
        origin = Coordinates(latitude=37.0, longitude=-122.0)
        result = calculate_destination_point(origin, azimuth=45.0, distance_nm=0.0)

        assert abs(result.latitude - origin.latitude) < 0.000001
        assert abs(result.longitude - origin.longitude) < 0.000001

    def test_known_distance_calculation(self):
        """Test calculation with known distance produces reasonable result."""
        origin = Coordinates(latitude=37.6213, longitude=-122.3790)
        # Calculate 10 NM at 45 degrees
        result = calculate_destination_point(origin, azimuth=45.0, distance_nm=10.0)

        # Should move northeast
        assert result.latitude > origin.latitude
        assert result.longitude > origin.longitude

        # Distance should be roughly 10 NM (verify both lat and lon changed)
        lat_diff = abs(result.latitude - origin.latitude)
        lon_diff = abs(result.longitude - origin.longitude)
        assert lat_diff > 0.05  # Significant change
        assert lon_diff > 0.05  # Significant change


class TestCalculateWaypoint:
    """Tests for calculate_waypoint function."""

    def test_with_positive_declination(self):
        """Test waypoint calculation with positive declination."""
        origin = Coordinates(latitude=37.6213, longitude=-122.3790)
        result = calculate_waypoint(
            origin=origin, magnetic_bearing=90.0, distance_nm=10.0, declination=15.0
        )

        # True bearing would be 105 (90 + 15), so should move east-southeast
        assert result.longitude > origin.longitude
        assert isinstance(result, Coordinates)

    def test_with_negative_declination(self):
        """Test waypoint calculation with negative declination."""
        origin = Coordinates(latitude=37.6213, longitude=-122.3790)
        result = calculate_waypoint(
            origin=origin, magnetic_bearing=90.0, distance_nm=10.0, declination=-15.0
        )

        # True bearing would be 75 (90 - 15), so should move east-northeast
        assert result.longitude > origin.longitude
        assert isinstance(result, Coordinates)

    def test_with_zero_declination(self):
        """Test waypoint calculation with zero declination."""
        origin = Coordinates(latitude=37.6213, longitude=-122.3790)
        result = calculate_waypoint(
            origin=origin, magnetic_bearing=90.0, distance_nm=10.0, declination=0.0
        )

        # True bearing equals magnetic bearing (90), so should move due east
        assert result.longitude > origin.longitude
        assert abs(result.latitude - origin.latitude) < 0.1

    def test_wrapping_declination(self):
        """Test waypoint calculation with declination that causes wrapping."""
        origin = Coordinates(latitude=37.6213, longitude=-122.3790)
        result = calculate_waypoint(
            origin=origin, magnetic_bearing=350.0, distance_nm=10.0, declination=20.0
        )

        # True bearing would be 10 (350 + 20 % 360), so should move north-northeast
        assert result.latitude > origin.latitude
        assert isinstance(result, Coordinates)
