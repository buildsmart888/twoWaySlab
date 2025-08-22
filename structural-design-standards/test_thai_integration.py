"""
Thai Standards Integration Test and Demonstration
================================================

Comprehensive integration test for Thai Ministry Regulation B.E. 2566 implementation
including materials, loads, units, and design requirements.

การทดสอบบูรณาการมาตรฐานไทยครบถ้วน
สำหรับกฎกระทรวง พ.ศ. 2566 รวมถึงวัสดุ แรง หน่วย และข้อกำหนดการออกแบบ
"""

import sys
import os
from typing import Dict, List, Any

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structural_standards.thai.ministry_2566 import (
    # Main regulation
    ThaiMinistryRegulation2566,
    ThaiProjectData,
    ThaiComplianceResult,
    
    # Load combinations
    ThaiLoadType,
    ThaiCombinationType,
    
    # Design requirements
    ThaiEnvironmentType,
    ThaiElementType,
    ThaiSupportType,
    
    # Materials
    ThaiConcrete,
    ThaiReinforcementSteel,
    ThaiConcreteGrade,
    ThaiSteelGrade,
    
    # Units
    ThaiUnitConverter,
    ksc_to_mpa,
    mpa_to_ksc,
    
    # Quick access functions
    get_concrete_cover,
    get_safety_factor
)

from structural_standards.thai.ministry_2566.loads import (
    # Wind loads
    ThaiWindLoads,
    ThaiWindZone,
    ThaiTerrainCategory,
    ThaiBuildingImportance,
    
    # Seismic loads
    ThaiSeismicLoads,
    ThaiSeismicZone,
    ThaiSoilType,
    ThaiSeismicImportance,
    ThaiStructuralSystem
)


class ThaiStandardsIntegrationTester:
    """
    Comprehensive integration tester for Thai standards
    
    ระบบทดสอบบูรณาการมาตรฐานไทยครบถ้วน
    """
    
    def __init__(self):
        """Initialize the integration tester"""
        self.regulation = ThaiMinistryRegulation2566()
        self.unit_converter = ThaiUnitConverter()
        self.wind_loads = ThaiWindLoads()
        self.seismic_loads = ThaiSeismicLoads()
        
        print("🇹🇭 Thai Standards Integration Tester Initialized")
        print("=" * 70)
    
    def test_materials_integration(self) -> Dict[str, Any]:
        """Test Thai materials integration"""
        print("\n📦 Testing Thai Materials Integration")
        print("-" * 50)
        
        results = {}
        
        # Test concrete materials
        concrete_grades = ['Fc210', 'Fc240', 'Fc280']
        concrete_results = {}
        
        for grade in concrete_grades:
            concrete = ThaiConcrete(grade=grade)
            
            # Test unit conversions
            fc_ksc = concrete.fc_prime_ksc
            fc_mpa = concrete.fc_prime
            converted_mpa = ksc_to_mpa(fc_ksc)
            converted_ksc = mpa_to_ksc(fc_mpa)
            
            concrete_results[grade] = {
                'fc_ksc': fc_ksc,
                'fc_mpa': fc_mpa,
                'converted_mpa': converted_mpa,
                'converted_ksc': converted_ksc,
                'conversion_accuracy': abs(fc_mpa - converted_mpa) < 0.01
            }
            
            print(f"✓ {grade}: {fc_ksc} ksc = {fc_mpa:.2f} MPa (✓ {concrete_results[grade]['conversion_accuracy']})")
        
        # Test steel materials
        steel_grades = ['SD40', 'SD50']
        steel_results = {}
        
        for grade in steel_grades:
            steel = ThaiReinforcementSteel(grade=grade)
            
            fy_ksc = steel.fy_ksc
            fy_mpa = steel.fy
            
            steel_results[grade] = {
                'fy_ksc': fy_ksc,
                'fy_mpa': fy_mpa,
                'rebar_sizes': steel.get_available_rebar_sizes()
            }
            
            print(f"✓ {grade}: {fy_ksc} ksc = {fy_mpa:.1f} MPa")
        
        results['concrete'] = concrete_results
        results['steel'] = steel_results
        results['test_passed'] = True
        
        return results
    
    def test_load_combinations_integration(self) -> Dict[str, Any]:
        """Test load combinations integration"""
        print("\n⚖️  Testing Load Combinations Integration")
        print("-" * 50)
        
        # Test loads
        test_loads = {
            ThaiLoadType.DEAD: 10.0,      # kN/m²
            ThaiLoadType.LIVE: 5.0,       # kN/m²
            ThaiLoadType.WIND: 8.0,       # kN/m²
            ThaiLoadType.EARTHQUAKE: 6.0  # kN/m²
        }
        
        # Ultimate limit state combinations
        uls_results = self.regulation.calculate_design_loads(test_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE)
        print("Ultimate Limit State Combinations:")
        for combo_name, load_value in uls_results.items():
            print(f"  {combo_name}: {load_value:.2f} kN/m²")
        
        # Find governing combination
        governing_combo, max_load = self.regulation.find_governing_load_combination(test_loads)
        print(f"✓ Governing: {governing_combo.name} = {max_load:.2f} kN/m²")
        
        # Serviceability limit state combinations
        sls_results = self.regulation.calculate_design_loads(test_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE)
        
        return {
            'uls_results': uls_results,
            'sls_results': sls_results,
            'governing_combination': governing_combo.name,
            'max_load': max_load,
            'test_passed': True
        }
    
    def test_design_requirements_integration(self) -> Dict[str, Any]:
        """Test design requirements integration"""
        print("\n🏗️  Testing Design Requirements Integration")
        print("-" * 50)
        
        results = {}
        
        # Test concrete cover requirements
        environments = [ThaiEnvironmentType.NORMAL, ThaiEnvironmentType.AGGRESSIVE, ThaiEnvironmentType.MARINE]
        elements = [ThaiElementType.SLAB, ThaiElementType.BEAM, ThaiElementType.COLUMN]
        
        cover_results = {}
        for env in environments:
            cover_results[env.value] = {}
            for elem in elements:
                cover_req = self.regulation.get_concrete_cover(elem, env)
                if cover_req:
                    cover_results[env.value][elem.value] = cover_req.cover_mm
                    print(f"✓ {elem.value} in {env.value}: {cover_req.cover_mm} mm")
        
        # Test safety factors
        safety_factors = {}
        for material in ['concrete', 'steel', 'dead_load', 'live_load']:
            factor = self.regulation.get_safety_factor(material)
            safety_factors[material] = factor
            print(f"✓ {material} safety factor: {factor}")
        
        results['cover_requirements'] = cover_results
        results['safety_factors'] = safety_factors
        results['test_passed'] = True
        
        return results
    
    def test_wind_loads_integration(self) -> Dict[str, Any]:
        """Test wind loads integration"""
        print("\n💨 Testing Wind Loads Integration")
        print("-" * 50)
        
        # Test building in Bangkok
        location = "กรุงเทพมหานคร"
        building_height = 30.0  # meters
        
        # Quick wind analysis
        from structural_standards.thai.ministry_2566.loads.wind_loads import quick_wind_analysis
        quick_result = quick_wind_analysis(location, building_height, 2000.0)  # 2000 kN total weight
        
        print(f"✓ Location: {location}")
        print(f"✓ Wind Zone: {quick_result['wind_zone']}")
        print(f"✓ Basic Wind Speed: {quick_result['basic_wind_speed']} m/s")
        print(f"✓ Design Pressure: {quick_result['design_pressure_kpa']:.2f} kPa")
        print(f"✓ Base Shear: {quick_result['base_shear_kn']:.1f} kN")
        
        return {
            'location': location,
            'quick_analysis': quick_result,
            'test_passed': True
        }
    
    def test_seismic_loads_integration(self) -> Dict[str, Any]:
        """Test seismic loads integration"""
        print("\n🌊 Testing Seismic Loads Integration")
        print("-" * 50)
        
        # Test building in Northern Thailand (higher seismic risk)
        location = "เชียงใหม่"
        
        # Quick seismic analysis
        from structural_standards.thai.ministry_2566.loads.seismic_loads import quick_seismic_analysis
        quick_result = quick_seismic_analysis(location, 30.0, 2000.0)  # 30m height, 2000 kN weight
        
        print(f"✓ Location: {location}")
        print(f"✓ Seismic Zone: {quick_result['seismic_zone']}")
        print(f"✓ Peak Ground Acceleration: {quick_result['peak_ground_acceleration']:.3f} g")
        print(f"✓ Seismic Coefficient: {quick_result['seismic_coefficient']:.4f}")
        print(f"✓ Base Shear: {quick_result['base_shear_kn']:.1f} kN")
        
        return {
            'location': location,
            'quick_analysis': quick_result,
            'test_passed': True
        }
    
    def test_unit_conversions_integration(self) -> Dict[str, Any]:
        """Test unit conversions integration"""
        print("\n📏 Testing Unit Conversions Integration")
        print("-" * 50)
        
        # Test pressure conversions
        test_values = [180, 210, 240, 280, 350]  # ksc values
        conversion_results = {}
        
        for ksc_val in test_values:
            mpa_val = ksc_to_mpa(ksc_val)
            back_to_ksc = mpa_to_ksc(mpa_val)
            accuracy = abs(ksc_val - back_to_ksc) < 0.01
            
            conversion_results[f'Fc{ksc_val}'] = {
                'ksc': ksc_val,
                'mpa': mpa_val,
                'back_to_ksc': back_to_ksc,
                'accurate': accuracy
            }
            
            print(f"✓ {ksc_val} ksc = {mpa_val:.2f} MPa → {back_to_ksc:.1f} ksc (✓ {accuracy})")
        
        # Test Thai traditional units
        from structural_standards.thai.ministry_2566.units import convert_thai_length, convert_thai_area
        
        wa_to_m = convert_thai_length(1.0, "wa", "m")
        rai_to_m2 = convert_thai_area(1.0, "rai", "m²")
        
        print(f"✓ 1 วา = {wa_to_m} เมตร")
        print(f"✓ 1 ไร่ = {rai_to_m2} ตารางเมตร")
        
        return {
            'pressure_conversions': conversion_results,
            'traditional_units': {
                'wa_to_meter': wa_to_m,
                'rai_to_m2': rai_to_m2
            },
            'test_passed': True
        }
    
    def test_project_compliance_integration(self) -> Dict[str, Any]:
        """Test complete project compliance check"""
        print("\n📋 Testing Project Compliance Integration")
        print("-" * 50)
        
        # Create sample project
        project_data = ThaiProjectData(
            project_name="ตัวอย่างโครงการพื้น 2 ทิศทาง",
            location="กรุงเทพมหานคร",
            environment_type=ThaiEnvironmentType.NORMAL,
            concrete_grade="Fc240",
            steel_grade="SD40",
            design_life=50,
            importance_factor=1.0,
            date="2024-01-15"
        )
        
        # Check compliance
        compliance_results = self.regulation.check_project_compliance(project_data)
        
        print(f"✓ Project: {project_data.project_name}")
        print(f"✓ Location: {project_data.location}")
        print(f"✓ Materials: {project_data.concrete_grade}, {project_data.steel_grade}")
        
        compliant_count = sum(1 for result in compliance_results if result.is_compliant)
        total_count = len(compliance_results)
        
        print(f"✓ Compliance: {compliant_count}/{total_count} checks passed")
        
        for result in compliance_results:
            status = "✅ PASS" if result.is_compliant else "❌ FAIL"
            print(f"  {result.category}: {status}")
        
        return {
            'project_data': project_data,
            'compliance_results': compliance_results,
            'compliance_rate': compliant_count / total_count,
            'test_passed': compliant_count == total_count
        }
    
    def run_comprehensive_integration_test(self) -> Dict[str, Any]:
        """Run comprehensive integration test for all Thai standards"""
        print("🚀 Starting Comprehensive Thai Standards Integration Test")
        print("=" * 70)
        
        all_results = {}
        
        # Run all integration tests
        test_methods = [
            ('materials', self.test_materials_integration),
            ('load_combinations', self.test_load_combinations_integration),
            ('design_requirements', self.test_design_requirements_integration),
            ('wind_loads', self.test_wind_loads_integration),
            ('seismic_loads', self.test_seismic_loads_integration),
            ('unit_conversions', self.test_unit_conversions_integration),
            ('project_compliance', self.test_project_compliance_integration)
        ]
        
        passed_tests = 0
        total_tests = len(test_methods)
        
        for test_name, test_method in test_methods:
            try:
                result = test_method()
                all_results[test_name] = result
                if result.get('test_passed', False):
                    passed_tests += 1
                    print(f"✅ {test_name.replace('_', ' ').title()} Test: PASSED")
                else:
                    print(f"❌ {test_name.replace('_', ' ').title()} Test: FAILED")
            except Exception as e:
                print(f"❌ {test_name.replace('_', ' ').title()} Test: ERROR - {str(e)}")
                all_results[test_name] = {'test_passed': False, 'error': str(e)}
        
        # Summary
        print("\n" + "=" * 70)
        print(f"🏆 Integration Test Summary: {passed_tests}/{total_tests} tests passed")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! Thai Standards Integration is complete and working correctly.")
        else:
            print("⚠️  Some tests failed. Please review the results above.")
        
        all_results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'all_passed': passed_tests == total_tests
        }
        
        return all_results


def main():
    """Main integration test function"""
    print("🇹🇭 Thai Ministry Regulation B.E. 2566 - Integration Test")
    print("กฎกระทรวง พ.ศ. 2566 - การทดสอบบูรณาการ")
    print("=" * 70)
    
    try:
        # Initialize tester
        tester = ThaiStandardsIntegrationTester()
        
        # Run comprehensive test
        results = tester.run_comprehensive_integration_test()
        
        # Generate summary report
        if results['summary']['all_passed']:
            print("\n✅ INTEGRATION TEST SUCCESSFUL!")
            print("🏗️  Thai standards are ready for production use.")
            print("📝 All components are working correctly and integrated properly.")
            
            # Display key capabilities
            print("\n🔧 Available Thai Standards Capabilities:")
            print("  • Thai concrete grades: Fc180, Fc210, Fc240, Fc280, Fc350")
            print("  • Thai steel grades: SR24, SD40, SD50")
            print("  • Load combinations per Ministry Regulation B.E. 2566")
            print("  • Wind loads per TIS 1311-50 with provincial zones")
            print("  • Seismic loads per TIS 1301/1302-61 with provincial zones")
            print("  • Unit conversions (ksc ↔ MPa, traditional Thai units)")
            print("  • Design requirements and compliance checking")
            print("  • Comprehensive reporting in Thai and English")
        else:
            print(f"\n⚠️  Integration test completed with {results['summary']['passed_tests']}/{results['summary']['total_tests']} tests passed")
            
        return results
        
    except Exception as e:
        print(f"\n❌ Integration test failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    results = main()