"""
Test suite for the validators module.
"""

import pytest

from src.models import Coordinates
from src.validators import (
    AirportCodeValidator,
    BearingValidator,
    CoordinateValidator,
    DeclinationValidator,
    DistanceValidator,
    RunwayCodeValidator,
    ValidationError,
    VORIdentifierValidator,
)


class TestValidationError:
    """Tests for ValidationError exception."""

    def test_can_raise_validation_error(self):
        """Test that ValidationError can be raised."""
        with pytest.raises(ValidationError):
            raise ValidationError("Test error")

    def test_validation_error_message(self):
        """Test that ValidationError preserves message."""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Custom message")
        assert str(exc_info.value) == "Custom message"


class TestCoordinateValidator:
    """Tests for CoordinateValidator class."""

    def test_valid_coordinates(self):
        """Test validation of valid coordinates."""
        CoordinateValidator.validate(37.6213, -122.3790)  # Should not raise

    def test_latitude_too_high(self):
        """Test that latitude above 90 raises error."""
        with pytest.raises(ValidationError, match="Latitude must be between"):
            CoordinateValidator.validate(91.0, 0.0)

    def test_latitude_too_low(self):
        """Test that latitude below -90 raises error."""
        with pytest.raises(ValidationError, match="Latitude must be between"):
            CoordinateValidator.validate(-91.0, 0.0)

    def test_longitude_too_high(self):
        """Test that longitude above 180 raises error."""
        with pytest.raises(ValidationError, match="Longitude must be between"):
            CoordinateValidator.validate(0.0, 181.0)

    def test_longitude_too_low(self):
        """Test that longitude below -180 raises error."""
        with pytest.raises(ValidationError, match="Longitude must be between"):
            CoordinateValidator.validate(0.0, -181.0)

    def test_boundary_values_valid(self):
        """Test that boundary values are valid."""
        CoordinateValidator.validate(90.0, 180.0)  # Max values
        CoordinateValidator.validate(-90.0, -180.0)  # Min values
        CoordinateValidator.validate(0.0, 0.0)  # Zero

    def test_parse_valid_coordinates(self):
        """Test parsing valid coordinate string."""
        result = CoordinateValidator.parse_coordinates("37.6213 -122.3790")
        assert isinstance(result, Coordinates)
        assert result.latitude == 37.6213
        assert result.longitude == -122.3790

    def test_parse_coordinates_with_extra_whitespace(self):
        """Test parsing coordinates with extra whitespace."""
        result = CoordinateValidator.parse_coordinates("  37.6213   -122.3790  ")
        assert result.latitude == 37.6213
        assert result.longitude == -122.3790

    def test_parse_empty_string(self):
        """Test that empty string raises error."""
        with pytest.raises(ValidationError, match="Coordinates cannot be empty"):
            CoordinateValidator.parse_coordinates("")

    def test_parse_whitespace_only(self):
        """Test that whitespace-only string raises error."""
        with pytest.raises(ValidationError, match="Coordinates cannot be empty"):
            CoordinateValidator.parse_coordinates("   ")

    def test_parse_single_value(self):
        """Test that single value raises error."""
        with pytest.raises(ValidationError, match="must be in format"):
            CoordinateValidator.parse_coordinates("37.6213")

    def test_parse_three_values(self):
        """Test that three values raises error."""
        with pytest.raises(ValidationError, match="must be in format"):
            CoordinateValidator.parse_coordinates("37.6213 -122.3790 100")

    def test_parse_non_numeric(self):
        """Test that non-numeric values raise error."""
        with pytest.raises(ValidationError, match="Invalid coordinate format"):
            CoordinateValidator.parse_coordinates("abc def")

    def test_parse_invalid_coordinates_raises_validation_error(self):
        """Test that invalid coordinates in string raise ValidationError."""
        with pytest.raises(ValidationError, match="Latitude must be between"):
            CoordinateValidator.parse_coordinates("91.0 0.0")


class TestBearingValidator:
    """Tests for BearingValidator class."""

    def test_valid_bearing(self):
        """Test validation of valid bearing."""
        BearingValidator.validate(180.0)  # Should not raise

    def test_bearing_zero(self):
        """Test that bearing 0 is valid."""
        BearingValidator.validate(0.0)

    def test_bearing_360(self):
        """Test that bearing 360 is valid."""
        BearingValidator.validate(360.0)

    def test_bearing_negative(self):
        """Test that negative bearing raises error."""
        with pytest.raises(ValidationError, match="Bearing must be between"):
            BearingValidator.validate(-1.0)

    def test_bearing_over_360(self):
        """Test that bearing over 360 raises error."""
        with pytest.raises(ValidationError, match="Bearing must be between"):
            BearingValidator.validate(361.0)

    def test_parse_valid_bearing(self):
        """Test parsing valid bearing string."""
        result = BearingValidator.parse("180")
        assert result == 180.0

    def test_parse_bearing_with_decimals(self):
        """Test parsing bearing with decimals."""
        result = BearingValidator.parse("180.5")
        assert result == 180.5

    def test_parse_bearing_with_whitespace(self):
        """Test parsing bearing with whitespace."""
        result = BearingValidator.parse("  180.5  ")
        assert result == 180.5

    def test_parse_bearing_360_normalized_to_zero(self):
        """Test that 360 is normalized to 0."""
        result = BearingValidator.parse("360")
        assert result == 0.0

    def test_parse_empty_bearing(self):
        """Test that empty bearing raises error."""
        with pytest.raises(ValidationError, match="Bearing cannot be empty"):
            BearingValidator.parse("")

    def test_parse_whitespace_bearing(self):
        """Test that whitespace-only bearing raises error."""
        with pytest.raises(ValidationError, match="Bearing cannot be empty"):
            BearingValidator.parse("   ")

    def test_parse_non_numeric_bearing(self):
        """Test that non-numeric bearing raises error."""
        with pytest.raises(ValidationError, match="Invalid bearing format"):
            BearingValidator.parse("abc")


class TestDistanceValidator:
    """Tests for DistanceValidator class."""

    def test_valid_distance(self):
        """Test validation of valid distance."""
        DistanceValidator.validate(10.0)  # Should not raise

    def test_distance_zero_invalid(self):
        """Test that zero distance is invalid."""
        with pytest.raises(ValidationError, match="Distance must be greater than"):
            DistanceValidator.validate(0.0)

    def test_distance_negative_invalid(self):
        """Test that negative distance is invalid."""
        with pytest.raises(ValidationError, match="Distance must be greater than"):
            DistanceValidator.validate(-1.0)

    def test_distance_very_small_valid(self):
        """Test that very small positive distance is valid."""
        DistanceValidator.validate(0.01)  # Should not raise

    def test_parse_valid_distance(self):
        """Test parsing valid distance string."""
        result = DistanceValidator.parse("10.5")
        assert result == 10.5

    def test_parse_distance_with_whitespace(self):
        """Test parsing distance with whitespace."""
        result = DistanceValidator.parse("  10.5  ")
        assert result == 10.5

    def test_parse_empty_distance(self):
        """Test that empty distance raises error."""
        with pytest.raises(ValidationError, match="Distance cannot be empty"):
            DistanceValidator.parse("")

    def test_parse_non_numeric_distance(self):
        """Test that non-numeric distance raises error."""
        with pytest.raises(ValidationError, match="Invalid distance format"):
            DistanceValidator.parse("abc")


class TestDeclinationValidator:
    """Tests for DeclinationValidator class."""

    def test_valid_declination(self):
        """Test validation of valid declination."""
        DeclinationValidator.validate(15.0)  # Should not raise

    def test_declination_positive_boundary(self):
        """Test positive boundary declination."""
        DeclinationValidator.validate(180.0)  # Should not raise

    def test_declination_negative_boundary(self):
        """Test negative boundary declination."""
        DeclinationValidator.validate(-180.0)  # Should not raise

    def test_declination_zero(self):
        """Test zero declination."""
        DeclinationValidator.validate(0.0)  # Should not raise

    def test_declination_too_high(self):
        """Test that declination above 180 raises error."""
        with pytest.raises(ValidationError, match="Declination must be between"):
            DeclinationValidator.validate(181.0)

    def test_declination_too_low(self):
        """Test that declination below -180 raises error."""
        with pytest.raises(ValidationError, match="Declination must be between"):
            DeclinationValidator.validate(-181.0)

    def test_parse_valid_declination(self):
        """Test parsing valid declination string."""
        result = DeclinationValidator.parse("15.5")
        assert result == 15.5

    def test_parse_negative_declination(self):
        """Test parsing negative declination."""
        result = DeclinationValidator.parse("-15.5")
        assert result == -15.5

    def test_parse_declination_with_whitespace(self):
        """Test parsing declination with whitespace."""
        result = DeclinationValidator.parse("  15.5  ")
        assert result == 15.5

    def test_parse_empty_declination(self):
        """Test that empty declination raises error."""
        with pytest.raises(ValidationError, match="Declination cannot be empty"):
            DeclinationValidator.parse("")

    def test_parse_non_numeric_declination(self):
        """Test that non-numeric declination raises error."""
        with pytest.raises(ValidationError, match="Invalid declination format"):
            DeclinationValidator.parse("abc")


class TestAirportCodeValidator:
    """Tests for AirportCodeValidator class."""

    def test_valid_airport_code(self):
        """Test validation of valid airport code."""
        AirportCodeValidator.validate("KSFO")  # Should not raise

    def test_airport_code_lowercase(self):
        """Test that lowercase code is accepted in validate."""
        AirportCodeValidator.validate("ksfo")  # Should not raise

    def test_airport_code_empty(self):
        """Test that empty code raises error."""
        with pytest.raises(ValidationError, match="Airport code cannot be empty"):
            AirportCodeValidator.validate("")

    def test_airport_code_too_short(self):
        """Test that short code raises error."""
        with pytest.raises(ValidationError, match="must be exactly 4 characters"):
            AirportCodeValidator.validate("KSF")

    def test_airport_code_too_long(self):
        """Test that long code raises error."""
        with pytest.raises(ValidationError, match="must be exactly 4 characters"):
            AirportCodeValidator.validate("KSFOO")

    def test_airport_code_with_numbers(self):
        """Test that code with numbers raises error."""
        with pytest.raises(ValidationError, match="must contain only letters"):
            AirportCodeValidator.validate("KSF1")

    def test_airport_code_with_special_chars(self):
        """Test that code with special chars raises error."""
        with pytest.raises(ValidationError, match="must contain only letters"):
            AirportCodeValidator.validate("KS-F")

    def test_parse_valid_airport_code(self):
        """Test parsing valid airport code."""
        result = AirportCodeValidator.parse("ksfo")
        assert result == "KSFO"

    def test_parse_airport_code_with_whitespace(self):
        """Test parsing airport code with whitespace."""
        result = AirportCodeValidator.parse("  ksfo  ")
        assert result == "KSFO"


class TestVORIdentifierValidator:
    """Tests for VORIdentifierValidator class."""

    def test_valid_vor_identifier_3_chars(self):
        """Test validation of valid 3-character VOR identifier."""
        VORIdentifierValidator.validate("SFO")  # Should not raise

    def test_valid_vor_identifier_4_chars(self):
        """Test validation of valid 4-character VOR identifier."""
        VORIdentifierValidator.validate("KSFO")  # Should not raise

    def test_vor_identifier_empty_when_allowed(self):
        """Test that empty identifier is valid when allowed."""
        VORIdentifierValidator.validate("", allow_empty=True)  # Should not raise

    def test_vor_identifier_empty_when_not_allowed(self):
        """Test that empty identifier raises error when not allowed."""
        with pytest.raises(ValidationError, match="VOR identifier cannot be empty"):
            VORIdentifierValidator.validate("", allow_empty=False)

    def test_vor_identifier_too_short(self):
        """Test that short identifier raises error."""
        with pytest.raises(ValidationError, match="must be 3-4 characters"):
            VORIdentifierValidator.validate("SF")

    def test_vor_identifier_too_long(self):
        """Test that long identifier raises error."""
        with pytest.raises(ValidationError, match="must be 3-4 characters"):
            VORIdentifierValidator.validate("KSFOO")

    def test_vor_identifier_with_numbers(self):
        """Test that identifier with numbers raises error."""
        with pytest.raises(ValidationError, match="must contain only letters"):
            VORIdentifierValidator.validate("SF1")

    def test_vor_identifier_with_special_chars(self):
        """Test that identifier with special chars raises error."""
        with pytest.raises(ValidationError, match="must contain only letters"):
            VORIdentifierValidator.validate("SF-")

    def test_parse_valid_vor_identifier(self):
        """Test parsing valid VOR identifier."""
        result = VORIdentifierValidator.parse("sfo")
        assert result == "SFO"

    def test_parse_vor_identifier_with_whitespace(self):
        """Test parsing VOR identifier with whitespace."""
        result = VORIdentifierValidator.parse("  sfo  ")
        assert result == "SFO"

    def test_parse_empty_vor_identifier_when_allowed(self):
        """Test parsing empty VOR identifier when allowed."""
        result = VORIdentifierValidator.parse("", allow_empty=True)
        assert result == ""

    def test_parse_whitespace_vor_identifier_when_allowed(self):
        """Test parsing whitespace VOR identifier when allowed."""
        result = VORIdentifierValidator.parse("   ", allow_empty=True)
        assert result == ""


class TestRunwayCodeValidator:
    """Tests for RunwayCodeValidator class."""

    def test_valid_runway_code(self):
        """Test validation of valid runway code."""
        RunwayCodeValidator.validate(18)  # Should not raise

    def test_runway_code_zero(self):
        """Test that runway code 0 is valid."""
        RunwayCodeValidator.validate(0)  # Should not raise

    def test_runway_code_max(self):
        """Test that runway code 99 is valid."""
        RunwayCodeValidator.validate(99)  # Should not raise

    def test_runway_code_negative(self):
        """Test that negative runway code raises error."""
        with pytest.raises(ValidationError, match="Runway code must be between"):
            RunwayCodeValidator.validate(-1)

    def test_runway_code_over_max(self):
        """Test that runway code over 99 raises error."""
        with pytest.raises(ValidationError, match="Runway code must be between"):
            RunwayCodeValidator.validate(100)

    def test_parse_valid_runway_code(self):
        """Test parsing valid runway code."""
        result = RunwayCodeValidator.parse("18")
        assert result == 18

    def test_parse_runway_code_with_whitespace(self):
        """Test parsing runway code with whitespace."""
        result = RunwayCodeValidator.parse("  18  ")
        assert result == 18

    def test_parse_runway_code_single_digit(self):
        """Test parsing single-digit runway code."""
        result = RunwayCodeValidator.parse("9")
        assert result == 9

    def test_parse_empty_runway_code(self):
        """Test that empty runway code raises error."""
        with pytest.raises(ValidationError, match="Runway code cannot be empty"):
            RunwayCodeValidator.parse("")

    def test_parse_non_numeric_runway_code(self):
        """Test that non-numeric runway code raises error."""
        with pytest.raises(ValidationError, match="Invalid runway code format"):
            RunwayCodeValidator.parse("abc")

    def test_parse_decimal_runway_code(self):
        """Test that decimal runway code raises error."""
        with pytest.raises(ValidationError, match="Invalid runway code format"):
            RunwayCodeValidator.parse("18.5")
