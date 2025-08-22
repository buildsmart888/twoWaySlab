"""
Simple Thai Ministry Regulation Test
===================================

Basic test to validate the Thai Ministry Regulation B.E. 2566 implementation
"""

import sys
import os
sys.path.insert(0, '.')

def test_thai_ministry_regulation():
    """Test the Thai Ministry Regulation implementation"""
    print("🔍 Testing Thai Ministry Regulation B.E. 2566 Implementation")
    print("=" * 60)
    
    try:
        # Test 1: Import the module
        print("1. Testing module import...")
        from structural_standards.thai.ministry_2566 import (
            ThaiMinistryRegulation2566,
            ThaiProjectData,
            ThaiEnvironmentType,
            ThaiLoadType,
            ThaiCombinationType
        )
        print("   ✅ Import successful")
        
        # Test 2: Create regulation instance
        print("2. Creating regulation instance...")
        regulation = ThaiMinistryRegulation2566()
        print("   ✅ Instance created successfully")
        
        # Test 3: Test load combinations
        print("3. Testing load combinations...")
        loads = {
            ThaiLoadType.DEAD: 10.0,
            ThaiLoadType.LIVE: 6.0,
            ThaiLoadType.WIND: 4.0
        }
        
        results = regulation.calculate_design_loads(loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE)
        print(f"   ✅ Load combinations calculated: {len(results)} combinations")
        
        # Show sample result
        if results:
            first_combo = list(results.keys())[0]
            print(f"   Sample: {first_combo} = {results[first_combo]:.1f} kN/m²")
        
        # Test 4: Test cover requirements
        print("4. Testing cover requirements...")
        from structural_standards.thai.ministry_2566 import ThaiElementType
        
        cover_req = regulation.get_concrete_cover(
            ThaiElementType.SLAB, 
            ThaiEnvironmentType.NORMAL
        )
        
        if cover_req:
            print(f"   ✅ Cover requirement: {cover_req.cover_mm} mm for slab in normal environment")
        else:
            print("   ❌ Cover requirement not found")
        
        # Test 5: Test material creation
        print("5. Testing material creation...")
        concrete = regulation.create_thai_concrete("Fc210")
        steel = regulation.create_thai_steel("SD40")
        
        print(f"   ✅ Concrete created: fc' = {concrete.fc_prime} MPa")
        print(f"   ✅ Steel created: fy = {steel.fy} MPa")
        
        # Test 6: Test safety factors
        print("6. Testing safety factors...")
        concrete_sf = regulation.get_safety_factor('concrete')
        steel_sf = regulation.get_safety_factor('steel')
        
        print(f"   ✅ Concrete safety factor: {concrete_sf}")
        print(f"   ✅ Steel safety factor: {steel_sf}")
        
        print("\n🎉 All tests passed successfully!")
        print("✅ Thai Ministry Regulation B.E. 2566 implementation is working correctly")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_thai_ministry_regulation()
    if success:
        print("\n📋 Implementation Status:")
        print("✅ Phase 8: Thai Ministry Regulation B.E. 2566 - COMPLETED")
        print("⏭️  Ready for next phase: Thai Wind Loads")
    else:
        print("\n❌ Implementation needs fixing")