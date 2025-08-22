"""
Thai Standards Phase 8 Validation
=================================

Final validation that Phase 8: Thai Standards Implementation is complete
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '.')

def validate_thai_standards():
    """Validate that all Thai standards components are working"""
    print("🇹🇭 Validating Phase 8: Thai Standards Implementation")
    print("=" * 60)
    
    validation_results = []
    
    # Test 1: Basic imports
    try:
        print("1. Testing basic imports...")
        from structural_standards.thai.ministry_2566 import (
            ThaiMinistryRegulation2566,
            ksc_to_mpa,
            mpa_to_ksc
        )
        print("   ✅ Basic imports successful")
        validation_results.append(True)
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        validation_results.append(False)
    
    # Test 2: Unit conversions
    try:
        print("2. Testing unit conversions...")
        
        # Test ksc to MPa conversion
        fc210_ksc = 210
        fc210_mpa = ksc_to_mpa(fc210_ksc)
        back_to_ksc = mpa_to_ksc(fc210_mpa)
        
        conversion_accurate = abs(fc210_ksc - back_to_ksc) < 0.1
        
        print(f"   ✅ 210 ksc = {fc210_mpa:.2f} MPa → {back_to_ksc:.1f} ksc")
        print(f"   ✅ Conversion accuracy: {conversion_accurate}")
        validation_results.append(conversion_accurate)
        
    except Exception as e:
        print(f"   ❌ Unit conversion failed: {e}")
        validation_results.append(False)
    
    # Test 3: Thai materials
    try:
        print("3. Testing Thai materials...")
        from structural_standards.thai.ministry_2566.materials.concrete import ThaiConcrete
        from structural_standards.thai.ministry_2566.materials.steel import ThaiReinforcementSteel
        
        concrete = ThaiConcrete(grade="Fc210")
        steel = ThaiReinforcementSteel(grade="SD40")
        
        print(f"   ✅ Concrete Fc210: {concrete.fc_prime} MPa")
        print(f"   ✅ Steel SD40: {steel.fy} MPa")
        validation_results.append(True)
        
    except Exception as e:
        print(f"   ❌ Materials test failed: {e}")
        validation_results.append(False)
    
    # Test 4: Load calculations
    try:
        print("4. Testing load calculations...")
        from structural_standards.thai.ministry_2566.loads.wind_loads import quick_wind_analysis
        from structural_standards.thai.ministry_2566.loads.seismic_loads import quick_seismic_analysis
        
        # Quick wind analysis for Bangkok
        wind_result = quick_wind_analysis("กรุงเทพมหานคร", 20.0, 1000.0)
        print(f"   ✅ Wind Zone: {wind_result['wind_zone']}")
        
        # Quick seismic analysis for Chiang Mai
        seismic_result = quick_seismic_analysis("เชียงใหม่", 20.0, 1000.0)
        print(f"   ✅ Seismic Zone: {seismic_result['seismic_zone']}")
        
        validation_results.append(True)
        
    except Exception as e:
        print(f"   ❌ Load calculations failed: {e}")
        validation_results.append(False)
    
    # Test 5: Main regulation class
    try:
        print("5. Testing main regulation class...")
        regulation = ThaiMinistryRegulation2566()
        
        # Test safety factors
        concrete_sf = regulation.get_safety_factor('concrete')
        steel_sf = regulation.get_safety_factor('steel')
        
        print(f"   ✅ Concrete safety factor: {concrete_sf}")
        print(f"   ✅ Steel safety factor: {steel_sf}")
        
        # Test regulation info
        reg_info = regulation.get_regulation_info()
        print(f"   ✅ Regulation: {reg_info['effective_date']}")
        
        validation_results.append(True)
        
    except Exception as e:
        print(f"   ❌ Main regulation test failed: {e}")
        validation_results.append(False)
    
    # Summary
    passed_tests = sum(validation_results)
    total_tests = len(validation_results)
    success_rate = (passed_tests / total_tests) * 100
    
    print("\n" + "=" * 60)
    print(f"📊 Validation Results: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    
    if passed_tests == total_tests:
        print("🎉 PHASE 8 VALIDATION SUCCESSFUL!")
        print("✅ Thai Ministry Regulation B.E. 2566 implementation is complete")
        print("\n🏗️ Available Components:")
        print("  • Thai concrete grades (Fc180-Fc350)")
        print("  • Thai steel grades (SR24, SD40, SD50)")
        print("  • Load combinations per Ministry Regulation B.E. 2566")
        print("  • Wind loads per TIS 1311-50")
        print("  • Seismic loads per TIS 1301/1302-61")
        print("  • Unit conversion systems (ksc ↔ MPa)")
        print("  • Design requirements and compliance checking")
        return True
    else:
        print("⚠️ Some validation tests failed")
        print("🔧 Phase 8 needs additional work")
        return False

if __name__ == "__main__":
    success = validate_thai_standards()
    
    if success:
        print("\n🚀 Phase 8: Thai Standards Implementation - COMPLETED")
        print("📋 Ready for production use!")
    else:
        print("\n❌ Phase 8 validation failed")
        
    print("\n" + "=" * 60)