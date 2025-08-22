# Enhanced twoWaySlab - Multi-Standard RC Slab Design Tool

## 🌟 Overview

Enhanced twoWaySlab is a comprehensive structural engineering software for designing reinforced concrete two-way slabs. This enhanced version supports multiple international building codes including **Thailand (TIS)**, Japan (AIJ), USA (ACI), and European (Eurocode) standards with full internationalization support.

## 🎯 Key Features

### ✨ **New Enhanced Features**

1. **🇹🇭 Thailand Building Code Support (TIS)**
   - Complete TIS (Thai Industrial Standards) implementation
   - Thai rebar designations (DB6, DB9, DB12, DB16, etc.)
   - Thai concrete and steel grade specifications
   - Compatibility with existing Japanese interface

2. **🌐 Multi-Language Support (i18n)**
   - English, Japanese (日本語), and Thai (ไทย) languages
   - Dynamic language switching
   - Localized number formatting and date formats
   - Comprehensive translation system

3. **⚙️ Configuration Management**
   - Multiple building code support
   - User preferences and settings
   - Automatic language switching based on building code
   - Persistent configuration storage

4. **📐 Unit Conversion System**
   - Metric SI, Metric Engineering, Imperial, and Mixed units
   - Automatic unit conversion between systems
   - Proper unit display and formatting
   - Support for different measurement standards

5. **✅ Advanced Input Validation**
   - Comprehensive input checking and validation
   - Real-time error detection and warnings
   - Building code specific validations
   - Cross-validation between related parameters

6. **📊 Enhanced Reporting**
   - Multi-language PDF reports
   - Building code specific information
   - Improved formatting and layout
   - Support for different fonts and character sets

### 🏗️ **Core Structural Features**

- **Advanced Calculation Engine**: Direct Fourier transform solutions for plate equations
- **Multiple Boundary Conditions**: 11 different support and fixity conditions
- **Comprehensive Analysis**: Moment, deflection, and stress calculations
- **Reinforcement Design**: Automatic rebar area and spacing calculations
- **Data Management**: Import/Export capabilities with CSV support

## 🚀 Quick Start

### Prerequisites

```bash
pip install numpy sympy pandas reportlab wxPython matplotlib
```

### Installation

1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies (see Prerequisites)
4. Run the enhanced application:

```bash
python twoWaySlab_enhanced.py
```

Or run tests to verify installation:

```bash
python run_tests.py
```

## 📚 Usage Guide

### Basic Workflow

1. **Select Building Code**: Choose from Thailand (TIS), Japan (AIJ), USA (ACI), or Eurocode
2. **Set Language**: Select English, Japanese, or Thai interface
3. **Input Slab Parameters**: Enter dimensions, loads, and material properties
4. **Choose Boundary Conditions**: Select from 11 available support conditions
5. **Calculate**: Run analysis with automatic validation
6. **Review Results**: Check moments, deflections, and reinforcement requirements
7. **Generate Report**: Create PDF reports in multiple languages

### Building Code Selection

#### 🇹🇭 Thailand (TIS)
- **Concrete Grades**: Fc18, Fc21, Fc24, Fc28, Fc35, Fc42, Fc50
- **Steel Grades**: SD30 (295 N/mm²), SD40 (390 N/mm²), SD50 (490 N/mm²)
- **Rebar Designations**: DB6, DB9, DB12, DB16, DB20, DB25, DB28, DB32, DB36, DB40
- **Concrete Modulus**: Ec = 4700 × √fc × (γ/24.0)^1.5

#### 🇯🇵 Japan (AIJ)
- **Steel Grades**: SR235, SD295, SD345, SD390, SD490
- **Rebar Designations**: D10, D13, D16, D19, D22, D25, D29, D32, D35, D38, D41
- **Concrete Modulus**: Ec = 3.35 × 10⁴ × (γ/24)² × (fc/60)^(1/3)

### Language Support

Switch between languages using the language selector:
- **English**: Full technical documentation and interface
- **日本語 (Japanese)**: Complete Japanese interface with proper character support
- **ไทย (Thai)**: Thai language interface with appropriate terminology

### Input Validation

The system provides comprehensive validation:

✅ **Valid Input Examples**:
- Slab length: 3.0-15.0 m
- Thickness: 100-500 mm
- Concrete strength: 15-50 N/mm²
- Load: 2.0-30.0 kN/m²

⚠️ **Warnings**: System provides warnings for unusual but valid inputs
❌ **Errors**: Invalid inputs are caught with clear error messages

## 🏗️ System Architecture

### Core Modules

```
Enhanced twoWaySlab/
├── Core Systems/
│   ├── config.py              # Configuration management
│   ├── i18n.py                # Internationalization
│   ├── units.py               # Unit conversion
│   ├── validation.py          # Input validation
│   └── thiRc.py               # Thailand building code
├── Original Modules/
│   ├── aijRc.py              # Japanese building code
│   ├── higashi.py            # Calculation engine
│   ├── gui.py                # GUI definition
│   └── report.py             # Original reporting
├── Enhanced Applications/
│   ├── twoWaySlab_enhanced.py # Enhanced main application
│   └── report_enhanced.py    # Enhanced reporting
├── Resources/
│   ├── translations/         # Language files
│   ├── fonts/               # Font files
│   └── images/              # Boundary condition images
└── Testing/
    └── run_tests.py         # Comprehensive test suite
```

### Design Patterns

- **Strategy Pattern**: Building code selection and material properties
- **Observer Pattern**: Configuration changes triggering UI updates
- **Factory Pattern**: Dynamic loading of material classes
- **Singleton Pattern**: Global configuration and i18n instances

## 🔧 Configuration

### Configuration File (config.json)

```json
{
    "building_code": "thai",
    "language": "th",
    "units": "metric",
    "precision": {
        "stress": 1,
        "moment": 2,
        "deflection": 3
    },
    "calculation_settings": {
        "creep_factor": 2.0,
        "safety_factors": {
            "concrete": 1.5,
            "steel": 1.15
        }
    }
}
```

### Available Building Codes

| Code | Name | Module | Standards |
|------|------|--------|-----------|
| `thai` | TIS (Thailand) | thiRc.py | Thai Industrial Standards |
| `japanese` | AIJ (Japan) | aijRc.py | Architectural Institute of Japan |
| `aci` | ACI (USA) | aciRc.py* | American Concrete Institute |
| `eurocode` | Eurocode (EU) | euRc.py* | European Standards |

*Not yet implemented in this version

## 🧪 Testing

Run the comprehensive test suite:

```bash
python run_tests.py
```

### Test Coverage

- ✅ Thai Building Code Implementation
- ✅ Configuration System
- ✅ Internationalization
- ✅ Unit Conversion
- ✅ Input Validation
- ✅ System Integration

Expected output:
```
Enhanced twoWaySlab System Tests
======================================================================
✓ Thai Building Code: PASSED
✓ Configuration System: PASSED
✓ Internationalization: PASSED
✓ Unit Conversion: PASSED
✓ Input Validation: PASSED
✓ System Integration: PASSED

Overall Result: 6/6 tests passed
🎉 ALL TESTS PASSED! The enhanced system is ready to use.
```

## 📖 API Reference

### Configuration API

```python
from config import config

# Get current building code
current_code = config.get_building_code()

# Switch to Thai building code
config.set_building_code('thai')

# Get material instance
material = config.get_material_instance()

# Get default values
defaults = config.get_default_values()
```

### Internationalization API

```python
from i18n import i18n

# Set language
i18n.set_language('th')

# Get translated text
title = i18n.t('app_title')
button_text = i18n.t('buttons.calculate')

# Get localized units
length_unit = i18n.t('units.length_m')
```

### Unit Conversion API

```python
from units import unit_converter

# Convert between units
length_m = unit_converter.convert_length(1000, 'mm', 'm')
stress_mpa = unit_converter.convert_stress(21, 'N/mm2', 'MPa')

# Set unit system
unit_converter.set_unit_system('metric_engineering')

# Format with units
formatted = unit_converter.format_value_with_unit(21.0, 'stress')
```

### Thai Building Code API

```python
from thiRc import ThaiRc_set

# Initialize Thai RC
thai_rc = ThaiRc_set()

# Get rebar area
area = thai_rc.Ra('DB16')  # Returns 201.1 mm²

# Get concrete modulus
ec = thai_rc.Ec(21.0, 24.0)  # Returns Young's modulus

# Get steel strength
fy = thai_rc.get_steel_strength('SD40')  # Returns 390 N/mm²
```

## 🔄 Migration from Original

### For Existing Users

The enhanced version is fully backward compatible:

1. **Existing data files** work without modification
2. **Original GUI** remains available as fallback
3. **Japanese building code** calculations unchanged
4. **All original features** preserved and enhanced

### Upgrading

1. Backup your existing data files
2. Copy enhanced files to your installation
3. Run `python run_tests.py` to verify
4. Launch with `python twoWaySlab_enhanced.py`

## 🌍 Internationalization

### Adding New Languages

1. Create translation file: `translations/[language_code].json`
2. Follow existing translation structure
3. Add language to `i18n.py` available languages
4. Update font settings if needed

### Translation Structure

```json
{
    "app_title": "Application Title",
    "menu": {
        "file": "File",
        "new": "New"
    },
    "input_labels": {
        "thickness": "Thickness",
        "load": "Load"
    },
    "units": {
        "length_m": "m",
        "stress": "N/mm²"
    }
}
```

## 🔧 Development

### Adding New Building Codes

1. Create new material module (e.g., `aciRc.py`)
2. Implement required interface methods:
   - `Ec(fc, gamma)`: Concrete modulus
   - `Ra(designation)`: Rebar area
   - `Ra_p(designation, pitch)`: Rebar per unit width
3. Add to `config.py` building codes dictionary
4. Update translations with new building code terms

### Code Structure

```python
class NewBuildingCode:
    def Ec(self, fc, gamma=24.0):
        """Calculate concrete modulus"""
        return modulus_value
    
    def Ra(self, bar_designation):
        """Get rebar area"""
        return area_mm2
    
    def Ra_p(self, bar_designation, pitch):
        """Get rebar area per unit width"""
        return self.Ra(bar_designation) * 1000.0 / pitch
```

## 🐛 Troubleshooting

### Common Issues

**Font Problems (Thai/Japanese text)**:
- Ensure font files are in `./fonts/` directory
- Check font file permissions
- Verify Unicode support in your system

**Building Code Not Loading**:
- Check `config.json` syntax
- Verify building code module exists
- Run test suite to identify issues

**Language Not Switching**:
- Verify translation file exists
- Check JSON syntax in translation files
- Clear configuration and restart

**Calculation Errors**:
- Validate all input parameters
- Check boundary condition selection
- Verify material property values

### Debug Mode

Enable debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

This enhanced version maintains compatibility with the original twoWaySlab license terms while adding new functionality for international structural engineering standards.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

### Development Guidelines

- Follow existing code structure and patterns
- Add comprehensive tests for new features
- Update documentation and translations
- Maintain backward compatibility
- Use type hints where appropriate

## 📞 Support

For issues, questions, or contributions:

1. **Testing**: Run `python run_tests.py` first
2. **Documentation**: Check this README and code comments
3. **Issues**: Create detailed issue reports with test cases
4. **Features**: Discuss new features before implementation

## 🎉 Acknowledgments

- Original twoWaySlab by Tsunoppy
- Dr. Higashi's plate theory implementation
- Thai Industrial Standards (TIS) specifications
- International structural engineering community

---

**Enhanced twoWaySlab v2.0** - Supporting global structural engineering standards with modern software architecture and comprehensive internationalization.