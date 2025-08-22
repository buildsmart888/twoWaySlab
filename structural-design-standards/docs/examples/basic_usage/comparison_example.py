#!/usr/bin/env python3
"""
ACI vs Thai Standards Comparison Example
========================================

This example demonstrates how to compare design results between 
ACI 318M-25 and Thai Ministry Regulation B.E. 2566 standards for 
the same structural element.

ตัวอย่างการเปรียบเทียบมาตรฐาน ACI กับมาตรฐานไทย
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.load_combinations import ACI318M25LoadCombinations

from structural_standards.thai.materials.concrete import ThaiConcrete
from structural_standards.thai.materials.steel import ThaiSteel
from structural_standards.thai.ministry_2566.load_combinations import ThaiMinistryLoadCombinations
from structural_standards.thai.unit_systems import ThaiUnitConverter


def compare_materials():
    """Compare material properties between ACI and Thai standards"""
    print("🔬 Material Properties Comparison")
    print("การเปรียบเทียบคุณสมบัติวัสดุ")
    print("=" * 60)
    
    # Concrete comparison - similar strength grades
    print("\n1. Concrete Comparison / เปรียบเทียบคอนกรีต:")
    print("-" * 40)
    
    # ACI concrete (28 MPa)
    aci_concrete = ACI318M25Concrete(fc_prime=28.0)
    
    # Thai concrete (Fc280 = 28 MPa)
    thai_concrete = ThaiConcrete(grade='Fc280')
    
    converter = ThaiUnitConverter()
    
    print(f"ACI 318M-25:")
    print(f"  f'c = {aci_concrete.fc_prime} MPa")
    print(f"  Ec = {aci_concrete.elastic_modulus():.0f} MPa")
    print(f"  fr = {aci_concrete.modulus_of_rupture():.2f} MPa")
    print(f"  Unit weight = {aci_concrete.unit_weight} kN/m³")
    
    print(f"\nThai Standards:")
    print(f"  f'c = {thai_concrete.fc_prime} MPa ({thai_concrete.fc_ksc:.0f} ksc)")
    print(f"  Ec = {thai_concrete.elastic_modulus():.0f} MPa")
    print(f"  fr = {thai_concrete.modulus_of_rupture():.2f} MPa")
    print(f"  Unit weight = {thai_concrete.unit_weight} kN/m³")
    
    # Steel comparison - similar strength grades
    print("\n2. Steel Comparison / เปรียบเทียบเหล็ก:")
    print("-" * 40)
    
    # ACI steel (Grade 420)
    aci_steel = ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')
    
    # Thai steel (SD40 ≈ 392 MPa, close to Grade 420)
    thai_steel = ThaiSteel(grade='SD40', bar_designation='DB20')
    
    print(f"ACI 318M-25:")
    print(f"  Grade: {aci_steel.grade}")
    print(f"  fy = {aci_steel.fy} MPa")
    print(f"  Bar: {aci_steel.bar_designation}")
    print(f"  Area = {aci_steel.bar_area():.0f} mm²")
    
    print(f"\nThai Standards:")
    print(f"  Grade: {thai_steel.grade}")
    print(f"  fy = {thai_steel.fy} MPa ({thai_steel.fy_ksc:.0f} ksc)")
    print(f"  Bar: {thai_steel.bar_designation}")
    print(f"  Area = {thai_steel.bar_area():.0f} mm²")
    
    # Material comparison summary
    print("\n3. Material Differences / ความแตกต่างของวัสดุ:")
    print("-" * 40)
    
    concrete_diff = abs(aci_concrete.elastic_modulus() - thai_concrete.elastic_modulus())
    steel_diff = abs(aci_steel.fy - thai_steel.fy)
    
    print(f"Concrete modulus difference: {concrete_diff:.0f} MPa ({concrete_diff/aci_concrete.elastic_modulus()*100:.1f}%)")
    print(f"Steel strength difference: {steel_diff:.0f} MPa ({steel_diff/aci_steel.fy*100:.1f}%)")
    
    return {
        'aci_concrete': aci_concrete,
        'thai_concrete': thai_concrete,
        'aci_steel': aci_steel,
        'thai_steel': thai_steel
    }


def compare_load_combinations():
    """Compare load combinations between ACI and Thai standards"""
    print("\n\n⚖️ Load Combinations Comparison")
    print("การเปรียบเทียบชุดน้ำหนักบรรทุก")
    print("=" * 60)
    
    # Sample loads
    dead_load = 5.0  # kN/m²
    live_load = 3.0  # kN/m²
    wind_load = 1.5  # kN/m²
    
    print(f"Sample loads:")
    print(f"  Dead load = {dead_load} kN/m²")
    print(f"  Live load = {live_load} kN/m²")
    print(f"  Wind load = {wind_load} kN/m²")
    
    # ACI Load Combinations
    print("\n1. ACI 318M-25 Load Combinations:")
    print("-" * 40)
    
    aci_loads = ACI318M25LoadCombinations()
    aci_combinations = aci_loads.get_ultimate_combinations()[:4]  # First 4 combinations
    
    aci_results = []
    for combo in aci_combinations:
        factors = combo.factors
        
        # Calculate factored load manually for demonstration
        if 'dead' in factors and 'live' in factors:
            factored = factors['dead'] * dead_load + factors['live'] * live_load
            if 'wind' in factors:
                factored += factors['wind'] * wind_load
        elif 'dead' in factors:
            factored = factors['dead'] * dead_load
        else:
            factored = 0
        
        aci_results.append(factored)
        print(f"  {combo.name}: {combo.get_equation()} = {factored:.1f} kN/m²")
    
    # Thai Load Combinations
    print("\n2. Thai Ministry B.E. 2566 Load Combinations:")
    print("-" * 40)
    
    thai_loads = ThaiMinistryLoadCombinations()
    thai_combinations = thai_loads.get_ultimate_combinations()[:4]  # First 4 combinations
    
    thai_results = []
    for combo in thai_combinations:
        factors = combo.factors
        
        # Calculate factored load manually for demonstration
        if 'DL' in factors and 'LL' in factors:
            factored = factors['DL'] * dead_load + factors['LL'] * live_load
            if 'W' in factors:
                factored += abs(factors['W']) * wind_load  # Take absolute value
        elif 'DL' in factors:
            factored = factors['DL'] * dead_load
        else:
            factored = 0
        
        thai_results.append(factored)
        print(f"  {combo.name}: {combo.get_equation()} = {factored:.1f} kN/m²")
    
    # Comparison of critical combinations
    print("\n3. Critical Combination Comparison:")
    print("-" * 40)
    
    aci_critical = max(aci_results)
    thai_critical = max(thai_results)
    
    print(f"ACI 318M-25 maximum: {aci_critical:.1f} kN/m²")
    print(f"Thai B.E. 2566 maximum: {thai_critical:.1f} kN/m²")
    
    difference = abs(aci_critical - thai_critical)
    percent_diff = difference / max(aci_critical, thai_critical) * 100
    
    print(f"Difference: {difference:.1f} kN/m² ({percent_diff:.1f}%)")
    
    if aci_critical > thai_critical:
        print("🔍 ACI combinations are more conservative for this load case")
    elif thai_critical > aci_critical:
        print("🔍 Thai combinations are more conservative for this load case")
    else:
        print("🔍 Both standards give similar results")
    
    return {
        'aci_critical': aci_critical,
        'thai_critical': thai_critical,
        'difference_percent': percent_diff
    }


def compare_design_approaches():
    """Compare design approaches and philosophies"""
    print("\n\n🏗️ Design Approach Comparison")
    print("การเปรียบเทียบแนวทางการออกแบบ")
    print("=" * 60)
    
    print("1. Design Philosophy / ปรัชญาการออกแบบ:")
    print("-" * 40)
    
    print("ACI 318M-25:")
    print("  ✓ Strength Design Method (Ultimate Strength)")
    print("  ✓ Load and Resistance Factor Design (LRFD)")
    print("  ✓ Strength reduction factors (φ factors)")
    print("  ✓ International standard, widely adopted")
    
    print("\nThai Ministry Regulation B.E. 2566:")
    print("  ✓ Follows international practices")
    print("  ✓ Load and Resistance Factor Design (LRFD)")
    print("  ✓ Strength reduction factors (φ factors)")
    print("  ✓ Adapted for Thai construction practices")
    print("  ✓ Considers local materials and conditions")
    
    print("\n2. Key Differences / ความแตกต่างหลัก:")
    print("-" * 40)
    
    print("Material Specifications:")
    print("  • ACI: ASTM standards (Grade 420, Grade 520)")
    print("  • Thai: TIS standards (SD40, SD50, SR24)")
    
    print("\nUnit Systems:")
    print("  • ACI: Primarily SI units (MPa, mm)")
    print("  • Thai: Mixed SI and traditional (ksc, kgf)")
    
    print("\nLoad Classifications:")
    print("  • ACI: D, L, W, E notation")
    print("  • Thai: DL, LL, W, E notation (similar)")
    
    print("\nEnvironmental Factors:")
    print("  • ACI: General climate considerations")
    print("  • Thai: Tropical climate, monsoon conditions")
    
    print("\n3. Practical Implications / ผลกระทบในทางปฏิบัติ:")
    print("-" * 40)
    
    print("For International Projects:")
    print("  ✓ ACI 318M-25 provides global consistency")
    print("  ✓ Widely recognized by international consultants")
    print("  ✓ Compatible with other international codes")
    
    print("\nFor Thai Projects:")
    print("  ✓ Thai standards ensure regulatory compliance")
    print("  ✓ Optimized for local materials and practices")
    print("  ✓ Required for building permits in Thailand")
    print("  ✓ Familiarity with local construction industry")


def design_comparison_example():
    """Practical design comparison example"""
    print("\n\n📊 Practical Design Comparison")
    print("ตัวอย่างการเปรียบเทียบการออกแบบจริง")
    print("=" * 60)
    
    # Common design scenario
    print("Design Scenario: Office Building Column")
    print("สถานการณ์: เสาอาคารสำนักงาน")
    print("-" * 40)
    
    # Loads
    axial_dead = 200  # kN
    axial_live = 150  # kN
    moment = 25       # kN⋅m
    
    print(f"Applied loads:")
    print(f"  Axial dead load = {axial_dead} kN")
    print(f"  Axial live load = {axial_live} kN")
    print(f"  Applied moment = {moment} kN⋅m")
    
    # ACI factored loads
    aci_factored_axial = 1.4 * axial_dead + 1.7 * axial_live
    aci_factored_moment = 1.4 * moment  # Assuming moment from dead load
    
    # Thai factored loads (using combination 1001)
    thai_factored_axial = 1.4 * axial_dead + 1.7 * axial_live
    thai_factored_moment = 1.4 * moment
    
    print(f"\nFactored loads:")
    print(f"  ACI 318M-25:")
    print(f"    Pu = {aci_factored_axial:.0f} kN")
    print(f"    Mu = {aci_factored_moment:.0f} kN⋅m")
    
    print(f"  Thai B.E. 2566:")
    print(f"    Pu = {thai_factored_axial:.0f} kN")
    print(f"    Mu = {thai_factored_moment:.0f} kN⋅m")
    
    # Column capacity estimation (simplified)
    column_area = 400 * 400  # mm²
    
    # ACI approach
    aci_materials = compare_materials()
    aci_fc = aci_materials['aci_concrete'].fc_prime
    aci_capacity_estimate = 0.8 * column_area * aci_fc / 1000  # kN (very simplified)
    
    # Thai approach
    thai_fc = aci_materials['thai_concrete'].fc_prime
    thai_capacity_estimate = 0.8 * column_area * thai_fc / 1000  # kN (very simplified)
    
    print(f"\nColumn capacity estimates (400×400 mm):")
    print(f"  ACI approach: ~{aci_capacity_estimate:.0f} kN")
    print(f"  Thai approach: ~{thai_capacity_estimate:.0f} kN")
    
    # Utilization ratios
    aci_utilization = aci_factored_axial / aci_capacity_estimate
    thai_utilization = thai_factored_axial / thai_capacity_estimate
    
    print(f"\nUtilization ratios:")
    print(f"  ACI: {aci_utilization:.2f}")
    print(f"  Thai: {thai_utilization:.2f}")
    
    return {
        'aci_utilization': aci_utilization,
        'thai_utilization': thai_utilization,
        'load_difference': abs(aci_factored_axial - thai_factored_axial)
    }


def main():
    """Main comparison function"""
    print("🔍 Comprehensive Standards Comparison")
    print("การเปรียบเทียบมาตรฐานอย่างครอบคลุม")
    print("=" * 80)
    
    # Run all comparisons
    materials = compare_materials()
    loads = compare_load_combinations()
    compare_design_approaches()
    design = design_comparison_example()
    
    # Final summary
    print("\n\n📋 Summary / สรุป")
    print("=" * 60)
    
    print("Material Compatibility:")
    if materials['aci_steel'].fy - materials['thai_steel'].fy < 50:
        print("  ✅ Steel grades are closely compatible")
    else:
        print("  ⚠️  Steel grades show significant difference")
    
    print("Load Combination Similarity:")
    if loads['difference_percent'] < 10:
        print("  ✅ Load combinations give similar results")
    else:
        print("  ⚠️  Load combinations show significant difference")
    
    print("Design Approach:")
    print("  ✅ Both use LRFD methodology")
    print("  ✅ Both use strength reduction factors")
    print("  ✅ Both suitable for modern design")
    
    print("\nRecommendations / คำแนะนำ:")
    print("  • Use ACI 318M-25 for international projects")
    print("  • Use Thai standards for local Thai projects")
    print("  • Both standards ensure safe, economical design")
    print("  • Consider project requirements and local regulations")
    
    return {
        'materials_compatible': True,
        'loads_similar': loads['difference_percent'] < 10,
        'both_suitable': True
    }


if __name__ == "__main__":
    # Run the comparison
    result = main()
    
    print("\n" + "=" * 80)
    print("Standards Comparison Completed!")
    print("การเปรียบเทียบมาตรฐานเสร็จสมบูรณ์!")
    print("=" * 80)
    
    if result['materials_compatible'] and result['loads_similar']:
        print("✅ Both standards are highly compatible for most applications")
        print("✅ ทั้งสองมาตรฐานเข้ากันได้ดีสำหรับการใช้งานส่วนใหญ่")
    
    print("\nBoth ACI 318M-25 and Thai Ministry Regulation B.E. 2566")
    print("provide reliable, safe structural design methods.")
    print("ทั้ง ACI 318M-25 และกฎกระทรวง พ.ศ. 2566")
    print("ให้วิธีการออกแบบโครงสร้างที่เชื่อถือได้และปลอดภัย")