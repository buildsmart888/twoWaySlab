"""
Simple Direct Test for ACI 318M-25 
==================================

Test individual modules directly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_load_combinations():
    """Test load combinations directly"""
    try:
        from structural_standards.aci.aci318m25.load_combinations import (
            ACI318M25LoadCombinations, LoadType, CombinationType
        )
        
        print("✓ Load combinations import successful")
        
        load_combos = ACI318M25LoadCombinations()
        print("✓ Load combinations object created")
        
        loads = {
            LoadType.DEAD: 10.0,
            LoadType.LIVE: 5.0
        }
        
        critical_combo, max_effect = load_combos.find_critical_combination(
            loads, CombinationType.STRENGTH
        )
        
        print(f"✓ Critical combination: {critical_combo.name}")
        print(f"✓ Maximum effect: {max_effect:.1f}")
        
        return True
    except Exception as e:
        print(f"✗ Load combinations failed: {e}")
        return False

def test_materials():
    """Test materials directly"""
    try:
        from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
        from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
        
        print("✓ Materials import successful")
        
        concrete = ACI318M25Concrete(fc_prime=28.0)
        print(f"✓ Concrete: fc' = {concrete.fc_prime} MPa")
        
        # Check the actual constructor for steel
        steel = ACI318M25ReinforcementSteel(bar_designation="20M")
        print(f"✓ Steel: {steel.bar_designation}")
        
        return True
    except Exception as e:
        print(f"✗ Materials failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_beam_design():
    """Test beam design directly"""
    try:
        from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
        from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
        from structural_standards.aci.aci318m25.members.beam_design import (
            ACI318M25BeamDesign, BeamGeometry
        )
        
        print("✓ Beam design import successful")
        
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(bar_designation="20M")
        
        beam_designer = ACI318M25BeamDesign(concrete, steel)
        print("✓ Beam designer created")
        
        geometry = BeamGeometry(
            width=300.0,
            height=500.0,
            effective_depth=450.0,
            span_length=6000.0
        )
        
        print("✓ Beam geometry created")
        
        return True
    except Exception as e:
        print(f"✗ Beam design failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Direct ACI Module Tests")
    print("=" * 30)
    
    tests = [
        ("Load Combinations", test_load_combinations),
        ("Materials", test_materials),
        ("Beam Design", test_beam_design)
    ]
    
    passed = 0
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 20)
        if test_func():
            passed += 1
            print(f"✓ {name} PASSED")
        else:
            print(f"✗ {name} FAILED")
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")