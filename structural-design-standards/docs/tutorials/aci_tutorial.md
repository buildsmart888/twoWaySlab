# ACI 318M-25 Design Tutorial

This tutorial covers advanced usage of the ACI 318M-25 structural design implementation.

## Table of Contents

1. [Overview](#overview)
2. [Materials](#materials)
3. [Load Combinations](#load-combinations)
4. [Beam Design](#beam-design)
5. [Column Design](#column-design)
6. [Advanced Applications](#advanced-applications)

## Overview

ACI 318M-25 implements strength design method with factored loads and reduced nominal strengths.

**Key Equation**: `U ≤ φRn` where U = factored loads, φ = reduction factor, Rn = nominal strength

## Materials

### Concrete Properties

```python
from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete

# Standard grades
concrete_28 = ACI318M25Concrete(fc_prime=28.0)  # Standard strength
concrete_55 = ACI318M25Concrete(fc_prime=55.0)  # High strength

print(f"Standard Concrete: f'c = {concrete_28.fc_prime} MPa, Ec = {concrete_28.elastic_modulus():.0f} MPa")
print(f"High Strength: f'c = {concrete_55.fc_prime} MPa, Ec = {concrete_55.elastic_modulus():.0f} MPa")
```

### Steel Properties

```python
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel

# Different grades
steel_420 = ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')
steel_520 = ACI318M25ReinforcementSteel(bar_designation='25M', grade='GRADE520')

print(f"Grade 420: fy = {steel_420.fy} MPa, Area = {steel_420.bar_area():.0f} mm²")
print(f"Grade 520: fy = {steel_520.fy} MPa, Area = {steel_520.bar_area():.0f} mm²")
```

## Load Combinations

```python
from structural_standards.aci.aci318m25.load_combinations import ACI318M25LoadCombinations

load_combos = ACI318M25LoadCombinations()
ultimate_combinations = load_combos.get_ultimate_combinations()

print("ACI Load Combinations:")
for combo in ultimate_combinations[:3]:  # Show first 3
    print(f"  {combo.name}: {combo.get_equation()}")

# Calculate factored loads
loads = {'dead': 10.0, 'live': 15.0, 'wind': 8.0}
critical = load_combos.get_critical_combination(loads)
print(f"Critical: {critical['factored_load']:.1f} kN/m")
```

## Beam Design

### Basic Beam Design

```python
from structural_standards.aci.aci318m25.members.beam_design import (
    ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
)

# Setup
concrete = ACI318M25Concrete(fc_prime=28.0)
steel = ACI318M25ReinforcementSteel(bar_designation='25M', grade='GRADE420')
beam_designer = ACI318M25BeamDesign(concrete, steel)

# Geometry and loads
geometry = BeamGeometry(width=400, height=750, effective_depth=690, span_length=8000)
loads = BeamLoads(dead_load=10.0, live_load=15.0, wind_load=3.0)

# Design
result = beam_designer.design(geometry, loads, BeamType.CONTINUOUS)

print("=== BEAM DESIGN ===")
print(f"Status: {result.overall_status}")
print(f"Moment: {result.design_moments['factored_moment']:.1f} kN⋅m")
print(f"Steel: {result.required_reinforcement['required_steel_area']:.0f} mm²")
print(f"Utilization: {result.utilization_ratio:.2f}")
```

### Advanced Beam Analysis

```python
# High-strength concrete beam
hsc = ACI318M25Concrete(fc_prime=55.0)
hsc_beam = ACI318M25BeamDesign(hsc, steel)

large_geometry = BeamGeometry(width=500, height=1000, effective_depth=920, span_length=12000)
heavy_loads = BeamLoads(dead_load=20.0, live_load=25.0)

hsc_result = hsc_beam.design(large_geometry, heavy_loads, BeamType.SIMPLY_SUPPORTED)

print(f"\n=== HIGH-STRENGTH BEAM ===")
print(f"Dimensions: {large_geometry.width} × {large_geometry.height} mm")
print(f"Concrete: f'c = {hsc.fc_prime} MPa")
print(f"Status: {hsc_result.overall_status} ({hsc_result.utilization_ratio:.1%} utilized)")

# Check section control
rho = hsc_result.required_reinforcement['reinforcement_ratio']
rho_bal = 0.85 * 0.85 * hsc.fc_prime / steel.fy * (600 / (600 + steel.fy))
if rho <= 0.75 * rho_bal:
    print("✅ Tension-controlled (φ = 0.90)")
else:
    print("⚠️ Compression-controlled or transition")
```

## Column Design

### Basic Column

```python
from structural_standards.aci.aci318m25.members.column_design import (
    ACI318M25ColumnDesign, ColumnGeometry, ColumnLoads, ColumnType
)

column_designer = ACI318M25ColumnDesign(concrete, steel)

# Square tied column
col_geometry = ColumnGeometry(width=450, depth=450, length=3500, cover=40)
col_loads = ColumnLoads(
    axial_dead=300, axial_live=200,
    moment_x_dead=40, moment_x_live=25,
    moment_y_dead=20, moment_y_live=15
)

col_result = column_designer.design(col_geometry, col_loads, ColumnType.TIED)

print("=== COLUMN DESIGN ===")
print(f"Section: {col_geometry.width} × {col_geometry.depth} mm")
print(f"Status: {col_result.overall_status}")
print(f"Steel: {col_result.required_reinforcement['required_steel_area']:.0f} mm²")
print(f"Ratio: {col_result.required_reinforcement['steel_ratio']:.3f}")
```

### Slender Column with Biaxial Bending

```python
# Slender column
slender_geom = ColumnGeometry(width=350, depth=350, length=5000, cover=40)
biaxial_loads = ColumnLoads(
    axial_dead=200, axial_live=120,
    moment_x_dead=50, moment_x_live=30,
    moment_y_dead=40, moment_y_live=25
)

slender_result = column_designer.design(slender_geom, biaxial_loads, ColumnType.TIED)

print(f"\n=== SLENDER COLUMN ===")
if hasattr(slender_result, 'slenderness_analysis'):
    s = slender_result.slenderness_analysis
    print(f"Slenderness: {s.get('slenderness_ratio_x', 'N/A'):.1f}")
    if s.get('is_slender', False):
        print(f"⚠️ Slender - Magnification: {s.get('magnification_factor_x', 1.0):.2f}")
    else:
        print("✅ Short column")

if hasattr(slender_result, 'interaction_analysis'):
    i = slender_result.interaction_analysis
    print(f"P-M Ratio: {i.get('interaction_ratio', 'N/A'):.2f}")
    print(f"Biaxial Ratio: {i.get('biaxial_ratio', 'N/A'):.2f}")
```

## Advanced Applications

### Slab Design

```python
from structural_standards.aci.aci318m25.members.slab_design import (
    ACI318M25SlabDesign, SlabGeometry, SlabLoads, SlabType
)

slab_designer = ACI318M25SlabDesign(concrete, steel)
slab_geom = SlabGeometry(length_x=6000, length_y=8000, thickness=200, effective_depth=160)
slab_loads = SlabLoads(dead_load=4.5, live_load=3.0, partition_load=1.0)

slab_result = slab_designer.design(slab_geom, slab_loads, SlabType.TWO_WAY)

print(f"=== TWO-WAY SLAB ===")
print(f"Size: {slab_geom.length_x/1000:.1f} × {slab_geom.length_y/1000:.1f} m")
print(f"Aspect Ratio: {slab_geom.length_y/slab_geom.length_x:.2f}")
print(f"Status: {slab_result.overall_status}")
```

### Wall Design

```python
from structural_standards.aci.aci318m25.members.wall_design import (
    ACI318M25WallDesign, WallGeometry, WallLoads, WallType
)

wall_designer = ACI318M25WallDesign(concrete, steel)

# Shear wall
wall_geom = WallGeometry(length=3000, thickness=300, height=12000, reinforcement_type="double")
wall_loads = WallLoads(
    axial_dead=50, axial_live=30,
    shear_wind=200, shear_seismic=150,
    overturning_moment=800
)

wall_result = wall_designer.design(wall_geom, wall_loads, WallType.SHEAR)

print(f"=== SHEAR WALL ===")
print(f"Height: {wall_geom.height/1000:.1f} m")
print(f"Aspect: {wall_geom.height/wall_geom.length:.1f}")
print(f"Status: {wall_result.overall_status}")
```

### Footing Design

```python
from structural_standards.aci.aci318m25.members.footing_design import (
    ACI318M25FootingDesign, FootingGeometry, FootingLoads, FootingType
)

footing_designer = ACI318M25FootingDesign(concrete, steel)
footing_geom = FootingGeometry(
    length=2000, width=2000, thickness=500,
    column_width=400, column_depth=400, cover=75
)
footing_loads = FootingLoads(
    axial_dead=400, axial_live=300,
    moment_x=50, moment_y=30,
    soil_bearing_capacity=200
)

footing_result = footing_designer.design(footing_geom, footing_loads, FootingType.ISOLATED)

print(f"=== ISOLATED FOOTING ===")
print(f"Size: {footing_geom.length/1000:.1f} × {footing_geom.width/1000:.1f} m")
print(f"Status: {footing_result.overall_status}")
```

### Integration Example

```python
# Complete building design workflow
def design_building_frame():
    """Example of integrated structural design"""
    
    # Materials
    concrete = ACI318M25Concrete(fc_prime=35.0)
    steel = ACI318M25ReinforcementSteel(bar_designation='25M', grade='GRADE420')
    
    # Designers
    beam_designer = ACI318M25BeamDesign(concrete, steel)
    column_designer = ACI318M25ColumnDesign(concrete, steel)
    footing_designer = ACI318M25FootingDesign(concrete, steel)
    
    results = {}
    
    # Typical beam
    beam_geom = BeamGeometry(width=350, height=650, effective_depth=590, span_length=7000)
    beam_loads = BeamLoads(dead_load=12.0, live_load=8.0)
    results['beam'] = beam_designer.design(beam_geom, beam_loads, BeamType.CONTINUOUS)
    
    # Typical column
    col_geom = ColumnGeometry(width=400, depth=400, length=3200, cover=40)
    col_loads = ColumnLoads(axial_dead=350, axial_live=250, moment_x_dead=45, moment_x_live=30)
    results['column'] = column_designer.design(col_geom, col_loads, ColumnType.TIED)
    
    # Foundation
    ftg_geom = FootingGeometry(length=1800, width=1800, thickness=450, 
                               column_width=400, column_depth=400, cover=75)
    ftg_loads = FootingLoads(axial_dead=350, axial_live=250, soil_bearing_capacity=200)
    results['footing'] = footing_designer.design(ftg_geom, ftg_loads, FootingType.ISOLATED)
    
    # Summary
    print("=== BUILDING FRAME DESIGN ===")
    for member, result in results.items():
        status = "✅" if result.overall_status == "PASS" else "❌"
        util = getattr(result, 'utilization_ratio', 0)
        print(f"{member.title()}: {status} {result.overall_status} ({util:.1%})")
    
    return results

# Run integrated design
building_results = design_building_frame()
```

## Best Practices

1. **Material Selection**: Use appropriate concrete strength for application
2. **Load Combinations**: Always check critical combination 
3. **Section Control**: Ensure tension-controlled sections for ductility
4. **Slenderness**: Check for moment magnification in columns
5. **Integration**: Verify compatibility between connected members

## Next Steps

- **Thai Tutorial**: Learn Thai Ministry B.E. 2566 standards
- **Advanced Examples**: Complex multi-story building design
- **Validation**: Compare with reference solutions
- **Optimization**: Performance tuning and material optimization

---

**ACI 318M-25 Tutorial Complete! 🏗️**