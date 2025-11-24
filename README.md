# VOR-FIX Coordinate Calculator

A professional desktop application for calculating aviation navigation waypoints and approach fixes using precise geodesic calculations based on VOR/DME/NDB navigation data.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey.svg)

## 🎯 Overview

VOR-FIX Calculator is designed for aviation professionals, flight simulation enthusiasts, and procedure designers who need to calculate precise geographic coordinates for waypoints and approach fixes. The tool uses WGS84 ellipsoid geodesic calculations to ensure accuracy in aviation navigation planning.

### Key Features

- **Waypoint Calculation**: Calculate waypoint coordinates from VOR/DME/NDB stations using:
  - Magnetic bearing
  - Distance (nautical miles)
  - Magnetic declination
  - Automatic radius designator assignment (A-Z)

- **Fix Calculation**: Define and format approach fixes with:
  - Support for multiple fix types (VORDME, VOR, NDBDME, NDB, ILS, RNP)
  - Fix usage classification (Final, Initial, Intermediate, etc.)
  - Runway association
  - Operation type specification (Departure, Arrival, Approach)

- **Navigation Data Integration**: 
  - Import and search through NAV and FIX data files
  - Compatible with X-Plane navigation data formats
  - Quick identifier-based coordinate lookup

- **User-Friendly Interface**:
  - Clean, intuitive Tkinter-based GUI
  - Dual-mode operation (Waypoint/Fix)
  - Real-time validation and error handling
  - Copy-to-clipboard functionality

## 📋 Requirements

- Python 3.8 or higher
- tkinter (usually included with Python)
- geographiclib >= 2.0

## 🚀 Installation

### From Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/vor-fix-calculator.git
   cd vor-fix-calculator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package** (optional):
   ```bash
   pip install -e .
   ```

### Using pip

```bash
pip install vor-fix-calculator
```

## 💻 Usage

### Running the Application

**As a Python script**:
```bash
python app.py
```

**If installed as a package**:
```bash
vor-fix-calculator
```

### Waypoint Calculation Mode

1. Select **WAYPOINT** mode
2. Load a NAV data file (contains VOR/DME/NDB coordinates)
3. Enter or search for a navigation aid identifier
4. Input the following parameters:
   - **Magnetic Bearing**: 0-360 degrees
   - **Distance**: Nautical miles from the reference point
   - **Magnetic Declination**: Local magnetic variation
   - **Airport Code**: 4-letter ICAO code
   - **VOR Identifier**: 3-4 character identifier
   - **Operation Type**: Departure, Arrival, or Approach
5. Click **Calculate Waypoint**
6. The result includes:
   - Precise latitude/longitude coordinates
   - Radius designator letter (A-Z based on distance)
   - Formatted output string

### Fix Calculation Mode

1. Select **FIX** mode
2. Load a FIX or NAV data file
3. Enter or search for a fix identifier
4. Configure:
   - **FIX Type**: VORDME, VOR, NDBDME, NDB, ILS, or RNP
   - **FIX Usage**: Final approach, Initial, Intermediate, etc.
   - **Runway Code**: Associated runway (01-36)
   - **Airport Code**: 4-letter ICAO code
   - **Operation Type**: Departure, Arrival, or Approach
5. Click **Calculate FIX**
6. Get formatted output for procedure design

## 📊 Data File Formats

### NAV File Format
The application expects NAV files in X-Plane format with space-separated values:
```
[TYPE] [LAT] [LON] [ELEV] [FREQ] [RANGE] [BEARING] [IDENTIFIER] [NAME] [OTHER_FIELDS]
```

### FIX File Format
FIX files should contain:
```
[LAT] [LON] [IDENTIFIER] [ADDITIONAL_FIELDS]
```

## 🔧 Development

### Setting Up Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/vor-fix-calculator.git
   cd vor-fix-calculator
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Install pre-commit hooks** (optional):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_models.py
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Lint with Flake8
flake8 src/ tests/

# Type checking with MyPy
mypy src/

# Run all quality checks
make lint
```

### Using the Makefile

```bash
make help          # Show all available commands
make install       # Install dependencies
make test          # Run tests with coverage
make lint          # Run all linters
make format        # Format code with Black
make clean         # Clean generated files
```

## 📁 Project Structure

```
vor-fix-calculator/
├── app.py                  # Main application entry point
├── src/                    # Source code package
│   ├── __init__.py
│   ├── calculations.py     # Geodesic calculations
│   ├── constants.py        # Configuration and enumerations
│   ├── file_operations.py  # Data file reading
│   ├── formatters.py       # Output formatting
│   ├── models.py           # Data models
│   ├── ui.py              # Tkinter GUI
│   └── validators.py       # Input validation
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_models.py
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── pyproject.toml         # Project metadata and configuration
├── setup.py               # Setup script
├── Makefile               # Development automation
├── LICENSE                # MIT License
├── README.md              # This file
└── CONTRIBUTING.md        # Contribution guidelines
```

## 🧮 Calculation Methodology

### Geodesic Calculations

The application uses the **GeographicLib** library, which implements Karney's algorithms for geodesic calculations on the WGS84 ellipsoid. This ensures:

- High accuracy (errors < 15 nanometers)
- Proper handling of antipodal cases
- Correct behavior at poles and equator
- Industry-standard WGS84 datum compliance

### Magnetic to True Bearing Conversion

```python
true_bearing = (magnetic_bearing + declination) % 360
```

### Radius Designator

Distance ranges are mapped to letters A-Z:
- A: 0.1-1.4 NM
- B: 1.5-2.4 NM
- ...
- Z: 25.5-26.4 NM

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Code of conduct
- Development workflow
- Coding standards
- Pull request process

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests and linters
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GeographicLib**: For providing accurate geodesic calculations
- **X-Plane**: For navigation data format specifications
- Aviation community for valuable feedback and testing

## 📧 Contact

- **Project Homepage**: https://github.com/yourusername/vor-fix-calculator
- **Issue Tracker**: https://github.com/yourusername/vor-fix-calculator/issues

## 🗺️ Roadmap

Future enhancements planned:
- [ ] Export to multiple data formats (CSV, JSON, XML)
- [ ] Batch calculation support
- [ ] Visual map display of calculated waypoints
- [ ] Integration with online magnetic declination services
- [ ] Support for additional navigation data sources
- [ ] Command-line interface (CLI) mode
- [ ] Distance and bearing calculation between points
- [ ] Route planning with multiple waypoints

## ❓ FAQ

### Q: What coordinate format does the application use?
**A**: Decimal degrees (DD) format. Example: `40.7128 -74.0060`

### Q: Can I use this with FSX or MSFS data?
**A**: The application is designed for X-Plane format but can work with any properly formatted NAV/FIX files.

### Q: How accurate are the calculations?
**A**: The geodesic calculations are accurate to within nanometers using the WGS84 ellipsoid model.

### Q: What is magnetic declination?
**A**: The angle between magnetic north and true north at a specific location. It varies by location and time.

### Q: Where can I get NAV and FIX data files?
**A**: Navigation data files can be obtained from X-Plane installations or aviation data providers like Navigraph.

---

**Built with ❤️ for the aviation community**
