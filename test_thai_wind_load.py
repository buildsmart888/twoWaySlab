#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Test Script for Thai Wind Load Library
การทดสอบไลบรารีการคำนวณแรงลมประเทศไทย

@author: Enhanced by AI Assistant
@date: 2024
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_wind_load_library():
    """Test Thai Wind Load Library functionality"""
    print("=" * 80)
    print("Thai Wind Load Library Test")
    print("การทดสอบไลบรารีการคำนวณแรงลมประเทศไทย")
    print("=" * 80)
    
    try:
        from thaiWindLoad import (
            ThaiWindLoad, TerrainCategory, WindZone, 
            BuildingType, BuildingGeometry
        )
        
        wind_calc = ThaiWindLoad()
        print("✓ Thai Wind Load Library loaded successfully")
        
        # Test 1: Wind zones and basic speeds
        print("\n1. Wind Zones and Basic Speeds (โซนลมและความเร็วพื้นฐาน)")
        print("-" * 60)
        
        test_locations = [
            'กรุงเทพมหานคร', 'เชียงใหม่', 'ขอนแก่น', 'สงขลา', 
            'ภูเก็ต', 'ระยอง', 'สุราษฎร์ธานี', 'นครราชสีมา'
        ]
        
        for location in test_locations:
            speed, desc = wind_calc.get_basic_wind_speed(location)
            speed_kmh = speed * 3.6
            print(f"{location:15}: {speed:4.1f} m/s ({speed_kmh:5.1f} km/h) - {desc}")
        
        # Test 2: Terrain factors
        print(f"\n2. Terrain Factors (ค่าประกอบภูมิประเทศ)")
        print("-" * 60)
        
        test_heights = [10, 20, 30, 50, 100]  # meters
        terrains = [
            (TerrainCategory.CATEGORY_I, 'ภูมิประเทศเปิด'),
            (TerrainCategory.CATEGORY_II, 'ภูมิประเทศขรุขระ'),
            (TerrainCategory.CATEGORY_III, 'ภูมิประเทศเมือง'),
            (TerrainCategory.CATEGORY_IV, 'ภูมิประเทศเมืองหนาแน่น')
        ]
        
        print(f"{'Height (m)':<10}", end="")
        for terrain, name in terrains:
            print(f"{terrain.value:<8}", end="")
        print()
        print("-" * 50)
        
        for height in test_heights:
            print(f"{height:<10}", end="")
            for terrain, name in terrains:
                kr = wind_calc.calculate_terrain_factor(height, terrain)
                print(f"{kr:<8.3f}", end="")
            print()
        
        # Test 3: Building importance factors
        print(f"\n3. Building Importance Factors (ค่าประกอบความสำคัญอาคาร)")
        print("-" * 60)
        
        for building_type in BuildingType:
            factor_info = wind_calc.importance_factors[building_type]
            print(f"{building_type.value:<12}: {factor_info['factor']:<4.2f} - {factor_info['description']}")
        
        # Test 4: Complete wind analysis example
        print(f"\n4. Complete Wind Analysis Example (ตัวอย่างการวิเคราะห์แรงลมครบถ้วน)")
        print("-" * 60)
        
        # Example building: 8-story office building in Bangkok
        building = BuildingGeometry(
            height=30.0,        # 30m height
            width=25.0,         # 25m width
            depth=20.0,         # 20m depth
            roof_angle=0,       # Flat roof
            building_type="office",
            exposure_category=TerrainCategory.CATEGORY_III  # Urban terrain
        )
        
        result = wind_calc.calculate_complete_wind_analysis(
            location='กรุงเทพมหานคร',
            building_geometry=building,
            building_type=BuildingType.STANDARD,
            topography='flat'
        )
        
        print(f"Building: 8-story office building in Bangkok")
        print(f"Dimensions: {building.height}m H × {building.width}m W × {building.depth}m D")
        print(f"")
        print(f"Basic Wind Speed: {result.basic_wind_speed:.1f} m/s")
        print(f"Design Wind Speed: {result.design_wind_speed:.1f} m/s")
        print(f"Design Wind Pressure: {result.design_wind_pressure:.1f} Pa ({result.design_wind_pressure/1000:.2f} kPa)")
        print(f"")
        print(f"Factors:")
        print(f"  Terrain Factor (Kr): {result.terrain_factor:.3f}")
        print(f"  Topographic Factor (Kt): {result.topographic_factor:.3f}")
        print(f"  Importance Factor (Ki): {result.importance_factor:.3f}")
        print(f"")
        print(f"Pressure Coefficients:")
        for surface, cp in result.pressure_coefficients.items():
            surface_thai = {
                'windward_wall': 'ผนังรับลม',
                'leeward_wall': 'ผนังหลังลม',
                'side_walls': 'ผนังข้าง',
                'roof_windward': 'หลังคาด้านรับลม',
                'roof_leeward': 'หลังคาด้านหลังลม'
            }.get(surface, surface)
            print(f"  {surface_thai} ({surface}): Cp = {cp:+.2f}")
        print(f"")
        print(f"Total Wind Force: {result.total_wind_force:.0f} N ({result.total_wind_force/1000:.1f} kN)")
        
        # Test 5: Wind load summary for different locations
        print(f"\n5. Wind Load Summary for Different Locations")
        print("-" * 60)
        
        building_height = 25.0  # 25m building
        summary_locations = ['กรุงเทพมหานคร', 'เชียงใหม่', 'ภูเก็ต', 'สงขลา']
        
        print(f"Building Height: {building_height} m")
        print(f"{'Location':<15} {'Zone':<8} {'Speed':<12} {'Pressure':<12} {'Force/m²'}")
        print(f"{'':15} {'':8} {'(m/s)':<12} {'(kPa)':<12} {'(kgf/m²)'}")
        print("-" * 65)
        
        for location in summary_locations:
            summary = wind_calc.get_wind_load_summary(location, building_height)
            print(f"{location:<15} {summary['zone'].split()[1]:<8} "
                  f"{summary['basic_wind_speed_ms']:<12.1f} "
                  f"{summary['design_pressure_kpa']:<12.2f} "
                  f"{summary['force_per_sqm_kgf']:<12.1f}")
        
        # Test 6: Generate detailed report
        print(f"\n6. Sample Wind Load Report")
        print("-" * 60)
        
        building_info = {
            'project_name': 'ตัวอย่างอาคารสำนักงาน 8 ชั้น',
            'location': 'กรุงเทพมหานคร',
            'date': '2024-01-15'
        }
        
        report = wind_calc.generate_wind_load_report(result, building_info)
        print(report)
        
        # Test 7: Ministry Regulation integration test
        print(f"\n7. Integration with Ministry Regulation (if available)")
        print("-" * 60)
        
        try:
            from thaiMinistryReg import ThaiMinistryRegulation2566
            ministry_reg = ThaiMinistryRegulation2566()
            
            # Test load combination with wind load
            loads = {
                'D': 5.0,   # Dead load (kN/m²)
                'L': 3.0,   # Live load (kN/m²)
                'W': result.design_wind_pressure / 1000,  # Wind load (kN/m²)
                'E': 0.0    # Earthquake load (kN/m²)
            }
            
            combinations = ministry_reg.check_load_combination(loads, 'ultimate')
            print("✓ Ministry Regulation integration available")
            print(f"Wind pressure used in load combinations: {loads['W']:.2f} kN/m²")
            print("Load combinations with wind:")
            for combo in combinations[:3]:  # Show first 3 combinations
                if 'W' in combo['formula']:
                    print(f"  {combo['name']}: {combo['formula']} = {combo['result']:.2f} kN/m²")
            
        except ImportError:
            print("⚠ Ministry Regulation module not available for integration test")
        
        assert True  # Test passed
        
    except Exception as e:
        print(f"✗ Error in wind load library test: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Wind load library test failed: {e}"

def test_practical_wind_examples():
    """Test practical wind load examples"""
    print("\n" + "=" * 80)
    print("Practical Wind Load Examples")
    print("ตัวอย่างการคำนวณแรงลมเชิงปฏิบัติ")
    print("=" * 80)
    
    try:
        from thaiWindLoad import ThaiWindLoad, TerrainCategory, BuildingType, BuildingGeometry
        
        wind_calc = ThaiWindLoad()
        
        # Example 1: High-rise residential building in Bangkok
        print("\nExample 1: High-rise Residential Building in Bangkok")
        print("ตัวอย่างที่ 1: อาคารที่พักอาศัยสูงในกรุงเทพฯ")
        print("-" * 60)
        
        building1 = BuildingGeometry(
            height=60.0, width=30.0, depth=25.0, roof_angle=0,
            building_type="residential", exposure_category=TerrainCategory.CATEGORY_III
        )
        
        result1 = wind_calc.calculate_complete_wind_analysis(
            location='กรุงเทพมหานคร',
            building_geometry=building1,
            building_type=BuildingType.STANDARD
        )
        
        print(f"Building: {building1.height}m high residential tower")
        print(f"Wind pressure: {result1.design_wind_pressure:.1f} Pa")
        print(f"Wind force on facade: {result1.total_wind_force/1000:.1f} kN")
        
        # Example 2: Hospital in Chiang Mai
        print("\nExample 2: Hospital in Chiang Mai (Important Building)")
        print("ตัวอย่างที่ 2: โรงพยาบาลในเชียงใหม่ (อาคารสำคัญ)")
        print("-" * 60)
        
        building2 = BuildingGeometry(
            height=25.0, width=50.0, depth=40.0, roof_angle=0,
            building_type="hospital", exposure_category=TerrainCategory.CATEGORY_II
        )
        
        result2 = wind_calc.calculate_complete_wind_analysis(
            location='เชียงใหม่',
            building_geometry=building2,
            building_type=BuildingType.IMPORTANT  # Higher importance factor
        )
        
        print(f"Building: {building2.height}m hospital building")
        print(f"Importance factor: {result2.importance_factor:.2f} (increased for important facility)")
        print(f"Wind pressure: {result2.design_wind_pressure:.1f} Pa")
        print(f"Wind force on facade: {result2.total_wind_force/1000:.1f} kN")
        
        # Example 3: Coastal hotel in Phuket
        print("\nExample 3: Coastal Hotel in Phuket (High Wind Zone)")
        print("ตัวอย่างที่ 3: โรงแรมชายฝั่งในภูเก็ต (พื้นที่ลมแรง)")
        print("-" * 60)
        
        building3 = BuildingGeometry(
            height=45.0, width=80.0, depth=30.0, roof_angle=0,
            building_type="hotel", exposure_category=TerrainCategory.CATEGORY_I  # Open terrain near coast
        )
        
        result3 = wind_calc.calculate_complete_wind_analysis(
            location='ภูเก็ต',
            building_geometry=building3,
            building_type=BuildingType.STANDARD,
            topography='flat'
        )
        
        print(f"Building: {building3.height}m coastal hotel")
        print(f"Basic wind speed: {result3.basic_wind_speed:.1f} m/s (coastal zone)")
        print(f"Terrain factor: {result3.terrain_factor:.3f} (open terrain)")
        print(f"Wind pressure: {result3.design_wind_pressure:.1f} Pa")
        print(f"Wind force on facade: {result3.total_wind_force/1000:.1f} kN")
        
        # Comparison summary
        print(f"\nComparison Summary")
        print("-" * 60)
        examples = [
            ("Bangkok Residential", result1),
            ("Chiang Mai Hospital", result2),
            ("Phuket Hotel", result3)
        ]
        
        print(f"{'Building':<20} {'Wind Speed':<12} {'Pressure':<12} {'Force'}")
        print(f"{'':20} {'(m/s)':<12} {'(Pa)':<12} {'(kN)'}")
        print("-" * 55)
        
        for name, result in examples:
            print(f"{name:<20} {result.design_wind_speed:<12.1f} "
                  f"{result.design_wind_pressure:<12.0f} "
                  f"{result.total_wind_force/1000:<12.0f}")
        
        assert True  # Test passed
        
    except Exception as e:
        print(f"✗ Error in practical examples: {e}")
        assert False, f"Practical examples test failed: {e}"

def main():
    """ฟังก์ชันทดสอบหลัก / Main test function"""
    print("การทดสอบไลบรารีการคำนวณแรงลมประเทศไทยอย่างครบถ้วน")
    print("Thai Wind Load Library Comprehensive Test")
    print("ตามกฎกระทรวง พ.ศ. 2566 และ มยผ. 1311-50")
    print("Based on Ministry Regulation B.E. 2566 + TIS 1311-50")
    
    test_results = []
    
    # Test 1: Basic library functionality
    result1 = test_wind_load_library()
    test_results.append(("Wind Load Library", result1))
    
    # Test 2: Practical examples
    result2 = test_practical_wind_examples()
    test_results.append(("Practical Examples", result2))
    
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
        print("🎉 ALL TESTS PASSED! Thai Wind Load Library is ready to use.")
        print("📚 The library can now be used in other projects.")
        print("\nUsage example:")
        print("```python")
        print("from thaiWindLoad import ThaiWindLoad, BuildingType, TerrainCategory")
        print("wind_calc = ThaiWindLoad()")
        print("summary = wind_calc.get_wind_load_summary('กรุงเทพมหานคร', 30.0)")
        print("```")
    else:
        print(f"⚠️ {total - passed} test(s) failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)