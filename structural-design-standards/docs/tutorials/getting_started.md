# Getting Started with Structural Design Standards

Welcome to the Structural Design Standards library! This comprehensive guide will help you get started with designing structural members using ACI 318M-25 and Thai Ministry Regulation B.E. 2566 standards.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install the Library

```bash
# Install from source (development)
git clone https://github.com/your-org/structural-design-standards.git
cd structural-design-standards
pip install -e .

# Or install from PyPI (when available)
pip install structural-design-standards
```

### Install Dependencies

```bash
# Core dependencies
pip install numpy scipy

# Optional dependencies for enhanced features
pip install matplotlib  # For plotting
pip install sphinx      # For documentation
pip install pytest      # For testing
```

## Quick Start

### Your First Beam Design

Let's design a simple concrete beam using ACI 318M-25:

```python
from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.beam_design import (
    ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
)

# Step 1: Create materials
concrete = ACI318M25Concrete(fc_prime=28.0)  # 28 MPa concrete
steel = ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')

print(f"Concrete: f'c = {concrete.fc_prime} MPa")
print(f"Steel: fy = {steel.fy} MPa, Grade = {steel.grade}")

# Step 2: Create beam designer
beam_designer = ACI318M25BeamDesign(concrete, steel)

# Step 3: Define geometry
geometry = BeamGeometry(
    width=300,           # mm
    height=600,          # mm  
    effective_depth=550, # mm
    span_length=6000     # mm
)

print(f"\nBeam Geometry:")
print(f"  Width: {geometry.width} mm")
print(f"  Height: {geometry.height} mm")
print(f"  Effective Depth: {geometry.effective_depth} mm")
print(f"  Span Length: {geometry.span_length} mm")

# Step 4: Define loads
loads = BeamLoads(
    dead_load=5.0,       # kN/m
    live_load=8.0        # kN/m
)

print(f"\nLoads:")
print(f"  Dead Load: {loads.dead_load} kN/m")
print(f"  Live Load: {loads.live_load} kN/m")

# Step 5: Perform design
result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)

# Step 6: Check results
print(f"\n=== DESIGN RESULTS ===")
print(f"Overall Status: {result.overall_status}")
print(f"Design Moment: {result.design_moments['factored_moment']:.1f} kN⋅m")
print(f"Required Steel Area: {result.required_reinforcement['required_steel_area']:.0f} mm²")
print(f"Utilization Ratio: {result.utilization_ratio:.2f}")

if result.overall_status == "PASS":
    print("✅ Design is adequate!")
else:
    print("❌ Design needs revision")
```

### Expected Output

```
Concrete: f'c = 28.0 MPa
Steel: fy = 420 MPa, Grade = GRADE420

Beam Geometry:
  Width: 300 mm
  Height: 600 mm
  Effective Depth: 550 mm
  Span Length: 6000 mm

Loads:
  Dead Load: 5.0 kN/m
  Live Load: 8.0 kN/m

=== DESIGN RESULTS ===
Overall Status: PASS
Design Moment: 97.2 kN⋅m
Required Steel Area: 680 mm²
Utilization Ratio: 0.85
✅ Design is adequate!
```

## Core Concepts

### 1. **Standards Architecture**

The library is organized by design standards:

```
structural_standards/
├── aci/                 # ACI standards
│   └── aci318m25/      # ACI 318M-25 specific
├── thai/               # Thai standards  
│   └── ministry_2566/  # Ministry Regulation B.E. 2566
├── base/               # Common base classes
└── utils/              # Utility functions
```

### 2. **Design Workflow**

Every structural design follows this pattern:

1. **Create Materials** → Define concrete and steel properties
2. **Define Geometry** → Specify member dimensions  
3. **Apply Loads** → Set dead, live, wind, seismic loads
4. **Run Design** → Execute design calculations
5. **Check Results** → Verify adequacy and compliance

### 3. **Multi-Language Support**

The library supports both English and Thai:

```python
from structural_standards.utils.i18n import set_language, get_message

# Switch to Thai
set_language('th')
message = get_message('beam_design_complete')
print(message)  # "การออกแบบคานเสร็จสมบูรณ์"

# Switch back to English  
set_language('en')
message = get_message('beam_design_complete')
print(message)  # "Beam design completed successfully"
```

## Working with Different Standards

### ACI 318M-25 (American Standard)

```python
from structural_standards.aci.aci318m25.materials import ACI318M25Concrete, ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.load_combinations import ACI318M25LoadCombinations

# Materials
concrete = ACI318M25Concrete(fc_prime=35.0)
steel = ACI318M25ReinforcementSteel(bar_designation='25M', grade='GRADE420')

# Load combinations
load_combos = ACI318M25LoadCombinations()
ultimate_combos = load_combos.get_ultimate_combinations()
print(f"ACI has {len(ultimate_combos)} ultimate load combinations")
```

### Thai Ministry B.E. 2566 (Thai Standard)

```python
from structural_standards.thai.materials import ThaiConcrete, ThaiSteel
from structural_standards.thai.ministry_2566 import ThaiMinistryLoadCombinations

# Thai materials
concrete = ThaiConcrete(grade='Fc240')  # Thai grade system
steel = ThaiSteel(grade='SD40', bar_designation='DB20')

print(f"Thai Concrete: {concrete.grade} = {concrete.fc_prime} MPa")
print(f"Thai Steel: {steel.grade} = {steel.fy} MPa")

# Thai load combinations
thai_combos = ThaiMinistryLoadCombinations()
ultimate_combos = thai_combos.get_ultimate_combinations()
```

## Common Use Cases

### 1. **Office Building Beam**

```python
# Typical office building beam
geometry = BeamGeometry(width=350, height=700, effective_depth=640, span_length=8000)
loads = BeamLoads(dead_load=8.0, live_load=12.0)  # Office loads
result = beam_designer.design(geometry, loads, BeamType.CONTINUOUS)
```

### 2. **Residential Column**

```python
from structural_standards.aci.aci318m25.members.column_design import (
    ACI318M25ColumnDesign, ColumnGeometry, ColumnLoads, ColumnType
)

column_designer = ACI318M25ColumnDesign(concrete, steel)

geometry = ColumnGeometry(width=400, depth=400, length=3000, cover=40)
loads = ColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=25, moment_x_live=15)

result = column_designer.design(geometry, loads, ColumnType.TIED)
```

### 3. **Two-Way Slab**

```python
from structural_standards.thai.members.slab_design import ThaiSlabDesign

# Thai two-way slab example
slab_designer = ThaiSlabDesign(concrete, steel)
# ... geometry and loads ...
result = slab_designer.design_two_way_slab(geometry, loads)
```

## Validation and Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_aci/
python -m pytest tests/test_thai/

# Run with coverage
python -m pytest tests/ --cov=structural_standards
```

### Validate Against Known Solutions

```python
from structural_standards.data.reference_solutions import verify_solution

# Test against reference solution
calculated_results = {
    "wu": 21.6,
    "Mu": 97.2,
    "As_required": 524,
    "As_final": 600,
    "phi_Mn": 120.4
}

verification = verify_solution("aci_simply_supported_beam_exact", calculated_results)
print(f"Verification: {verification['overall_status']}")
print(f"Passed: {verification['passed_checks']}/{verification['total_checks']}")
```

## Next Steps

Now that you have the basics, explore these tutorials:

1. **[ACI Tutorial](aci_tutorial.md)** - Deep dive into ACI 318M-25 design
2. **[Thai Tutorial](thai_tutorial.md)** - Complete Thai standards workflow  
3. **[Advanced Examples](../examples/advanced_usage/)** - Complex design scenarios

## Getting Help

### Documentation
- **API Reference**: Complete function and class documentation
- **Examples**: Working code examples for common scenarios
- **Reference Solutions**: Hand-calculated verification examples

### Common Issues

**Import Errors**
```python
# If you get import errors, ensure the package is installed
import sys
sys.path.append('/path/to/structural-design-standards')
```

**Material Property Errors**
```python
# Always validate material properties
try:
    concrete = ACI318M25Concrete(fc_prime=28.0)
except ValueError as e:
    print(f"Material error: {e}")
```

**Design Failures**
```python
# Check why design failed
if result.overall_status == "FAIL":
    print(f"Design failed. Check: {result.error_message}")
    print(f"Utilization: {result.utilization_ratio}")
```

### Support Resources

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive API and examples
- **Community**: Join discussions and get help from other users

## Best Practices

1. **Always validate inputs** before running design
2. **Check design status** and utilization ratios  
3. **Use appropriate standards** for your location
4. **Test with known solutions** for verification
5. **Document assumptions** and design criteria

## License

This library is licensed under the MIT License. See LICENSE file for details.

---

**Happy designing! 🏗️**