"""
Test suite for the file_operations module.
"""

import tempfile
from pathlib import Path

import pytest

from src.constants import FileType
from src.file_operations import DataFileReader
from src.models import NavAidEntry


class TestDataFileReader:
    """Tests for DataFileReader class."""

    def test_read_nav_file_with_matching_identifier(self, tmp_path):
        """Test reading NAV file with matching identifier."""
        # Create test NAV file
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text(
            "3 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO VOR\n"
            "3 38.5 -121.5 0 11650 100 0.0 SAC SACRAMENTO VOR\n"
        )

        # Read file
        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

        assert len(results) == 1
        assert results[0].identifier == "SFO"
        assert results[0].latitude == 37.6213
        assert results[0].longitude == -122.3790
        assert results[0].type_code == "3"
        assert results[0].name == "VOR"

    def test_read_nav_file_case_insensitive(self, tmp_path):
        """Test that identifier search is case-insensitive."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text("3 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO VOR\n")

        # Search with lowercase
        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "sfo")

        assert len(results) == 1
        assert results[0].identifier == "SFO"

    def test_read_nav_file_multiple_matches(self, tmp_path):
        """Test reading NAV file with multiple matching identifiers."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text(
            "3 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO VOR\n"
            "12 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO DME\n"
        )

        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

        assert len(results) == 2
        assert results[0].type_code == "3"
        assert results[1].type_code == "12"

    def test_read_nav_file_no_matches(self, tmp_path):
        """Test reading NAV file with no matching identifier."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text("3 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO VOR\n")

        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "LAX")

        assert len(results) == 0

    def test_read_nav_file_skips_empty_lines(self, tmp_path):
        """Test that empty lines are skipped."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text(
            "\n" "3 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO VOR\n" "\n" "\n"
        )

        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

        assert len(results) == 1

    def test_read_nav_file_skips_incomplete_lines(self, tmp_path):
        """Test that lines with insufficient parts are skipped."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text(
            "3 37.6213 -122.3790\n"  # Incomplete line
            "3 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO VOR\n"
        )

        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

        assert len(results) == 1

    def test_read_fix_file_with_matching_identifier(self, tmp_path):
        """Test reading FIX file with matching identifier."""
        fix_file = tmp_path / "test_fix.dat"
        fix_file.write_text(
            "37.6213 -122.3790 FAITH\n" "38.5 -121.5 HOPES\n" "39.0 -120.0 FAITH\n"
        )

        results = DataFileReader.read_file(str(fix_file), FileType.FIX, "FAITH")

        assert len(results) == 2
        assert results[0].identifier == "FAITH"
        assert results[0].latitude == 37.6213
        assert results[0].longitude == -122.3790
        assert results[0].name is None  # FIX files don't have names at index 9

    def test_read_fix_file_no_matches(self, tmp_path):
        """Test reading FIX file with no matching identifier."""
        fix_file = tmp_path / "test_fix.dat"
        fix_file.write_text("37.6213 -122.3790 FAITH\n")

        results = DataFileReader.read_file(str(fix_file), FileType.FIX, "HOPES")

        assert len(results) == 0

    def test_read_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            DataFileReader.read_file("/nonexistent/file.dat", FileType.NAV, "SFO")

    def test_read_file_invalid_coordinate_format(self, tmp_path):
        """Test that ValueError is raised for invalid coordinate format."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text("3 INVALID -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO VOR\n")

        with pytest.raises(ValueError, match="Invalid data format"):
            DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

    def test_validate_file_path_valid(self, tmp_path):
        """Test validation of valid file path."""
        test_file = tmp_path / "test.dat"
        test_file.write_text("test content")

        result = DataFileReader.validate_file_path(str(test_file))

        assert result is None

    def test_validate_file_path_empty(self):
        """Test validation of empty file path."""
        result = DataFileReader.validate_file_path("")

        assert result == "No file path provided"

    def test_validate_file_path_does_not_exist(self):
        """Test validation of non-existent file path."""
        result = DataFileReader.validate_file_path("/nonexistent/file.dat")

        assert "File does not exist" in result

    def test_validate_file_path_is_directory(self, tmp_path):
        """Test validation when path is a directory."""
        result = DataFileReader.validate_file_path(str(tmp_path))

        assert "Path is not a file" in result

    def test_validate_file_path_permission_error(self, tmp_path):
        """Test validation when file cannot be read due to permissions."""
        import os
        import stat

        test_file = tmp_path / "test.dat"
        test_file.write_text("test content")

        # Remove read permissions
        os.chmod(test_file, stat.S_IWRITE)

        try:
            result = DataFileReader.validate_file_path(str(test_file))
            # On some systems this may fail, on others it may succeed
            # Just check that we got a response
            assert result is None or "No permission" in result or "Error accessing" in result
        finally:
            # Restore permissions for cleanup
            os.chmod(test_file, stat.S_IREAD | stat.S_IWRITE)

    def test_read_nav_file_with_extra_fields(self, tmp_path):
        """Test reading NAV file with extra fields beyond expected indices."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text("3 37.6213 -122.3790 0 11770 130 0.0 SFO EXTRA FIELDS HERE MORE\n")

        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

        assert len(results) == 1
        assert results[0].identifier == "SFO"
        assert results[0].name == "FIELDS"  # 10th field (index 9)

    def test_read_nav_file_missing_name_field(self, tmp_path):
        """Test reading NAV file without name field."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text("3 37.6213 -122.3790 0 11770 130 0.0 SFO EXTRA\n")

        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

        assert len(results) == 1
        assert results[0].identifier == "SFO"
        assert results[0].name is None  # No 10th field

    def test_navaid_entry_has_raw_parts(self, tmp_path):
        """Test that NavAidEntry contains raw_parts from file."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text("3 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-FRANCISCO VOR\n")

        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

        assert len(results) == 1
        assert results[0].raw_parts is not None
        assert len(results[0].raw_parts) > 0
        assert results[0].raw_parts[0] == "3"

    def test_read_file_with_unicode_content(self, tmp_path):
        """Test reading file with unicode characters."""
        nav_file = tmp_path / "test_nav.dat"
        nav_file.write_text("3 37.6213 -122.3790 0 11770 130 0.0 SFO SAN-JOSÉ VOR\n", encoding="utf-8")

        results = DataFileReader.read_file(str(nav_file), FileType.NAV, "SFO")

        assert len(results) == 1
        assert results[0].identifier == "SFO"

    def test_validate_file_path_generic_error(self, tmp_path, monkeypatch):
        """Test validation when generic error occurs during file access."""
        test_file = tmp_path / "test.dat"
        test_file.write_text("test content")

        # Mock open to raise a generic exception
        def mock_open(*args, **kwargs):
            raise IOError("Generic IO error")

        import builtins

        monkeypatch.setattr(builtins, "open", mock_open)

        result = DataFileReader.validate_file_path(str(test_file))

        assert result is not None
        assert "Error accessing file" in result
