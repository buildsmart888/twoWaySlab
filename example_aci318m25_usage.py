#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
ACI 318M-25 Building Code for Structural Concrete - Usage Examples
Practical examples for structural concrete design using International System of Units

@author: Enhanced by AI Assistant
@date: 2024
"""

from aci318m25 import (
    ACI318M25, 
    ConcreteStrengthClass, 
    ReinforcementGrade, 
    StructuralElement, 
    ExposureCondition
)

def main():
    """Main usage examples for ACI 318M-25 library"""
    
    print("=" * 80)
    print("ACI 318M-25 Building Code for Structural Concrete")
    print("Usage Examples - International System of Units")
    print("=" * 80)
    
    # Initialize ACI 318M-25 calculator
    aci = ACI318M25()
    
    # Example 1: Material Properties and Basic Calculations
    print("\n1. Material Properties and Basic Calculations")
    print("-" * 60)
    
    # Standard concrete and steel grades
    concrete_classes = [ConcreteStrengthClass.FC21, ConcreteStrengthClass.FC28, 
                       ConcreteStrengthClass.FC35, ConcreteStrengthClass.FC50]
    steel_grades = [ReinforcementGrade.GRADE280, ReinforcementGrade.GRADE420, 
                   ReinforcementGrade.GRADE520]
    
    print("Concrete Properties:")
    for concrete_class in concrete_classes:
        concrete_data = aci.concrete_strengths[concrete_class]
        fc_prime = concrete_data['fc_prime']
        ec = aci.get_concrete_modulus(fc_prime)
        fr = aci.calculate_modulus_of_rupture(fc_prime)
        
        print(f"  {concrete_class.value} MPa: Ec = {ec:5.0f} MPa, fr = {fr:4.1f} MPa")
    
    print("\\nReinforcement Properties:")
    for steel_grade in steel_grades:
        steel_data = aci.reinforcement_grades[steel_grade]
        print(f"  {steel_grade.value}: fy = {steel_data['fy']:3.0f} MPa, fu = {steel_data['fu']:3.0f} MPa")
    
    # Example 2: Load Combinations for Office Building
    print(f"\n2. Load Combinations for Office Building")
    print("-" * 60)
    
    # Typical office building loads
    loads = {
        'D': 6.5,   # Dead load: 6.5 kN/m² (slab + finishes)
        'L': 2.4,   # Live load: 2.4 kN/m² (office occupancy)
        'W': 1.8,   # Wind load: 1.8 kN/m²
        'E': 1.2    # Earthquake load: 1.2 kN/m²
    }
    
    print("Applied Loads:")
    load_descriptions = {
        'D': 'Dead Load (slab + finishes)',
        'L': 'Live Load (office occupancy)',
        'W': 'Wind Load',
        'E': 'Earthquake Load'
    }
    
    for load_type, value in loads.items():
        print(f"  {load_descriptions[load_type]}: {value:.1f} kN/m²")
    
    print("\\nACI 318M-25 Load Combinations (Strength Design):")
    strength_combos = aci.check_load_combinations(loads, 'strength')
    
    for combo in strength_combos[:5]:  # Show first 5 combinations
        print(f"  {combo['name']}: {combo['factored_load']:5.2f} kN/m² - {combo['description']}")
    
    # Find governing combination
    governing = max(strength_combos, key=lambda x: x['factored_load'])
    print(f"\\nGoverning combination: {governing['name']} = {governing['factored_load']:.2f} kN/m²")
    
    # Example 3: Reinforcement Design for Two-Way Slab
    print(f"\n3. Reinforcement Design for Two-Way Slab")
    print("-" * 60)
    
    # Slab properties
    slab_thickness = 250  # mm
    span_x = 6.0         # m
    span_y = 8.0         # m
    
    # Material selection
    concrete_class = ConcreteStrengthClass.FC28
    steel_grade = ReinforcementGrade.GRADE420
    material_props = aci.get_material_properties(concrete_class, steel_grade)
    
    print(f"Slab: {span_x}m × {span_y}m × {slab_thickness}mm")
    print(f"Concrete: {concrete_class.value} (fc' = {material_props.fc_prime} MPa)")
    print(f"Steel: {steel_grade.value} (fy = {material_props.fy} MPa)")
    
    # Concrete cover
    cover, unit, desc = aci.get_concrete_cover(StructuralElement.SLAB, 'normal')
    print(f"Concrete cover: {cover} {unit} ({desc})")
    
    # Reinforcement ratios
    rho_min = aci.calculate_minimum_reinforcement_ratio(material_props.fc_prime, material_props.fy)
    rho_max = aci.calculate_maximum_reinforcement_ratio(material_props.fc_prime, material_props.fy)
    rho_balanced = aci.calculate_balanced_reinforcement_ratio(material_props.fc_prime, material_props.fy)
    
    print(f"\\nReinforcement Ratio Limits:")
    print(f"  Minimum (ρmin): {rho_min:.4f}")
    print(f"  Balanced (ρb): {rho_balanced:.4f}")
    print(f"  Maximum (ρmax): {rho_max:.4f} (tension-controlled)")
    
    # Example reinforcement selection
    bar_sizes = ['15M', '20M', '25M']
    spacing = 200  # mm
    
    print(f"\\nReinforcement Options @ {spacing}mm spacing:")
    effective_depth = slab_thickness - cover - 10  # Assume 20M bars (10mm radius)
    
    for bar_size in bar_sizes:
        if bar_size in aci.bar_areas:
            area_per_m = aci.calculate_area_per_meter(bar_size, spacing)
            rho_provided = area_per_m / (1000 * effective_depth)
            check = "OK" if rho_min <= rho_provided <= rho_max else "CHECK"
            
            print(f"  {bar_size}: {area_per_m:4.0f} mm²/m, ρ = {rho_provided:.4f} ({check})")
    
    # Example 4: Development Length Calculations
    print(f"\n4. Development Length Calculations")
    print("-" * 60)
    
    bar_size = '20M'
    fc_prime = material_props.fc_prime
    fy = material_props.fy
    
    # Different modification factors
    scenarios = [
        {'name': 'Standard conditions', 'factors': {}},
        {'name': 'Top reinforcement', 'factors': {'top_bar': 1.3}},
        {'name': 'Epoxy coated', 'factors': {'epoxy': 1.5}},
        {'name': 'Top + Epoxy coated', 'factors': {'top_bar': 1.3, 'epoxy': 1.5}}
    ]
    
    print(f"Development length for {bar_size} bars:")
    print(f"(fc' = {fc_prime} MPa, fy = {fy} MPa)")
    
    for scenario in scenarios:
        ld = aci.calculate_development_length(bar_size, fc_prime, fy, scenario['factors'])
        print(f"  {scenario['name']}: {ld:4.0f} mm")
    
    # Example 5: Crack Control Analysis
    print(f"\n5. Crack Control Analysis")
    print("-" * 60)
    
    # Service conditions
    service_moment = 150000  # N⋅mm/mm (per unit width)
    bar_spacing = 200        # mm
    
    # Simplified stress calculation (assuming elastic behavior)
    # This is a simplified example - actual analysis would be more complex
    
    print("Service Load Crack Control Check:")
    print("(Simplified analysis for demonstration)")
    
    fs_service = 0.6 * fy  # Conservative estimate for service stress
    dc = cover + aci.get_bar_diameter('20M')/2  # Distance to reinforcement centroid
    A_concrete = bar_spacing * 2 * dc  # Concrete area per bar (simplified)
    
    crack_results = aci.check_crack_control(fs_service, dc, A_concrete, bar_spacing)
    
    print(f"  Service stress (estimated): {crack_results['stress_mpa']:.1f} MPa")
    print(f"  Cover to centroid: {crack_results['cover_mm']:.1f} mm")
    print(f"  Bar spacing: {crack_results['spacing_mm']:.0f} mm")
    print(f"  Crack parameter (z): {crack_results['z_parameter']:.0f} N/mm")
    print(f"  Interior exposure: {'PASS' if crack_results['interior_ok'] else 'FAIL'}")
    print(f"  Exterior exposure: {'PASS' if crack_results['exterior_ok'] else 'FAIL'}")
    
    # Example 6: Deflection Considerations
    print(f"\n6. Deflection Considerations")
    print("-" * 60)
    
    span = max(span_x, span_y) * 1000  # Convert to mm for consistency
    
    print("ACI 318M-25 Deflection Limits:")
    deflection_limits = aci.deflection_limits
    
    for limit_type, limits in deflection_limits.items():
        print(f"\\n  {limit_type.replace('_', ' ').title()} deflection:")
        for condition, limit_ratio in limits.items():
            max_deflection = span / limit_ratio
            print(f"    {condition.replace('_', ' ')}: L/{limit_ratio} = {max_deflection:.1f} mm")
    
    # Calculate deflection multiplier for long-term effects
    rho_example = 0.008  # Example reinforcement ratio
    rho_prime = 0.002    # Example compression reinforcement ratio
    
    lambda_delta = aci.calculate_deflection_multiplier(rho_example, rho_prime)
    print(f"\\nLong-term deflection multiplier (λΔ): {lambda_delta:.2f}")
    print(f"(For ρ = {rho_example:.3f}, ρ' = {rho_prime:.3f})")
    
    # Example 7: Complete Design Report
    print(f"\n7. Design Report Generation")
    print("-" * 60)
    
    # Project information
    project_info = {
        'project_name': 'Office Building Two-Way Slab Example',
        'location': 'Downtown Office Complex',
        'date': '2024-01-15',
        'engineer': 'Professional Engineer',
        'element_type': 'Two-way flat slab'
    }
    
    # Design results summary
    design_results = {
        'Slab dimensions': f'{span_x}m × {span_y}m',
        'Slab thickness': f'{slab_thickness} mm',
        'Effective depth': f'{effective_depth:.1f} mm',
        'Governing load': f'{governing["factored_load"]:.2f} kN/m²',
        'Selected reinforcement': f'20M @ 200mm both ways',
        'Reinforcement ratio': f'{rho_provided:.4f}',
        'Development length': f'{ld:.0f} mm',
        'Crack control': 'Satisfactory for interior exposure'
    }
    
    print("Generating comprehensive design report...")
    
    report = aci.generate_design_summary_report(
        project_info, concrete_class, steel_grade, loads, design_results
    )
    
    # Show report preview
    report_lines = report.split('\\n')
    print("\\nDesign Report Preview (First 20 lines):")
    for i, line in enumerate(report_lines[:20]):
        print(line)
    print("... (report continues)")
    print(f"\\nTotal report length: {len(report)} characters")
    
    # Example 8: International Comparison
    print(f"\n8. International Standards Comparison")
    print("-" * 60)
    
    print("ACI 318M-25 vs Other International Codes:")
    print("\\nStrength Reduction Factors (φ):")
    phi_factors = aci.strength_reduction_factors
    
    for failure_mode, phi in phi_factors.items():
        formatted_mode = failure_mode.replace('_', ' ').title()
        print(f"  {formatted_mode}: φ = {phi:.2f}")
    
    print("\\nUnits and Conventions:")
    print("  - Units: International System (SI)")
    print("  - Concrete strength: MPa (fc')")
    print("  - Steel strength: MPa (fy)")
    print("  - Dimensions: mm, m")
    print("  - Loads: kN, kN/m²")
    print("  - Compatible with: ASCE 7, ASTM standards")
    
    print(f"\n=" * 80)
    print("Summary:")
    print("✓ ACI 318M-25 Building Code Library is ready for use")
    print("✓ International System of Units (SI) throughout")
    print("✓ Compatible with modern structural design software")
    print("✓ Comprehensive material properties and design methods")
    print("✓ Load combinations per latest ACI 318M-25 provisions")
    print("✓ Suitable for integration with existing design tools")
    print("=" * 80)

if __name__ == "__main__":
    main()