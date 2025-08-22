#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
ตัวอย่างการใช้งานไลบรารีการคำนวณแรงลมประเทศไทย
Example Usage of Thai Wind Load Calculation Library

@author: Enhanced by AI Assistant
@date: 2024
"""

from thaiWindLoad import (
    ThaiWindLoad, 
    TerrainCategory, 
    WindZone, 
    BuildingType, 
    BuildingGeometry
)

def main():
    """ตัวอย่างการใช้งานหลัก / Main usage examples"""
    
    print("=" * 70)
    print("ตัวอย่างการใช้งานไลบรารีการคำนวณแรงลมประเทศไทย")
    print("Thai Wind Load Library Usage Examples")
    print("=" * 70)
    
    # เริ่มต้นเครื่องคำนวณ / Initialize calculator
    wind_calc = ThaiWindLoad()
    
    # ตัวอย่างที่ 1: การดูความเร็วลมพื้นฐาน / Example 1: Basic wind speed lookup
    print("\n1. การดูความเร็วลมพื้นฐาน / Basic Wind Speed Lookup")
    print("-" * 50)
    
    provinces = ['กรุงเทพมหานคร', 'เชียงใหม่', 'ขอนแก่น', 'ภูเก็ต', 'สงขลา']
    
    for province in provinces:
        speed, zone_desc = wind_calc.get_basic_wind_speed(province)
        print(f"{province}: {speed} m/s ({zone_desc})")
    
    # ตัวอย่างที่ 2: การคำนวณแรงลมอย่างรวดเร็ว / Example 2: Quick wind load calculation
    print(f"\n2. การคำนวณแรงลมอย่างรวดเร็ว / Quick Wind Load Calculation")
    print("-" * 50)
    
    # อาคาร 8 ชั้นในกรุงเทพฯ / 8-story building in Bangkok
    building_height = 25.0  # ความสูง 25 เมตร / Height 25m
    location = 'กรุงเทพมหานคร'
    
    summary = wind_calc.get_wind_load_summary(location, building_height)
    
    print(f"ตำแหน่งที่ตั้ง / Location: {summary['location']}")
    print(f"โซนลม / Wind Zone: {summary['zone']}")
    print(f"ความเร็วลมพื้นฐาน / Basic Wind Speed: {summary['basic_wind_speed_ms']:.1f} m/s ({summary['basic_wind_speed_kmh']:.1f} km/h)")
    print(f"แรงดันลมออกแบบ / Design Wind Pressure: {summary['design_pressure_kpa']:.2f} kPa")
    print(f"แรงต่อตารางเมตร / Force per m²: {summary['force_per_sqm_kgf']:.1f} kgf/m²")
    
    # ตัวอย่างที่ 3: การวิเคราะห์แรงลมครบถ้วน / Example 3: Complete wind load analysis
    print(f"\n3. การวิเคราะห์แรงลมครบถ้วน / Complete Wind Load Analysis")
    print("-" * 50)
    
    # กำหนดข้อมูลอาคาร / Define building geometry
    building = BuildingGeometry(
        height=30.0,          # ความสูง 30 เมตร / Height 30m
        width=25.0,           # ความกว้าง 25 เมตร / Width 25m
        depth=20.0,           # ความลึก 20 เมตร / Depth 20m
        roof_angle=0,         # หลังคาเรียบ / Flat roof
        building_type="อาคารสำนักงาน / Office building",
        exposure_category=TerrainCategory.CATEGORY_III  # ภูมิประเทศเมือง / Urban terrain
    )
    
    # วิเคราะห์แรงลม / Analyze wind load
    result = wind_calc.calculate_complete_wind_analysis(
        location='กรุงเทพมหานคร',
        building_geometry=building,
        building_type=BuildingType.STANDARD  # อาคารทั่วไป / Standard building
    )
    
    print(f"ข้อมูลอาคาร / Building Information:")
    print(f"  ขนาด / Dimensions: {building.height}m × {building.width}m × {building.depth}m")
    print(f"  ประเภท / Type: {building.building_type}")
    print(f"")
    print(f"ผลลัพธ์การคำนวณ / Calculation Results:")
    print(f"  ความเร็วลมพื้นฐาน / Basic Wind Speed: {result.basic_wind_speed:.1f} m/s")
    print(f"  ความเร็วลมออกแบบ / Design Wind Speed: {result.design_wind_speed:.1f} m/s")
    print(f"  แรงดันลมออกแบบ / Design Wind Pressure: {result.design_wind_pressure:.1f} Pa")
    print(f"")
    print(f"ค่าประกอบต่างๆ / Factors:")
    print(f"  ค่าประกอบภูมิประเทศ / Terrain Factor (Kr): {result.terrain_factor:.3f}")
    print(f"  ค่าประกอบภูมิทัศน์ / Topographic Factor (Kt): {result.topographic_factor:.3f}")
    print(f"  ค่าประกอบความสำคัญ / Importance Factor (Ki): {result.importance_factor:.3f}")
    print(f"")
    print(f"แรงลมรวม / Total Wind Force: {result.total_wind_force:.0f} N ({result.total_wind_force/1000:.1f} kN)")
    
    # ตัวอย่างที่ 4: การสร้างรายงาน / Example 4: Report generation
    print(f"\n4. การสร้างรายงาน / Report Generation")
    print("-" * 50)
    
    # ข้อมูลโครงการ / Project information
    building_info = {
        'project_name': 'ตัวอย่างอาคารสำนักงาน 8 ชั้น กรุงเทพฯ',
        'location': 'กรุงเทพมหานคร',
        'date': '2024-01-15',
        'engineer': 'วิศวกรตัวอย่าง'
    }
    
    # สร้างรายงาน / Generate report
    report = wind_calc.generate_wind_load_report(result, building_info)
    
    print("รายงานถูกสร้างเรียบร้อยแล้ว / Report generated successfully")
    print(f"ความยาวรายงาน / Report length: {len(report)} ตัวอักษร / characters")
    
    # แสดงส่วนหัวของรายงาน / Show report header
    report_lines = report.split('\n')
    print("\nตัวอย่างรายงาน (10 บรรทัดแรก) / Sample Report (First 10 lines):")
    for i, line in enumerate(report_lines[:10]):
        print(line)
    print("... (รายงานต่อ / report continues)")
    
    # ตัวอย่างที่ 5: การเปรียบเทียบแรงลมในจังหวัดต่างๆ / Example 5: Wind load comparison
    print(f"\n5. การเปรียบเทียบแรงลมในจังหวัดต่างๆ / Wind Load Comparison")
    print("-" * 50)
    
    comparison_provinces = [
        ('กรุงเทพมหานคร', 'Central Thailand'),
        ('เชียงใหม่', 'Northern Thailand'),
        ('ภูเก็ต', 'Coastal (Andaman)'),
        ('สงขลา', 'Coastal (Gulf)')
    ]
    
    building_height_comparison = 30.0  # 30m building
    
    print(f"อาคารสูง {building_height_comparison} เมตร / {building_height_comparison}m building:")
    print(f"{'จังหวัด/Province':<15} {'Zone':<6} {'ความเร็วลม/Wind Speed':<20} {'แรงดัน/Pressure':<15} {'แรง/Force'}")
    print(f"{'':15} {'':6} {'(m/s)':<20} {'(kPa)':<15} {'(kgf/m²)'}")
    print("-" * 80)
    
    for province, region in comparison_provinces:
        summary = wind_calc.get_wind_load_summary(province, building_height_comparison)
        zone_num = summary['zone'].split()[1]
        print(f"{province:<15} {zone_num:<6} {summary['basic_wind_speed_ms']:<20.1f} "
              f"{summary['design_pressure_kpa']:<15.2f} {summary['force_per_sqm_kgf']:<15.1f}")
    
    print(f"\n=" * 70)
    print("สรุป / Summary:")
    print("✓ ไลบรารีการคำนวณแรงลมประเทศไทยพร้อมใช้งาน")
    print("✓ Thai Wind Load Library is ready for use")
    print("✓ รองรับการใช้งานในโครงการต่างๆ")
    print("✓ Supports use in various projects")
    print("✓ คำนวณตามมาตรฐานไทย กฎกระทรวง พ.ศ. 2566 และ มยผ. 1311-50")
    print("✓ Calculates according to Thai standards: Ministry Regulation B.E. 2566 and TIS 1311-50")
    print("=" * 70)

if __name__ == "__main__":
    main()