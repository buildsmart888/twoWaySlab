#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
ตัวอย่างการใช้งานไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย
Example Usage of Thai Earthquake Load Calculation Library

@author: Enhanced by AI Assistant
@date: 2024
"""

from thaiEarthquakeLoad import (
    ThaiEarthquakeLoad, 
    SeismicZone, 
    SoilType, 
    BuildingImportance, 
    StructuralSystem, 
    BuildingGeometrySeismic
)

def main():
    """ตัวอย่างการใช้งานหลัก / Main usage examples"""
    
    print("=" * 80)
    print("ตัวอย่างการใช้งานไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย")
    print("Thai Earthquake Load Library Usage Examples")
    print("ตาม มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1)")
    print("=" * 80)
    
    # เริ่มต้นเครื่องคำนวณ / Initialize calculator
    earthquake_calc = ThaiEarthquakeLoad()
    
    # ตัวอย่างที่ 1: การดูโซนแผ่นดินไหว / Example 1: Seismic zone lookup
    print("\n1. การดูโซนแผ่นดินไหว / Seismic Zone Lookup")
    print("-" * 60)
    
    provinces = ['เชียงใหม่', 'เชียงราย', 'กรุงเทพมหานคร', 'ขอนแก่น', 'ภูเก็ต', 'สงขลา']
    
    for province in provinces:
        zone, pga, description = earthquake_calc.get_seismic_zone_info(province)
        risk_level = {
            'A': 'ต่ำ / Low',
            'B': 'ปานกลาง / Moderate', 
            'C': 'สูง / High'
        }[zone.value]
        print(f"{province}: Zone {zone.value} (PGA = {pga:.2f}g) - ความเสี่ยง{risk_level}")
    
    # ตัวอย่างที่ 2: การคำนวณแรงแผ่นดินไหวอย่างรวดเร็ว / Example 2: Quick earthquake calculation
    print(f"\n2. การคำนวณแรงแผ่นดินไหวอย่างรวดเร็ว / Quick Earthquake Calculation")
    print("-" * 60)
    
    # อาคาร 6 ชั้นในเชียงใหม่ / 6-story building in Chiang Mai
    building_height = 20.0  # ความสูง 20 เมตร / Height 20m
    location = 'เชียงใหม่'
    
    summary = earthquake_calc.get_seismic_load_summary(location, building_height, SoilType.TYPE_C)
    
    print(f"ตำแหน่งที่ตั้ง / Location: {summary['location']}")
    print(f"โซนแผ่นดินไหว / Seismic Zone: {summary['zone']}")
    print(f"ความเร่งพื้นดินสูงสุด / Peak Ground Acceleration: {summary['peak_ground_acceleration_g']:.2f}g")
    print(f"ค่าสัมประสิทธิ์ดิน Fa / Site Coefficient Fa: {summary['site_coefficient_fa']:.2f}")
    print(f"ค่าสัมประสิทธิ์ดิน Fv / Site Coefficient Fv: {summary['site_coefficient_fv']:.2f}")
    print(f"ค่าสัมประสิทธิ์แผ่นดินไหว / Seismic Coefficient: {summary['seismic_coefficient']:.4f}")
    print(f"คาบธรรมชาติประมาณ / Approximate Period: {summary['fundamental_period_sec']:.3f} วินาที / seconds")
    print(f"แรงเฉือนฐานประมาณ / Estimated Base Shear: {summary['estimated_base_shear_kn']:.1f} kN")
    
    # ตัวอย่างที่ 3: การวิเคราะห์แรงแผ่นดินไหวครบถ้วน / Example 3: Complete earthquake analysis
    print(f"\n3. การวิเคราะห์แรงแผ่นดินไหวครบถ้วน / Complete Earthquake Analysis")
    print("-" * 60)
    
    # กำหนดข้อมูลอาคาร / Define building geometry
    building = BuildingGeometrySeismic(
        total_height=28.0,          # ความสูงรวม 28 เมตร / Total height 28m
        story_heights=[4.0] + [3.5] * 7,  # ชั้นล่าง 4m + ชั้นอื่น 3.5m / Ground floor 4m + others 3.5m
        story_weights=[1000.0] + [800.0] * 7,  # น้ำหนักแต่ละชั้น kN / Story weights kN
        plan_dimensions=(30.0, 25.0),  # ขนาดผัง 30x25 เมตร / Plan 30x25m
        structural_system=StructuralSystem.MOMENT_FRAME,  # ระบบโครงข้อแข็ง / Moment frame
        building_type="อาคารสำนักงาน / Office building",
        irregularity_factors={}  # ไม่มีความผิดปกติ / No irregularities
    )
    
    # วิเคราะห์แรงแผ่นดินไหว / Analyze earthquake load
    result = earthquake_calc.calculate_complete_seismic_analysis(
        location='เชียงใหม่',
        building_geometry=building,
        soil_type=SoilType.TYPE_C,  # ดินแน่นมาก / Very dense soil
        building_importance=BuildingImportance.STANDARD,  # อาคารทั่วไป / Standard building
        material='concrete'  # คอนกรีต / Concrete
    )
    
    print(f"ข้อมูลอาคาร / Building Information:")
    print(f"  ความสูง / Height: {building.total_height} m")
    print(f"  จำนวนชั้น / Number of Stories: {len(building.story_heights)}")
    print(f"  ขนาดผัง / Plan Dimensions: {building.plan_dimensions[0]} × {building.plan_dimensions[1]} m")
    print(f"  ระบบโครงสร้าง / Structural System: {building.structural_system.value.replace('_', ' ')}")
    print(f"  น้ำหนักรวม / Total Weight: {sum(building.story_weights):.0f} kN")
    print(f"")
    print(f"ผลลัพธ์การคำนวณ / Calculation Results:")
    print(f"  ความเร่งพื้นดินสูงสุด / Peak Ground Acceleration: {result.peak_ground_acceleration:.2f}g")
    print(f"  ค่าประกอบความสำคัญ / Importance Factor: {result.importance_factor:.2f}")
    print(f"  ค่าปรับลดแรง / Response Modification Factor: {result.response_modification:.1f}")
    print(f"  คาบธรรมชาติ / Fundamental Period: {result.fundamental_period:.3f} วินาที / seconds")
    print(f"  ค่าสัมประสิทธิ์แผ่นดินไหว / Seismic Coefficient: {result.seismic_coefficient:.4f}")
    print(f"  แรงเฉือนฐานออกแบบ / Design Base Shear: {result.design_base_shear:.1f} kN")
    
    # แสดงแรงแผ่นดินไหวแต่ละชั้น / Show story forces
    print(f"\n  แรงแผ่นดินไหวแต่ละชั้น / Story Forces:")
    print(f"  {'ชั้น':<6} {'แรง (kN)':<12} {'การเคลื่อนตัว (mm)':<18} {'อัตราส่วนเอียง'}")
    print(f"  {'Floor':<6} {'Force (kN)':<12} {'Displacement (mm)':<18} {'Drift Ratio'}")
    print(f"  {'-'*55}")
    
    for floor in sorted(result.story_forces.keys()):
        force = result.story_forces[floor]
        displacement = result.lateral_displacement.get(floor, 0)
        drift = result.drift_ratio.get(floor, 0)
        print(f"  {floor:<6} {force:<12.1f} {displacement:<18.1f} {drift:<12.4f}")
    
    # ตัวอย่างที่ 4: การสร้างรายงาน / Example 4: Report generation
    print(f"\n4. การสร้างรายงาน / Report Generation")
    print("-" * 60)
    
    # ข้อมูลโครงการ / Project information
    building_info = {
        'project_name': 'ตัวอย่างอาคารสำนักงาน 8 ชั้น เชียงใหม่',
        'location': 'เชียงใหม่',
        'date': '2024-01-15',
        'engineer': 'วิศวกรตัวอย่าง',
        'building_type': 'office'
    }
    
    # สร้างรายงาน / Generate report
    report = earthquake_calc.generate_seismic_load_report(result, building_info)
    
    print("รายงานถูกสร้างเรียบร้อยแล้ว / Report generated successfully")
    print(f"ความยาวรายงาน / Report length: {len(report)} ตัวอักษร / characters")
    
    # แสดงส่วนหัวของรายงาน / Show report header
    report_lines = report.split('\n')
    print("\nตัวอย่างรายงาน (10 บรรทัดแรก) / Sample Report (First 10 lines):")
    for i, line in enumerate(report_lines[:10]):
        print(line)
    print("... (รายงานต่อ / report continues)")
    
    # ตัวอย่างที่ 5: การเปรียบเทียบแรงแผ่นดินไหวในจังหวัดต่างๆ / Example 5: Seismic comparison
    print(f"\n5. การเปรียบเทียบแรงแผ่นดินไหวในจังหวัดต่างๆ / Seismic Force Comparison")
    print("-" * 60)
    
    comparison_provinces = [
        ('กรุงเทพมหานคร', 'Central Thailand - Low risk'),
        ('เชียงใหม่', 'Northern Thailand - High risk'),
        ('เชียงราย', 'Northern Thailand - High risk'),
        ('ขอนแก่น', 'Northeastern Thailand - Low risk')
    ]
    
    building_height_comparison = 25.0  # 25m building
    
    print(f"อาคารสูง {building_height_comparison} เมตร / {building_height_comparison}m building:")
    print(f"{'จังหวัด/Province':<20} {'Zone':<6} {'PGA':<8} {'แรงเฉือนฐาน/Base Shear':<20}")
    print(f"{'':20} {'':6} {'(g)':<8} {'(kN/m height)':<20}")
    print("-" * 60)
    
    for province, region in comparison_provinces:
        summary = earthquake_calc.get_seismic_load_summary(province, building_height_comparison)
        zone_letter = summary['zone'].split()[1]
        base_shear_per_height = summary['base_shear_per_height_kn_m']
        print(f"{province:<20} {zone_letter:<6} {summary['peak_ground_acceleration_g']:<8.2f} "
              f"{base_shear_per_height:<20.1f}")
    
    # ตัวอย่างที่ 6: การตรวจสอบขีดจำกัดการเอียง / Example 6: Drift limit check
    print(f"\n6. การตรวจสอบขีดจำกัดการเอียง / Drift Limit Check")
    print("-" * 60)
    
    # ขีดจำกัดการเอียงตามประเภทอาคาร / Drift limits by building type
    drift_limits = earthquake_calc.drift_limits
    max_drift = max(result.drift_ratio.values()) if result.drift_ratio else 0
    
    print("ขีดจำกัดการเอียงตามประเภทอาคาร / Drift Limits by Building Type:")
    for building_type, limit in drift_limits.items():
        print(f"  {building_type}: {limit:.1%}")
    
    print(f"\nอาคารสำนักงานนี้ / This Office Building:")
    print(f"การเอียงสูงสุด / Maximum Drift: {max_drift:.1%}")
    office_limit = drift_limits.get('office', 0.02)
    print(f"ขีดจำกัด / Limit: {office_limit:.1%}")
    
    if max_drift <= office_limit:
        print("✓ ผ่านการตรวจสอบ / PASS - Within acceptable limits")
    else:
        print("✗ ไม่ผ่านการตรวจสอบ / FAIL - Exceeds drift limit")
    
    print(f"\n=" * 80)
    print("สรุป / Summary:")
    print("✓ ไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทยพร้อมใช้งาน")
    print("✓ Thai Earthquake Load Library is ready for use")
    print("✓ รองรับการใช้งานในโครงการต่างๆ")
    print("✓ Supports use in various projects")
    print("✓ คำนวณตามมาตรฐานไทย มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1)")
    print("✓ Calculates according to TIS 1301/1302-61 (Revised Edition 1)")
    print("=" * 80)

if __name__ == "__main__":
    main()