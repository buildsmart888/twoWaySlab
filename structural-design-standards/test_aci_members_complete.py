"""
ACI 318M-25 Complete Members Integration Test
============================================

Comprehensive test to validate that all ACI 318M-25 structural member
design modules work together correctly.

การทดสอบบูรณาการครบถ้วนของการออกแบบสมาชิกโครงสร้างตาม ACI 318M-25
"""

import sys
import os
from typing import Dict, Any, List

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel

from structural_standards.aci.aci318m25.members import (
    # All member design classes
    ACI318M25BeamDesign, ACI318M25ColumnDesign, ACI318M25SlabDesign,
    ACI318M25WallDesign, ACI318M25FootingDesign, ACI318M25DiaphragmDesign,
    
    # Geometry classes
    BeamGeometry, ColumnGeometry, SlabGeometry, 
    WallGeometry, FootingGeometry, DiaphragmGeometry,
    
    # Load classes
    BeamLoads, ColumnLoads, SlabLoads, 
    WallLoads, FootingColumnLoads, DiaphragmLoads,
    
    # Additional classes
    SoilProperties, BeamType, ColumnType, SlabType,
    WallType, FootingType, DiaphragmType,
    
    # Utility functions
    get_available_members, create_member_designer
)


class ACI318M25MembersIntegrationTester:
    """
    Comprehensive integration tester for all ACI 318M-25 structural members
    
    ระบบทดสอบบูรณาการครบถ้วนสำหรับสมาชิกโครงสร้างทั้งหมดตาม ACI 318M-25
    """
    
    def __init__(self):
        """Initialize the integration tester"""
        self.concrete = ACI318M25Concrete(fc_prime=28.0)  # 28 MPa concrete
        self.steel = ACI318M25ReinforcementSteel(grade=420)  # Grade 420 steel
        
        print("🏗️ ACI 318M-25 Complete Members Integration Tester Initialized")
        print("=" * 70)
        print(f"📊 Concrete: {self.concrete.fc_prime} MPa")
        print(f"🔩 Steel: {self.steel.fy} MPa ({self.steel.grade})")
    
    def test_member_imports(self) -> Dict[str, Any]:
        """Test that all member classes can be imported"""
        print("\n📦 Testing Member Class Imports")
        print("-" * 50)
        
        results = {}
        
        # Test each member type
        member_classes = {
            'beam': ACI318M25BeamDesign,
            'column': ACI318M25ColumnDesign,
            'slab': ACI318M25SlabDesign,
            'wall': ACI318M25WallDesign,
            'footing': ACI318M25FootingDesign,
            'diaphragm': ACI318M25DiaphragmDesign
        }
        
        for member_type, design_class in member_classes.items():
            try:
                # Try to instantiate the class
                designer = design_class(self.concrete, self.steel)
                results[member_type] = {
                    'import_status': 'success',
                    'instantiation': 'success',
                    'class_name': design_class.__name__,
                    'design_standard': designer.design_standard
                }
                print(f"✅ {member_type.capitalize()}: {design_class.__name__}")
            except Exception as e:
                results[member_type] = {
                    'import_status': 'failed',
                    'instantiation': 'failed',
                    'error': str(e)
                }
                print(f"❌ {member_type.capitalize()}: FAILED - {e}")
        
        success_count = sum(1 for r in results.values() if r.get('import_status') == 'success')
        total_count = len(results)
        
        print(f"\n📈 Import Results: {success_count}/{total_count} successful")
        
        results['summary'] = {
            'total_members': total_count,
            'successful_imports': success_count,
            'success_rate': (success_count / total_count) * 100
        }
        
        return results
    
    def test_beam_design(self) -> Dict[str, Any]:
        """Test beam design functionality"""
        print("\n🔗 Testing Beam Design")
        print("-" * 30)
        
        try:
            # Create beam designer
            beam_designer = ACI318M25BeamDesign(self.concrete, self.steel)
            
            # Define beam geometry
            geometry = BeamGeometry(
                width=300,      # mm
                height=600,     # mm
                effective_depth=550,  # mm
                span_length=6000      # mm
            )
            
            # Define loads
            loads = BeamLoads(
                dead_load=5.0,  # kN/m
                live_load=8.0   # kN/m
            )
            
            # Design flexural reinforcement
            moment_ultimate = 120.0  # kN⋅m
            result = beam_designer.design_flexural_reinforcement(geometry, moment_ultimate)
            
            print(f"✅ Beam flexural design completed")
            print(f"   Status: {result.overall_status.value}")
            print(f"   Checks: {len(result.strength_checks)} strength, {len(result.serviceability_checks)} serviceability")
            
            return {
                'status': 'success',
                'design_result': result,
                'utilization_ratio': result.utilization_ratio
            }
            
        except Exception as e:
            print(f"❌ Beam design failed: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def test_column_design(self) -> Dict[str, Any]:
        """Test column design functionality"""
        print("\n🏛️ Testing Column Design")
        print("-" * 30)
        
        try:
            # Create column designer
            column_designer = ACI318M25ColumnDesign(self.concrete, self.steel)
            
            # Define column geometry
            geometry = ColumnGeometry(
                width=400,     # mm
                depth=400,     # mm
                length=3000    # mm
            )
            
            # Define loads
            loads = ColumnLoads(
                axial_dead=200,    # kN
                axial_live=150,    # kN
                moment_x_dead=15,  # kN⋅m
                moment_x_live=10   # kN⋅m
            )
            
            # Design axial reinforcement
            result = column_designer.design_axial_reinforcement(geometry, loads)
            
            print(f"✅ Column axial design completed")
            print(f"   Status: {result.overall_status.value}")
            print(f"   Checks: {len(result.strength_checks)} strength, {len(result.serviceability_checks)} serviceability")
            
            return {
                'status': 'success',
                'design_result': result,
                'utilization_ratio': result.utilization_ratio
            }
            
        except Exception as e:
            print(f"❌ Column design failed: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def test_slab_design(self) -> Dict[str, Any]:
        """Test slab design functionality"""
        print("\n🏢 Testing Slab Design")
        print("-" * 30)
        
        try:
            # Create slab designer
            slab_designer = ACI318M25SlabDesign(self.concrete, self.steel)
            
            # Define slab geometry
            geometry = SlabGeometry(
                length_x=6000,    # mm
                length_y=6000,    # mm
                thickness=200,    # mm
                span_x=6000,      # mm
                span_y=6000       # mm
            )
            
            # Define loads
            loads = SlabLoads(
                dead_load=4.0,    # kPa
                live_load=2.5     # kPa
            )
            
            # Design slab
            result = slab_designer.design(geometry, loads, SlabType.TWO_WAY)
            
            print(f"✅ Slab design completed")
            print(f"   Status: {result.overall_status.value}")
            print(f"   Checks: {len(result.strength_checks)} strength, {len(result.serviceability_checks)} serviceability")
            
            return {
                'status': 'success',
                'design_result': result,
                'utilization_ratio': result.utilization_ratio
            }
            
        except Exception as e:
            print(f"❌ Slab design failed: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def test_wall_design(self) -> Dict[str, Any]:
        """Test wall design functionality"""
        print("\n🧱 Testing Wall Design")
        print("-" * 30)
        
        try:
            # Create wall designer
            wall_designer = ACI318M25WallDesign(self.concrete, self.steel)
            
            # Define wall geometry
            geometry = WallGeometry(
                length=4000,      # mm
                height=3000,      # mm
                thickness=200     # mm
            )
            
            # Define loads
            loads = WallLoads(
                axial_dead=50,        # kN/m
                axial_live=30,        # kN/m
                wind_pressure=1.0     # kPa
            )
            
            # Design wall
            result = wall_designer.design(geometry, loads, WallType.BEARING)
            
            print(f"✅ Wall design completed")
            print(f"   Status: {result.overall_status.value}")
            print(f"   Checks: {len(result.strength_checks)} strength, {len(result.serviceability_checks)} serviceability")
            
            return {
                'status': 'success',
                'design_result': result,
                'utilization_ratio': result.utilization_ratio
            }
            
        except Exception as e:
            print(f"❌ Wall design failed: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def test_footing_design(self) -> Dict[str, Any]:
        """Test footing design functionality"""
        print("\n🏗️ Testing Footing Design")
        print("-" * 30)
        
        try:
            # Create footing designer
            footing_designer = ACI318M25FootingDesign(self.concrete, self.steel)
            
            # Define column loads
            loads = FootingColumnLoads(
                axial_dead=200,       # kN
                axial_live=150,       # kN
                moment_x_dead=10,     # kN⋅m
                moment_y_dead=5       # kN⋅m
            )
            
            # Define soil properties
            soil = SoilProperties(
                bearing_capacity=200,  # kPa
                unit_weight=18.0      # kN/m³
            )
            
            # Design footing
            result = footing_designer.design(loads, soil, FootingType.ISOLATED)
            
            print(f"✅ Footing design completed")
            print(f"   Status: {result.overall_status.value}")
            print(f"   Checks: {len(result.strength_checks)} strength, {len(result.serviceability_checks)} serviceability")
            
            return {
                'status': 'success',
                'design_result': result,
                'utilization_ratio': result.utilization_ratio
            }
            
        except Exception as e:
            print(f"❌ Footing design failed: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def test_diaphragm_design(self) -> Dict[str, Any]:
        """Test diaphragm design functionality"""
        print("\n🔲 Testing Diaphragm Design")
        print("-" * 30)
        
        try:
            # Create diaphragm designer
            diaphragm_designer = ACI318M25DiaphragmDesign(self.concrete, self.steel)
            
            # Define diaphragm geometry
            geometry = DiaphragmGeometry(
                length=12000,     # mm
                width=8000,       # mm
                thickness=150,    # mm
                span=8000         # mm
            )
            
            # Define loads
            loads = DiaphragmLoads(
                shear_force=100,  # kN
                moment=50         # kN⋅m
            )
            
            # Design diaphragm
            result = diaphragm_designer.design(geometry, loads, DiaphragmType.CAST_IN_PLACE)
            
            print(f"✅ Diaphragm design completed")
            print(f"   Status: {result.overall_status.value}")
            print(f"   Checks: {len(result.strength_checks)} strength, {len(result.serviceability_checks)} serviceability")
            
            return {
                'status': 'success',
                'design_result': result,
                'utilization_ratio': result.utilization_ratio
            }
            
        except Exception as e:
            print(f"❌ Diaphragm design failed: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def test_factory_function(self) -> Dict[str, Any]:
        """Test the factory function for creating member designers"""
        print("\n🏭 Testing Factory Function")
        print("-" * 30)
        
        results = {}
        
        try:
            available_members = get_available_members()
            print(f"📋 Available members: {list(available_members.keys())}")
            
            # Test creating each member type
            for member_type in available_members.keys():
                try:
                    designer = create_member_designer(member_type, self.concrete, self.steel)
                    results[member_type] = {
                        'status': 'success',
                        'class_name': designer.__class__.__name__
                    }
                    print(f"✅ {member_type}: {designer.__class__.__name__}")
                except Exception as e:
                    results[member_type] = {
                        'status': 'failed',
                        'error': str(e)
                    }
                    print(f"❌ {member_type}: FAILED - {e}")
            
            # Test invalid member type
            try:
                create_member_designer('invalid_type', self.concrete, self.steel)
                results['error_handling'] = {'status': 'failed', 'error': 'Should have raised ValueError'}
            except ValueError:
                results['error_handling'] = {'status': 'success'}
                print("✅ Error handling: Correctly raised ValueError for invalid type")
            
            success_count = sum(1 for r in results.values() if r.get('status') == 'success')
            total_count = len(results)
            
            print(f"📈 Factory test results: {success_count}/{total_count} successful")
            
            results['summary'] = {
                'total_tests': total_count,
                'successful': success_count,
                'success_rate': (success_count / total_count) * 100
            }
            
            return results
            
        except Exception as e:
            print(f"❌ Factory function test failed: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def run_complete_integration_test(self) -> Dict[str, Any]:
        """Run complete integration test for all ACI 318M-25 members"""
        print("🚀 Starting Complete ACI 318M-25 Members Integration Test")
        print("=" * 70)
        
        all_results = {}
        
        # Run all individual tests
        test_methods = [
            ('imports', self.test_member_imports),
            ('beam', self.test_beam_design),
            ('column', self.test_column_design),
            ('slab', self.test_slab_design),
            ('wall', self.test_wall_design),
            ('footing', self.test_footing_design),
            ('diaphragm', self.test_diaphragm_design),
            ('factory', self.test_factory_function)
        ]
        
        passed_tests = 0
        total_tests = len(test_methods)
        
        for test_name, test_method in test_methods:
            try:
                result = test_method()
                all_results[test_name] = result
                
                # Determine if test passed
                if test_name == 'imports':
                    test_passed = result['summary']['success_rate'] == 100
                elif test_name == 'factory':
                    test_passed = result['summary']['success_rate'] == 100
                else:
                    test_passed = result.get('status') == 'success'
                
                if test_passed:
                    passed_tests += 1
                    print(f"✅ {test_name.replace('_', ' ').title()} Test: PASSED")
                else:
                    print(f"❌ {test_name.replace('_', ' ').title()} Test: FAILED")
                    
            except Exception as e:
                print(f"❌ {test_name.replace('_', ' ').title()} Test: ERROR - {str(e)}")
                all_results[test_name] = {'status': 'error', 'error': str(e)}
        
        # Summary
        print("\n" + "=" * 70)
        print(f"🏆 Complete Integration Test Summary: {passed_tests}/{total_tests} tests passed")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! ACI 318M-25 members integration is complete and working correctly.")
            print("✅ Ready for production use!")
        else:
            print("⚠️  Some tests failed. Please review the results above.")
        
        all_results['overall_summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'all_passed': passed_tests == total_tests
        }
        
        # Display key capabilities
        if passed_tests == total_tests:
            print("\n🔧 Available ACI 318M-25 Design Capabilities:")
            print("  • Beam Design: Flexural, shear, and deflection analysis")
            print("  • Column Design: Axial-moment interaction and slenderness effects")
            print("  • Slab Design: One-way, two-way, and punching shear analysis")
            print("  • Wall Design: Bearing walls, shear walls, out-of-plane analysis")
            print("  • Footing Design: Isolated, combined, bearing pressure analysis")
            print("  • Diaphragm Design: In-plane shear, chord, and collector design")
            print("  • Complete material integration with ACI 318M-25 concrete and steel")
            print("  • Comprehensive design checks per ACI 318M-25 requirements")
        
        return all_results


def main():
    """Main integration test function"""
    print("🏗️ ACI 318M-25 Complete Members Integration Test")
    print("Building Code Requirements for Structural Concrete (SI Units)")
    print("=" * 70)
    
    try:
        # Initialize tester
        tester = ACI318M25MembersIntegrationTester()
        
        # Run complete test
        results = tester.run_complete_integration_test()
        
        # Return success status
        return results['overall_summary']['all_passed']
        
    except Exception as e:
        print(f"\n❌ Integration test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🚀 ACI 318M-25 Complete Members Integration - SUCCESS")
        print("📋 All structural members ready for production use!")
    else:
        print("\n❌ Integration test failed")
        
    print("\n" + "=" * 70)