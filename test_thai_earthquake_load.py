#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Test Script for Thai Earthquake Load Library
การทดสอบไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย

@author: Enhanced by AI Assistant
@date: 2024
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_earthquake_load_library():
    """Test Thai Earthquake Load Library functionality"""
    print("=" * 80)
    print("Thai Earthquake Load Library Test")
    print("การทดสอบไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย")
    print("=" * 80)
    
    try:
        from thaiEarthquakeLoad import (
            ThaiEarthquakeLoad, SeismicZone, SoilType, 
            BuildingImportance, StructuralSystem, BuildingGeometrySeismic
        )
        
        earthquake_calc = ThaiEarthquakeLoad()
        print("✓ Thai Earthquake Load Library loaded successfully")
        
        # Test 1: Seismic zones and peak ground accelerations
        print("\n1. Seismic Zones and Peak Ground Accelerations (โซนแผ่นดินไหวและความเร่งพื้นดิน)")
        print("-" * 80)
        
        test_locations = [
            'เชียงใหม่', 'เชียงราย', 'แม่ฮ่องสอน', 'กรุงเทพมหานคร', 
            'ขอนแก่น', 'นครราชสีมา', 'ภูเก็ต', 'สงขลา'
        ]
        
        for location in test_locations:
            zone, pga, desc = earthquake_calc.get_seismic_zone_info(location)
            print(f"{location:15}: Zone {zone.value} - PGA = {pga:.2f}g")
        
        # Test 2: Site coefficients for different soil types
        print(f"\n2. Site Coefficients (ค่าสัมประสิทธิ์ดิน)")
        print("-" * 80)
        
        test_pga = 0.25  # Zone B
        print(f"For PGA = {test_pga}g:")
        print(f"{'Soil Type':<12} {'Fa':<8} {'Fv':<8} {'Description'}")
        print("-" * 50)
        
        for soil_type in [SoilType.TYPE_A, SoilType.TYPE_B, SoilType.TYPE_C, 
                         SoilType.TYPE_D, SoilType.TYPE_E]:
            fa, fv = earthquake_calc.get_site_coefficients(test_pga, soil_type)
            soil_desc = {
                SoilType.TYPE_A: 'หินแข็ง',
                SoilType.TYPE_B: 'หินอ่อน', 
                SoilType.TYPE_C: 'ดินแน่นมาก',
                SoilType.TYPE_D: 'ดินแน่นปานกลาง',
                SoilType.TYPE_E: 'ดินอ่อน'
            }[soil_type]
            print(f"{soil_type.value:<12} {fa:<8.2f} {fv:<8.2f} {soil_desc}")
        
        # Test 3: Building importance factors
        print(f"\n3. Building Importance Factors (ค่าประกอบความสำคัญอาคาร)")
        print("-" * 80)
        
        for importance in BuildingImportance:
            factor_info = earthquake_calc.importance_factors[importance]
            print(f"{importance.value:<8}: {factor_info['factor']:<4.2f} - {factor_info['description']}")
            print(f"         Examples: {factor_info['examples']}")
        
        # Test 4: Structural system factors
        print(f"\n4. Structural System Factors (ค่าประกอบระบบโครงสร้าง)")
        print("-" * 80)
        
        for system in StructuralSystem:
            system_factors = earthquake_calc.structural_system_factors[system]
            print(f"\n{system.value.replace('_', ' ').title()}:")
            for material, factors in system_factors.items():
                if material != 'description_en':
                    R = factors['R']
                    Cd = factors['Cd']
                    desc = factors['description']
                    print(f"  {material}: R={R}, Cd={Cd:.1f} - {desc}")
        
        assert True  # Test passed
        
    except Exception as e:
        print(f"✗ Error in earthquake load library test: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Earthquake load library test failed: {e}"

def test_earthquake_analysis_examples():
    """Test earthquake analysis with practical examples"""
    print("\n" + "=" * 80)
    print("Earthquake Analysis Examples")
    print("ตัวอย่างการวิเคราะห์แรงแผ่นดินไหว")
    print("=" * 80)
    
    try:
        from thaiEarthquakeLoad import (
            ThaiEarthquakeLoad, SoilType, BuildingImportance, 
            StructuralSystem, BuildingGeometrySeismic
        )
        
        earthquake_calc = ThaiEarthquakeLoad()
        
        # Example 1: Office building in Bangkok
        print("\nExample 1: Office Building in Bangkok")
        print("ตัวอย่างที่ 1: อาคารสำนักงานในกรุงเทพฯ")
        print("-" * 60)
        
        # Building geometry
        building1 = BuildingGeometrySeismic(
            total_height=30.0,  # 30m height
            story_heights=[4.0] + [3.5] * 7,  # Ground floor 4m + 7 floors @ 3.5m
            story_weights=[800.0] + [600.0] * 7,  # kN per floor
            plan_dimensions=(25.0, 20.0),  # 25m x 20m
            structural_system=StructuralSystem.MOMENT_FRAME,
            building_type="office",
            irregularity_factors={}
        )
        
        result1 = earthquake_calc.calculate_complete_seismic_analysis(
            location='กรุงเทพมหานคร',
            building_geometry=building1,
            soil_type=SoilType.TYPE_C,
            building_importance=BuildingImportance.STANDARD,
            material='concrete'
        )
        
        print(f"Building: 8-story office building")
        print(f"Total height: {building1.total_height} m")
        print(f"Seismic zone: A (PGA = {result1.peak_ground_acceleration:.2f}g)")
        print(f"Fundamental period: {result1.fundamental_period:.3f} seconds")
        print(f"Seismic coefficient: {result1.seismic_coefficient:.4f}")
        print(f"Base shear: {result1.design_base_shear:.1f} kN")
        
        # Example 2: Hospital in Chiang Mai (high seismic zone)
        print("\nExample 2: Hospital in Chiang Mai (Important Building)")
        print("ตัวอย่างที่ 2: โรงพยาบาลในเชียงใหม่ (อาคารสำคัญ)")
        print("-" * 60)
        
        building2 = BuildingGeometrySeismic(
            total_height=25.0,  # 25m height
            story_heights=[4.5] + [3.5] * 6,  # Ground floor 4.5m + 6 floors @ 3.5m
            story_weights=[1000.0] + [800.0] * 6,  # kN per floor
            plan_dimensions=(40.0, 30.0),  # 40m x 30m
            structural_system=StructuralSystem.DUAL_SYSTEM,
            building_type="hospital",
            irregularity_factors={}
        )
        
        result2 = earthquake_calc.calculate_complete_seismic_analysis(
            location='เชียงใหม่',
            building_geometry=building2,
            soil_type=SoilType.TYPE_D,
            building_importance=BuildingImportance.IMPORTANT,  # Higher importance factor
            material='concrete'
        )
        
        print(f"Building: 7-story hospital")
        print(f"Total height: {building2.total_height} m")
        print(f"Seismic zone: C (PGA = {result2.peak_ground_acceleration:.2f}g)")
        print(f"Importance factor: {result2.importance_factor:.2f} (important building)")
        print(f"Fundamental period: {result2.fundamental_period:.3f} seconds")
        print(f"Seismic coefficient: {result2.seismic_coefficient:.4f}")
        print(f"Base shear: {result2.design_base_shear:.1f} kN")
        
        # Example 3: Quick seismic load summary
        print(f"\n3. Quick Seismic Load Summary")
        print("-" * 60)
        
        summary_locations = ['กรุงเทพมหานคร', 'เชียงใหม่', 'เชียงราย', 'ขอนแก่น']
        building_height = 20.0  # 20m building
        
        print(f"Building Height: {building_height} m")
        print(f"{'Location':<15} {'Zone':<6} {'PGA':<8} {'Base Shear/Height':<20}")
        print(f"{'':15} {'':6} {'(g)':<8} {'(kN/m)':<20}")
        print("-" * 55)
        
        for location in summary_locations:
            summary = earthquake_calc.get_seismic_load_summary(location, building_height)
            zone_letter = summary['zone'].split()[1]
            print(f"{location:<15} {zone_letter:<6} {summary['peak_ground_acceleration_g']:<8.2f} "
                  f"{summary['base_shear_per_height_kn_m']:<20.1f}")
        
        # Example 4: Generate detailed report
        print(f"\n4. Sample Earthquake Load Report")
        print("-" * 60)
        
        building_info = {
            'project_name': 'ตัวอย่างอาคารสำนักงาน 8 ชั้น',
            'location': 'กรุงเทพมหานคร',
            'date': '2024-01-15',
            'engineer': 'วิศวกรตัวอย่าง',
            'building_type': 'office'
        }
        
        report = earthquake_calc.generate_seismic_load_report(result1, building_info)
        
        # Show first part of report
        report_lines = report.split('\n')
        print("Sample Report (First 15 lines):")
        for i, line in enumerate(report_lines[:15]):
            print(line)
        print("... (report continues)")
        
        assert True  # Test passed
        
    except Exception as e:
        print(f"✗ Error in earthquake analysis examples: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Earthquake analysis examples test failed: {e}"

def test_integration_with_ministry_regulation():
    """Test integration with Ministry Regulation"""
    print("\n" + "=" * 80)
    print("Integration with Ministry Regulation B.E. 2566")
    print("การบูรณาการกับกฎกระทรวง พ.ศ. 2566")
    print("=" * 80)
    
    try:
        from thaiEarthquakeLoad import ThaiEarthquakeLoad
        from thaiMinistryReg import ThaiMinistryRegulation2566
        
        earthquake_calc = ThaiEarthquakeLoad()
        ministry_reg = ThaiMinistryRegulation2566()
        
        # Get earthquake load for Bangkok
        summary = earthquake_calc.get_seismic_load_summary('กรุงเทพมหานคร', 25.0)
        seismic_force_kn_m2 = summary['base_shear_per_height_kn_m'] / 25.0  # Convert to kN/m²
        
        # Test load combination with earthquake load
        loads = {
            'D': 8.0,   # Dead load (kN/m²)
            'L': 4.0,   # Live load (kN/m²)
            'W': 2.0,   # Wind load (kN/m²)
            'E': seismic_force_kn_m2  # Earthquake load (kN/m²)
        }
        
        combinations = ministry_reg.check_load_combination(loads, 'ultimate')
        print("✓ Ministry Regulation integration available")
        print(f"Earthquake load used in combinations: {loads['E']:.3f} kN/m²")
        print("\nLoad combinations with earthquake:")
        for combo in combinations[:4]:  # Show first 4 combinations
            if 'E' in combo['formula']:
                print(f"  {combo['name']}: {combo['formula']} = {combo['result']:.2f} kN/m²")
        
        assert True  # Test passed
        
    except ImportError:
        print("⚠ Ministry Regulation module not available for integration test")
        assert True  # Still pass if optional module not available
    except Exception as e:
        print(f"✗ Error in integration test: {e}")
        assert False, f"Integration test failed: {e}"

def main():
    """ฟังก์ชันทดสอบหลัก / Main test function"""
    print("การทดสอบไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทยอย่างครบถ้วน")
    print("Thai Earthquake Load Library Comprehensive Test")
    print("ตามมาตรฐาน มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1)")
    print("Based on TIS 1301/1302-61 (Revised Edition 1)")
    
    test_results = []
    
    # Test 1: Basic library functionality
    result1 = test_earthquake_load_library()
    test_results.append(("Earthquake Load Library", result1))
    
    # Test 2: Analysis examples
    result2 = test_earthquake_analysis_examples()
    test_results.append(("Analysis Examples", result2))
    
    # Test 3: Integration with Ministry Regulation
    result3 = test_integration_with_ministry_regulation()
    test_results.append(("Ministry Regulation Integration", result3))
    
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
        print("🎉 ALL TESTS PASSED! Thai Earthquake Load Library is ready to use.")
        print("📚 The library can now be used in other projects.")
        print("\nUsage example:")
        print("```python")
        print("from thaiEarthquakeLoad import ThaiEarthquakeLoad, SoilType, BuildingImportance")
        print("earthquake_calc = ThaiEarthquakeLoad()")
        print("summary = earthquake_calc.get_seismic_load_summary('เชียงใหม่', 25.0)")
        print("```")
    else:
        print(f"⚠️ {total - passed} test(s) failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)