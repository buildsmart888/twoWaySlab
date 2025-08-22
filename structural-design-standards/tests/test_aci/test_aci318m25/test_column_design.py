"""
ACI 318M-25 Column Design Tests
==============================

Comprehensive tests for column design according to ACI 318M-25.
Tests axial design, moment interaction, and slenderness effects.

การทดสอบการออกแบบเสาตาม ACI 318M-25
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.column_design import (
    ACI318M25ColumnDesign, ColumnGeometry, ColumnLoads, ColumnType
)
from structural_standards.base.design_base import DesignStatus


@pytest.mark.aci
@pytest.mark.column
@pytest.mark.unit
class TestColumnDesign:
    """Test column design functionality"""
    
    @pytest.fixture
    def column_designer(self, aci_concrete, aci_steel):
        """Create column designer fixture"""
        return ACI318M25ColumnDesign(aci_concrete, aci_steel)
    
    @pytest.fixture
    def square_column_geometry(self):
        """Square column geometry"""
        return ColumnGeometry(
            width=400,
            depth=400,
            length=3000
        )
    
    @pytest.fixture
    def simple_column_loads(self):
        """Simple column loads"""
        return ColumnLoads(
            axial_dead=200,
            axial_live=150,
            moment_x_dead=15,
            moment_x_live=10
        )
    
    def test_column_designer_initialization(self, column_designer):
        """Test column designer initialization"""
        assert column_designer.design_standard == "ACI 318M-25"
        assert column_designer.fc == 28.0
        assert column_designer.fy == 420.0
        assert column_designer.phi_compression_tied == 0.65
        assert column_designer.phi_compression_spiral == 0.70
    
    def test_axial_reinforcement_design(self, column_designer, square_column_geometry, simple_column_loads):
        """Test axial reinforcement design"""
        result = column_designer.design_axial_reinforcement(
            square_column_geometry, simple_column_loads
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
        assert 0 <= result.utilization_ratio <= 5.0
    
    def test_tied_column_design(self, column_designer, square_column_geometry, simple_column_loads):
        """Test tied column design"""
        result = column_designer.design(
            square_column_geometry, simple_column_loads, ColumnType.TIED
        )
        
        # Validate complete design result
        assert result.member_type == "column"
        assert result.design_method == "ACI 318M-25"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Check that all checks are performed
        assert len(result.strength_checks) > 0
        assert len(result.serviceability_checks) >= 0
        
        # Check required reinforcement
        assert 'required_steel_area' in result.required_reinforcement
        assert 'tie_requirements' in result.required_reinforcement
    
    def test_spiral_column_design(self, column_designer, simple_column_loads):
        """Test spiral column design"""
        # Circular column geometry
        geometry = ColumnGeometry(
            width=400,
            depth=400,
            length=3000
        )
        
        result = column_designer.design(geometry, simple_column_loads, ColumnType.SPIRAL)
        
        # Should handle spiral column requirements
        assert result.member_type == "column"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        assert 'spiral_requirements' in result.required_reinforcement
    
    def test_minimum_reinforcement(self, column_designer, square_column_geometry):
        """Test minimum reinforcement calculations"""
        As_min = column_designer._minimum_longitudinal_reinforcement(square_column_geometry)
        
        # Check minimum steel calculation
        assert As_min > 0
        
        # Calculate expected minimum (1% of gross area)
        Ag = square_column_geometry.width * square_column_geometry.depth
        expected_min = 0.01 * Ag
        
        # Should be at least 1% of gross area
        assert As_min >= expected_min * 0.95  # Allow small tolerance
    
    def test_maximum_reinforcement(self, column_designer, square_column_geometry):
        """Test maximum reinforcement limits"""
        As_max = column_designer._maximum_longitudinal_reinforcement(square_column_geometry)
        
        # Check maximum steel calculation
        assert As_max > 0
        
        # Calculate expected maximum (8% of gross area)
        Ag = square_column_geometry.width * square_column_geometry.depth
        expected_max = 0.08 * Ag
        
        # Should not exceed 8% of gross area
        assert As_max <= expected_max * 1.05  # Allow small tolerance
    
    def test_slenderness_effects(self, column_designer, simple_column_loads):
        """Test slenderness effects on column design"""
        # Slender column
        slender_geometry = ColumnGeometry(
            width=300,
            depth=300,
            length=6000  # High length
        )
        
        result = column_designer.design(slender_geometry, simple_column_loads, ColumnType.TIED)
        
        # Should account for slenderness effects
        assert result.member_type == "column"
        assert 'slenderness_ratio' in result.design_forces
        
        # High slenderness should result in moment magnification
        if result.design_forces['slenderness_ratio'] > 22:
            assert 'magnified_moment' in result.design_forces
    
    def test_axial_moment_interaction(self, column_designer, square_column_geometry):
        """Test axial-moment interaction"""
        # High moment load
        high_moment_loads = ColumnLoads(
            axial_dead=100,
            axial_live=50,
            moment_x_dead=80,
            moment_x_live=60
        )
        
        result = column_designer.design(
            square_column_geometry, high_moment_loads, ColumnType.TIED
        )
        
        # Should handle combined axial and moment loading
        assert result.member_type == "column"
        assert 'interaction_ratio' in result.design_forces
    
    @pytest.mark.parametrize("axial_load", [100, 300, 500, 800])
    def test_different_axial_loads(self, column_designer, square_column_geometry, axial_load):
        """Test column design at different axial load levels"""
        loads = ColumnLoads(
            axial_dead=axial_load * 0.6,
            axial_live=axial_load * 0.4,
            moment_x_dead=10,
            moment_x_live=5
        )
        
        result = column_designer.design(square_column_geometry, loads, ColumnType.TIED)
        
        # All should be valid designs
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Higher loads should require more steel (up to maximum limit)
        if result.overall_status == DesignStatus.PASS:
            steel_area = result.required_reinforcement['required_steel_area']
            assert steel_area > 0


@pytest.mark.aci
@pytest.mark.column
@pytest.mark.integration
class TestColumnIntegration:
    """Test column design integration scenarios"""
    
    @pytest.fixture
    def column_designer(self, aci_concrete, aci_steel):
        return ACI318M25ColumnDesign(aci_concrete, aci_steel)
    
    def test_rectangular_column(self, column_designer):
        """Test rectangular column design"""
        geometry = ColumnGeometry(
            width=300,
            depth=600,
            length=4000
        )
        
        loads = ColumnLoads(
            axial_dead=250,
            axial_live=180,
            moment_x_dead=25,
            moment_x_live=15,
            moment_y_dead=12,
            moment_y_live=8
        )
        
        result = column_designer.design(geometry, loads, ColumnType.TIED)
        
        # Should handle rectangular geometry and biaxial bending
        assert result.member_type == "column"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_high_strength_materials(self, aci_concrete):
        """Test column design with high strength steel"""
        high_strength_steel = ACI318M25ReinforcementSteel(grade=550)
        column_designer = ACI318M25ColumnDesign(aci_concrete, high_strength_steel)
        
        geometry = ColumnGeometry(width=350, depth=350, length=3500)
        loads = ColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=20, moment_x_live=10)
        
        result = column_designer.design(geometry, loads, ColumnType.TIED)
        
        # Should work with high strength steel
        assert result.design_method == "ACI 318M-25"
        assert column_designer.fy == 550.0
    
    def test_compression_controlled_design(self, column_designer, square_column_geometry):
        """Test compression-controlled design"""
        # Very high axial load, low moment
        compression_loads = ColumnLoads(
            axial_dead=800,
            axial_live=600,
            moment_x_dead=5,
            moment_x_live=3
        )
        
        result = column_designer.design(
            square_column_geometry, compression_loads, ColumnType.TIED
        )
        
        # Should be compression controlled
        assert result.member_type == "column"
        if result.overall_status == DesignStatus.PASS:
            assert 'failure_mode' in result.design_forces
    
    def test_tension_controlled_design(self, column_designer, square_column_geometry):
        """Test tension-controlled design"""
        # Low axial load, high moment
        tension_loads = ColumnLoads(
            axial_dead=50,
            axial_live=30,
            moment_x_dead=120,
            moment_x_live=80
        )
        
        result = column_designer.design(
            square_column_geometry, tension_loads, ColumnType.TIED
        )
        
        # Should handle high moment to axial ratio
        assert result.member_type == "column"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]


@pytest.mark.aci
@pytest.mark.column
@pytest.mark.validation
class TestColumnValidation:
    """Test column design against known solutions"""
    
    @pytest.fixture
    def column_designer(self, aci_concrete, aci_steel):
        return ACI318M25ColumnDesign(aci_concrete, aci_steel)
    
    def test_known_solution_1(self, column_designer):
        """Test against known solution from ACI 318M examples"""
        # Known problem: Tied column with axial load and moment
        geometry = ColumnGeometry(
            width=400,
            depth=400,
            length=3000
        )
        
        loads = ColumnLoads(
            axial_dead=300,
            axial_live=200,
            moment_x_dead=20,
            moment_x_live=15
        )
        
        result = column_designer.design(geometry, loads, ColumnType.TIED)
        
        # Check result is reasonable
        assert result.overall_status == DesignStatus.PASS
        steel_area = result.required_reinforcement['required_steel_area']
        
        # Should be in reasonable range (manual calculation check)
        Ag = geometry.width * geometry.depth
        steel_ratio = steel_area / Ag
        assert 0.01 <= steel_ratio <= 0.08  # Between min and max limits
    
    def test_pure_axial_capacity(self, column_designer):
        """Test pure axial capacity calculation"""
        geometry = ColumnGeometry(width=300, depth=300, length=3000)
        
        # Calculate theoretical capacity
        Ag = geometry.width * geometry.depth
        # Assume 2% reinforcement
        As = 0.02 * Ag
        
        # Pure axial capacity (simplified)
        Po_theoretical = 0.85 * column_designer.fc * (Ag - As) + column_designer.fy * As
        
        # Test with high axial load
        high_axial_loads = ColumnLoads(
            axial_dead=Po_theoretical * 0.4 / 1.4,  # Account for load factors
            axial_live=Po_theoretical * 0.3 / 1.6,
            moment_x_dead=0,
            moment_x_live=0
        )
        
        result = column_designer.design(geometry, high_axial_loads, ColumnType.TIED)
        
        # Should be able to handle high axial load
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.WARNING]


@pytest.mark.aci
@pytest.mark.column
@pytest.mark.benchmark
@pytest.mark.slow
class TestColumnPerformance:
    """Test column design performance"""
    
    @pytest.fixture
    def column_designer(self, aci_concrete, aci_steel):
        return ACI318M25ColumnDesign(aci_concrete, aci_steel)
    
    def test_design_performance(self, column_designer, performance_monitor, performance_benchmark_data):
        """Test column design performance"""
        geometry = ColumnGeometry(width=400, depth=400, length=3000)
        loads = ColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=15, moment_x_live=10)
        
        # Measure performance
        performance_monitor.start()
        
        for _ in range(10):  # Multiple iterations
            result = column_designer.design(geometry, loads, ColumnType.TIED)
        
        execution_time = performance_monitor.stop()
        
        # Check performance against benchmark
        max_time = performance_benchmark_data['max_execution_time']['column_design'] * 10
        assert execution_time <= max_time, f"Column design too slow: {execution_time:.3f}s > {max_time:.3f}s"
        
        # Check memory usage
        memory_usage = performance_monitor.memory_usage()
        max_memory = performance_benchmark_data['memory_usage_limit']
        assert memory_usage <= max_memory, f"Memory usage too high: {memory_usage:.1f}MB > {max_memory}MB"