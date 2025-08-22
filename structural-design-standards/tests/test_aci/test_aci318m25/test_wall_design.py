"""
ACI 318M-25 Wall Design Tests
============================

Comprehensive tests for wall design according to ACI 318M-25.
Tests bearing walls, shear walls, and non-bearing walls.

การทดสอบการออกแบบกำแพงตาม ACI 318M-25
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.wall_design import (
    ACI318M25WallDesign, WallGeometry, WallLoads, WallType, WallBoundaryCondition
)
from structural_standards.base.design_base import DesignStatus


@pytest.mark.aci
@pytest.mark.wall
@pytest.mark.unit
class TestWallDesign:
    """Test wall design functionality"""
    
    @pytest.fixture
    def wall_designer(self, aci_concrete, aci_steel):
        """Create wall designer fixture"""
        return ACI318M25WallDesign(aci_concrete, aci_steel)
    
    @pytest.fixture
    def typical_wall_geometry(self):
        """Typical wall geometry"""
        return WallGeometry(
            length=4000,
            height=3000,
            thickness=200
        )
    
    @pytest.fixture
    def bearing_wall_loads(self):
        """Bearing wall loads"""
        return WallLoads(
            axial_dead=50,        # kN/m
            axial_live=30,        # kN/m
            wind_pressure=1.0     # kPa
        )
    
    def test_wall_designer_initialization(self, wall_designer):
        """Test wall designer initialization"""
        assert wall_designer.design_standard == "ACI 318M-25"
        assert wall_designer.fc == 28.0
        assert wall_designer.fy == 420.0
        assert wall_designer.phi_compression == 0.65
        assert wall_designer.phi_tension == 0.9
        assert wall_designer.phi_shear == 0.75
    
    def test_bearing_wall_design(self, wall_designer, typical_wall_geometry, bearing_wall_loads):
        """Test bearing wall design"""
        result = wall_designer.design(
            typical_wall_geometry, 
            bearing_wall_loads, 
            WallType.BEARING,
            WallBoundaryCondition.PINNED_TOP_BOTTOM
        )
        
        # Validate result structure
        assert hasattr(result, 'member_type')
        assert hasattr(result, 'design_method')
        assert hasattr(result, 'overall_status')
        assert hasattr(result, 'utilization_ratio')
        
        # Check design method
        assert result.design_method == "ACI 318M-25"
        assert result.member_type == "wall"
        
        # Check that reinforcement is calculated
        assert 'vertical_reinforcement_ratio' in result.required_reinforcement
        assert 'horizontal_reinforcement_ratio' in result.required_reinforcement
    
    def test_shear_wall_design(self, wall_designer, typical_wall_geometry):
        """Test shear wall design"""
        shear_loads = WallLoads(
            axial_dead=30,
            axial_live=20,
            shear_force=150,          # kN
            overturning_moment=300    # kN⋅m
        )
        
        result = wall_designer.design(
            typical_wall_geometry,
            shear_loads,
            WallType.SHEAR,
            WallBoundaryCondition.FIXED_TOP_BOTTOM
        )
        
        # Validate complete design result
        assert result.member_type == "wall"
        assert result.design_method == "ACI 318M-25"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Check that all checks are performed
        assert len(result.strength_checks) > 0
        
        # Check required reinforcement for shear wall
        assert 'flexural_reinforcement' in result.required_reinforcement
        assert 'shear_reinforcement_area' in result.required_reinforcement
    
    def test_non_bearing_wall_design(self, wall_designer, typical_wall_geometry):
        """Test non-bearing wall design"""
        lateral_loads = WallLoads(
            wind_pressure=1.5,    # kPa
            seismic_pressure=0.8  # kPa
        )
        
        result = wall_designer.design(
            typical_wall_geometry,
            lateral_loads,
            WallType.NON_BEARING,
            WallBoundaryCondition.PINNED_TOP_BOTTOM
        )
        
        # Should handle lateral loads only
        assert result.member_type == "wall"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Check required reinforcement
        assert 'required_reinforcement' in result.required_reinforcement
    
    def test_slenderness_checks(self, wall_designer, bearing_wall_loads):
        """Test slenderness ratio checks"""
        # Slender wall
        slender_geometry = WallGeometry(
            length=4000,
            height=6000,  # High wall
            thickness=150  # Thin wall
        )
        
        result = wall_designer.design(
            slender_geometry,
            bearing_wall_loads,
            WallType.BEARING
        )
        
        # Should include slenderness checks
        slenderness_check_found = any(
            'slenderness' in check.name.lower() 
            for check in result.strength_checks
        )
        assert slenderness_check_found
    
    def test_minimum_thickness_requirements(self, wall_designer, bearing_wall_loads):
        """Test minimum thickness requirements"""
        test_cases = [
            (WallType.BEARING, 3000, 100),    # Bearing wall
            (WallType.SHEAR, 3000, 150),      # Shear wall  
            (WallType.NON_BEARING, 3000, 75)  # Non-bearing wall
        ]
        
        for wall_type, height, min_thickness in test_cases:
            geometry = WallGeometry(
                length=4000,
                height=height,
                thickness=min_thickness + 50  # Above minimum
            )
            
            result = wall_designer.design(geometry, bearing_wall_loads, wall_type)
            
            # Check thickness requirements
            thickness_check_found = any(
                'thickness' in check.name.lower() 
                for check in result.detailing_checks
            )
            assert thickness_check_found
    
    @pytest.mark.parametrize("boundary_condition", [
        WallBoundaryCondition.PINNED_TOP_BOTTOM,
        WallBoundaryCondition.FIXED_TOP_BOTTOM,
        WallBoundaryCondition.CANTILEVER
    ])
    def test_different_boundary_conditions(self, wall_designer, typical_wall_geometry, 
                                         bearing_wall_loads, boundary_condition):
        """Test wall design with different boundary conditions"""
        result = wall_designer.design(
            typical_wall_geometry,
            bearing_wall_loads,
            WallType.BEARING,
            boundary_condition
        )
        
        # All boundary conditions should be handled
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Boundary condition should affect design
        assert 'moment_per_meter' in result.design_forces


@pytest.mark.aci
@pytest.mark.wall
@pytest.mark.integration
class TestWallIntegration:
    """Test wall design integration scenarios"""
    
    @pytest.fixture
    def wall_designer(self, aci_concrete, aci_steel):
        return ACI318M25WallDesign(aci_concrete, aci_steel)
    
    def test_high_wall_design(self, wall_designer):
        """Test high wall design"""
        high_geometry = WallGeometry(
            length=6000,
            height=8000,  # High wall
            thickness=250
        )
        
        loads = WallLoads(
            axial_dead=80,
            axial_live=50,
            wind_pressure=1.2
        )
        
        result = wall_designer.design(
            high_geometry, loads, WallType.BEARING
        )
        
        # Should handle high wall with special considerations
        assert result.member_type == "wall"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_thick_wall_design(self, wall_designer, bearing_wall_loads):
        """Test thick wall design"""
        thick_geometry = WallGeometry(
            length=4000,
            height=3000,
            thickness=400  # Thick wall
        )
        
        result = wall_designer.design(
            thick_geometry, bearing_wall_loads, WallType.BEARING
        )
        
        # Should handle thick wall analysis
        assert result.member_type == "wall"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_combined_loading(self, wall_designer, typical_wall_geometry):
        """Test wall with combined loading"""
        combined_loads = WallLoads(
            axial_dead=60,
            axial_live=40,
            wind_pressure=1.5,
            seismic_pressure=1.0,
            shear_force=100,
            overturning_moment=200
        )
        
        result = wall_designer.design(
            typical_wall_geometry,
            combined_loads,
            WallType.SHEAR
        )
        
        # Should handle combined effects
        assert result.member_type == "wall"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]


@pytest.mark.aci
@pytest.mark.wall
@pytest.mark.validation
class TestWallValidation:
    """Test wall design against known solutions"""
    
    @pytest.fixture
    def wall_designer(self, aci_concrete, aci_steel):
        return ACI318M25WallDesign(aci_concrete, aci_steel)
    
    def test_known_bearing_wall_solution(self, wall_designer):
        """Test against known bearing wall solution"""
        # Known problem: Bearing wall with axial load and wind
        geometry = WallGeometry(
            length=4000,
            height=3000,
            thickness=200
        )
        
        loads = WallLoads(
            axial_dead=50,
            axial_live=30,
            wind_pressure=1.0
        )
        
        result = wall_designer.design(
            geometry, loads, WallType.BEARING, 
            WallBoundaryCondition.PINNED_TOP_BOTTOM
        )
        
        # Check result is reasonable
        assert result.overall_status == DesignStatus.PASS
        
        # Check reinforcement ratios
        rho_v = result.required_reinforcement['vertical_reinforcement_ratio']
        rho_h = result.required_reinforcement['horizontal_reinforcement_ratio']
        
        # Should be reasonable ratios
        assert 0.0012 <= rho_v <= 0.04  # ACI limits
        assert 0.0012 <= rho_h <= 0.04
    
    def test_shear_wall_capacity(self, wall_designer):
        """Test shear wall capacity"""
        geometry = WallGeometry(
            length=3000,
            height=4000,
            thickness=200
        )
        
        # High shear load
        loads = WallLoads(
            axial_dead=40,
            axial_live=25,
            shear_force=200,
            overturning_moment=600
        )
        
        result = wall_designer.design(geometry, loads, WallType.SHEAR)
        
        # Should handle high shear loads
        assert result.member_type == "wall"
        
        # Check if boundary elements are required
        if 'boundary_elements_required' in result.required_reinforcement:
            boundary_required = result.required_reinforcement['boundary_elements_required']
            # High overturning moment should typically require boundary elements
            assert isinstance(boundary_required, bool)


@pytest.mark.aci
@pytest.mark.wall
@pytest.mark.benchmark
@pytest.mark.slow
class TestWallPerformance:
    """Test wall design performance"""
    
    @pytest.fixture
    def wall_designer(self, aci_concrete, aci_steel):
        return ACI318M25WallDesign(aci_concrete, aci_steel)
    
    def test_design_performance(self, wall_designer, performance_monitor, performance_benchmark_data):
        """Test wall design performance"""
        geometry = WallGeometry(length=4000, height=3000, thickness=200)
        loads = WallLoads(axial_dead=50, axial_live=30, wind_pressure=1.0)
        
        # Measure performance
        performance_monitor.start()
        
        for _ in range(10):  # Multiple iterations
            result = wall_designer.design(
                geometry, loads, WallType.BEARING,
                WallBoundaryCondition.PINNED_TOP_BOTTOM
            )
        
        execution_time = performance_monitor.stop()
        
        # Check performance against benchmark
        max_time = performance_benchmark_data['max_execution_time']['wall_design'] * 10
        assert execution_time <= max_time, f"Wall design too slow: {execution_time:.3f}s > {max_time:.3f}s"
        
        # Check memory usage
        memory_usage = performance_monitor.memory_usage()
        max_memory = performance_benchmark_data['memory_usage_limit']
        assert memory_usage <= max_memory, f"Memory usage too high: {memory_usage:.1f}MB > {max_memory}MB"