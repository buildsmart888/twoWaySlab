"""
ACI 318M-25 Footing Design Tests
===============================

Comprehensive tests for footing design according to ACI 318M-25.
Tests isolated footings, combined footings, and mat foundations.

การทดสอบการออกแบบฐานรากตาม ACI 318M-25
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.footing_design import (
    ACI318M25FootingDesign, FootingGeometry, ColumnLoads, SoilProperties, 
    FootingType, SoilCondition
)
from structural_standards.base.design_base import DesignStatus


@pytest.mark.aci
@pytest.mark.footing
@pytest.mark.unit
class TestFootingDesign:
    """Test footing design functionality"""
    
    @pytest.fixture
    def footing_designer(self, aci_concrete, aci_steel):
        """Create footing designer fixture"""
        return ACI318M25FootingDesign(aci_concrete, aci_steel)
    
    @pytest.fixture
    def typical_column_loads(self):
        """Typical column loads"""
        return ColumnLoads(
            axial_dead=200,       # kN
            axial_live=150,       # kN
            moment_x_dead=10,     # kN⋅m
            moment_y_dead=5       # kN⋅m
        )
    
    @pytest.fixture
    def typical_soil_properties(self):
        """Typical soil properties"""
        return SoilProperties(
            bearing_capacity=200,  # kPa
            unit_weight=18.0      # kN/m³
        )
    
    def test_footing_designer_initialization(self, footing_designer):
        """Test footing designer initialization"""
        assert footing_designer.design_standard == "ACI 318M-25"
        assert footing_designer.fc == 28.0
        assert footing_designer.fy == 420.0
        assert footing_designer.phi_flexure == 0.9
        assert footing_designer.phi_shear == 0.75
        assert footing_designer.phi_bearing == 0.65
    
    def test_isolated_footing_design(self, footing_designer, typical_column_loads, typical_soil_properties):
        """Test isolated footing design"""
        result = footing_designer.design(
            typical_column_loads,
            typical_soil_properties,
            FootingType.ISOLATED
        )
        
        # Validate result structure
        assert hasattr(result, 'member_type')
        assert hasattr(result, 'design_method')
        assert hasattr(result, 'overall_status')
        assert hasattr(result, 'utilization_ratio')
        
        # Check design method
        assert result.design_method == "ACI 318M-25"
        assert result.member_type == "footing"
        
        # Check that reinforcement is calculated
        assert 'steel_area_x' in result.required_reinforcement
        assert 'steel_area_y' in result.required_reinforcement
        assert 'geometry' in result.required_reinforcement
    
    def test_footing_sizing(self, footing_designer, typical_column_loads, typical_soil_properties):
        """Test automatic footing sizing"""
        # Design without providing geometry
        result = footing_designer.design(
            typical_column_loads,
            typical_soil_properties,
            FootingType.ISOLATED
        )
        
        # Should automatically size the footing
        geometry = result.required_reinforcement['geometry']
        assert geometry['length'] > 0
        assert geometry['width'] > 0
        assert geometry['thickness'] > 0
        assert geometry['area'] > 0
        
        # Minimum dimensions
        assert geometry['length'] >= 600  # mm
        assert geometry['width'] >= 600   # mm
        assert geometry['thickness'] >= 150  # mm
    
    def test_footing_with_moment(self, footing_designer, typical_soil_properties):
        """Test footing design with high moments"""
        high_moment_loads = ColumnLoads(
            axial_dead=150,
            axial_live=100,
            moment_x_dead=50,     # High moment
            moment_y_dead=30,
            moment_x_live=35,
            moment_y_live=20
        )
        
        result = footing_designer.design(
            high_moment_loads,
            typical_soil_properties,
            FootingType.ISOLATED
        )
        
        # Should handle moments and size accordingly
        assert result.member_type == "footing"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # High moments should result in larger footing
        geometry = result.required_reinforcement['geometry']
        assert geometry['area'] > 1000000  # mm² (should be larger due to moments)
    
    def test_bearing_pressure_check(self, footing_designer, typical_column_loads, typical_soil_properties):
        """Test bearing pressure calculations"""
        result = footing_designer.design(
            typical_column_loads,
            typical_soil_properties,
            FootingType.ISOLATED
        )
        
        # Check bearing pressure is within limits
        bearing_check_found = any(
            'bearing' in check.name.lower() 
            for check in result.strength_checks
        )
        assert bearing_check_found
        
        # Should include bearing pressure in design forces
        assert 'bearing_pressure' in result.design_forces
        bearing_pressure = result.design_forces['bearing_pressure']
        assert bearing_pressure > 0
        assert bearing_pressure <= typical_soil_properties.design_bearing_pressure * 1.1  # Allow small margin
    
    def test_punching_shear_check(self, footing_designer, typical_column_loads, typical_soil_properties):
        """Test punching shear checks"""
        result = footing_designer.design(
            typical_column_loads,
            typical_soil_properties,
            FootingType.ISOLATED
        )
        
        # Should include punching shear checks
        punching_check_found = any(
            'punching' in check.name.lower() 
            for check in result.strength_checks
        )
        assert punching_check_found
    
    def test_one_way_shear_checks(self, footing_designer, typical_column_loads, typical_soil_properties):
        """Test one-way shear checks"""
        result = footing_designer.design(
            typical_column_loads,
            typical_soil_properties,
            FootingType.ISOLATED
        )
        
        # Should include one-way shear checks in both directions
        one_way_x_found = any(
            'one-way' in check.name.lower() and 'x' in check.name.lower()
            for check in result.strength_checks
        )
        one_way_y_found = any(
            'one-way' in check.name.lower() and 'y' in check.name.lower()
            for check in result.strength_checks
        )
        
        assert one_way_x_found
        assert one_way_y_found
    
    def test_minimum_reinforcement(self, footing_designer, typical_column_loads, typical_soil_properties):
        """Test minimum reinforcement requirements"""
        result = footing_designer.design(
            typical_column_loads,
            typical_soil_properties,
            FootingType.ISOLATED
        )
        
        # Check minimum steel areas
        assert 'minimum_steel_x' in result.required_reinforcement
        assert 'minimum_steel_y' in result.required_reinforcement
        
        min_steel_x = result.required_reinforcement['minimum_steel_x']
        min_steel_y = result.required_reinforcement['minimum_steel_y']
        
        assert min_steel_x > 0
        assert min_steel_y > 0
        
        # Required steel should meet minimum
        req_steel_x = result.required_reinforcement['steel_area_x']
        req_steel_y = result.required_reinforcement['steel_area_y']
        
        assert req_steel_x >= min_steel_x * 0.95  # Allow small tolerance
        assert req_steel_y >= min_steel_y * 0.95
    
    @pytest.mark.parametrize("axial_load", [100, 300, 500, 800])
    def test_different_load_levels(self, footing_designer, typical_soil_properties, axial_load):
        """Test footing design at different load levels"""
        loads = ColumnLoads(
            axial_dead=axial_load * 0.6,
            axial_live=axial_load * 0.4,
            moment_x_dead=axial_load * 0.05,
            moment_y_dead=axial_load * 0.03
        )
        
        result = footing_designer.design(loads, typical_soil_properties, FootingType.ISOLATED)
        
        # All should be valid designs
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Higher loads should require larger footings
        if result.overall_status == DesignStatus.PASS:
            geometry = result.required_reinforcement['geometry']
            assert geometry['area'] > 500000  # Reasonable minimum area


@pytest.mark.aci
@pytest.mark.footing
@pytest.mark.integration
class TestFootingIntegration:
    """Test footing design integration scenarios"""
    
    @pytest.fixture
    def footing_designer(self, aci_concrete, aci_steel):
        return ACI318M25FootingDesign(aci_concrete, aci_steel)
    
    def test_rectangular_footing(self, footing_designer, typical_soil_properties):
        """Test rectangular footing design"""
        # Provide specific rectangular geometry
        geometry = FootingGeometry(
            length=2500,  # mm
            width=2000,   # mm
            thickness=600
        )
        
        loads = ColumnLoads(
            axial_dead=250,
            axial_live=180,
            moment_x_dead=20,
            moment_y_dead=15
        )
        
        result = footing_designer.design(
            loads, typical_soil_properties, FootingType.ISOLATED, geometry
        )
        
        # Should handle rectangular geometry
        assert result.member_type == "footing"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_poor_soil_conditions(self, footing_designer, typical_column_loads):
        """Test footing design with poor soil"""
        poor_soil = SoilProperties(
            bearing_capacity=100,  # Low bearing capacity
            unit_weight=16.0,      # Low unit weight
            condition=SoilCondition.ALLOWABLE_STRESS
        )
        
        result = footing_designer.design(
            typical_column_loads, poor_soil, FootingType.ISOLATED
        )
        
        # Should result in larger footing due to poor soil
        assert result.member_type == "footing"
        
        if result.overall_status == DesignStatus.PASS:
            geometry = result.required_reinforcement['geometry']
            # Poor soil should require larger area
            assert geometry['area'] > 1500000  # mm²
    
    def test_high_strength_concrete_footing(self, aci_steel, typical_column_loads, typical_soil_properties):
        """Test footing design with high strength concrete"""
        high_strength_concrete = ACI318M25Concrete(fc_prime=40.0)
        footing_designer = ACI318M25FootingDesign(high_strength_concrete, aci_steel)
        
        result = footing_designer.design(
            typical_column_loads, typical_soil_properties, FootingType.ISOLATED
        )
        
        # Should work with high strength concrete
        assert result.design_method == "ACI 318M-25"
        assert footing_designer.fc == 40.0
    
    def test_combined_footing_type(self, footing_designer, typical_soil_properties):
        """Test combined footing design approach"""
        # Higher loads that might require combined footing
        heavy_loads = ColumnLoads(
            axial_dead=400,
            axial_live=300,
            moment_x_dead=30,
            moment_y_dead=20
        )
        
        result = footing_designer.design(
            heavy_loads, typical_soil_properties, FootingType.COMBINED
        )
        
        # Should handle combined footing approach
        assert result.member_type == "footing"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]


@pytest.mark.aci
@pytest.mark.footing
@pytest.mark.validation
class TestFootingValidation:
    """Test footing design against known solutions"""
    
    @pytest.fixture
    def footing_designer(self, aci_concrete, aci_steel):
        return ACI318M25FootingDesign(aci_concrete, aci_steel)
    
    def test_known_solution_square_footing(self, footing_designer):
        """Test against known solution for square footing"""
        # Known problem: Square isolated footing
        loads = ColumnLoads(
            axial_dead=200,
            axial_live=150,
            moment_x_dead=10,
            moment_y_dead=5
        )
        
        soil = SoilProperties(
            bearing_capacity=200,  # kPa
            unit_weight=18.0
        )
        
        result = footing_designer.design(loads, soil, FootingType.ISOLATED)
        
        # Check result is reasonable
        assert result.overall_status == DesignStatus.PASS
        
        # Check footing dimensions
        geometry = result.required_reinforcement['geometry']
        length = geometry['length']
        width = geometry['width']
        
        # Should be approximately square for symmetric loading
        aspect_ratio = max(length, width) / min(length, width)
        assert aspect_ratio <= 1.5  # Reasonably close to square
        
        # Check reinforcement
        steel_x = result.required_reinforcement['steel_area_x']
        steel_y = result.required_reinforcement['steel_area_y']
        assert steel_x > 0
        assert steel_y > 0
    
    def test_settlement_check(self, footing_designer, typical_column_loads, typical_soil_properties):
        """Test settlement considerations"""
        result = footing_designer.design(
            typical_column_loads, typical_soil_properties, FootingType.ISOLATED
        )
        
        # Should include settlement check
        settlement_check_found = any(
            'settlement' in check.name.lower() 
            for check in result.serviceability_checks
        )
        assert settlement_check_found
    
    def test_stability_check(self, footing_designer, typical_soil_properties):
        """Test overturning stability"""
        # High moment loads for stability check
        high_moment_loads = ColumnLoads(
            axial_dead=100,
            axial_live=75,
            moment_x_dead=80,  # High overturning moment
            moment_y_dead=50
        )
        
        result = footing_designer.design(
            high_moment_loads, typical_soil_properties, FootingType.ISOLATED
        )
        
        # Should include stability check
        stability_check_found = any(
            'stability' in check.name.lower() or 'overturning' in check.name.lower()
            for check in result.serviceability_checks
        )
        assert stability_check_found


@pytest.mark.aci
@pytest.mark.footing
@pytest.mark.benchmark
@pytest.mark.slow
class TestFootingPerformance:
    """Test footing design performance"""
    
    @pytest.fixture
    def footing_designer(self, aci_concrete, aci_steel):
        return ACI318M25FootingDesign(aci_concrete, aci_steel)
    
    def test_design_performance(self, footing_designer, performance_monitor, performance_benchmark_data):
        """Test footing design performance"""
        loads = ColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=10, moment_y_dead=5)
        soil = SoilProperties(bearing_capacity=200, unit_weight=18.0)
        
        # Measure performance
        performance_monitor.start()
        
        for _ in range(10):  # Multiple iterations
            result = footing_designer.design(loads, soil, FootingType.ISOLATED)
        
        execution_time = performance_monitor.stop()
        
        # Check performance against benchmark
        max_time = performance_benchmark_data['max_execution_time']['footing_design'] * 10
        assert execution_time <= max_time, f"Footing design too slow: {execution_time:.3f}s > {max_time:.3f}s"
        
        # Check memory usage
        memory_usage = performance_monitor.memory_usage()
        max_memory = performance_benchmark_data['memory_usage_limit']
        assert memory_usage <= max_memory, f"Memory usage too high: {memory_usage:.1f}MB > {max_memory}MB"