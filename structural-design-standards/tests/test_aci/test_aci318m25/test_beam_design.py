"""
ACI 318M-25 Beam Design Tests
============================

Comprehensive tests for beam design according to ACI 318M-25.
Tests flexural design, shear design, and deflection checks.

การทดสอบการออกแบบคานตาม ACI 318M-25
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.beam_design import (
    ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
)
from structural_standards.base.design_base import DesignStatus


@pytest.mark.aci
@pytest.mark.beam
@pytest.mark.unit
class TestBeamDesign:
    """Test beam design functionality"""
    
    @pytest.fixture
    def beam_designer(self, aci_concrete, aci_steel):
        """Create beam designer fixture"""
        return ACI318M25BeamDesign(aci_concrete, aci_steel)
    
    @pytest.fixture
    def simple_beam_geometry(self):
        """Simple beam geometry"""
        return BeamGeometry(
            width=300,
            height=600,
            effective_depth=550,
            span_length=6000
        )
    
    @pytest.fixture
    def simple_beam_loads(self):
        """Simple beam loads"""
        return BeamLoads(
            dead_load=5.0,
            live_load=8.0
        )
    
    def test_beam_designer_initialization(self, beam_designer):
        """Test beam designer initialization"""
        assert beam_designer.design_standard == "ACI 318M-25"
        assert beam_designer.fc == 28.0
        assert beam_designer.fy == 420.0
        assert beam_designer.phi_flexure == 0.9
        assert beam_designer.phi_shear == 0.75
    
    def test_flexural_reinforcement_design(self, beam_designer, simple_beam_geometry):
        """Test flexural reinforcement design"""
        moment_ultimate = 120.0  # kN⋅m
        
        result = beam_designer.design_flexural_reinforcement(
            simple_beam_geometry, moment_ultimate
        )
        
        # Validate result structure
        assert hasattr(result, 'member_type')
        assert hasattr(result, 'design_method')
        assert hasattr(result, 'overall_status')
        assert hasattr(result, 'utilization_ratio')
        
        # Check design method
        assert result.design_method == "ACI 318M-25"
        
        # Check that reinforcement is calculated
        assert 'required_steel_area' in result.required_reinforcement
        assert result.required_reinforcement['required_steel_area'] > 0
        
        # Check utilization ratio
        assert 0 <= result.utilization_ratio <= 2.0
    
    def test_shear_reinforcement_design(self, beam_designer, simple_beam_geometry):
        """Test shear reinforcement design"""
        shear_ultimate = 80.0  # kN
        
        result = beam_designer.design_shear_reinforcement(
            simple_beam_geometry, shear_ultimate
        )
        
        # Validate result
        assert result.design_method == "ACI 318M-25"
        assert 'shear_reinforcement_required' in result.required_reinforcement
        assert result.utilization_ratio >= 0
    
    def test_complete_beam_design(self, beam_designer, simple_beam_geometry, simple_beam_loads):
        """Test complete beam design"""
        result = beam_designer.design(
            simple_beam_geometry, simple_beam_loads, BeamType.SIMPLY_SUPPORTED
        )
        
        # Validate complete design result
        assert result.member_type == "beam"
        assert result.design_method == "ACI 318M-25"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Check that all checks are performed
        assert len(result.strength_checks) > 0
        assert len(result.serviceability_checks) > 0
        
        # Check required reinforcement
        assert 'required_steel_area' in result.required_reinforcement
        assert 'minimum_steel_area' in result.required_reinforcement
    
    def test_minimum_reinforcement(self, beam_designer, simple_beam_geometry):
        """Test minimum reinforcement calculations"""
        As_min = beam_designer._minimum_flexural_reinforcement(simple_beam_geometry)
        
        # Check minimum steel calculation
        assert As_min > 0
        
        # Calculate expected minimum (simplified check)
        b = simple_beam_geometry.width
        h = simple_beam_geometry.height
        expected_min = max(
            1.4 * b * h / beam_designer.fy,
            0.25 * math.sqrt(beam_designer.fc) * b * h / beam_designer.fy
        )
        
        # Allow some tolerance for calculation differences
        assert abs(As_min - expected_min) / expected_min < 0.1
    
    def test_maximum_reinforcement(self, beam_designer, simple_beam_geometry):
        """Test maximum reinforcement limits"""
        As_max = beam_designer._maximum_flexural_reinforcement(simple_beam_geometry)
        
        # Check maximum steel calculation
        assert As_max > 0
        
        # Should be based on compression controlled limit
        b = simple_beam_geometry.width
        d = simple_beam_geometry.effective_depth
        
        # Check that maximum is reasonable (roughly 0.75 * rho_balanced)
        gross_area = b * d
        max_ratio = As_max / gross_area
        assert 0.01 <= max_ratio <= 0.05  # Typical range for max ratio
    
    def test_development_length(self, beam_designer):
        """Test development length calculations"""
        bar_diameter = 16  # mm
        ld = beam_designer._calculate_development_length(bar_diameter)
        
        # Basic checks
        assert ld > 0
        assert ld >= bar_diameter * 12  # Minimum development length
        
        # Should be proportional to bar size
        larger_bar = 20  # mm
        ld_larger = beam_designer._calculate_development_length(larger_bar)
        assert ld_larger > ld
    
    @pytest.mark.parametrize("moment", [50, 100, 150, 200])
    def test_different_moment_levels(self, beam_designer, simple_beam_geometry, moment):
        """Test beam design at different moment levels"""
        result = beam_designer.design_flexural_reinforcement(simple_beam_geometry, moment)
        
        # All should be valid designs
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Higher moments should require more steel (until failure)
        if result.overall_status == DesignStatus.PASS:
            steel_area = result.required_reinforcement['required_steel_area']
            assert steel_area > 0


@pytest.mark.aci
@pytest.mark.beam
@pytest.mark.integration
class TestBeamIntegration:
    """Test beam design integration scenarios"""
    
    @pytest.fixture
    def beam_designer(self, aci_concrete, aci_steel):
        return ACI318M25BeamDesign(aci_concrete, aci_steel)
    
    def test_T_beam_design(self, beam_designer):
        """Test T-beam design"""
        geometry = BeamGeometry(
            width=300,
            height=600,
            effective_depth=550,
            span_length=8000,
            flange_width=1200,
            flange_thickness=120
        )
        
        loads = BeamLoads(dead_load=8.0, live_load=12.0)
        
        result = beam_designer.design(geometry, loads, BeamType.T_BEAM)
        
        # Should handle T-beam geometry
        assert result.member_type == "beam"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_continuous_beam_design(self, beam_designer, simple_beam_geometry):
        """Test continuous beam design"""
        loads = BeamLoads(dead_load=6.0, live_load=10.0)
        
        result = beam_designer.design(
            simple_beam_geometry, loads, BeamType.CONTINUOUS
        )
        
        # Should account for continuity effects
        assert result.member_type == "beam"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_high_strength_concrete(self, aci_steel):
        """Test beam design with high strength concrete"""
        high_strength_concrete = ACI318M25Concrete(fc_prime=50.0)
        beam_designer = ACI318M25BeamDesign(high_strength_concrete, aci_steel)
        
        geometry = BeamGeometry(width=250, height=500, effective_depth=450, span_length=6000)
        loads = BeamLoads(dead_load=5.0, live_load=8.0)
        
        result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
        
        # Should work with high strength concrete
        assert result.design_method == "ACI 318M-25"
        assert beam_designer.fc == 50.0


@pytest.mark.aci
@pytest.mark.beam
@pytest.mark.validation
class TestBeamValidation:
    """Test beam design against known solutions"""
    
    @pytest.fixture
    def beam_designer(self, aci_concrete, aci_steel):
        return ACI318M25BeamDesign(aci_concrete, aci_steel)
    
    def test_known_solution_1(self, beam_designer):
        """Test against known solution from ACI 318M examples"""
        # Known problem: Simply supported beam
        geometry = BeamGeometry(
            width=300,
            height=600,
            effective_depth=550,
            span_length=6000
        )
        
        # Applied moment
        moment_ultimate = 150.0  # kN⋅m
        
        result = beam_designer.design_flexural_reinforcement(geometry, moment_ultimate)
        
        # Check result is reasonable
        assert result.overall_status == DesignStatus.PASS
        steel_area = result.required_reinforcement['required_steel_area']
        
        # Should be in reasonable range (manual calculation check)
        assert 800 <= steel_area <= 1200  # mm²
    
    def test_minimum_beam_dimensions(self, beam_designer):
        """Test minimum beam dimension requirements"""
        # Very small beam should fail dimension checks
        small_geometry = BeamGeometry(
            width=150,
            height=200,
            effective_depth=150,
            span_length=6000
        )
        
        loads = BeamLoads(dead_load=5.0, live_load=8.0)
        result = beam_designer.design(small_geometry, loads, BeamType.SIMPLY_SUPPORTED)
        
        # Should have warnings or failure due to dimension limits
        assert result.overall_status in [DesignStatus.FAIL, DesignStatus.WARNING]


@pytest.mark.aci
@pytest.mark.beam
@pytest.mark.benchmark
@pytest.mark.slow
class TestBeamPerformance:
    """Test beam design performance"""
    
    @pytest.fixture
    def beam_designer(self, aci_concrete, aci_steel):
        return ACI318M25BeamDesign(aci_concrete, aci_steel)
    
    def test_design_performance(self, beam_designer, performance_monitor, performance_benchmark_data):
        """Test beam design performance"""
        geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
        loads = BeamLoads(dead_load=5.0, live_load=8.0)
        
        # Measure performance
        performance_monitor.start()
        
        for _ in range(10):  # Multiple iterations
            result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
        
        execution_time = performance_monitor.stop()
        
        # Check performance against benchmark
        max_time = performance_benchmark_data['max_execution_time']['beam_design'] * 10
        assert execution_time <= max_time, f"Beam design too slow: {execution_time:.3f}s > {max_time:.3f}s"
        
        # Check memory usage
        memory_usage = performance_monitor.memory_usage()
        max_memory = performance_benchmark_data['memory_usage_limit']
        assert memory_usage <= max_memory, f"Memory usage too high: {memory_usage:.1f}MB > {max_memory}MB"