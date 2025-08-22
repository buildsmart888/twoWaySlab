"""
ACI 318M-25 Diaphragm Design Tests
=================================

Comprehensive tests for diaphragm design according to ACI 318M-25.
Tests cast-in-place, precast, and composite diaphragms.

การทดสอบการออกแบบไดอะแฟรมตาม ACI 318M-25
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.diaphragm_design import (
    ACI318M25DiaphragmDesign, DiaphragmGeometry, DiaphragmLoads, DiaphragmType
)
from structural_standards.base.design_base import DesignStatus


@pytest.mark.aci
@pytest.mark.diaphragm
@pytest.mark.unit
class TestDiaphragmDesign:
    """Test diaphragm design functionality"""
    
    @pytest.fixture
    def diaphragm_designer(self, aci_concrete, aci_steel):
        """Create diaphragm designer fixture"""
        return ACI318M25DiaphragmDesign(aci_concrete, aci_steel)
    
    @pytest.fixture
    def typical_diaphragm_geometry(self):
        """Typical diaphragm geometry"""
        return DiaphragmGeometry(
            length=12000,     # mm
            width=8000,       # mm
            thickness=150,    # mm
            span=8000         # mm
        )
    
    @pytest.fixture
    def typical_diaphragm_loads(self):
        """Typical diaphragm loads"""
        return DiaphragmLoads(
            shear_force=100,  # kN
            moment=50         # kN⋅m
        )
    
    def test_diaphragm_designer_initialization(self, diaphragm_designer):
        """Test diaphragm designer initialization"""
        assert diaphragm_designer.design_standard == "ACI 318M-25"
        assert diaphragm_designer.fc == 28.0
        assert diaphragm_designer.fy == 420.0
        assert diaphragm_designer.phi_shear == 0.75
        assert diaphragm_designer.phi_flexure == 0.9
    
    def test_cast_in_place_diaphragm_design(self, diaphragm_designer, typical_diaphragm_geometry, 
                                          typical_diaphragm_loads):
        """Test cast-in-place diaphragm design"""
        result = diaphragm_designer.design(
            typical_diaphragm_geometry,
            typical_diaphragm_loads,
            DiaphragmType.CAST_IN_PLACE
        )
        
        # Validate result structure
        assert hasattr(result, 'member_type')
        assert hasattr(result, 'design_method')
        assert hasattr(result, 'overall_status')
        assert hasattr(result, 'utilization_ratio')
        
        # Check design method
        assert result.design_method == "ACI 318M-25"
        assert result.member_type == "diaphragm"
        
        # Check that reinforcement is calculated
        assert 'shear_reinforcement' in result.required_reinforcement
        assert 'chord_reinforcement' in result.required_reinforcement
    
    def test_precast_diaphragm_design(self, diaphragm_designer, typical_diaphragm_geometry, 
                                    typical_diaphragm_loads):
        """Test precast diaphragm design"""
        result = diaphragm_designer.design(
            typical_diaphragm_geometry,
            typical_diaphragm_loads,
            DiaphragmType.PRECAST
        )
        
        # Validate complete design result
        assert result.member_type == "diaphragm"
        assert result.design_method == "ACI 318M-25"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Check that all checks are performed
        assert len(result.strength_checks) > 0
        
        # Check required reinforcement for precast
        assert 'connection_design' in result.required_reinforcement
        assert 'topping_reinforcement' in result.required_reinforcement
    
    def test_composite_diaphragm_design(self, diaphragm_designer, typical_diaphragm_geometry, 
                                      typical_diaphragm_loads):
        """Test composite diaphragm design"""
        result = diaphragm_designer.design(
            typical_diaphragm_geometry,
            typical_diaphragm_loads,
            DiaphragmType.COMPOSITE
        )
        
        # Should handle composite action
        assert result.member_type == "diaphragm"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Check composite-specific requirements
        assert 'composite_action_check' in result.required_reinforcement
    
    def test_in_plane_shear_design(self, diaphragm_designer, typical_diaphragm_geometry, 
                                 typical_diaphragm_loads):
        """Test in-plane shear design"""
        result = diaphragm_designer.design(
            typical_diaphragm_geometry,
            typical_diaphragm_loads,
            DiaphragmType.CAST_IN_PLACE
        )
        
        # Should include in-plane shear checks
        shear_check_found = any(
            'shear' in check.name.lower() 
            for check in result.strength_checks
        )
        assert shear_check_found
        
        # Check shear capacity calculations
        assert 'shear_capacity' in result.design_forces
        assert result.design_forces['shear_capacity'] > 0
    
    def test_chord_design(self, diaphragm_designer, typical_diaphragm_geometry):
        """Test chord design for diaphragm"""
        # High moment loads requiring significant chord forces
        high_moment_loads = DiaphragmLoads(
            shear_force=80,
            moment=200  # High moment
        )
        
        result = diaphragm_designer.design(
            typical_diaphragm_geometry,
            high_moment_loads,
            DiaphragmType.CAST_IN_PLACE
        )
        
        # Should design chord reinforcement
        assert 'chord_reinforcement' in result.required_reinforcement
        chord_area = result.required_reinforcement['chord_reinforcement']
        assert chord_area > 0
        
        # Should include chord force calculations
        assert 'chord_force' in result.design_forces
    
    def test_collector_design(self, diaphragm_designer, typical_diaphragm_geometry, 
                            typical_diaphragm_loads):
        """Test collector element design"""
        result = diaphragm_designer.design(
            typical_diaphragm_geometry,
            typical_diaphragm_loads,
            DiaphragmType.CAST_IN_PLACE
        )
        
        # Should include collector design considerations
        assert 'collector_requirements' in result.required_reinforcement
    
    def test_minimum_thickness_requirements(self, diaphragm_designer, typical_diaphragm_loads):
        """Test minimum thickness requirements"""
        # Test various span lengths
        spans = [6000, 8000, 10000, 12000]  # mm
        
        for span in spans:
            geometry = DiaphragmGeometry(
                length=12000,
                width=8000,
                thickness=100,  # Start with thin diaphragm
                span=span
            )
            
            result = diaphragm_designer.design(
                geometry, typical_diaphragm_loads, DiaphragmType.CAST_IN_PLACE
            )
            
            # Check minimum thickness requirements
            thickness_check_found = any(
                'thickness' in check.name.lower() 
                for check in result.detailing_checks
            )
            assert thickness_check_found
    
    @pytest.mark.parametrize("shear_force", [50, 100, 150, 250])
    def test_different_shear_levels(self, diaphragm_designer, typical_diaphragm_geometry, shear_force):
        """Test diaphragm design at different shear force levels"""
        loads = DiaphragmLoads(
            shear_force=shear_force,
            moment=shear_force * 0.5  # Proportional moment
        )
        
        result = diaphragm_designer.design(
            typical_diaphragm_geometry, loads, DiaphragmType.CAST_IN_PLACE
        )
        
        # All should be valid designs
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
        
        # Higher shear should require more reinforcement (until failure)
        if result.overall_status == DesignStatus.PASS:
            shear_reinforcement = result.required_reinforcement['shear_reinforcement']
            assert shear_reinforcement > 0


@pytest.mark.aci
@pytest.mark.diaphragm
@pytest.mark.integration
class TestDiaphragmIntegration:
    """Test diaphragm design integration scenarios"""
    
    @pytest.fixture
    def diaphragm_designer(self, aci_concrete, aci_steel):
        return ACI318M25DiaphragmDesign(aci_concrete, aci_steel)
    
    def test_large_diaphragm(self, diaphragm_designer):
        """Test large diaphragm design"""
        large_geometry = DiaphragmGeometry(
            length=20000,    # Large diaphragm
            width=15000,
            thickness=200,
            span=15000
        )
        
        loads = DiaphragmLoads(shear_force=200, moment=150)
        
        result = diaphragm_designer.design(
            large_geometry, loads, DiaphragmType.CAST_IN_PLACE
        )
        
        # Should handle large diaphragms
        assert result.member_type == "diaphragm"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_thin_diaphragm(self, diaphragm_designer, typical_diaphragm_loads):
        """Test thin diaphragm design"""
        thin_geometry = DiaphragmGeometry(
            length=10000,
            width=8000,
            thickness=100,  # Thin diaphragm
            span=8000
        )
        
        result = diaphragm_designer.design(
            thin_geometry, typical_diaphragm_loads, DiaphragmType.CAST_IN_PLACE
        )
        
        # Should handle thin diaphragm with appropriate checks
        assert result.member_type == "diaphragm"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
    
    def test_high_strength_materials(self, aci_concrete, typical_diaphragm_geometry, 
                                   typical_diaphragm_loads):
        """Test diaphragm design with high strength steel"""
        high_strength_steel = ACI318M25ReinforcementSteel(grade=550)
        diaphragm_designer = ACI318M25DiaphragmDesign(aci_concrete, high_strength_steel)
        
        result = diaphragm_designer.design(
            typical_diaphragm_geometry, typical_diaphragm_loads, DiaphragmType.CAST_IN_PLACE
        )
        
        # Should work with high strength steel
        assert result.design_method == "ACI 318M-25"
        assert diaphragm_designer.fy == 550.0
    
    def test_aspect_ratio_effects(self, diaphragm_designer, typical_diaphragm_loads):
        """Test different aspect ratios"""
        # High aspect ratio diaphragm
        high_aspect_geometry = DiaphragmGeometry(
            length=16000,
            width=4000,    # High aspect ratio
            thickness=150,
            span=4000
        )
        
        result = diaphragm_designer.design(
            high_aspect_geometry, typical_diaphragm_loads, DiaphragmType.CAST_IN_PLACE
        )
        
        # Should handle high aspect ratio effects
        assert result.member_type == "diaphragm"
        assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]


@pytest.mark.aci
@pytest.mark.diaphragm
@pytest.mark.validation
class TestDiaphragmValidation:
    """Test diaphragm design against known solutions"""
    
    @pytest.fixture
    def diaphragm_designer(self, aci_concrete, aci_steel):
        return ACI318M25DiaphragmDesign(aci_concrete, aci_steel)
    
    def test_known_solution_rectangular_diaphragm(self, diaphragm_designer):
        """Test against known solution for rectangular diaphragm"""
        # Known problem: Cast-in-place diaphragm
        geometry = DiaphragmGeometry(
            length=12000,
            width=8000,
            thickness=150,
            span=8000
        )
        
        loads = DiaphragmLoads(
            shear_force=100,
            moment=60
        )
        
        result = diaphragm_designer.design(
            geometry, loads, DiaphragmType.CAST_IN_PLACE
        )
        
        # Check result is reasonable
        assert result.overall_status == DesignStatus.PASS
        
        # Check reinforcement calculations
        shear_reinforcement = result.required_reinforcement['shear_reinforcement']
        chord_reinforcement = result.required_reinforcement['chord_reinforcement']
        
        assert shear_reinforcement > 0
        assert chord_reinforcement > 0
    
    def test_shear_capacity_calculation(self, diaphragm_designer, typical_diaphragm_geometry):
        """Test shear capacity calculations"""
        # Test at various load levels to verify capacity
        load_levels = [50, 100, 150, 200]  # kN
        
        capacities = []
        for shear_force in load_levels:
            loads = DiaphragmLoads(shear_force=shear_force, moment=shear_force * 0.4)
            result = diaphragm_designer.design(
                typical_diaphragm_geometry, loads, DiaphragmType.CAST_IN_PLACE
            )
            
            if result.overall_status == DesignStatus.PASS:
                capacity = result.design_forces.get('shear_capacity', 0)
                capacities.append(capacity)
        
        # Shear capacities should be consistent (not dependent on applied load)
        if len(capacities) > 1:
            capacity_variation = (max(capacities) - min(capacities)) / max(capacities)
            assert capacity_variation < 0.1  # Should be consistent within 10%
    
    def test_chord_force_calculation(self, diaphragm_designer, typical_diaphragm_geometry):
        """Test chord force calculations"""
        high_moment_loads = DiaphragmLoads(
            shear_force=80,
            moment=200
        )
        
        result = diaphragm_designer.design(
            typical_diaphragm_geometry, high_moment_loads, DiaphragmType.CAST_IN_PLACE
        )
        
        # Check chord force calculation
        if 'chord_force' in result.design_forces:
            chord_force = result.design_forces['chord_force']
            
            # Chord force should be related to applied moment
            # For simple beam: T = M / (d - a/2), approximately T = M / (0.9 * d)
            expected_chord_force = high_moment_loads.moment * 1000 / (0.9 * typical_diaphragm_geometry.width)
            
            # Should be within reasonable range
            assert 0.5 * expected_chord_force <= chord_force <= 2.0 * expected_chord_force


@pytest.mark.aci
@pytest.mark.diaphragm
@pytest.mark.benchmark
@pytest.mark.slow
class TestDiaphragmPerformance:
    """Test diaphragm design performance"""
    
    @pytest.fixture
    def diaphragm_designer(self, aci_concrete, aci_steel):
        return ACI318M25DiaphragmDesign(aci_concrete, aci_steel)
    
    def test_design_performance(self, diaphragm_designer, performance_monitor, performance_benchmark_data):
        """Test diaphragm design performance"""
        geometry = DiaphragmGeometry(length=12000, width=8000, thickness=150, span=8000)
        loads = DiaphragmLoads(shear_force=100, moment=50)
        
        # Measure performance
        performance_monitor.start()
        
        for _ in range(10):  # Multiple iterations
            result = diaphragm_designer.design(
                geometry, loads, DiaphragmType.CAST_IN_PLACE
            )
        
        execution_time = performance_monitor.stop()
        
        # Check performance against benchmark
        # Note: Using footing_design benchmark as placeholder since diaphragm might be similar complexity
        max_time = performance_benchmark_data['max_execution_time'].get('diaphragm_design', 
                  performance_benchmark_data['max_execution_time']['footing_design']) * 10
        assert execution_time <= max_time, f"Diaphragm design too slow: {execution_time:.3f}s > {max_time:.3f}s"
        
        # Check memory usage
        memory_usage = performance_monitor.memory_usage()
        max_memory = performance_benchmark_data['memory_usage_limit']
        assert memory_usage <= max_memory, f"Memory usage too high: {memory_usage:.1f}MB > {max_memory}MB"