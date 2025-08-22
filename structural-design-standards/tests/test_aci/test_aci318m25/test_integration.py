"""
ACI 318M-25 Integration Tests
============================

Comprehensive integration tests for all ACI 318M-25 structural members.
Tests that all member types work together correctly.

การทดสอบบูรณาการครบถ้วนของการออกแบบสมาชิกโครงสร้างตาม ACI 318M-25
"""

import pytest
import math
from typing import Dict, Any, List

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel

# Import all member design classes
from structural_standards.aci.aci318m25.members.beam_design import (
    ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
)
from structural_standards.aci.aci318m25.members.column_design import (
    ACI318M25ColumnDesign, ColumnGeometry, ColumnLoads, ColumnType
)
from structural_standards.aci.aci318m25.members.slab_design import (
    ACI318M25SlabDesign, SlabGeometry, SlabLoads, SlabType
)
from structural_standards.aci.aci318m25.members.wall_design import (
    ACI318M25WallDesign, WallGeometry, WallLoads, WallType, WallBoundaryCondition
)
from structural_standards.aci.aci318m25.members.footing_design import (
    ACI318M25FootingDesign, FootingGeometry, ColumnLoads as FootingColumnLoads, 
    SoilProperties, FootingType
)
from structural_standards.aci.aci318m25.members.diaphragm_design import (
    ACI318M25DiaphragmDesign, DiaphragmGeometry, DiaphragmLoads, DiaphragmType
)

from structural_standards.base.design_base import DesignStatus


@pytest.mark.aci
@pytest.mark.integration
@pytest.mark.slow
class TestACI318M25Integration:
    """Comprehensive integration tests for all ACI 318M-25 members"""
    
    @pytest.fixture(scope="class")
    def materials(self):
        """Common materials for all tests"""
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        return {'concrete': concrete, 'steel': steel}
    
    @pytest.fixture(scope="class")
    def all_designers(self, materials):
        """Create all member designers"""
        concrete = materials['concrete']
        steel = materials['steel']
        
        return {
            'beam': ACI318M25BeamDesign(concrete, steel),
            'column': ACI318M25ColumnDesign(concrete, steel),
            'slab': ACI318M25SlabDesign(concrete, steel),
            'wall': ACI318M25WallDesign(concrete, steel),
            'footing': ACI318M25FootingDesign(concrete, steel),
            'diaphragm': ACI318M25DiaphragmDesign(concrete, steel)
        }
    
    def test_all_designers_initialization(self, all_designers):
        """Test that all designers initialize correctly"""
        for member_type, designer in all_designers.items():
            assert designer.design_standard == "ACI 318M-25"
            assert designer.fc == 28.0
            assert designer.fy == 420.0
            print(f"✅ {member_type.capitalize()} designer initialized successfully")
    
    def test_complete_building_frame_design(self, all_designers):
        """Test complete building frame with all member types"""
        print("\n🏗️ Testing Complete Building Frame Design")
        
        results = {}
        
        # 1. Design beam
        beam_geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
        beam_loads = BeamLoads(dead_load=5.0, live_load=8.0)
        beam_result = all_designers['beam'].design(beam_geometry, beam_loads, BeamType.SIMPLY_SUPPORTED)
        results['beam'] = beam_result
        
        # 2. Design column supporting the beam
        column_geometry = ColumnGeometry(width=400, depth=400, length=3000)
        # Column loads from beam reactions
        beam_reaction = (beam_loads.dead_load + beam_loads.live_load) * beam_geometry.span_length / 1000  # kN
        column_loads = ColumnLoads(
            axial_dead=beam_reaction * 0.6,
            axial_live=beam_reaction * 0.4,
            moment_x_dead=15,
            moment_x_live=10
        )
        column_result = all_designers['column'].design(column_geometry, column_loads, ColumnType.TIED)
        results['column'] = column_result
        
        # 3. Design slab supported by beam
        slab_geometry = SlabGeometry(
            length_x=6000, length_y=6000, thickness=200,
            span_x=6000, span_y=6000
        )
        slab_loads = SlabLoads(dead_load=4.0, live_load=2.5)
        slab_result = all_designers['slab'].design(slab_geometry, slab_loads, SlabType.TWO_WAY)
        results['slab'] = slab_result
        
        # 4. Design wall (bearing wall)
        wall_geometry = WallGeometry(length=4000, height=3000, thickness=200)
        wall_loads = WallLoads(axial_dead=50, axial_live=30, wind_pressure=1.0)
        wall_result = all_designers['wall'].design(
            wall_geometry, wall_loads, WallType.BEARING, WallBoundaryCondition.PINNED_TOP_BOTTOM
        )
        results['wall'] = wall_result
        
        # 5. Design footing for column
        footing_loads = FootingColumnLoads(
            axial_dead=column_loads.axial_dead,
            axial_live=column_loads.axial_live,
            moment_x_dead=column_loads.moment_x_dead,
            moment_y_dead=5
        )
        soil_properties = SoilProperties(bearing_capacity=200, unit_weight=18.0)
        footing_result = all_designers['footing'].design(footing_loads, soil_properties, FootingType.ISOLATED)
        results['footing'] = footing_result
        
        # 6. Design diaphragm (floor diaphragm)
        diaphragm_geometry = DiaphragmGeometry(length=12000, width=8000, thickness=200, span=8000)
        diaphragm_loads = DiaphragmLoads(shear_force=100, moment=50)
        diaphragm_result = all_designers['diaphragm'].design(
            diaphragm_geometry, diaphragm_loads, DiaphragmType.CAST_IN_PLACE
        )
        results['diaphragm'] = diaphragm_result
        
        # Verify all designs
        for member_type, result in results.items():
            assert result.member_type == member_type or result.member_type == "footing"  # Special case
            assert result.design_method == "ACI 318M-25"
            assert result.overall_status in [DesignStatus.PASS, DesignStatus.FAIL, DesignStatus.WARNING]
            print(f"✅ {member_type.capitalize()}: {result.overall_status.value}")
        
        # Check that most designs pass (allowing some to fail for edge cases)
        passed_designs = sum(1 for result in results.values() if result.overall_status == DesignStatus.PASS)
        total_designs = len(results)
        success_rate = passed_designs / total_designs
        
        assert success_rate >= 0.8, f"Too many design failures: {passed_designs}/{total_designs} passed"
        print(f"🎉 Building frame design success rate: {success_rate:.1%}")
        
        return results
    
    def test_material_consistency(self, all_designers):
        """Test that all designers use consistent material properties"""
        fc_values = [designer.fc for designer in all_designers.values()]
        fy_values = [designer.fy for designer in all_designers.values()]
        
        # All should have the same material properties
        assert all(fc == 28.0 for fc in fc_values), "Inconsistent concrete strength"
        assert all(fy == 420.0 for fy in fy_values), "Inconsistent steel strength"
        
        print("✅ Material properties consistent across all designers")
    
    def test_load_factor_consistency(self, all_designers):
        """Test that load factors are consistent across member types"""
        # Check that strength reduction factors are consistent where applicable
        flexure_factors = []
        shear_factors = []
        
        for member_type, designer in all_designers.items():
            if hasattr(designer, 'phi_flexure'):
                flexure_factors.append(designer.phi_flexure)
            if hasattr(designer, 'phi_shear'):
                shear_factors.append(designer.phi_shear)
        
        # Should be consistent
        if flexure_factors:
            assert all(abs(phi - 0.9) < 0.01 for phi in flexure_factors), "Inconsistent flexure factors"
        if shear_factors:
            assert all(abs(phi - 0.75) < 0.01 for phi in shear_factors), "Inconsistent shear factors"
        
        print("✅ Load factors consistent across member types")
    
    def test_seismic_design_integration(self, all_designers):
        """Test seismic design considerations across member types"""
        print("\n🌍 Testing Seismic Design Integration")
        
        # Enhanced loads for seismic design
        seismic_results = {}
        
        # Beam with seismic loads
        beam_geometry = BeamGeometry(width=350, height=650, effective_depth=600, span_length=7000)
        beam_loads = BeamLoads(dead_load=6.0, live_load=4.0, seismic_load=3.0)
        beam_result = all_designers['beam'].design(beam_geometry, beam_loads, BeamType.CONTINUOUS)
        seismic_results['beam'] = beam_result
        
        # Column with high ductility requirements
        column_geometry = ColumnGeometry(width=450, depth=450, length=3500)
        column_loads = ColumnLoads(
            axial_dead=300, axial_live=200,
            moment_x_dead=40, moment_x_live=30,
            moment_y_dead=25, moment_y_live=20
        )
        column_result = all_designers['column'].design(column_geometry, column_loads, ColumnType.TIED)
        seismic_results['column'] = column_result
        
        # Shear wall for lateral resistance
        wall_geometry = WallGeometry(length=3000, height=4000, thickness=250)
        wall_loads = WallLoads(
            axial_dead=40, axial_live=25,
            shear_force=250, overturning_moment=800,
            seismic_pressure=2.0
        )
        wall_result = all_designers['wall'].design(
            wall_geometry, wall_loads, WallType.SHEAR, WallBoundaryCondition.FIXED_TOP_BOTTOM
        )
        seismic_results['wall'] = wall_result
        
        # Verify seismic designs
        for member_type, result in seismic_results.items():
            assert result.design_method == "ACI 318M-25"
            print(f"✅ Seismic {member_type}: {result.overall_status.value}")
        
        return seismic_results
    
    def test_high_rise_building_scenario(self, all_designers):
        """Test high-rise building scenario with larger members"""
        print("\n🏢 Testing High-Rise Building Scenario")
        
        high_rise_results = {}
        
        # Large beam for long spans
        large_beam_geometry = BeamGeometry(width=400, height=800, effective_depth=740, span_length=10000)
        large_beam_loads = BeamLoads(dead_load=12.0, live_load=8.0)
        large_beam_result = all_designers['beam'].design(
            large_beam_geometry, large_beam_loads, BeamType.CONTINUOUS
        )
        high_rise_results['beam'] = large_beam_result
        
        # Large column for high loads
        large_column_geometry = ColumnGeometry(width=600, depth=600, length=4000)
        large_column_loads = ColumnLoads(
            axial_dead=800, axial_live=600,
            moment_x_dead=80, moment_x_live=60,
            moment_y_dead=60, moment_y_live=40
        )
        large_column_result = all_designers['column'].design(
            large_column_geometry, large_column_loads, ColumnType.TIED
        )
        high_rise_results['column'] = large_column_result
        
        # Thick slab for heavy loads
        thick_slab_geometry = SlabGeometry(
            length_x=8000, length_y=8000, thickness=250,
            span_x=8000, span_y=8000
        )
        thick_slab_loads = SlabLoads(dead_load=8.0, live_load=5.0)
        thick_slab_result = all_designers['slab'].design(
            thick_slab_geometry, thick_slab_loads, SlabType.TWO_WAY
        )
        high_rise_results['slab'] = thick_slab_result
        
        # Large footing for heavy column
        large_footing_loads = FootingColumnLoads(
            axial_dead=large_column_loads.axial_dead,
            axial_live=large_column_loads.axial_live,
            moment_x_dead=large_column_loads.moment_x_dead,
            moment_y_dead=large_column_loads.moment_y_dead
        )
        good_soil = SoilProperties(bearing_capacity=300, unit_weight=19.0)  # Better soil for high-rise
        large_footing_result = all_designers['footing'].design(
            large_footing_loads, good_soil, FootingType.ISOLATED
        )
        high_rise_results['footing'] = large_footing_result
        
        # Verify high-rise designs
        for member_type, result in high_rise_results.items():
            assert result.design_method == "ACI 318M-25"
            print(f"✅ High-rise {member_type}: {result.overall_status.value}")
        
        return high_rise_results
    
    def test_performance_consistency(self, all_designers, performance_monitor):
        """Test that all member designs have consistent performance"""
        print("\n⚡ Testing Performance Consistency")
        
        performance_results = {}
        
        for member_type, designer in all_designers.items():
            performance_monitor.start()
            
            # Run multiple designs for each member type
            for _ in range(5):
                if member_type == 'beam':
                    geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
                    loads = BeamLoads(dead_load=5.0, live_load=8.0)
                    designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
                    
                elif member_type == 'column':
                    geometry = ColumnGeometry(width=400, depth=400, length=3000)
                    loads = ColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=15, moment_x_live=10)
                    designer.design(geometry, loads, ColumnType.TIED)
                    
                elif member_type == 'slab':
                    geometry = SlabGeometry(length_x=6000, length_y=6000, thickness=200, span_x=6000, span_y=6000)
                    loads = SlabLoads(dead_load=4.0, live_load=2.5)
                    designer.design(geometry, loads, SlabType.TWO_WAY)
                    
                elif member_type == 'wall':
                    geometry = WallGeometry(length=4000, height=3000, thickness=200)
                    loads = WallLoads(axial_dead=50, axial_live=30, wind_pressure=1.0)
                    designer.design(geometry, loads, WallType.BEARING, WallBoundaryCondition.PINNED_TOP_BOTTOM)
                    
                elif member_type == 'footing':
                    loads = FootingColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=10, moment_y_dead=5)
                    soil = SoilProperties(bearing_capacity=200, unit_weight=18.0)
                    designer.design(loads, soil, FootingType.ISOLATED)
                    
                elif member_type == 'diaphragm':
                    geometry = DiaphragmGeometry(length=12000, width=8000, thickness=150, span=8000)
                    loads = DiaphragmLoads(shear_force=100, moment=50)
                    designer.design(geometry, loads, DiaphragmType.CAST_IN_PLACE)
            
            execution_time = performance_monitor.stop()
            performance_results[member_type] = execution_time
            print(f"✅ {member_type.capitalize()}: {execution_time:.3f}s for 5 designs")
        
        # Check that no member type is significantly slower than others
        max_time = max(performance_results.values())
        min_time = min(performance_results.values())
        
        if max_time > 0:
            performance_ratio = max_time / min_time
            assert performance_ratio < 10.0, f"Performance inconsistency: ratio {performance_ratio:.1f}"
        
        print(f"✅ Performance consistency verified (ratio: {performance_ratio:.1f})")
        
        return performance_results


@pytest.mark.aci
@pytest.mark.integration
@pytest.mark.validation
class TestACI318M25Validation:
    """Validation tests against known design examples"""
    
    @pytest.fixture(scope="class")
    def materials(self):
        """Standard materials for validation"""
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        return {'concrete': concrete, 'steel': steel}
    
    def test_aci_design_example_integration(self, materials):
        """Test integration using ACI design examples"""
        print("\n📚 Testing ACI Design Example Integration")
        
        concrete = materials['concrete']
        steel = materials['steel']
        
        # Example building frame from ACI 318M examples
        beam_designer = ACI318M25BeamDesign(concrete, steel)
        column_designer = ACI318M25ColumnDesign(concrete, steel)
        footing_designer = ACI318M25FootingDesign(concrete, steel)
        
        # Beam design
        beam_geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=8000)
        beam_loads = BeamLoads(dead_load=6.0, live_load=9.0)
        beam_result = beam_designer.design(beam_geometry, beam_loads, BeamType.SIMPLY_SUPPORTED)
        
        # Column design (supporting beam)
        column_geometry = ColumnGeometry(width=400, depth=400, length=3500)
        beam_reaction = (beam_loads.dead_load + beam_loads.live_load) * beam_geometry.span_length / 1000
        column_loads = ColumnLoads(
            axial_dead=beam_reaction * 0.6 + 100,  # Additional dead load
            axial_live=beam_reaction * 0.4 + 75,   # Additional live load
            moment_x_dead=20,
            moment_x_live=15
        )
        column_result = column_designer.design(column_geometry, column_loads, ColumnType.TIED)
        
        # Footing design (supporting column)
        footing_loads = FootingColumnLoads(
            axial_dead=column_loads.axial_dead,
            axial_live=column_loads.axial_live,
            moment_x_dead=column_loads.moment_x_dead,
            moment_y_dead=10
        )
        soil_properties = SoilProperties(bearing_capacity=250, unit_weight=18.5)
        footing_result = footing_designer.design(footing_loads, soil_properties, FootingType.ISOLATED)
        
        # All designs should pass for this reasonable example
        assert beam_result.overall_status == DesignStatus.PASS, "Beam design should pass"
        assert column_result.overall_status == DesignStatus.PASS, "Column design should pass"
        assert footing_result.overall_status == DesignStatus.PASS, "Footing design should pass"
        
        print("✅ ACI Design Example Integration: All members passed")
        
        # Check force flow consistency
        # (This is a simplified check - in practice, more detailed analysis would be needed)
        beam_steel = beam_result.required_reinforcement.get('required_steel_area', 0)
        column_steel = column_result.required_reinforcement.get('required_steel_area', 0)
        footing_area = footing_result.required_reinforcement.get('geometry', {}).get('area', 0)
        
        assert beam_steel > 0, "Beam should require reinforcement"
        assert column_steel > 0, "Column should require reinforcement"
        assert footing_area > 0, "Footing should have reasonable area"
        
        print(f"✅ Force flow: Beam={beam_steel:.0f}mm², Column={column_steel:.0f}mm², Footing={footing_area/1e6:.1f}m²")


@pytest.mark.aci
@pytest.mark.integration
@pytest.mark.benchmark
@pytest.mark.slow
class TestACI318M25BenchmarkIntegration:
    """Benchmark tests for integrated ACI 318M-25 system"""
    
    def test_complete_system_benchmark(self, performance_monitor, performance_benchmark_data):
        """Benchmark the complete ACI 318M-25 system"""
        print("\n🏎️ Running Complete System Benchmark")
        
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        
        # Create all designers
        designers = {
            'beam': ACI318M25BeamDesign(concrete, steel),
            'column': ACI318M25ColumnDesign(concrete, steel),
            'slab': ACI318M25SlabDesign(concrete, steel),
            'wall': ACI318M25WallDesign(concrete, steel),
            'footing': ACI318M25FootingDesign(concrete, steel),
            'diaphragm': ACI318M25DiaphragmDesign(concrete, steel)
        }
        
        performance_monitor.start()
        
        # Run comprehensive building design multiple times
        for iteration in range(3):
            print(f"  Running iteration {iteration + 1}/3...")
            
            # Design all members
            beam_geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
            beam_loads = BeamLoads(dead_load=5.0, live_load=8.0)
            beam_result = designers['beam'].design(beam_geometry, beam_loads, BeamType.SIMPLY_SUPPORTED)
            
            column_geometry = ColumnGeometry(width=400, depth=400, length=3000)
            column_loads = ColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=15, moment_x_live=10)
            column_result = designers['column'].design(column_geometry, column_loads, ColumnType.TIED)
            
            slab_geometry = SlabGeometry(length_x=6000, length_y=6000, thickness=200, span_x=6000, span_y=6000)
            slab_loads = SlabLoads(dead_load=4.0, live_load=2.5)
            slab_result = designers['slab'].design(slab_geometry, slab_loads, SlabType.TWO_WAY)
            
            wall_geometry = WallGeometry(length=4000, height=3000, thickness=200)
            wall_loads = WallLoads(axial_dead=50, axial_live=30, wind_pressure=1.0)
            wall_result = designers['wall'].design(
                wall_geometry, wall_loads, WallType.BEARING, WallBoundaryCondition.PINNED_TOP_BOTTOM
            )
            
            footing_loads = FootingColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=10, moment_y_dead=5)
            soil_properties = SoilProperties(bearing_capacity=200, unit_weight=18.0)
            footing_result = designers['footing'].design(footing_loads, soil_properties, FootingType.ISOLATED)
            
            diaphragm_geometry = DiaphragmGeometry(length=12000, width=8000, thickness=150, span=8000)
            diaphragm_loads = DiaphragmLoads(shear_force=100, moment=50)
            diaphragm_result = designers['diaphragm'].design(
                diaphragm_geometry, diaphragm_loads, DiaphragmType.CAST_IN_PLACE
            )
        
        total_execution_time = performance_monitor.stop()
        
        # Check performance
        max_total_time = 3.0  # Maximum 3 seconds for complete system (3 iterations)
        assert total_execution_time <= max_total_time, \
            f"Complete system too slow: {total_execution_time:.3f}s > {max_total_time:.3f}s"
        
        # Check memory usage
        memory_usage = performance_monitor.memory_usage()
        max_memory = performance_benchmark_data['memory_usage_limit'] * 2  # Allow more for complete system
        assert memory_usage <= max_memory, \
            f"Memory usage too high: {memory_usage:.1f}MB > {max_memory}MB"
        
        print(f"✅ Complete system benchmark: {total_execution_time:.3f}s, {memory_usage:.1f}MB")
        print(f"✅ Average per iteration: {total_execution_time/3:.3f}s")
        
        return total_execution_time