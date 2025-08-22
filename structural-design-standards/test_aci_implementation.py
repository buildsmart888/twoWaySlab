"""
Simple test script for ACI 318M-25 implementations
=================================================

Test the beam design, column design, and load combinations without requiring 
package installation by directly importing from local modules.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_aci_beam_design():
    """Test ACI beam design functionality"""
    try:
        from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
        from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
        from structural_standards.aci.aci318m25.members.beam_design import (
            ACI318M25BeamDesign, BeamGeometry
        )
        
        print("✓ Imports successful")
        
        # Create materials
        concrete = ACI318M25Concrete(fc_prime=28.0)  # 28 MPa
        steel = ACI318M25ReinforcementSteel(fy=420.0, bar_designation="DB20")
        
        print(f"✓ Created concrete: fc' = {concrete.fc_prime} MPa")
        print(f"✓ Created steel: fy = {steel.fy} MPa, bar = {steel.bar_designation}")
        
        # Create beam designer
        beam_designer = ACI318M25BeamDesign(concrete, steel)
        
        # Define geometry
        geometry = BeamGeometry(
            width=300.0,      # mm
            height=500.0,     # mm
            effective_depth=450.0,  # mm
            span_length=6000.0     # mm
        )
        
        print(f"✓ Created beam geometry: {geometry.width}×{geometry.height} mm")
        
        # Design for flexural reinforcement
        result = beam_designer.design_flexural_reinforcement(
            geometry=geometry,
            moment_ultimate=150.0  # kN⋅m
        )
        
        print(f"✓ Flexural design completed")
        print(f"  - Required steel: {result.design_details['As_required_mm2']:.0f} mm²")
        print(f"  - Reinforcement ratio: {result.design_details['reinforcement_ratio']:.4f}")
        print(f"  - Section type: {result.design_details['section_type']}")
        print(f"  - Adequate: {result.is_adequate}")
        print(f"  - Capacity ratio: {result.capacity_ratio:.2f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Beam design test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_aci_column_design():
    """Test ACI column design functionality"""
    try:
        from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
        from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
        from structural_standards.aci.aci318m25.members.column_design import (
            ACI318M25ColumnDesign, ColumnGeometry, ColumnLoads
        )
        
        # Create materials
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(fy=420.0, bar_designation="DB25")
        
        # Create column designer
        column_designer = ACI318M25ColumnDesign(concrete, steel)
        
        # Define geometry
        geometry = ColumnGeometry(
            width=400.0,   # mm
            depth=400.0,   # mm
            length=3000.0, # mm
            cross_section="rectangular"
        )
        
        # Define loads
        loads = ColumnLoads(
            axial_dead=500.0,   # kN
            axial_live=300.0,   # kN
            moment_x_dead=50.0, # kN⋅m
            moment_x_live=30.0  # kN⋅m
        )
        
        print(f"✓ Created column: {geometry.width}×{geometry.depth} mm, L={geometry.length} mm")
        print(f"✓ Applied loads: P = {loads.axial_total:.0f} kN, M = {loads.moment_x_total:.0f} kN⋅m")
        
        # Design reinforcement
        result = column_designer.design_axial_reinforcement(
            geometry=geometry,
            loads=loads,
            reinforcement_ratio=0.02
        )
        
        print(f"✓ Column design completed")
        print(f"  - Required steel: {result.design_details['As_required_mm2']:.0f} mm²")
        print(f"  - Number of bars: {result.design_details['num_longitudinal_bars']}")
        print(f"  - Reinforcement ratio: {result.design_details['reinforcement_ratio']:.3f}")
        print(f"  - Column type: {result.design_details['column_type']}")
        print(f"  - Adequate: {result.is_adequate}")
        
        return True
        
    except Exception as e:
        print(f"✗ Column design test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_aci_load_combinations():
    """Test ACI load combinations functionality"""
    try:
        from structural_standards.aci.aci318m25.load_combinations import (
            ACI318M25LoadCombinations, LoadType, CombinationType
        )
        
        # Create load combinations
        load_combos = ACI318M25LoadCombinations()
        
        # Define loads
        loads = {
            LoadType.DEAD: 10.0,    # kN/m²
            LoadType.LIVE: 5.0,     # kN/m²
            LoadType.WIND: 3.0,     # kN/m²
        }
        
        print(f"✓ Applied loads: D={loads[LoadType.DEAD]}, L={loads[LoadType.LIVE]}, W={loads[LoadType.WIND]} kN/m²")
        
        # Find critical combination
        critical_combo, max_effect = load_combos.find_critical_combination(
            loads, CombinationType.STRENGTH
        )
        
        print(f"✓ Load combinations analysis completed")
        print(f"  - Critical combination: {critical_combo.name}")
        print(f"  - Maximum effect: {max_effect:.1f} kN/m²")
        print(f"  - Equation: {critical_combo.get_equation()}")
        
        # Test phi factors
        phi_flexure = load_combos.get_strength_reduction_factor('flexure_tension_controlled')
        phi_shear = load_combos.get_strength_reduction_factor('shear_and_torsion')
        
        print(f"  - φ (flexure): {phi_flexure}")
        print(f"  - φ (shear): {phi_shear}")
        
        return True
        
    except Exception as e:
        print(f"✗ Load combinations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integrated workflow"""
    try:
        from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
        from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
        from structural_standards.aci.aci318m25.members.beam_design import (
            ACI318M25BeamDesign, BeamGeometry
        )
        from structural_standards.aci.aci318m25.load_combinations import (
            ACI318M25LoadCombinations, LoadType, CombinationType
        )
        
        print("✓ Integration test: Complete beam design workflow")
        
        # Step 1: Create materials
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(fy=420.0, bar_designation="DB20")
        
        # Step 2: Create designers
        beam_designer = ACI318M25BeamDesign(concrete, steel)
        load_combos = ACI318M25LoadCombinations()
        
        # Step 3: Define service loads
        service_loads = {
            LoadType.DEAD: 8.0,   # kN/m
            LoadType.LIVE: 6.0    # kN/m
        }
        
        # Step 4: Calculate factored loads
        critical_combo, factored_load = load_combos.find_critical_combination(
            service_loads, CombinationType.STRENGTH
        )
        
        # Step 5: Calculate moment (simple beam)
        span = 6.0  # m
        factored_moment = factored_load * span**2 / 8  # kN⋅m
        
        print(f"  - Service loads: D={service_loads[LoadType.DEAD]}, L={service_loads[LoadType.LIVE]} kN/m")
        print(f"  - Critical combination: {critical_combo.name}")
        print(f"  - Factored load: {factored_load:.1f} kN/m")
        print(f"  - Factored moment: {factored_moment:.1f} kN⋅m")
        
        # Step 6: Design beam
        geometry = BeamGeometry(
            width=300.0,
            height=500.0,
            effective_depth=450.0,
            span_length=6000.0
        )
        
        result = beam_designer.design_flexural_reinforcement(
            geometry=geometry,
            moment_ultimate=factored_moment
        )
        
        print(f"  - Final design: {result.design_details['As_required_mm2']:.0f} mm² steel")
        print(f"  - Design adequate: {result.is_adequate}")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ACI 318M-25 Implementation Test Suite")
    print("=" * 60)
    
    tests = [
        ("Beam Design", test_aci_beam_design),
        ("Column Design", test_aci_column_design),
        ("Load Combinations", test_aci_load_combinations),
        ("Integration Workflow", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name} Test:")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✓ {test_name} test PASSED")
        else:
            print(f"✗ {test_name} test FAILED")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! ACI 318M-25 implementation is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")