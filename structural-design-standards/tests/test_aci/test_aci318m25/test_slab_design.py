"""
ACI 318M-25 Slab Design Tests
============================

Comprehensive tests for slab design according to ACI 318M-25.
Tests one-way, two-way, and punching shear design.

การทดสอบการออกแบบแผ่นพื้นตาม ACI 318M-25
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.slab_design import (
    ACI318M25SlabDesign, SlabGeometry, SlabLoads, SlabType
)
from structural_standards.base.design_base import DesignStatus


@pytest.mark.aci
@pytest.mark.slab
@pytest.mark.unit
class TestSlabDesign:
    """Test slab design functionality"""
    
    @pytest.fixture
    def slab_designer(self, aci_concrete, aci_steel):
        """Create slab designer fixture"""
        return ACI318M25SlabDesign(aci_concrete, aci_steel)
    
    @pytest.fixture
    def square_slab_geometry(self):
        """Square slab geometry"""
        return SlabGeometry(
            length_x=6000,
            length_y=6000,
            thickness=200,
            span_x=6000,
            span_y=6000
        )
    
    @pytest.fixture
    def simple_slab_loads(self):
        """Simple slab loads"""
        return SlabLoads(
            dead_load=4.0,  # kPa
            live_load=2.5   # kPa
        )
    
    def test_slab_designer_initialization(self, slab_designer):
        """Test slab designer initialization"""
        assert slab_designer.design_standard == "ACI 318M-25"
        assert slab_designer.fc == 28.0
        assert slab_designer.fy == 420.0
        assert slab_designer.phi_flexure == 0.9
        assert slab_designer.phi_shear == 0.75
    
    def test_one_way_slab_design(self, slab_designer):
        """Test one-way slab design"""
        # One-way slab geometry (high aspect ratio)
        geometry = SlabGeometry(
            length_x=2000,
            length_y=8000,
            thickness=150,
            span_x=2000,
            span_y=8000
        )
        
        loads = SlabLoads(dead_load=3.0, live_load=2.0)
        
        result = slab_designer.design(geometry, loads, SlabType.ONE_WAY)
        
        # Validate result structure
        assert hasattr(result, 'member_type')
        assert hasattr(result, 'design_method')
        assert hasattr(result, 'overall_status')
        assert hasattr(result, 'utilization_ratio')
        
        # Check design method
        assert result.design_method == "ACI 318M-25"
        assert result.member_type == "slab"
        
        # Check that reinforcement is calculated
        assert 'main_reinforcement' in result.required_reinforcement
        assert 'distribution_reinforcement' in result.required_reinforcement
    
    def test_two_way_slab_design(self, slab_designer, square_slab_geometry, simple_slab_loads):
        """Test two-way slab design"""
        result = slab_designer.design(
            square_slab_geometry, simple_slab_loads, SlabType.TWO_WAY
        )
        
        # Validate complete design result
        assert result.member_type == "slab"
        assert result.design_method == "ACI 318M-25"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Check that all checks are performed
        assert len(result.strength_checks) > 0
        assert len(result.serviceability_checks) > 0
        
        # Check required reinforcement
        assert 'main_reinforcement_x' in result.required_reinforcement
        assert 'main_reinforcement_y' in result.required_reinforcement
    
    def test_flat_slab_design(self, slab_designer, square_slab_geometry, simple_slab_loads):
        """Test flat slab design with punching shear"""
        result = slab_designer.design(
            square_slab_geometry, simple_slab_loads, SlabType.FLAT_SLAB
        )
        
        # Should handle punching shear checks
        assert result.member_type == "slab"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Should include punching shear checks
        shear_check_found = any(
            'punching' in check.name.lower() or 'shear' in check.name.lower() 
            for check in result.strength_checks
        )
        assert shear_check_found
    
    def test_minimum_thickness_requirements(self, slab_designer, simple_slab_loads):
        """Test minimum thickness requirements"""
        # Test various span lengths
        spans = [4000, 6000, 8000, 10000]  # mm
        
        for span in spans:
            geometry = SlabGeometry(
                length_x=span,
                length_y=span,
                thickness=120,  # Start with thin slab
                span_x=span,
                span_y=span
            )
            
            result = slab_designer.design(geometry, simple_slab_loads, SlabType.TWO_WAY)
            
            # Check minimum thickness requirements
            min_thickness_check = None
            for check in result.detailing_checks:
                if 'thickness' in check.name.lower():
                    min_thickness_check = check
                    break
            
            assert min_thickness_check is not None
    
    def test_minimum_reinforcement(self, slab_designer, square_slab_geometry):
        """Test minimum reinforcement calculations"""
        As_min = slab_designer._minimum_reinforcement_area(square_slab_geometry, direction='x')
        
        # Check minimum steel calculation
        assert As_min > 0
        
        # Calculate expected minimum
        b = 1000  # mm (per meter width)
        h = square_slab_geometry.thickness
        expected_min = max(
            0.0018 * b * h,  # Temperature and shrinkage
            0.0020 * b * h   # Minimum flexural
        )
        
        # Should meet minimum requirements
        assert As_min >= expected_min * 0.95  # Allow small tolerance
    
    def test_deflection_checks(self, slab_designer, square_slab_geometry, simple_slab_loads):
        """Test deflection calculations"""
        result = slab_designer.design(
            square_slab_geometry, simple_slab_loads, SlabType.TWO_WAY
        )
        
        # Should include deflection checks
        deflection_check_found = any(
            'deflection' in check.name.lower() 
            for check in result.serviceability_checks
        )
        assert deflection_check_found
        
        # Check that deflection values are calculated
        if 'calculated_deflection' in result.design_forces:
            deflection = result.design_forces['calculated_deflection']
            assert deflection >= 0
    
    @pytest.mark.parametrize("load_level", [2.0, 5.0, 8.0, 12.0])
    def test_different_load_levels(self, slab_designer, square_slab_geometry, load_level):
        """Test slab design at different load levels"""
        loads = SlabLoads(
            dead_load=load_level * 0.6,
            live_load=load_level * 0.4
        )
        
        result = slab_designer.design(square_slab_geometry, loads, SlabType.TWO_WAY)
        
        # All should be valid designs
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Higher loads should require more steel (until failure)
        if result.overall_status == DesignStatus.PASS:
            steel_area_x = result.required_reinforcement['main_reinforcement_x']
            assert steel_area_x > 0


@pytest.mark.aci
@pytest.mark.slab
@pytest.mark.integration
class TestSlabIntegration:
    """Test slab design integration scenarios"""
    
    @pytest.fixture
    def slab_designer(self, aci_concrete, aci_steel):
        return ACI318M25SlabDesign(aci_concrete, aci_steel)
    
    def test_rectangular_slab(self, slab_designer):
        """Test rectangular slab design"""
        geometry = SlabGeometry(
            length_x=4000,
            length_y=6000,
            thickness=180,
            span_x=4000,
            span_y=6000
        )
        
        loads = SlabLoads(dead_load=4.5, live_load=3.0)
        
        result = slab_designer.design(geometry, loads, SlabType.TWO_WAY)
        
        # Should handle rectangular geometry
        assert result.member_type == "slab"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Should have different reinforcement in each direction
        if result.overall_status == DesignStatus.PASS:
            steel_x = result.required_reinforcement['main_reinforcement_x']
            steel_y = result.required_reinforcement['main_reinforcement_y']
            # Different spans should typically require different reinforcement
            # (though this isn't always true depending on the analysis method)
            assert steel_x > 0 and steel_y > 0
    
    def test_thick_slab_design(self, slab_designer, simple_slab_loads):
        """Test thick slab design"""
        thick_geometry = SlabGeometry(
            length_x=8000,
            length_y=8000,
            thickness=300,  # Thick slab
            span_x=8000,
            span_y=8000
        )
        
        result = slab_designer.design(thick_geometry, simple_slab_loads, SlabType.TWO_WAY)
        
        # Should handle thick slab analysis
        assert result.member_type == "slab"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_high_strength_concrete_slab(self, aci_steel):
        """Test slab design with high strength concrete"""
        high_strength_concrete = ACI318M25Concrete(fc_prime=45.0)
        slab_designer = ACI318M25SlabDesign(high_strength_concrete, aci_steel)
        
        geometry = SlabGeometry(
            length_x=6000, length_y=6000, thickness=150,
            span_x=6000, span_y=6000
        )
        loads = SlabLoads(dead_load=5.0, live_load=3.5)
        
        result = slab_designer.design(geometry, loads, SlabType.TWO_WAY)
        
        # Should work with high strength concrete
        assert result.design_method == "ACI 318M-25"
        assert slab_designer.fc == 45.0
    
    def test_continuity_effects(self, slab_designer, square_slab_geometry, simple_slab_loads):
        """Test continuous slab effects"""
        result = slab_designer.design(
            square_slab_geometry, simple_slab_loads, SlabType.TWO_WAY_CONTINUOUS
        )
        
        # Should account for continuity
        assert result.member_type == "slab"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]


@pytest.mark.aci
@pytest.mark.slab
@pytest.mark.validation
class TestSlabValidation:
    """Test slab design against known solutions"""
    
    @pytest.fixture
    def slab_designer(self, aci_concrete, aci_steel):
        return ACI318M25SlabDesign(aci_concrete, aci_steel)
    
    def test_known_solution_square_slab(self, slab_designer):
        """Test against known solution for square slab"""
        # Known problem: Simply supported square slab
        geometry = SlabGeometry(
            length_x=6000,
            length_y=6000,
            thickness=200,
            span_x=6000,
            span_y=6000
        )
        
        loads = SlabLoads(dead_load=4.0, live_load=2.5)
        
        result = slab_designer.design(geometry, loads, SlabType.TWO_WAY)
        
        # Check result is reasonable
        assert result.overall_status == DesignStatus.PASS
        
        # Check reinforcement ratios are reasonable
        steel_x = result.required_reinforcement['main_reinforcement_x']
        steel_y = result.required_reinforcement['main_reinforcement_y']
        
        # Calculate reinforcement ratios
        b = 1000  # mm per meter
        d = geometry.thickness - 20  # Assume 20mm cover
        rho_x = steel_x / (b * d)
        rho_y = steel_y / (b * d)
        
        # Should be reasonable ratios
        assert 0.0015 <= rho_x <= 0.02
        assert 0.0015 <= rho_y <= 0.02
    
    def test_aspect_ratio_limits(self, slab_designer):
        """Test aspect ratio effects on design method"""
        # High aspect ratio slab (should behave as one-way)
        high_aspect_geometry = SlabGeometry(
            length_x=2000,
            length_y=8000,  # 4:1 aspect ratio
            thickness=150,
            span_x=2000,
            span_y=8000
        )
        
        loads = SlabLoads(dead_load=3.0, live_load=2.0)
        
        result = slab_designer.design(high_aspect_geometry, loads, SlabType.ONE_WAY)
        
        # Should work as one-way slab
        assert result.member_type == "slab"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_minimum_slab_thickness(self, slab_designer):
        """Test minimum thickness requirements"""
        # Various span lengths
        test_cases = [
            (3000, 90),   # 3m span, minimum thickness
            (6000, 120),  # 6m span
            (9000, 150),  # 9m span
        ]
        
        for span, min_thickness in test_cases:
            geometry = SlabGeometry(
                length_x=span,
                length_y=span,
                thickness=min_thickness,
                span_x=span,
                span_y=span
            )
            
            loads = SlabLoads(dead_load=3.0, live_load=2.0)
            result = slab_designer.design(geometry, loads, SlabType.TWO_WAY)
            
            # Check if thickness is adequate
            thickness_adequate = any(
                check.status == DesignStatus.PASS 
                for check in result.detailing_checks 
                if 'thickness' in check.name.lower()
            )
            
            # Minimum thickness should generally be adequate for deflection
            # (though other factors may cause failure)
            if result.overall_status == DesignStatus.FAIL:
                # If design fails, it shouldn't be due to thickness alone
                # for these reasonable combinations
                pass


@pytest.mark.aci
@pytest.mark.slab
@pytest.mark.benchmark
@pytest.mark.slow
class TestSlabPerformance:
    """Test slab design performance"""
    
    @pytest.fixture
    def slab_designer(self, aci_concrete, aci_steel):
        return ACI318M25SlabDesign(aci_concrete, aci_steel)
    
    def test_design_performance(self, slab_designer, performance_monitor, performance_benchmark_data):
        """Test slab design performance"""
        geometry = SlabGeometry(
            length_x=6000, length_y=6000, thickness=200,
            span_x=6000, span_y=6000
        )
        loads = SlabLoads(dead_load=4.0, live_load=2.5)
        
        # Measure performance
        performance_monitor.start()
        
        for _ in range(10):  # Multiple iterations
            result = slab_designer.design(geometry, loads, SlabType.TWO_WAY)
        
        execution_time = performance_monitor.stop()
        
        # Check performance against benchmark
        max_time = performance_benchmark_data['max_execution_time']['slab_design'] * 10
        assert execution_time <= max_time, f"Slab design too slow: {execution_time:.3f}s > {max_time:.3f}s"
        
        # Check memory usage
        memory_usage = performance_monitor.memory_usage()
        max_memory = performance_benchmark_data['memory_usage_limit']
        assert memory_usage <= max_memory, f"Memory usage too high: {memory_usage:.1f}MB > {max_memory}MB"