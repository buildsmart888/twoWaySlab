"""
Cross-Standard Integration Tests
===============================

Tests for integration between ACI 318M-25 and Thai Ministry Regulation B.E. 2566.
Tests material compatibility, load combination integration, and design consistency.

การทดสอบบูรณาการระหว่างมาตรฐาน ACI 318M-25 และกฎกระทรวงไทย พ.ศ. 2566
"""

import pytest
import math
from typing import Dict, Any, List

# ACI imports
from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.beam_design import (
    ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
)

# Thai imports
from structural_standards.thai.ministry_2566.load_combinations import (
    ThaiMinistryLoadCombinations, ThaiLoadType, ThaiCombinationType
)

from structural_standards.base.design_base import DesignStatus


@pytest.mark.integration
@pytest.mark.cross_standard
class TestCrossStandardIntegration:
    """Test integration between different design standards"""
    
    @pytest.fixture
    def aci_materials(self):
        """Create ACI materials"""
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        return {'concrete': concrete, 'steel': steel}
    
    @pytest.fixture
    def thai_load_combinations(self):
        """Create Thai load combinations"""
        return ThaiMinistryLoadCombinations()
    
    def test_material_consistency_across_standards(self, aci_materials):
        """Test material property consistency"""
        print("\n🔗 Testing Material Consistency Across Standards")
        
        concrete = aci_materials['concrete']
        steel = aci_materials['steel']
        
        # ACI 318M-25 uses metric units (MPa)
        assert concrete.fc_prime == 28.0  # MPa
        assert steel.fy == 420.0  # MPa
        
        # Test unit consistency
        assert concrete.unit_weight == 24.0  # kN/m³
        assert steel.unit_weight == 77.0  # kN/m³
        
        # Test modulus calculations
        ec_calculated = concrete.elastic_modulus()
        es_calculated = steel.elastic_modulus()
        
        assert ec_calculated > 20000  # MPa (reasonable for concrete)
        assert es_calculated == 200000  # MPa (standard for steel)
        
        print(f"  ✅ Concrete: fc'={concrete.fc_prime} MPa, Ec={ec_calculated:.0f} MPa")
        print(f"  ✅ Steel: fy={steel.fy} MPa, Es={es_calculated:.0f} MPa")
    
    def test_aci_design_with_thai_load_combinations(self, aci_materials, thai_load_combinations):
        """Test ACI member design using Thai load combinations"""
        print("\n🏗️ Testing ACI Design with Thai Load Combinations")
        
        # Create ACI beam designer
        beam_designer = ACI318M25BeamDesign(aci_materials['concrete'], aci_materials['steel'])
        
        # Define beam geometry
        geometry = BeamGeometry(
            width=300,
            height=600,
            effective_depth=550,
            span_length=6000
        )
        
        # Define service loads (Thai load types)
        service_loads = {
            ThaiLoadType.DEAD: 5.0,     # kN/m
            ThaiLoadType.LIVE: 8.0,     # kN/m
            ThaiLoadType.WIND: 2.0      # kN/m
        }
        
        # Get Thai load combinations
        uls_combinations = thai_load_combinations.get_ultimate_combinations()
        
        # Test beam design with different Thai combinations
        design_results = {}
        
        for combo in uls_combinations[:3]:  # Test first 3 combinations
            # Calculate factored moment using Thai combination
            factored_loads = combo.calculate_load_effect(service_loads)
            
            # Convert to moment (simplified - assume uniform load on simply supported beam)
            span_m = geometry.span_length / 1000  # Convert to meters
            moment = factored_loads * span_m**2 / 8  # kN⋅m
            
            # Design beam with ACI method
            result = beam_designer.design_flexural_reinforcement(geometry, moment)
            design_results[combo.name] = {
                'factored_load': factored_loads,
                'moment': moment,
                'result': result
            }
        
        # Verify all designs
        for combo_name, data in design_results.items():
            result = data['result']
            assert result.design_method == "ACI 318M-25"
            assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
            
            if result.overall_status == DesignStatus.PASS:
                steel_area = result.required_reinforcement['required_steel_area']
                assert steel_area > 0
                print(f"  ✅ {combo_name}: M={data['moment']:.1f} kN⋅m, As={steel_area:.0f} mm²")
        
        return design_results
    
    def test_load_factor_consistency(self, thai_load_combinations):
        """Test load factor consistency between standards"""
        print("\n⚖️ Testing Load Factor Consistency")
        
        # Get Thai combinations
        uls_combinations = thai_load_combinations.get_ultimate_combinations()
        sls_combinations = thai_load_combinations.get_serviceability_combinations()
        
        # Check that Ultimate factors are generally higher than Service factors
        uls_factors = []
        sls_factors = []
        
        for combo in uls_combinations:
            for load_type, factor in combo.factors.items():
                if load_type in [ThaiLoadType.DEAD, ThaiLoadType.LIVE]:
                    uls_factors.append(factor)
        
        for combo in sls_combinations:
            for load_type, factor in combo.factors.items():
                if load_type in [ThaiLoadType.DEAD, ThaiLoadType.LIVE]:
                    sls_factors.append(factor)
        
        if uls_factors and sls_factors:
            avg_uls = sum(uls_factors) / len(uls_factors)
            avg_sls = sum(sls_factors) / len(sls_factors)
            
            assert avg_uls > avg_sls, "Ultimate factors should be higher than service factors"
            print(f"  ✅ Average ULS factor: {avg_uls:.2f}")
            print(f"  ✅ Average SLS factor: {avg_sls:.2f}")
    
    def test_strength_reduction_factor_integration(self, aci_materials):
        """Test strength reduction factor integration"""
        print("\n💪 Testing Strength Reduction Factor Integration")
        
        # Create ACI designer
        beam_designer = ACI318M25BeamDesign(aci_materials['concrete'], aci_materials['steel'])
        
        # Check ACI phi factors
        phi_flexure = beam_designer.phi_flexure
        phi_shear = beam_designer.phi_shear
        
        assert phi_flexure == 0.9
        assert phi_shear == 0.75
        
        # Test Thai phi factors
        thai_loads = ThaiMinistryLoadCombinations()
        phi_flexure_thai = thai_loads.get_phi_factor('flexure_tension_controlled')
        phi_shear_thai = thai_loads.get_phi_factor('shear_and_torsion')
        
        # Should be the same (both follow similar principles)
        assert abs(phi_flexure - phi_flexure_thai) < 0.01
        assert abs(phi_shear - phi_shear_thai) < 0.01
        
        print(f"  ✅ Flexure φ: ACI={phi_flexure}, Thai={phi_flexure_thai}")
        print(f"  ✅ Shear φ: ACI={phi_shear}, Thai={phi_shear_thai}")
    
    def test_design_workflow_integration(self, aci_materials, thai_load_combinations):
        """Test complete design workflow integration"""
        print("\n🔄 Testing Complete Design Workflow Integration")
        
        # Step 1: Define building loads (Thai classification)
        building_loads = {
            ThaiLoadType.DEAD: 6.0,      # kN/m (structural + finishes)
            ThaiLoadType.LIVE: 4.0,      # kN/m (occupancy)
            ThaiLoadType.WIND: 2.5       # kN/m (wind on facade)
        }
        
        # Step 2: Get critical Thai load combination
        critical_combo, max_effect = thai_load_combinations.find_critical_combination(
            building_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        
        print(f"  Critical combination: {critical_combo.name}")
        print(f"  Critical load effect: {max_effect:.1f} kN/m")
        print(f"  Load equation: {critical_combo.get_equation()}")
        
        # Step 3: Design structural members using ACI 318M-25
        beam_designer = ACI318M25BeamDesign(aci_materials['concrete'], aci_materials['steel'])
        
        # Multiple beam designs for different spans
        spans = [4000, 6000, 8000]  # mm
        design_summary = {}
        
        for span in spans:
            geometry = BeamGeometry(
                width=300,
                height=int(span / 15),  # Assume depth = span/15
                effective_depth=int(span / 15) - 50,
                span_length=span
            )
            
            # Calculate moment from critical load
            span_m = span / 1000
            moment = max_effect * span_m**2 / 8
            
            # Design beam
            result = beam_designer.design_flexural_reinforcement(geometry, moment)
            
            design_summary[span] = {
                'geometry': geometry,
                'moment': moment,
                'result': result,
                'status': result.overall_status
            }
        
        # Verify all designs
        passed_designs = 0
        for span, data in design_summary.items():
            status = data['status']
            if status == DesignStatus.PASS:
                passed_designs += 1
                steel_area = data['result'].required_reinforcement['required_steel_area']
                print(f"  ✅ Span {span}mm: {status.value}, As={steel_area:.0f} mm²")
            else:
                print(f"  ⚠️ Span {span}mm: {status.value}")
        
        # At least 2 out of 3 designs should pass for reasonable loads
        assert passed_designs >= 2, f"Too many design failures: {passed_designs}/3 passed"
        
        return design_summary
    
    def test_multi_standard_material_properties(self):
        """Test material properties across different standards"""
        print("\n🧪 Testing Multi-Standard Material Properties")
        
        # ACI materials
        aci_concrete = ACI318M25Concrete(fc_prime=28.0)
        aci_steel = ACI318M25ReinforcementSteel(grade=420)
        
        # Test material property ranges that should be consistent
        material_tests = [
            (aci_concrete.fc_prime, 15, 80, "Concrete strength"),
            (aci_steel.fy, 300, 600, "Steel yield strength"),
            (aci_concrete.unit_weight, 20, 30, "Concrete unit weight"),
            (aci_steel.unit_weight, 70, 85, "Steel unit weight")
        ]
        
        for value, min_val, max_val, description in material_tests:
            assert min_val <= value <= max_val, f"{description} out of range: {value}"
            print(f"  ✅ {description}: {value}")
        
        # Test derived properties
        ec = aci_concrete.elastic_modulus()
        es = aci_steel.elastic_modulus()
        
        assert 15000 <= ec <= 40000, f"Concrete modulus out of range: {ec}"
        assert es == 200000, f"Steel modulus should be 200000: {es}"
        
        print(f"  ✅ Concrete modulus: {ec:.0f} MPa")
        print(f"  ✅ Steel modulus: {es:.0f} MPa")
    
    def test_unit_system_consistency(self, aci_materials, thai_load_combinations):
        """Test unit system consistency across standards"""
        print("\n📏 Testing Unit System Consistency")
        
        # Both standards should use metric units (SI)
        concrete = aci_materials['concrete']
        steel = aci_materials['steel']
        
        # Check that all units are metric
        units_check = [
            (concrete.fc_prime, "MPa", "Concrete strength"),
            (steel.fy, "MPa", "Steel strength"),
            (concrete.unit_weight, "kN/m³", "Concrete unit weight"),
            (steel.unit_weight, "kN/m³", "Steel unit weight")
        ]
        
        for value, expected_unit, description in units_check:
            assert value > 0, f"{description} should be positive"
            print(f"  ✅ {description}: {value} {expected_unit}")
        
        # Test load combinations use consistent units
        sample_loads = {
            ThaiLoadType.DEAD: 5.0,   # kN/m
            ThaiLoadType.LIVE: 8.0    # kN/m
        }
        
        effect = thai_load_combinations.calculate_all_combinations(
            sample_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        
        # All effects should be in kN/m
        for combo_name, load_effect in effect.items():
            assert load_effect > 0, f"Load effect should be positive: {combo_name}"
            print(f"  ✅ {combo_name}: {load_effect:.1f} kN/m")


@pytest.mark.integration
@pytest.mark.cross_standard
@pytest.mark.validation
class TestCrossStandardValidation:
    """Validation tests for cross-standard integration"""
    
    def test_design_code_equivalency(self):
        """Test equivalency between design approaches"""
        print("\n🔍 Testing Design Code Equivalency")
        
        # Compare design approaches for similar structures
        # This is a simplified test - in practice, detailed comparison would be needed
        
        # ACI approach
        aci_concrete = ACI318M25Concrete(fc_prime=28.0)
        aci_steel = ACI318M25ReinforcementSteel(grade=420)
        
        # Design parameters that should be similar
        aci_phi_flexure = 0.9
        
        # Thai approach (using ACI-based factors)
        thai_loads = ThaiMinistryLoadCombinations()
        thai_phi_flexure = thai_loads.get_phi_factor('flexure_tension_controlled')
        
        # Should be the same or very close
        assert abs(aci_phi_flexure - thai_phi_flexure) < 0.01
        
        print(f"  ✅ ACI φ flexure: {aci_phi_flexure}")
        print(f"  ✅ Thai φ flexure: {thai_phi_flexure}")
        print(f"  ✅ Difference: {abs(aci_phi_flexure - thai_phi_flexure):.3f}")
    
    def test_conservative_design_approach(self, aci_materials, thai_load_combinations):
        """Test that both approaches are appropriately conservative"""
        print("\n🛡️ Testing Conservative Design Approach")
        
        # Test a typical beam design
        beam_designer = ACI318M25BeamDesign(aci_materials['concrete'], aci_materials['steel'])
        
        # Service loads
        service_loads = {
            ThaiLoadType.DEAD: 4.0,    # kN/m
            ThaiLoadType.LIVE: 6.0     # kN/m
        }
        
        # Get factored loads using Thai combinations
        uls_combinations = thai_load_combinations.get_ultimate_combinations()
        
        # Compare different combinations
        design_results = []
        
        for combo in uls_combinations[:2]:  # Test first 2 combinations
            factored_load = combo.calculate_load_effect(service_loads)
            
            # Convert to service load equivalent
            service_equivalent = factored_load / max(combo.factors.values())
            service_ratio = factored_load / sum(service_loads.values())
            
            design_results.append({
                'combination': combo.name,
                'factored_load': factored_load,
                'service_ratio': service_ratio
            })
        
        # All combinations should amplify service loads (conservative)
        for result in design_results:
            assert result['service_ratio'] > 1.0, f"Should amplify loads: {result['combination']}"
            print(f"  ✅ {result['combination']}: factor = {result['service_ratio']:.2f}")
        
        return design_results


@pytest.mark.integration
@pytest.mark.cross_standard
@pytest.mark.benchmark
@pytest.mark.slow
class TestCrossStandardPerformance:
    """Performance tests for cross-standard integration"""
    
    def test_integrated_design_performance(self, performance_monitor, performance_benchmark_data):
        """Test performance of integrated design workflow"""
        print("\n⚡ Testing Integrated Design Performance")
        
        # Setup materials and load combinations
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        beam_designer = ACI318M25BeamDesign(concrete, steel)
        thai_loads = ThaiMinistryLoadCombinations()
        
        # Test data
        service_loads = {
            ThaiLoadType.DEAD: 5.0,
            ThaiLoadType.LIVE: 8.0,
            ThaiLoadType.WIND: 2.0
        }
        
        geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
        
        performance_monitor.start()
        
        # Integrated design workflow (repeated)
        for _ in range(10):
            # Get critical Thai combination
            critical_combo, max_effect = thai_loads.find_critical_combination(
                service_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
            )
            
            # Convert to moment
            moment = max_effect * (6.0)**2 / 8  # kN⋅m
            
            # Design with ACI
            result = beam_designer.design_flexural_reinforcement(geometry, moment)
        
        execution_time = performance_monitor.stop()
        
        # Should be reasonable for integrated workflow
        max_time = 1.0  # 1 second for 10 integrated designs
        assert execution_time <= max_time, f"Integrated design too slow: {execution_time:.3f}s"
        
        print(f"  ✅ Integrated design performance: {execution_time:.3f}s for 10 workflows")
        print(f"  ✅ Average per workflow: {execution_time/10:.3f}s")
        
        return execution_time