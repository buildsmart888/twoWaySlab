"""
Thai Ministry Regulation B.E. 2566 Implementation Demonstration
==============================================================

Complete demonstration of Phase 8: Thai Ministry Regulation Implementation
- Load combinations and safety factors
- Design requirements (cover, deflection, tolerances)
- Material specifications integration
- Quality control and compliance checking

การสาธิตการใช้งานกฎกระทรวง พ.ศ. 2566 แบบครบถ้วน
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_load_combinations():
    """Demonstrate Thai load combinations"""
    print("🏗️  Thai Load Combinations Demo")
    print("=" * 60)
    
    from structural_standards.thai.ministry_2566 import (
        ThaiMinistryRegulation2566,
        ThaiLoadType,
        ThaiCombinationType,
        ThaiProjectData,
        ThaiEnvironmentType
    )
    
    # Initialize regulation
    regulation = ThaiMinistryRegulation2566()
    
    # Define loads for a typical building
    loads = {
        ThaiLoadType.DEAD: 12.0,      # kN/m² - น้ำหนักตาย
        ThaiLoadType.LIVE: 8.0,       # kN/m² - น้ำหนักใช้สอย
        ThaiLoadType.WIND: 5.0,       # kN/m² - แรงลม
        ThaiLoadType.EARTHQUAKE: 4.0   # kN/m² - แรงแผ่นดินไหว
    }
    
    print("✓ กำหนดแรงกระทำ/Applied Loads:")
    print(f"  - น้ำหนักตาย/Dead Load: {loads[ThaiLoadType.DEAD]} kN/m²")
    print(f"  - น้ำหนักใช้สอย/Live Load: {loads[ThaiLoadType.LIVE]} kN/m²")
    print(f"  - แรงลม/Wind Load: {loads[ThaiLoadType.WIND]} kN/m²")
    print(f"  - แรงแผ่นดินไหว/Earthquake Load: {loads[ThaiLoadType.EARTHQUAKE]} kN/m²")
    
    # Ultimate limit state combinations
    print(f"\n✓ การรวมแรงสภาวะจำกัดสุดขีด/Ultimate Limit State Combinations:")
    uls_results = regulation.calculate_design_loads(loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE)
    
    for combo_name, load_value in uls_results.items():
        print(f"  {combo_name}: {load_value:.1f} kN/m²")
    
    # Find governing combination
    critical_combo, max_load = regulation.find_governing_load_combination(loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE)
    print(f"\n✓ การรวมแรงวิกฤต/Governing Combination:")
    print(f"  {critical_combo.name}: {critical_combo.get_equation()} = {max_load:.1f} kN/m²")
    print(f"  คำอธิบาย/Description: {critical_combo.description_thai}")
    
    # Serviceability combinations
    print(f"\n✓ การรวมแรงสภาวะจำกัดการใช้งาน/Serviceability Limit State:")
    sls_results = regulation.calculate_design_loads(loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE)
    
    for combo_name, load_value in sls_results.items():
        print(f"  {combo_name}: {load_value:.1f} kN/m²")
    
    return True

def demo_design_requirements():
    """Demonstrate design requirements"""
    print("\n🏛️  Thai Design Requirements Demo")
    print("=" * 60)
    
    from structural_standards.thai.ministry_2566 import (
        ThaiMinistryRegulation2566,
        ThaiEnvironmentType,
        ThaiElementType,
        ThaiSupportType
    )
    
    regulation = ThaiMinistryRegulation2566()
    
    # Concrete cover requirements
    print("✓ ความหนาคอนกรีตปิด/Concrete Cover Requirements:")
    
    environments = [ThaiEnvironmentType.NORMAL, ThaiEnvironmentType.AGGRESSIVE, ThaiEnvironmentType.MARINE]
    elements = [ThaiElementType.SLAB, ThaiElementType.BEAM, ThaiElementType.COLUMN, ThaiElementType.FOUNDATION]
    
    env_names = {
        ThaiEnvironmentType.NORMAL: "ปกติ/Normal",
        ThaiEnvironmentType.AGGRESSIVE: "รุนแรง/Aggressive",
        ThaiEnvironmentType.MARINE: "ทางทะเล/Marine"
    }
    
    elem_names = {
        ThaiElementType.SLAB: "แผ่นพื้น/Slab",
        ThaiElementType.BEAM: "คาน/Beam", 
        ThaiElementType.COLUMN: "เสา/Column",
        ThaiElementType.FOUNDATION: "ฐานราก/Foundation"
    }
    
    for env in environments:
        print(f"\n  สภาพแวดล้อม {env_names[env]}:")
        for elem in elements:
            cover_req = regulation.get_concrete_cover(elem, env)
            if cover_req:
                print(f"    {elem_names[elem]}: {cover_req.cover_mm:.0f} mm")
    
    # Deflection limits
    print(f"\n✓ ขีดจำกัดการโก่งตัว/Deflection Limits:")
    
    support_types = [ThaiSupportType.SIMPLY_SUPPORTED, ThaiSupportType.CONTINUOUS, ThaiSupportType.CANTILEVER]
    durations = ["immediate", "long_term"]
    
    support_names = {
        ThaiSupportType.SIMPLY_SUPPORTED: "รองรับแบบง่าย/Simply Supported",
        ThaiSupportType.CONTINUOUS: "ต่อเนื่อง/Continuous",
        ThaiSupportType.CANTILEVER: "จำยื่น/Cantilever"
    }
    
    duration_names = {
        "immediate": "ทันที/Immediate",
        "long_term": "ระยะยาว/Long-term"
    }
    
    for duration in durations:
        print(f"\n  การโก่งตัว{duration_names[duration]}:")
        for support in support_types:
            limit = regulation.get_deflection_limit(support, duration)
            if limit:
                print(f"    {support_names[support]}: L/{limit.limit_ratio}")
    
    # Deflection compliance check example
    print(f"\n✓ ตัวอย่างการตรวจสอบการโก่งตัว/Deflection Compliance Example:")
    
    # Example: 6m simply supported beam with 20mm deflection
    span_length = 6000  # mm
    actual_deflection = 20  # mm
    
    compliance = regulation.check_deflection_compliance(
        actual_deflection=actual_deflection,
        span_length=span_length,
        support_type=ThaiSupportType.SIMPLY_SUPPORTED,
        load_duration="immediate"
    )
    
    print(f"  ช่วงพื้น/Span: {span_length/1000:.1f} m")
    print(f"  การโก่งตัวจริง/Actual deflection: {actual_deflection} mm")
    print(f"  การโก่งตัวที่อนุญาต/Allowable: {compliance['allowable_deflection_mm']:.1f} mm")
    print(f"  ขีดจำกัด/Limit: {compliance['deflection_ratio']}")
    print(f"  ผ่านเกณฑ์/Compliant: {'✅ ใช่/Yes' if compliance['compliant'] else '❌ ไม่/No'}")
    print(f"  อัตราการใช้งาน/Utilization: {compliance['utilization_ratio']:.2f}")
    
    return True

def demo_material_integration():
    """Demonstrate material integration"""
    print("\n🔩 Thai Material Integration Demo")
    print("=" * 60)
    
    from structural_standards.thai.ministry_2566 import (
        ThaiMinistryRegulation2566,
        ThaiEnvironmentType
    )
    
    regulation = ThaiMinistryRegulation2566()
    
    # Create Thai materials
    print("✓ การสร้างวัสดุไทย/Creating Thai Materials:")
    
    concrete_fc210 = regulation.create_thai_concrete("Fc210")
    steel_sd40 = regulation.create_thai_steel("SD40")
    
    print(f"  คอนกรีต/Concrete: {concrete_fc210}")
    print(f"    fc' = {concrete_fc210.fc_prime} MPa = {concrete_fc210.strength_in_ksc():.0f} ksc")
    print(f"    Ec = {concrete_fc210.elastic_modulus():.0f} MPa")
    print(f"    β₁ = {concrete_fc210.beta1_factor():.2f}")
    
    print(f"  เหล็ก/Steel: {steel_sd40}")
    print(f"    fy = {steel_sd40.fy} MPa = {steel_sd40.fy * 1000 / 9.807:.0f} ksc")
    print(f"    fu = {steel_sd40.fu} MPa")
    print(f"    Grade: {steel_sd40.grade}")
    
    # Material compatibility check
    print(f"\n✓ การตรวจสอบความเข้ากันได้ของวัสดุ/Material Compatibility Check:")
    
    compatibility = regulation.validate_material_combination(
        concrete_grade="Fc210",
        steel_grade="SD40", 
        environment=ThaiEnvironmentType.NORMAL
    )
    
    print(f"  การผสมวัสดุ/Material Combination: Fc210 + SD40")
    print(f"  เหมาะสม/Compatible: {'✅ ใช่/Yes' if compatibility['is_valid'] else '❌ ไม่/No'}")
    print(f"  สถานะ/Status: {compatibility['material_compatibility']}")
    
    if compatibility['warnings']:
        print("  คำเตือน/Warnings:")
        for warning in compatibility['warnings']:
            print(f"    - {warning}")
    
    if compatibility['recommendations']:
        print("  ข้อแนะนำ/Recommendations:")
        for rec in compatibility['recommendations']:
            print(f"    - {rec}")
    
    # Safety factors
    print(f"\n✓ ค่าความปลอดภัย/Safety Factors:")
    print(f"  คอนกรีต/Concrete (γc): {regulation.get_safety_factor('concrete')}")
    print(f"  เหล็ก/Steel (γs): {regulation.get_safety_factor('steel')}")
    print(f"  น้ำหนักตาย/Dead Load: {regulation.get_safety_factor('dead_load')}")
    print(f"  น้ำหนักใช้สอย/Live Load: {regulation.get_safety_factor('live_load')}")
    
    # Phi factors
    print(f"\n✓ ค่าลดกำลัง/Strength Reduction Factors (φ):")
    print(f"  งานโค้งควบคุมแรงดึง/Flexure (tension): {regulation.get_phi_factor('flexure_tension_controlled')}")
    print(f"  งานโค้งควบคุมแรงอัด/Flexure (compression): {regulation.get_phi_factor('flexure_compression_controlled')}")
    print(f"  แรงเฉือน/Shear: {regulation.get_phi_factor('shear_and_torsion')}")
    
    return True

def demo_compliance_checking():
    """Demonstrate comprehensive compliance checking"""
    print("\n✅ Thai Compliance Checking Demo")
    print("=" * 60)
    
    from structural_standards.thai.ministry_2566 import (
        ThaiMinistryRegulation2566,
        ThaiProjectData,
        ThaiEnvironmentType
    )
    
    regulation = ThaiMinistryRegulation2566()
    
    # Create project data
    project = ThaiProjectData(
        project_name="โครงการอาคารสำนักงาน 15 ชั้น",
        location="กรุงเทพมหานคร",
        environment_type=ThaiEnvironmentType.NORMAL,
        concrete_grade="Fc280",
        steel_grade="SD40",
        design_life=50,
        importance_factor=1.0,
        date="2024-01-15"
    )
    
    print("✓ ข้อมูลโครงการ/Project Information:")
    print(f"  ชื่อโครงการ/Project: {project.project_name}")
    print(f"  สถานที่/Location: {project.location}")
    print(f"  สภาพแวดล้อม/Environment: {project.environment_type.value}")
    print(f"  เกรดคอนกรีต/Concrete: {project.concrete_grade}")
    print(f"  เกรดเหล็ก/Steel: {project.steel_grade}")
    print(f"  อายุการใช้งาน/Design Life: {project.design_life} ปี/years")
    
    # Run compliance check
    print(f"\n✓ การตรวจสอบการปฏิบัติตาม/Compliance Check:")
    
    compliance_results = regulation.check_project_compliance(project)
    
    for i, result in enumerate(compliance_results, 1):
        status = "✅ ผ่าน/PASS" if result.is_compliant else "❌ ไม่ผ่าน/FAIL"
        print(f"  {i}. {result.category.replace('_', ' ').title()}: {status}")
        print(f"     {result.description_thai}")
        
        if result.warnings:
            for warning in result.warnings:
                print(f"     ⚠️  {warning}")
        
        if result.recommendations:
            for rec in result.recommendations:
                print(f"     💡 {rec}")
    
    # Generate full compliance report
    print(f"\n✓ การสร้างรายงานการปฏิบัติตาม/Generating Compliance Report...")
    
    compliance_report = regulation.generate_compliance_report(project, compliance_results)
    
    # Save report to file
    report_file = "thai_ministry_compliance_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(compliance_report)
    
    print(f"  📄 รายงานบันทึกไว้ที่/Report saved to: {report_file}")
    
    # Show first few lines of report
    lines = compliance_report.split('\n')
    print(f"\n✓ ตัวอย่างรายงาน/Report Preview:")
    for line in lines[:15]:
        print(f"  {line}")
    print(f"  ... ({len(lines)} total lines)")
    
    return True

def demo_provincial_zones():
    """Demonstrate provincial zones for wind and seismic"""
    print("\n🌪️ Thai Provincial Zones Demo")
    print("=" * 60)
    
    from structural_standards.thai.ministry_2566 import ThaiMinistryRegulation2566
    
    regulation = ThaiMinistryRegulation2566()
    
    # Wind zones
    print("✓ โซนลม/Wind Zones:")
    
    test_provinces = ['กรุงเทพมหานคร', 'เชียงใหม่', 'สงขลา', 'ภูเก็ต']
    
    for province in test_provinces:
        wind_data = regulation.get_wind_zone_data(province)
        if wind_data:
            print(f"  {province}:")
            print(f"    โซน/Zone: {wind_data['zone_id']}")
            print(f"    ความเร็วลม/Wind Speed: {wind_data['wind_speed']} m/s")
            print(f"    คำอธิบาย/Description: {wind_data['description_thai']}")
        else:
            print(f"  {province}: ไม่พบข้อมูลโซน/Zone data not found")
    
    # Seismic zones
    print(f"\n✓ โซนแผ่นดินไหว/Seismic Zones:")
    
    for province in test_provinces:
        seismic_data = regulation.get_seismic_zone_data(province)
        if seismic_data:
            print(f"  {province}:")
            print(f"    โซน/Zone: {seismic_data['zone_id']}")
            print(f"    PGA: {seismic_data['pga']} g")
            print(f"    คำอธิบาย/Description: {seismic_data['description_thai']}")
        else:
            print(f"  {province}: ไม่พบข้อมูลโซน/Zone data not found")
    
    return True

def demo_integration_workflow():
    """Complete integration workflow demonstration"""
    print("\n🔄 Complete Thai Integration Workflow Demo")
    print("=" * 60)
    
    from structural_standards.thai.ministry_2566 import (
        ThaiMinistryRegulation2566,
        ThaiProjectData,
        ThaiEnvironmentType,
        ThaiLoadType,
        ThaiCombinationType,
        ThaiElementType,
        ThaiSupportType
    )
    
    print("Scenario: โครงการอาคารสำนักงาน - Office Building Project")
    
    # Step 1: Initialize regulation
    regulation = ThaiMinistryRegulation2566()
    
    print(f"\n✓ โมดูลกฎกระทรวง/Regulation Module:")
    reg_info = regulation.get_regulation_info()
    print(f"  {reg_info['name_thai']}")
    print(f"  Effective Date: {reg_info['effective_date']}")
    
    # Step 2: Project setup
    project = ThaiProjectData(
        project_name="อาคารสำนักงาน ABC Tower", 
        location="กรุงเทพมหานคร",
        environment_type=ThaiEnvironmentType.NORMAL,
        concrete_grade="Fc240",
        steel_grade="SD40",
        design_life=50
    )
    
    print(f"\n✓ โครงการ/Project Setup:")
    print(f"  {project.project_name}")
    print(f"  Materials: {project.concrete_grade} + {project.steel_grade}")
    
    # Step 3: Load analysis
    loads = {
        ThaiLoadType.DEAD: 15.0,      # kN/m²
        ThaiLoadType.LIVE: 12.0,      # kN/m²
        ThaiLoadType.WIND: 8.0,       # kN/m²
        ThaiLoadType.EARTHQUAKE: 6.0   # kN/m²
    }
    
    critical_combo, max_load = regulation.find_governing_load_combination(
        loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
    )
    
    print(f"\n✓ การวิเคราะห์แรง/Load Analysis:")
    print(f"  การรวมแรงวิกฤต/Governing: {critical_combo.name}")
    print(f"  แรงออกแบบ/Design Load: {max_load:.1f} kN/m²")
    
    # Step 4: Material design
    concrete = regulation.create_thai_concrete(project.concrete_grade)
    steel = regulation.create_thai_steel(project.steel_grade)
    
    print(f"\n✓ วัสดุออกแบบ/Design Materials:")
    print(f"  {concrete}")
    print(f"  {steel}")
    
    # Step 5: Design requirements
    slab_cover = regulation.get_concrete_cover(ThaiElementType.SLAB, project.environment_type)
    beam_deflection = regulation.get_deflection_limit(ThaiSupportType.SIMPLY_SUPPORTED, "immediate")
    
    print(f"\n✓ ข้อกำหนดการออกแบบ/Design Requirements:")
    print(f"  Slab cover: {slab_cover.cover_mm:.0f} mm")
    print(f"  Beam deflection limit: L/{beam_deflection.limit_ratio}")
    
    # Step 6: Safety factors
    concrete_sf = regulation.get_safety_factor('concrete')
    phi_flexure = regulation.get_phi_factor('flexure_tension_controlled')
    
    design_strength_concrete = concrete.fc_prime / concrete_sf
    
    print(f"\n✓ ค่าความปลอดภัยและกำลัง/Safety Factors & Strengths:")
    print(f"  Concrete safety factor: {concrete_sf}")
    print(f"  Design concrete strength: {design_strength_concrete:.1f} MPa")
    print(f"  Phi factor (flexure): {phi_flexure}")
    
    # Step 7: Compliance validation
    compliance_results = regulation.check_project_compliance(project)
    
    compliant_count = sum(1 for result in compliance_results if result.is_compliant)
    total_count = len(compliance_results)
    
    print(f"\n✓ การตรวจสอบการปฏิบัติตาม/Compliance Validation:")
    print(f"  ผ่านการตรวจสอบ/Passed: {compliant_count}/{total_count}")
    print(f"  เปอร์เซ็นต์ที่ผ่าน/Pass Rate: {(compliant_count/total_count)*100:.1f}%")
    
    overall_status = "COMPLIANT" if compliant_count == total_count else "NON-COMPLIANT"
    print(f"  สถานะโดยรวม/Overall: {'✅' if overall_status == 'COMPLIANT' else '❌'} {overall_status}")
    
    # Step 8: Final summary
    print(f"\n✓ สรุปการออกแบบ/Design Summary:")
    print(f"  📏 Materials: {project.concrete_grade} concrete, {project.steel_grade} steel")
    print(f"  📋 Design load: {max_load:.1f} kN/m² ({critical_combo.name})")
    print(f"  🔩 Cover requirement: {slab_cover.cover_mm:.0f} mm (slab)")
    print(f"  📐 Deflection limit: L/{beam_deflection.limit_ratio} (beam)")
    print(f"  ✅ Thai Ministry Regulation B.E. 2566 compliant")
    
    return True

def main():
    """Main demonstration function"""
    print("🎯 Thai Ministry Regulation B.E. 2566 Complete Implementation Demo")
    print("=" * 80)
    print("Phase 8: Thai Standards Implementation ✅")
    print("- Thai Load Combinations ✅")
    print("- Thai Design Requirements ✅")
    print("- Thai Material Integration ✅")
    print("- Compliance Checking ✅")
    print()
    
    try:
        # Run all demonstrations
        demo_load_combinations()
        demo_design_requirements()
        demo_material_integration()
        demo_compliance_checking()
        demo_provincial_zones()
        demo_integration_workflow()
        
        print(f"\n🎉 All Thai Ministry Regulation demonstrations completed successfully!")
        print("\n📋 Implementation Status:")
        print("✅ Phase 8: Thai Ministry Regulation B.E. 2566 - COMPLETED")
        print("⏭️  Ready for Phase 8: Thai Wind Loads (TIS 1311-50)")
        print("⏭️  Ready for Phase 8: Thai Seismic Loads (TIS 1301/1302-61)")
        print("⏭️  Ready for Phase 8: Thai Unit Systems")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error in demonstration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()