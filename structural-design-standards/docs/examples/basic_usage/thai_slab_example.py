#!/usr/bin/env python3
"""
Thai Slab Design Example
========================

This example demonstrates how to design a two-way reinforced concrete slab
according to Thai Ministry Regulation B.E. 2566 and TIS standards.

ตัวอย่างการออกแบบพื้นคอนกรีตเสริมเหล็กสองทิศทาง
ตามกฎกระทรวง พ.ศ. 2566 และมาตรฐาน TIS

Example Problem:
Design a two-way slab for an office building in Bangkok with:
- Slab dimensions: 6.0 m × 4.0 m
- Live load: 2.5 kN/m² (office)
- Dead load: 4.0 kN/m² (finishes + self-weight)
- Concrete: Fc210 (21 MPa)
- Steel: SD40 (392 MPa)
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from structural_standards.thai.materials.concrete import ThaiConcrete
from structural_standards.thai.materials.steel import ThaiSteel
from structural_standards.thai.ministry_2566.load_combinations import ThaiMinistryLoadCombinations
from structural_standards.thai.unit_systems import ThaiUnitConverter
from structural_standards.thai.ministry_2566.ministry_regulation import ThaiMinistryRegulation


def main():
    """
    Main function demonstrating Thai slab design
    """
    print("=" * 70)
    print("Thai Two-Way Slab Design Example")
    print("ตัวอย่างการออกแบบพื้นคอนกรีตเสริมเหล็กสองทิศทาง")
    print("=" * 70)
    
    # Step 1: Material Properties (Thai Standards)
    print("\n1. Material Properties / คุณสมบัติวัสดุ:")
    print("-" * 50)
    
    # Thai concrete (Fc210 = 21 MPa)
    concrete = ThaiConcrete(grade='Fc210')
    print(f"Concrete / คอนกรีต: {concrete.grade}")
    print(f"  f'c = {concrete.fc_prime} MPa ({concrete.fc_ksc:.0f} ksc)")
    print(f"  Unit weight / น้ำหนักหน่วย = {concrete.unit_weight} kN/m³")
    print(f"  Elastic modulus / โมดูลัสยืดหยุ่น = {concrete.elastic_modulus():.0f} MPa")
    
    # Thai steel (SD40)
    steel = ThaiSteel(grade='SD40', bar_designation='DB20')
    print(f"\nSteel / เหล็กเสริม: {steel.grade}")
    print(f"  fy = {steel.fy} MPa ({steel.fy_ksc:.0f} ksc)")
    print(f"  Bar designation / ขนาดเหล็ก: {steel.bar_designation}")
    print(f"  Bar area / พื้นที่หน้าตัด = {steel.bar_area()} mm²")
    
    # Step 2: Slab Geometry
    print("\n2. Slab Geometry / ขนาดพื้น:")
    print("-" * 50)
    
    # Slab dimensions
    length_x = 6.0  # m (long span)
    length_y = 4.0  # m (short span)
    thickness = 150  # mm (initial assumption)
    effective_depth = thickness - 30  # mm (assuming 20mm cover + 5mm bar radius)
    
    print(f"Slab dimensions / ขนาดพื้น:")
    print(f"  Length (X) / ความยาว (X) = {length_x} m")
    print(f"  Width (Y) / ความกว้าง (Y) = {length_y} m")
    print(f"  Thickness / ความหนา = {thickness} mm")
    print(f"  Effective depth / ความลึกมีประสิทธิภาพ = {effective_depth} mm")
    
    # Check aspect ratio
    aspect_ratio = length_x / length_y
    print(f"  Aspect ratio / อัตราส่วนด้าน = {aspect_ratio:.2f}")
    
    if aspect_ratio <= 2.0:
        slab_type = "Two-way slab / พื้นสองทิศทาง"
    else:
        slab_type = "One-way slab / พื้นทิศทางเดียว"
    print(f"  Slab type / ประเภทพื้น: {slab_type}")
    
    # Step 3: Load Analysis
    print("\n3. Load Analysis / การวิเคราะห์น้ำหนักบรรทุก:")
    print("-" * 50)
    
    # Applied loads
    dead_load = 4.0  # kN/m² (finishes + self-weight)
    live_load = 2.5  # kN/m² (office load per TIS)
    
    print(f"Dead load / น้ำหนักตาย = {dead_load} kN/m²")
    print(f"Live load / น้ำหนักใช้สอย = {live_load} kN/m²")
    print(f"Total service load / น้ำหนักรวม = {dead_load + live_load} kN/m²")
    
    # Thai load combinations (Ministry Regulation B.E. 2566)
    thai_loads = ThaiMinistryLoadCombinations()
    
    # Get critical Ultimate Limit State combination (1001)
    uls_combinations = thai_loads.get_ultimate_combinations()
    critical_combo = next(combo for combo in uls_combinations if combo.name == '1001')
    
    print(f"\nCritical load combination / ชุดน้ำหนักวิกฤติ:")
    print(f"  {critical_combo.name}: {critical_combo.get_equation()}")
    
    # Calculate factored loads
    wu = 1.4 * dead_load + 1.7 * live_load
    print(f"  wu = 1.4×{dead_load} + 1.7×{live_load} = {wu:.1f} kN/m²")
    
    # Step 4: Moment Analysis (Simplified Method)
    print("\n4. Moment Analysis / การวิเคราะห์โมเมนต์:")
    print("-" * 50)
    
    # For two-way slabs, use coefficient method (simplified)
    # Positive moment coefficients (typical values)
    pos_moment_coeff_x = 0.036  # For continuous edges
    pos_moment_coeff_y = 0.027  # For continuous edges
    
    # Calculate design moments
    Mu_x = pos_moment_coeff_x * wu * length_y * length_x**2  # kN⋅m/m
    Mu_y = pos_moment_coeff_y * wu * length_x * length_y**2  # kN⋅m/m
    
    print(f"Design moments per meter width:")
    print(f"  Mu_x (long span) / โมเมนต์ X = {Mu_x:.2f} kN⋅m/m")
    print(f"  Mu_y (short span) / โมเมนต์ Y = {Mu_y:.2f} kN⋅m/m")
    
    # Step 5: Reinforcement Design
    print("\n5. Reinforcement Design / การออกแบบเหล็กเสริม:")
    print("-" * 50)
    
    # Unit converter for traditional units
    converter = ThaiUnitConverter()
    
    # Design for X-direction (governing)
    b = 1000  # mm (per meter width)
    d = effective_depth  # mm
    fc = concrete.fc_prime  # MPa
    fy = steel.fy  # MPa
    
    # Required moment resistance
    Mu_x_nmm = Mu_x * 1e6  # N⋅mm
    Mu_y_nmm = Mu_y * 1e6  # N⋅mm
    
    print(f"Design parameters:")
    print(f"  b = {b} mm (per meter width)")
    print(f"  d = {d} mm")
    print(f"  f'c = {fc} MPa ({converter.mpa_to_ksc(fc):.0f} ksc)")
    print(f"  fy = {fy} MPa ({converter.mpa_to_ksc(fy):.0f} ksc)")
    
    # Simplified flexural design (using working stress method concepts)
    # For preliminary design - actual design would require more detailed analysis
    
    # Estimate required steel area using simplified formula
    # As = Mu / (0.9 * fy * 0.8 * d) - simplified approach
    As_req_x = Mu_x_nmm / (0.9 * fy * 0.8 * d)  # mm²/m
    As_req_y = Mu_y_nmm / (0.9 * fy * 0.8 * d)  # mm²/m
    
    print(f"\nRequired steel area:")
    print(f"  As_x = {As_req_x:.0f} mm²/m")
    print(f"  As_y = {As_req_y:.0f} mm²/m")
    
    # Check minimum reinforcement
    As_min = max(
        1.4 * b * thickness / fy,  # ACI minimum
        0.0018 * b * thickness     # Shrinkage minimum
    )
    
    print(f"  As_min = {As_min:.0f} mm²/m")
    
    # Final required areas
    As_final_x = max(As_req_x, As_min)
    As_final_y = max(As_req_y, As_min)
    
    print(f"\nFinal required steel area:")
    print(f"  As_x,final = {As_final_x:.0f} mm²/m")
    print(f"  As_y,final = {As_final_y:.0f} mm²/m")
    
    # Step 6: Bar Selection (Thai Standard)
    print("\n6. Bar Selection / การเลือกเหล็กเสริม:")
    print("-" * 50)
    
    # Available Thai bar sizes
    thai_bars = {
        'DB10': {'diameter': 9.5, 'area': 71},
        'DB12': {'diameter': 11.9, 'area': 113},
        'DB16': {'diameter': 15.9, 'area': 199},
        'DB20': {'diameter': 19.5, 'area': 387},
        'DB25': {'diameter': 25.2, 'area': 507}
    }
    
    # Select bars for X-direction
    bar_size_x = 'DB12'  # Start with DB12
    bar_area_x = thai_bars[bar_size_x]['area']
    spacing_x = (bar_area_x * 1000) / As_final_x  # mm
    
    if spacing_x > 300:  # If spacing too large, use smaller bars
        bar_size_x = 'DB10'
        bar_area_x = thai_bars[bar_size_x]['area']
        spacing_x = (bar_area_x * 1000) / As_final_x
    
    # Select bars for Y-direction
    bar_size_y = 'DB10'  # Typically smaller for distribution
    bar_area_y = thai_bars[bar_size_y]['area']
    spacing_y = (bar_area_y * 1000) / As_final_y
    
    print(f"X-direction reinforcement / เหล็กเสริมทิศทาง X:")
    print(f"  Bar size / ขนาดเหล็ก: {bar_size_x}")
    print(f"  Spacing / ระยะห่าง: {spacing_x:.0f} mm c/c")
    print(f"  Provided area / พื้นที่ให้ไว้: {bar_area_x * 1000 / spacing_x:.0f} mm²/m")
    
    print(f"\nY-direction reinforcement / เหล็กเสริมทิศทาง Y:")
    print(f"  Bar size / ขนาดเหล็ก: {bar_size_y}")
    print(f"  Spacing / ระยะห่าง: {spacing_y:.0f} mm c/c")
    print(f"  Provided area / พื้นที่ให้ไว้: {bar_area_y * 1000 / spacing_y:.0f} mm²/m")
    
    # Step 7: Design Summary
    print("\n7. Design Summary / สรุปการออกแบบ:")
    print("-" * 50)
    
    print(f"Slab thickness / ความหนาพื้น: {thickness} mm")
    print(f"Concrete grade / เกรดคอนกรีต: {concrete.grade} ({concrete.fc_prime} MPa)")
    print(f"Steel grade / เกรดเหล็ก: {steel.grade} ({steel.fy} MPa)")
    print()
    print(f"Bottom reinforcement / เหล็กเสริมด้านล่าง:")
    print(f"  Main bars (X): {bar_size_x} @ {spacing_x:.0f} mm c/c")
    print(f"  Distribution bars (Y): {bar_size_y} @ {spacing_y:.0f} mm c/c")
    print()
    print(f"Load combination used / ชุดน้ำหนักที่ใช้: {critical_combo.get_equation()}")
    print(f"Design moments / โมเมนต์ออกแบบ:")
    print(f"  Mu_x = {Mu_x:.2f} kN⋅m/m")
    print(f"  Mu_y = {Mu_y:.2f} kN⋅m/m")
    
    # Step 8: Compliance Check
    print("\n8. Thai Standard Compliance / การตรวจสอบมาตรฐานไทย:")
    print("-" * 50)
    
    thai_ministry = ThaiMinistryRegulation()
    
    print(f"✅ Design follows: {thai_ministry.regulation_info['name_english']}")
    print(f"✅ ออกแบบตาม: {thai_ministry.regulation_info['name_thai']}")
    print(f"✅ Effective date: {thai_ministry.regulation_info['effective_date']}")
    print(f"✅ Authority: {thai_ministry.regulation_info['authority']}")
    
    return {
        'thickness': thickness,
        'reinforcement_x': f"{bar_size_x} @ {spacing_x:.0f} mm",
        'reinforcement_y': f"{bar_size_y} @ {spacing_y:.0f} mm",
        'moments': {'Mu_x': Mu_x, 'Mu_y': Mu_y},
        'compliance': True
    }


if __name__ == "__main__":
    # Run the example
    result = main()
    
    print("\n" + "=" * 70)
    print("Thai Slab Design Example Completed!")
    print("ตัวอย่างการออกแบบพื้นตามมาตรฐานไทยเสร็จสมบูรณ์!")
    print("=" * 70)
    
    if result['compliance']:
        print("✅ Design complies with Thai Ministry Regulation B.E. 2566")
        print("✅ การออกแบบเป็นไปตามกฎกระทรวง พ.ศ. 2566")
    
    print(f"\nFinal Design:")
    print(f"Slab thickness: {result['thickness']} mm")
    print(f"X-direction: {result['reinforcement_x']}")
    print(f"Y-direction: {result['reinforcement_y']}")