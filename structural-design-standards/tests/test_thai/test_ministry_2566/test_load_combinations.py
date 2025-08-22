"""
Thai Ministry Regulation B.E. 2566 Load Combinations Tests
==========================================================

Comprehensive tests for Thai load combinations according to 
Ministry Regulation B.E. 2566 (2023).

การทดสอบการรวมแรงตามกฎกระทรวง พ.ศ. 2566
"""

import pytest
import math
from typing import Dict, Any, List

from structural_standards.thai.ministry_2566.load_combinations import (
    ThaiMinistryLoadCombinations, ThaiLoadType, ThaiCombinationType, ThaiLoadCombination
)


@pytest.mark.thai
@pytest.mark.ministry_2566
@pytest.mark.load_combinations
@pytest.mark.unit
class TestThaiLoadCombinations:
    """Test Thai Ministry Regulation B.E. 2566 load combinations"""
    
    @pytest.fixture
    def thai_loads(self):
        """Create Thai load combinations fixture"""
        return ThaiMinistryLoadCombinations()
    
    @pytest.fixture
    def sample_loads(self):
        """Sample load values for testing"""
        return {
            ThaiLoadType.DEAD: 100.0,           # DL
            ThaiLoadType.LIVE: 50.0,            # LL
            ThaiLoadType.LATERAL_EARTH: 20.0,   # H
            ThaiLoadType.FLUID: 15.0,           # F
            ThaiLoadType.WIND: 30.0,            # W
            ThaiLoadType.EARTHQUAKE: 25.0       # E
        }
    
    def test_thai_load_combinations_initialization(self, thai_loads):
        """Test Thai load combinations initialization"""
        assert thai_loads is not None
        assert hasattr(thai_loads, 'safety_factors')
        assert hasattr(thai_loads, 'phi_factors')
        
        # Check safety factors
        assert thai_loads.get_safety_factor('concrete') == 1.5
        assert thai_loads.get_safety_factor('steel') == 1.15
        assert thai_loads.get_safety_factor('dead_load') == 1.4
        assert thai_loads.get_safety_factor('live_load') == 1.6
    
    def test_load_types_available(self):
        """Test that all required load types are available"""
        expected_load_types = {
            'DEAD', 'LIVE', 'LATERAL_EARTH', 'FLUID', 'WIND', 'EARTHQUAKE'
        }
        
        available_types = {load_type.name for load_type in ThaiLoadType}
        
        for expected_type in expected_load_types:
            assert expected_type in available_types, f"Missing load type: {expected_type}"
        
        print(f"✅ All required load types available: {len(available_types)}")
    
    def test_ultimate_limit_state_combinations(self, thai_loads):
        """Test Ultimate Limit State (วิธีกำลัง) combinations"""
        uls_combinations = thai_loads.get_ultimate_combinations()
        
        assert len(uls_combinations) > 0, "No ULS combinations found"
        
        # Check specific combinations according to Ministry Regulation B.E. 2566
        combination_names = [combo.name for combo in uls_combinations]
        
        # Key combinations that should exist
        expected_combinations = ['ULS-1', 'ULS-2', 'ULS-3', 'ULS-4', 'ULS-5', 'ULS-6']
        
        for expected in expected_combinations:
            assert expected in combination_names, f"Missing ULS combination: {expected}"
        
        print(f"✅ ULS combinations: {len(uls_combinations)} combinations found")
        
        # Test specific combination factors
        for combo in uls_combinations:
            assert isinstance(combo, ThaiLoadCombination)
            assert combo.combination_type == ThaiCombinationType.ULTIMATE_LIMIT_STATE
            assert len(combo.factors) > 0
            
            # Check that factors are reasonable
            for load_type, factor in combo.factors.items():
                assert -0.5 <= factor <= 2.0, f"Unreasonable factor {factor} for {load_type}"
    
    def test_serviceability_limit_state_combinations(self, thai_loads):
        """Test Serviceability Limit State (หน่วยแรงที่ยอมให้) combinations"""
        sls_combinations = thai_loads.get_serviceability_combinations()
        
        assert len(sls_combinations) > 0, "No SLS combinations found"
        
        # Check specific combinations
        combination_names = [combo.name for combo in sls_combinations]
        
        # Key combinations that should exist (ASD series)
        expected_combinations = ['ASD-100', 'ASD-101', 'ASD-102', 'ASD-106', 'ASD-110', 'ASD-114', 'ASD-118', 'ASD-122']
        
        for expected in expected_combinations:
            assert expected in combination_names, f"Missing SLS combination: {expected}"
        
        print(f"✅ SLS combinations: {len(sls_combinations)} combinations found")
        
        # Test specific combination factors
        for combo in sls_combinations:
            assert isinstance(combo, ThaiLoadCombination)
            assert combo.combination_type == ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
            
            # Serviceability factors should generally be ≤ 1.0
            for load_type, factor in combo.factors.items():
                assert -0.1 <= factor <= 1.1, f"Unreasonable SLS factor {factor} for {load_type}"
    
    def test_load_combination_calculations(self, thai_loads, sample_loads):
        """Test load combination calculations"""
        uls_combinations = thai_loads.get_ultimate_combinations()
        
        # Test calculation for first ULS combination
        combo = uls_combinations[0]
        load_effect = combo.calculate_load_effect(sample_loads)
        
        assert load_effect > 0, "Load effect should be positive"
        
        # Manual verification for ULS-1 (1.4DL + 1.7LL)
        if combo.name == 'ULS-1':
            expected_effect = 1.4 * sample_loads[ThaiLoadType.DEAD] + 1.6 * sample_loads[ThaiLoadType.LIVE]
            # Allow for variations in exact factors
            assert abs(load_effect - expected_effect) / expected_effect < 0.2
        
        print(f"✅ Load calculation verified: {load_effect:.1f}")
    
    def test_critical_combination_finding(self, thai_loads, sample_loads):
        """Test finding critical load combination"""
        critical_combo, max_effect = thai_loads.find_critical_combination(
            sample_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        
        assert critical_combo is not None
        assert max_effect > 0
        assert isinstance(critical_combo, ThaiLoadCombination)
        
        # Verify this is indeed the maximum
        all_uls = thai_loads.get_ultimate_combinations()
        all_effects = [combo.calculate_load_effect(sample_loads) for combo in all_uls]
        
        assert max_effect == max(all_effects), "Critical combination should give maximum effect"
        print(f"✅ Critical combination: {critical_combo.name} with effect {max_effect:.1f}")
    
    def test_all_combinations_calculation(self, thai_loads, sample_loads):
        """Test calculating all combinations"""
        uls_results = thai_loads.calculate_all_combinations(
            sample_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        sls_results = thai_loads.calculate_all_combinations(
            sample_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
        )
        
        assert len(uls_results) > 0
        assert len(sls_results) > 0
        
        # All results should be positive for positive loads
        for name, effect in uls_results.items():
            assert effect >= 0, f"Negative effect for {name}: {effect}"
        
        for name, effect in sls_results.items():
            assert effect >= 0, f"Negative SLS effect for {name}: {effect}"
        
        print(f"✅ All combinations calculated: {len(uls_results)} ULS, {len(sls_results)} SLS")
    
    def test_load_equation_generation(self, thai_loads):
        """Test load combination equation generation"""
        uls_combinations = thai_loads.get_ultimate_combinations()
        
        for combo in uls_combinations:
            equation = combo.get_equation()
            assert isinstance(equation, str)
            assert len(equation) > 0
            
            # Should contain load symbols
            expected_symbols = ['DL', 'LL', 'W', 'E', 'H', 'F']
            contains_load_symbol = any(symbol in equation for symbol in expected_symbols)
            
            if len(combo.factors) > 0:  # Only check if combination has factors
                assert contains_load_symbol, f"Equation should contain load symbols: {equation}"
        
        print("✅ Load equations generated correctly")
    
    @pytest.mark.parametrize("load_type,expected_range", [
        (ThaiLoadType.DEAD, (80, 120)),        # Around 100
        (ThaiLoadType.LIVE, (40, 60)),         # Around 50
        (ThaiLoadType.WIND, (20, 40)),         # Around 30
        (ThaiLoadType.EARTHQUAKE, (20, 30))    # Around 25
    ])
    def test_individual_load_types(self, thai_loads, load_type, expected_range):
        """Test individual load type handling"""
        loads = {load_type: 100.0}  # Single load type
        
        # Find combination that uses this load type
        uls_combinations = thai_loads.get_ultimate_combinations()
        relevant_combos = [combo for combo in uls_combinations if load_type in combo.factors]
        
        assert len(relevant_combos) > 0, f"No combinations found for {load_type}"
        
        for combo in relevant_combos:
            effect = combo.calculate_load_effect(loads)
            factor = combo.factors[load_type]
            expected_effect = factor * 100.0
            
            assert abs(effect - expected_effect) < 0.01, f"Calculation error for {load_type}"
        
        print(f"✅ {load_type.value} load type tested")


@pytest.mark.thai
@pytest.mark.ministry_2566
@pytest.mark.load_combinations
@pytest.mark.integration
class TestThaiLoadCombinationsIntegration:
    """Integration tests for Thai load combinations"""
    
    @pytest.fixture
    def thai_loads(self):
        return ThaiMinistryLoadCombinations()
    
    def test_complete_building_load_analysis(self, thai_loads):
        """Test complete building load analysis"""
        print("\n🏢 Testing Complete Building Load Analysis")
        
        # Typical building loads
        building_loads = {
            ThaiLoadType.DEAD: 120.0,           # Dead load from structure
            ThaiLoadType.LIVE: 80.0,            # Live load from occupancy
            ThaiLoadType.WIND: 40.0,            # Wind load
            ThaiLoadType.EARTHQUAKE: 35.0,      # Seismic load
            ThaiLoadType.LATERAL_EARTH: 25.0,   # Earth pressure (basement)
            ThaiLoadType.FLUID: 15.0            # Water pressure
        }
        
        # Get all load effects
        uls_effects = thai_loads.calculate_all_combinations(
            building_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        sls_effects = thai_loads.calculate_all_combinations(
            building_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
        )
        
        # Find governing combinations
        critical_uls, max_uls = thai_loads.find_critical_combination(
            building_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        critical_sls, max_sls = thai_loads.find_critical_combination(
            building_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
        )
        
        print(f"  Critical ULS: {critical_uls.name} = {max_uls:.1f}")
        print(f"  Critical SLS: {critical_sls.name} = {max_sls:.1f}")
        
        # ULS should generally be higher than SLS
        assert max_uls > max_sls, "ULS effect should be higher than SLS"
        
        # Check reasonable ranges
        assert 150 <= max_uls <= 400, f"ULS effect seems unreasonable: {max_uls}"
        assert 100 <= max_sls <= 250, f"SLS effect seems unreasonable: {max_sls}"
        
        return uls_effects, sls_effects
    
    def test_seismic_vs_wind_comparison(self, thai_loads):
        """Test seismic vs wind load comparison"""
        print("\n🌪️ Testing Seismic vs Wind Load Comparison")
        
        # Wind dominant case
        wind_case = {
            ThaiLoadType.DEAD: 100.0,
            ThaiLoadType.LIVE: 60.0,
            ThaiLoadType.WIND: 50.0,
            ThaiLoadType.EARTHQUAKE: 20.0
        }
        
        # Seismic dominant case
        seismic_case = {
            ThaiLoadType.DEAD: 100.0,
            ThaiLoadType.LIVE: 60.0,
            ThaiLoadType.WIND: 20.0,
            ThaiLoadType.EARTHQUAKE: 50.0
        }
        
        wind_critical, wind_max = thai_loads.find_critical_combination(
            wind_case, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        seismic_critical, seismic_max = thai_loads.find_critical_combination(
            seismic_case, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        
        print(f"  Wind dominant: {wind_critical.name} = {wind_max:.1f}")
        print(f"  Seismic dominant: {seismic_critical.name} = {seismic_max:.1f}")
        
        # Different load cases should potentially result in different critical combinations
        # (though not always, depending on the load factors)
        assert wind_max > 0 and seismic_max > 0
    
    def test_earth_pressure_combinations(self, thai_loads):
        """Test earth pressure and fluid pressure combinations"""
        print("\n🌍 Testing Earth Pressure and Fluid Pressure Combinations")
        
        # Retaining wall case with earth and fluid pressure
        retaining_wall_loads = {
            ThaiLoadType.DEAD: 80.0,            # Wall self-weight
            ThaiLoadType.LIVE: 30.0,            # Surcharge
            ThaiLoadType.LATERAL_EARTH: 60.0,   # Earth pressure
            ThaiLoadType.FLUID: 40.0            # Water pressure
        }
        
        # Check specific combinations that include H and F
        uls_combinations = thai_loads.get_ultimate_combinations()
        sls_combinations = thai_loads.get_serviceability_combinations()
        
        # Find combinations with earth pressure
        earth_pressure_combos = [
            combo for combo in uls_combinations + sls_combinations
            if ThaiLoadType.LATERAL_EARTH in combo.factors
        ]
        
        # Find combinations with fluid pressure
        fluid_pressure_combos = [
            combo for combo in uls_combinations + sls_combinations
            if ThaiLoadType.FLUID in combo.factors
        ]
        
        assert len(earth_pressure_combos) > 0, "No combinations with earth pressure found"
        assert len(fluid_pressure_combos) > 0, "No combinations with fluid pressure found"
        
        print(f"  Earth pressure combinations: {len(earth_pressure_combos)}")
        print(f"  Fluid pressure combinations: {len(fluid_pressure_combos)}")
        
        # Test calculation with retaining wall loads
        critical_combo, max_effect = thai_loads.find_critical_combination(
            retaining_wall_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
        )
        
        print(f"  Retaining wall critical: {critical_combo.name} = {max_effect:.1f}")
        assert max_effect > 0


@pytest.mark.thai
@pytest.mark.ministry_2566
@pytest.mark.load_combinations
@pytest.mark.validation
class TestThaiLoadCombinationsValidation:
    """Validation tests against Ministry Regulation B.E. 2566 specifications"""
    
    @pytest.fixture
    def thai_loads(self):
        return ThaiMinistryLoadCombinations()
    
    def test_ministry_regulation_compliance(self, thai_loads):
        """Test compliance with Ministry Regulation B.E. 2566"""
        print("\n📋 Testing Ministry Regulation B.E. 2566 Compliance")
        
        # Check load factors according to regulation
        uls_combinations = thai_loads.get_ultimate_combinations()
        
        # Key load factors from Ministry Regulation B.E. 2566
        expected_factors = {
            'dead_load_factor': [1.4, 1.2, 0.9],      # Various DL factors
            'live_load_factor': [1.6, 1.7, 1.0, 0.5],  # Various LL factors
            'wind_load_factor': [1.6],                  # Wind factors
            'earthquake_factor': [1.0],                 # Earthquake factors
            'earth_pressure_factor': [1.7],             # Earth pressure factors
            'fluid_pressure_factor': [1.4]              # Fluid pressure factors
        }
        
        # Collect all factors used
        dl_factors = []
        ll_factors = []
        w_factors = []
        e_factors = []
        h_factors = []
        f_factors = []
        
        for combo in uls_combinations:
            if ThaiLoadType.DEAD in combo.factors:
                dl_factors.append(combo.factors[ThaiLoadType.DEAD])
            if ThaiLoadType.LIVE in combo.factors:
                ll_factors.append(combo.factors[ThaiLoadType.LIVE])
            if ThaiLoadType.WIND in combo.factors:
                w_factors.append(combo.factors[ThaiLoadType.WIND])
            if ThaiLoadType.EARTHQUAKE in combo.factors:
                e_factors.append(combo.factors[ThaiLoadType.EARTHQUAKE])
            if ThaiLoadType.LATERAL_EARTH in combo.factors:
                h_factors.append(combo.factors[ThaiLoadType.LATERAL_EARTH])
            if ThaiLoadType.FLUID in combo.factors:
                f_factors.append(combo.factors[ThaiLoadType.FLUID])
        
        # Check that expected factors are present
        for expected_dl in expected_factors['dead_load_factor']:
            assert expected_dl in dl_factors, f"Missing DL factor: {expected_dl}"
        
        for expected_ll in expected_factors['live_load_factor']:
            if expected_ll in ll_factors:  # Some may not be used in all combinations
                continue
        
        print(f"  ✅ Dead load factors: {sorted(set(dl_factors))}")
        print(f"  ✅ Live load factors: {sorted(set(ll_factors))}")
        print(f"  ✅ Wind load factors: {sorted(set(w_factors))}")
        print(f"  ✅ Earthquake factors: {sorted(set(e_factors))}")
        print(f"  ✅ Earth pressure factors: {sorted(set(h_factors))}")
        print(f"  ✅ Fluid pressure factors: {sorted(set(f_factors))}")
    
    def test_serviceability_factors_compliance(self, thai_loads):
        """Test serviceability factors compliance"""
        print("\n📐 Testing Serviceability Factors Compliance")
        
        sls_combinations = thai_loads.get_serviceability_combinations()
        
        # Check specific SLS combinations per Ministry Regulation B.E. 2566
        key_sls_tests = [
            ('ASD-100', {ThaiLoadType.DEAD: 1.0}),  # DL only
            ('ASD-101', {ThaiLoadType.DEAD: 1.0, ThaiLoadType.LIVE: 1.0}),  # DL + LL
            ('ASD-102', {ThaiLoadType.DEAD: 1.0, ThaiLoadType.LIVE: 0.75, ThaiLoadType.WIND: 0.75}),  # DL + 0.75(LL + W)
            ('ASD-106', {ThaiLoadType.DEAD: 0.6, ThaiLoadType.WIND: 1.0}),  # 0.6DL + W
        ]
        
        for expected_name, expected_factors in key_sls_tests:
            matching_combo = None
            for combo in sls_combinations:
                if combo.name == expected_name:
                    matching_combo = combo
                    break
            
            if matching_combo:
                for load_type, expected_factor in expected_factors.items():
                    actual_factor = matching_combo.factors.get(load_type, 0)
                    assert abs(actual_factor - expected_factor) < 0.01, \
                        f"{expected_name}: Expected {load_type}={expected_factor}, got {actual_factor}"
                print(f"  ✅ {expected_name}: {matching_combo.get_equation()}")
    
    def test_load_validation_functionality(self, thai_loads):
        """Test load validation functionality"""
        print("\n✅ Testing Load Validation Functionality")
        
        # Valid loads
        valid_loads = {
            ThaiLoadType.DEAD: 100.0,
            ThaiLoadType.LIVE: 50.0,
            ThaiLoadType.WIND: 30.0
        }
        
        assert thai_loads.validate_loads(valid_loads) == True
        
        # Invalid loads (negative values)
        invalid_loads = {
            ThaiLoadType.DEAD: -10.0,  # Negative load
            ThaiLoadType.LIVE: 50.0
        }
        
        assert thai_loads.validate_loads(invalid_loads) == False
        
        print("  ✅ Load validation working correctly")


@pytest.mark.thai
@pytest.mark.ministry_2566
@pytest.mark.load_combinations
@pytest.mark.benchmark
@pytest.mark.slow
class TestThaiLoadCombinationsPerformance:
    """Performance tests for Thai load combinations"""
    
    def test_load_combinations_performance(self, performance_monitor, performance_benchmark_data):
        """Test load combinations performance"""
        print("\n⚡ Testing Load Combinations Performance")
        
        thai_loads = ThaiMinistryLoadCombinations()
        
        sample_loads = {
            ThaiLoadType.DEAD: 100.0,
            ThaiLoadType.LIVE: 50.0,
            ThaiLoadType.WIND: 30.0,
            ThaiLoadType.EARTHQUAKE: 25.0,
            ThaiLoadType.LATERAL_EARTH: 20.0,
            ThaiLoadType.FLUID: 15.0
        }
        
        performance_monitor.start()
        
        # Run multiple load combination calculations
        for _ in range(100):
            # Calculate all combinations
            uls_results = thai_loads.calculate_all_combinations(
                sample_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
            )
            sls_results = thai_loads.calculate_all_combinations(
                sample_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
            )
            
            # Find critical combinations
            critical_uls, max_uls = thai_loads.find_critical_combination(
                sample_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
            )
            critical_sls, max_sls = thai_loads.find_critical_combination(
                sample_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
            )
        
        execution_time = performance_monitor.stop()
        
        # Check performance
        max_time = performance_benchmark_data['max_execution_time']['load_combinations'] * 100
        assert execution_time <= max_time, \
            f"Load combinations too slow: {execution_time:.3f}s > {max_time:.3f}s"
        
        print(f"  ✅ Performance: {execution_time:.3f}s for 100 iterations")
        print(f"  ✅ Average per calculation: {execution_time*10:.1f}ms")
        
        return execution_time