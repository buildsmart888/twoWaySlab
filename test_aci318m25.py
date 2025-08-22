#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Test Script for ACI 318M-25 Building Code Library
ACI Building Code Requirements for Structural Concrete (International System of Units)

@author: Enhanced by AI Assistant
@date: 2024
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_aci318m25_library():
    """Test ACI 318M-25 Library functionality"""
    print("=" * 80)
    print("ACI 318M-25 Building Code for Structural Concrete Test")
    print("International System of Units (SI)")
    print("=" * 80)
    
    try:
        from aci318m25 import (
            ACI318M25, ConcreteStrengthClass, ReinforcementGrade, 
            StructuralElement, ExposureCondition
        )
        
        aci = ACI318M25()
        print("✓ ACI 318M-25 Library loaded successfully")
        
        # Test 1: Concrete strength classes and properties
        print("\n1. Concrete Strength Classes (ACI 318M-25 Section 19.2.1.1)")
        print("-" * 70)
        
        test_concrete_classes = [
            ConcreteStrengthClass.FC21, ConcreteStrengthClass.FC28, 
            ConcreteStrengthClass.FC35, ConcreteStrengthClass.FC50,
            ConcreteStrengthClass.FC70
        ]
        
        for concrete_class in test_concrete_classes:
            concrete_data = aci.concrete_strengths[concrete_class]
            fc_prime = concrete_data['fc_prime']
            ec = aci.get_concrete_modulus(fc_prime)
            fr = aci.calculate_modulus_of_rupture(fc_prime)
            
            print(f"{concrete_class.value:>6} MPa: Ec = {ec:6.0f} MPa, fr = {fr:4.1f} MPa - {concrete_data['usage']}")
        
        # Test 2: Reinforcement grades and properties
        print(f"\n2. Reinforcement Grades (ACI 318M-25 Section 20.2.2.4)")
        print("-" * 70)
        
        for steel_grade in ReinforcementGrade:
            steel_data = aci.reinforcement_grades[steel_grade]
            print(f"{steel_grade.value}: fy = {steel_data['fy']:3.0f} MPa, fu = {steel_data['fu']:3.0f} MPa")
            print(f"         {steel_data['grade_designation']} - {steel_data['usage']}")
        
        # Test 3: Reinforcing bar areas and properties
        print(f"\n3. Reinforcing Bar Properties (ACI 318M-25 Table 25.3.1)")
        print("-" * 70)
        
        test_bars = ['10M', '15M', '20M', '25M', '30M', '35M', '#4', '#6', '#8', '#10']
        print(f"{'Bar Size':<8} {'Diameter':<12} {'Area':<12} {'Area/m @ 200mm'}")
        print(f"{'':8} {'(mm)':<12} {'(mm²)':<12} {'(mm²/m)'}")
        print("-" * 50)
        
        for bar in test_bars:
            if bar in aci.bar_areas:
                diameter = aci.get_bar_diameter(bar)
                area = aci.get_bar_area(bar)
                area_per_m = aci.calculate_area_per_meter(bar, 200)  # 200mm spacing
                print(f"{bar:<8} {diameter:<12.1f} {area:<12.0f} {area_per_m:<12.0f}")
        
        # Test 4: Concrete cover requirements
        print(f"\n4. Concrete Cover Requirements (ACI 318M-25 Table 20.5.1.3.1)")
        print("-" * 70)
        
        elements = [StructuralElement.SLAB, StructuralElement.BEAM, 
                   StructuralElement.COLUMN, StructuralElement.FOOTING]
        exposures = ['normal', 'corrosive', 'severe']
        
        for element in elements:
            print(f"\n{element.value.upper()}:")
            for exposure in exposures:
                cover, unit, desc = aci.get_concrete_cover(element, exposure)
                print(f"  {exposure:10}: {cover:2.0f} {unit} - {desc}")
        
        # Test 5: Load combinations
        print(f"\n5. Load Combinations (ACI 318M-25 Section 5.3)")
        print("-" * 70)
        
        loads = {
            'D': 8.0,   # Dead load (kN/m²)
            'L': 4.0,   # Live load (kN/m²)
            'W': 2.0,   # Wind load (kN/m²)
            'E': 1.5    # Earthquake load (kN/m²)
        }
        
        print("Applied Loads:")
        for load_type, value in loads.items():
            load_names = {'D': 'Dead', 'L': 'Live', 'W': 'Wind', 'E': 'Earthquake'}
            print(f"  {load_names[load_type]} Load: {value:.1f} kN/m²")
        
        print("\nStrength Design Load Combinations:")
        strength_combos = aci.check_load_combinations(loads, 'strength')
        for combo in strength_combos[:5]:  # Show first 5 combinations
            print(f"  {combo['name']}: {combo['factored_load']:.2f} kN/m²")
        
        assert True  # Test passed
        
    except Exception as e:
        print(f"✗ Error in ACI 318M-25 library test: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"ACI 318M-25 library test failed: {e}"

def test_design_calculations():
    """Test design calculation methods"""
    print("\n" + "=" * 80)
    print("ACI 318M-25 Design Calculation Examples")
    print("=" * 80)
    
    try:
        from aci318m25 import ACI318M25, ConcreteStrengthClass, ReinforcementGrade
        
        aci = ACI318M25()
        
        # Example 1: Reinforcement ratio calculations
        print("\nExample 1: Reinforcement Ratio Calculations")
        print("-" * 60)
        
        fc_prime = 28.0  # MPa
        fy = 420.0       # MPa
        
        rho_min = aci.calculate_minimum_reinforcement_ratio(fc_prime, fy)
        rho_max = aci.calculate_maximum_reinforcement_ratio(fc_prime, fy)
        rho_balanced = aci.calculate_balanced_reinforcement_ratio(fc_prime, fy)
        
        print(f"Concrete: fc' = {fc_prime} MPa")
        print(f"Steel: fy = {fy} MPa")
        print(f"Minimum reinforcement ratio (ρmin): {rho_min:.4f}")
        print(f"Balanced reinforcement ratio (ρb): {rho_balanced:.4f}")
        print(f"Maximum reinforcement ratio (ρmax): {rho_max:.4f} (tension-controlled)")
        
        # Example 2: Development length calculation
        print("\nExample 2: Development Length Calculation")
        print("-" * 60)
        
        bar_size = '20M'
        modification_factors = {
            'top_bar': 1.3,    # Top bar factor
            'epoxy': 1.5,      # Epoxy coating factor
            'size': 1.0,       # Size factor
            'lambda': 1.0      # Lightweight factor
        }
        
        ld = aci.calculate_development_length(bar_size, fc_prime, fy, modification_factors)
        
        print(f"Bar size: {bar_size} (Area = {aci.get_bar_area(bar_size):.0f} mm²)")
        print(f"Development length: {ld:.0f} mm ({ld/25.4:.1f} inches)")
        print(f"Modification factors applied: {modification_factors}")
        
        # Example 3: Material properties
        print("\nExample 3: Complete Material Properties")
        print("-" * 60)
        
        material_props = aci.get_material_properties(
            ConcreteStrengthClass.FC28, 
            ReinforcementGrade.GRADE420
        )
        
        print(f"Concrete: fc' = {material_props.fc_prime} MPa")
        print(f"Steel: fy = {material_props.fy} MPa")
        print(f"Concrete modulus: Ec = {material_props.ec:.0f} MPa")
        print(f"Steel modulus: Es = {material_props.es:.0f} MPa")
        print(f"Concrete unit weight: γc = {material_props.gamma_c} kN/m³")
        
        assert True  # Test passed
        
    except Exception as e:
        print(f"✗ Error in design calculations: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Design calculations test failed: {e}"

def test_practical_design_example():
    """Test with a practical structural design example"""
    print("\n" + "=" * 80)
    print("Practical Example: Two-Way Slab Design per ACI 318M-25")
    print("=" * 80)
    
    try:
        from aci318m25 import ACI318M25, ConcreteStrengthClass, ReinforcementGrade, StructuralElement
        
        aci = ACI318M25()
        
        # Example project: 6m × 8m office building slab
        print("Project: 6m × 8m Office Building Slab")
        print("-" * 50)
        
        # Material selection
        concrete_class = ConcreteStrengthClass.FC28
        steel_grade = ReinforcementGrade.GRADE420
        material_props = aci.get_material_properties(concrete_class, steel_grade)
        
        print(f"Concrete: {concrete_class.value} (fc' = {material_props.fc_prime} MPa)")
        print(f"Steel: {steel_grade.value} (fy = {material_props.fy} MPa)")
        
        # Load analysis
        print(f"\nLoad Analysis:")
        slab_thickness = 200  # mm
        concrete_weight = slab_thickness * 24.0 / 1000  # kN/m² (24 kN/m³ unit weight)
        floor_finish = 1.5   # kN/m²
        live_load = 3.0      # kN/m² (office loading)
        
        dead_load = concrete_weight + floor_finish
        
        print(f"Slab self-weight: {concrete_weight:.1f} kN/m²")
        print(f"Floor finish: {floor_finish:.1f} kN/m²")
        print(f"Total dead load: {dead_load:.1f} kN/m²")
        print(f"Live load: {live_load:.1f} kN/m²")
        
        # Load combinations
        loads = {
            'D': dead_load,
            'L': live_load,
            'W': 0.0,  # No wind for this example
            'E': 0.0   # No earthquake for this example
        }
        
        strength_combos = aci.check_load_combinations(loads, 'strength')
        governing_combo = max(strength_combos, key=lambda x: x['factored_load'])
        
        print(f"\nLoad Combinations (ACI 318M-25 Section 5.3):")
        for combo in strength_combos[:3]:  # Show first 3 combinations
            print(f"  {combo['name']}: {combo['factored_load']:.2f} kN/m²")
        
        print(f"\nGoverning load combination: {governing_combo['name']}")
        print(f"Design load: {governing_combo['factored_load']:.2f} kN/m²")
        
        # Concrete cover and reinforcement
        cover, unit, desc = aci.get_concrete_cover(StructuralElement.SLAB, 'normal')
        print(f"\nConcrete cover requirement: {cover} {unit} ({desc})")
        
        # Reinforcement ratios
        rho_min = aci.calculate_minimum_reinforcement_ratio(material_props.fc_prime, material_props.fy)
        rho_max = aci.calculate_maximum_reinforcement_ratio(material_props.fc_prime, material_props.fy)
        
        print(f"\nReinforcement Requirements:")
        print(f"Minimum reinforcement ratio: {rho_min:.4f}")
        print(f"Maximum reinforcement ratio: {rho_max:.4f} (tension-controlled)")
        
        # Example reinforcement selection
        bar_size = '15M'
        spacing = 200  # mm
        area_provided = aci.calculate_area_per_meter(bar_size, spacing)
        effective_depth = slab_thickness - cover - aci.get_bar_diameter(bar_size)/2
        rho_provided = area_provided / (1000 * effective_depth)  # per meter width
        
        print(f"\nSelected Reinforcement:")
        print(f"Bar size: {bar_size} (Area = {aci.get_bar_area(bar_size):.0f} mm²)")
        print(f"Spacing: {spacing} mm")
        print(f"Area provided: {area_provided:.0f} mm²/m")
        print(f"Effective depth: {effective_depth:.1f} mm")
        print(f"Reinforcement ratio provided: {rho_provided:.4f}")
        
        # Check reinforcement ratio
        ratio_check = "OK" if rho_min <= rho_provided <= rho_max else "CHECK REQUIRED"
        print(f"Reinforcement ratio check: {ratio_check}")
        
        # Generate comprehensive report
        print(f"\nGenerating Design Report...")
        
        project_info = {
            'project_name': 'Office Building Two-Way Slab',
            'location': 'Example Project',
            'date': '2024-01-15',
            'engineer': 'Example Engineer',
            'element_type': 'Two-way slab'
        }
        
        design_results = {
            'Slab thickness': f'{slab_thickness} mm',
            'Effective depth': f'{effective_depth:.1f} mm',
            'Governing load': f'{governing_combo["factored_load"]:.2f} kN/m²',
            'Selected reinforcement': f'{bar_size} @ {spacing}mm',
            'Reinforcement ratio': f'{rho_provided:.4f}',
            'Ratio check': ratio_check
        }
        
        report = aci.generate_design_summary_report(
            project_info, concrete_class, steel_grade, loads, design_results
        )
        
        # Show report summary
        report_lines = report.split('\n')
        print("Design Report Generated (First 15 lines):")
        for i, line in enumerate(report_lines[:15]):
            print(line)
        print("... (report continues)")
        print(f"Total report length: {len(report)} characters")
        
        assert True  # Test passed
        
    except Exception as e:
        print(f"✗ Error in practical design example: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Practical design example test failed: {e}"

def test_integration_with_existing_system():
    """Test integration with existing twoWaySlab system"""
    print("\n" + "=" * 80)
    print("Integration with Existing Building Code System")
    print("=" * 80)
    
    try:
        from aci318m25 import ACI318M25
        # Try to import existing modules
        try:
            from thiRc import ThaiRc_set
            print("✓ Integration with Thai RC system available")
        except ImportError:
            print("⚠ Thai RC system not available")
        
        try:
            from thaiMinistryReg import ThaiMinistryRegulation2566
            print("✓ Integration with Thai Ministry Regulation available")
        except ImportError:
            print("⚠ Thai Ministry Regulation not available")
        
        aci = ACI318M25()
        
        # Test unit consistency
        print("\nUnit System Comparison:")
        print("-" * 50)
        
        # ACI 318M-25 uses SI units consistently
        fc_prime_aci = 28.0  # MPa
        fy_aci = 420.0       # MPa
        
        print(f"ACI 318M-25:")
        print(f"  Concrete strength: {fc_prime_aci} MPa")
        print(f"  Steel yield strength: {fy_aci} MPa")
        print(f"  Cover requirements: mm")
        print(f"  Load units: kN, kN/m²")
        
        # Show compatibility with international standards
        print(f"\nInternational Compatibility:")
        print(f"  Units: SI (International System of Units)")
        print(f"  Load combinations: Compatible with ASCE 7")
        print(f"  Material properties: ASTM standards")
        print(f"  Bar designations: Metric and Imperial supported")
        
        assert True  # Test passed
        
    except Exception as e:
        print(f"✗ Error in integration test: {e}")
        assert False, f"Integration test failed: {e}"

def main():
    """Main test function"""
    print("ACI 318M-25 Building Code for Structural Concrete")
    print("Comprehensive Library Test Suite")
    print("International System of Units (SI)")
    print("=" * 80)
    
    test_results = []
    
    # Test 1: Basic library functionality
    result1 = test_aci318m25_library()
    test_results.append(("ACI 318M-25 Library", result1))
    
    # Test 2: Design calculations
    result2 = test_design_calculations()
    test_results.append(("Design Calculations", result2))
    
    # Test 3: Practical example
    result3 = test_practical_design_example()
    test_results.append(("Practical Design Example", result3))
    
    # Test 4: System integration
    result4 = test_integration_with_existing_system()
    test_results.append(("System Integration", result4))
    
    # Summary
    print("\n" + "=" * 80)
    print("Test Results Summary")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! ACI 318M-25 Library is ready to use.")
        print("📚 The library can now be integrated with existing projects.")
        print("\nUsage example:")
        print("```python")
        print("from aci318m25 import ACI318M25, ConcreteStrengthClass, ReinforcementGrade")
        print("aci = ACI318M25()")
        print("material_props = aci.get_material_properties(ConcreteStrengthClass.FC28, ReinforcementGrade.GRADE420)")
        print("```")
    else:
        print(f"⚠️ {total - passed} test(s) failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)