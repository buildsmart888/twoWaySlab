"""
ACI 318M-25 Performance Benchmarks
==================================

Performance benchmarks for ACI 318M-25 structural design modules.
Tests execution time, memory usage, and scalability.

การทดสอบประสิทธิภาพการทำงานของการออกแบบตาม ACI 318M-25
"""

import pytest
import time
import psutil
import os
from typing import Dict, Any, List

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.beam_design import (
    ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
)
from structural_standards.aci.aci318m25.members.column_design import (
    ACI318M25ColumnDesign, ColumnGeometry, ColumnLoads, ColumnType
)
from structural_standards.aci.aci318m25.members.slab_design import (
    ACI318M25SlabDesign, SlabGeometry, SlabLoads, SlabType
)


@pytest.mark.aci
@pytest.mark.benchmark
@pytest.mark.slow
class TestACIPerformanceBenchmarks:
    """Performance benchmarks for ACI 318M-25 design modules"""
    
    @pytest.fixture(scope="class")
    def materials(self):
        """Standard materials for benchmarks"""
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        return {'concrete': concrete, 'steel': steel}
    
    @pytest.fixture(scope="class")
    def performance_tracker(self):
        """Performance tracking utilities"""
        class PerformanceTracker:
            def __init__(self):
                self.process = psutil.Process(os.getpid())
                self.start_time = None
                self.start_memory = None
            
            def start(self):
                self.start_time = time.time()
                self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            def stop(self):
                end_time = time.time()
                end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
                
                execution_time = end_time - self.start_time
                memory_delta = end_memory - self.start_memory
                
                return {
                    'execution_time': execution_time,
                    'memory_usage': end_memory,
                    'memory_delta': memory_delta
                }
        
        return PerformanceTracker()
    
    def test_beam_design_benchmark(self, materials, performance_tracker):
        """Benchmark beam design performance"""
        print("\n🔗 Benchmarking Beam Design Performance")
        
        beam_designer = ACI318M25BeamDesign(materials['concrete'], materials['steel'])
        
        # Test parameters
        test_cases = [
            (300, 600, 6000),   # Small beam
            (400, 800, 8000),   # Medium beam
            (500, 1000, 10000), # Large beam
        ]
        
        benchmark_results = {}
        
        for width, height, span in test_cases:
            geometry = BeamGeometry(
                width=width,
                height=height,
                effective_depth=height - 50,
                span_length=span
            )
            loads = BeamLoads(dead_load=5.0, live_load=8.0)
            
            performance_tracker.start()
            
            # Run multiple designs
            for _ in range(50):  # 50 iterations
                result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
            
            metrics = performance_tracker.stop()
            
            case_name = f"{width}x{height}x{span}"
            benchmark_results[case_name] = {
                'avg_time_per_design': metrics['execution_time'] / 50,
                'total_time': metrics['execution_time'],
                'memory_usage': metrics['memory_usage'],
                'designs_per_second': 50 / metrics['execution_time']
            }
            
            print(f"  {case_name}: {metrics['execution_time']:.3f}s total, "
                  f"{benchmark_results[case_name]['avg_time_per_design']*1000:.1f}ms avg")
        
        # Performance targets
        for case_name, metrics in benchmark_results.items():
            assert metrics['avg_time_per_design'] < 0.1, \
                f"Beam design too slow: {case_name} = {metrics['avg_time_per_design']:.3f}s"
            assert metrics['designs_per_second'] > 10, \
                f"Beam design throughput too low: {case_name} = {metrics['designs_per_second']:.1f} designs/s"
        
        return benchmark_results
    
    def test_column_design_benchmark(self, materials, performance_tracker):
        """Benchmark column design performance"""
        print("\n🏛️ Benchmarking Column Design Performance")
        
        column_designer = ACI318M25ColumnDesign(materials['concrete'], materials['steel'])
        
        # Test load levels
        load_levels = [
            (200, 150),    # Light loads
            (500, 400),    # Medium loads
            (1000, 800),   # Heavy loads
        ]
        
        benchmark_results = {}
        
        for axial_dead, axial_live in load_levels:
            geometry = ColumnGeometry(width=400, depth=400, length=3000)
            loads = ColumnLoads(
                axial_dead=axial_dead,
                axial_live=axial_live,
                moment_x_dead=axial_dead * 0.1,
                moment_x_live=axial_live * 0.1
            )
            
            performance_tracker.start()
            
            # Run multiple designs
            for _ in range(30):  # 30 iterations
                result = column_designer.design(geometry, loads, ColumnType.TIED)
            
            metrics = performance_tracker.stop()
            
            case_name = f"DL{axial_dead}_LL{axial_live}"
            benchmark_results[case_name] = {
                'avg_time_per_design': metrics['execution_time'] / 30,
                'total_time': metrics['execution_time'],
                'memory_usage': metrics['memory_usage'],
                'designs_per_second': 30 / metrics['execution_time']
            }
            
            print(f"  {case_name}: {metrics['execution_time']:.3f}s total, "
                  f"{benchmark_results[case_name]['avg_time_per_design']*1000:.1f}ms avg")
        
        # Performance targets
        for case_name, metrics in benchmark_results.items():
            assert metrics['avg_time_per_design'] < 0.15, \
                f"Column design too slow: {case_name} = {metrics['avg_time_per_design']:.3f}s"
        
        return benchmark_results
    
    def test_slab_design_benchmark(self, materials, performance_tracker):
        """Benchmark slab design performance"""
        print("\n🏢 Benchmarking Slab Design Performance")
        
        slab_designer = ACI318M25SlabDesign(materials['concrete'], materials['steel'])
        
        # Test slab sizes
        slab_sizes = [
            (4000, 4000, 150),   # Small slab
            (6000, 6000, 200),   # Medium slab
            (8000, 8000, 250),   # Large slab
        ]
        
        benchmark_results = {}
        
        for length, width, thickness in slab_sizes:
            geometry = SlabGeometry(
                length_x=length,
                length_y=width,
                thickness=thickness,
                span_x=length,
                span_y=width
            )
            loads = SlabLoads(dead_load=4.0, live_load=2.5)
            
            performance_tracker.start()
            
            # Run multiple designs
            for _ in range(20):  # 20 iterations
                result = slab_designer.design(geometry, loads, SlabType.TWO_WAY)
            
            metrics = performance_tracker.stop()
            
            case_name = f"{length}x{width}x{thickness}"
            benchmark_results[case_name] = {
                'avg_time_per_design': metrics['execution_time'] / 20,
                'total_time': metrics['execution_time'],
                'memory_usage': metrics['memory_usage'],
                'designs_per_second': 20 / metrics['execution_time']
            }
            
            print(f"  {case_name}: {metrics['execution_time']:.3f}s total, "
                  f"{benchmark_results[case_name]['avg_time_per_design']*1000:.1f}ms avg")
        
        # Performance targets
        for case_name, metrics in benchmark_results.items():
            assert metrics['avg_time_per_design'] < 0.2, \
                f"Slab design too slow: {case_name} = {metrics['avg_time_per_design']:.3f}s"
        
        return benchmark_results
    
    def test_scalability_benchmark(self, materials, performance_tracker):
        """Test scalability with increasing problem complexity"""
        print("\n📈 Benchmarking Scalability")
        
        beam_designer = ACI318M25BeamDesign(materials['concrete'], materials['steel'])
        
        # Increasing complexity
        complexity_levels = [10, 50, 100, 200]
        
        scalability_results = {}
        
        for num_designs in complexity_levels:
            geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
            loads = BeamLoads(dead_load=5.0, live_load=8.0)
            
            performance_tracker.start()
            
            # Run increasing number of designs
            for i in range(num_designs):
                # Vary loads slightly to prevent caching effects
                varied_loads = BeamLoads(
                    dead_load=5.0 + i * 0.01,
                    live_load=8.0 + i * 0.01
                )
                result = beam_designer.design(geometry, varied_loads, BeamType.SIMPLY_SUPPORTED)
            
            metrics = performance_tracker.stop()
            
            scalability_results[num_designs] = {
                'total_time': metrics['execution_time'],
                'avg_time_per_design': metrics['execution_time'] / num_designs,
                'memory_usage': metrics['memory_usage'],
                'throughput': num_designs / metrics['execution_time']
            }
            
            print(f"  {num_designs} designs: {metrics['execution_time']:.3f}s total, "
                  f"{scalability_results[num_designs]['throughput']:.1f} designs/s")
        
        # Check that performance scales reasonably (shouldn't degrade significantly)
        times = [result['avg_time_per_design'] for result in scalability_results.values()]
        max_time = max(times)
        min_time = min(times)
        
        performance_degradation = (max_time - min_time) / min_time
        assert performance_degradation < 0.5, \
            f"Performance degradation too high: {performance_degradation:.2f}"
        
        print(f"  ✅ Performance degradation: {performance_degradation:.2%}")
        
        return scalability_results
    
    def test_memory_usage_benchmark(self, materials, performance_tracker):
        """Test memory usage patterns"""
        print("\n💾 Benchmarking Memory Usage")
        
        beam_designer = ACI318M25BeamDesign(materials['concrete'], materials['steel'])
        column_designer = ACI318M25ColumnDesign(materials['concrete'], materials['steel'])
        slab_designer = ACI318M25SlabDesign(materials['concrete'], materials['steel'])
        
        memory_results = {}
        
        # Test each designer type
        designers = [
            ('beam', beam_designer),
            ('column', column_designer),
            ('slab', slab_designer)
        ]
        
        for designer_name, designer in designers:
            performance_tracker.start()
            
            # Run designs and monitor memory
            for i in range(100):
                if designer_name == 'beam':
                    geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
                    loads = BeamLoads(dead_load=5.0, live_load=8.0)
                    result = designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
                    
                elif designer_name == 'column':
                    geometry = ColumnGeometry(width=400, depth=400, length=3000)
                    loads = ColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=15, moment_x_live=10)
                    result = designer.design(geometry, loads, ColumnType.TIED)
                    
                elif designer_name == 'slab':
                    geometry = SlabGeometry(length_x=6000, length_y=6000, thickness=200, span_x=6000, span_y=6000)
                    loads = SlabLoads(dead_load=4.0, live_load=2.5)
                    result = designer.design(geometry, loads, SlabType.TWO_WAY)
            
            metrics = performance_tracker.stop()
            
            memory_results[designer_name] = {
                'final_memory': metrics['memory_usage'],
                'memory_delta': metrics['memory_delta'],
                'memory_per_design': metrics['memory_delta'] / 100 if metrics['memory_delta'] > 0 else 0
            }
            
            print(f"  {designer_name}: {metrics['memory_usage']:.1f}MB final, "
                  f"Δ{metrics['memory_delta']:.1f}MB")
        
        # Memory usage should be reasonable
        for designer_name, metrics in memory_results.items():
            assert metrics['final_memory'] < 200, \
                f"Memory usage too high for {designer_name}: {metrics['final_memory']:.1f}MB"
            
            # Memory delta should be small (no major leaks)
            if metrics['memory_delta'] > 0:
                assert metrics['memory_delta'] < 50, \
                    f"Memory delta too high for {designer_name}: {metrics['memory_delta']:.1f}MB"
        
        return memory_results
    
    def test_concurrent_performance(self, materials, performance_tracker):
        """Test performance under concurrent operations (simulated)"""
        print("\n⚡ Benchmarking Concurrent Performance")
        
        # Simulate concurrent operations by rapid sequential execution
        designers = [
            ACI318M25BeamDesign(materials['concrete'], materials['steel']),
            ACI318M25ColumnDesign(materials['concrete'], materials['steel']),
            ACI318M25SlabDesign(materials['concrete'], materials['steel'])
        ]
        
        performance_tracker.start()
        
        # Rapid interleaved operations
        for i in range(30):  # 30 iterations of each
            # Beam design
            beam_geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
            beam_loads = BeamLoads(dead_load=5.0, live_load=8.0)
            beam_result = designers[0].design(beam_geometry, beam_loads, BeamType.SIMPLY_SUPPORTED)
            
            # Column design
            column_geometry = ColumnGeometry(width=400, depth=400, length=3000)
            column_loads = ColumnLoads(axial_dead=200, axial_live=150, moment_x_dead=15, moment_x_live=10)
            column_result = designers[1].design(column_geometry, column_loads, ColumnType.TIED)
            
            # Slab design
            slab_geometry = SlabGeometry(length_x=6000, length_y=6000, thickness=200, span_x=6000, span_y=6000)
            slab_loads = SlabLoads(dead_load=4.0, live_load=2.5)
            slab_result = designers[2].design(slab_geometry, slab_loads, SlabType.TWO_WAY)
        
        metrics = performance_tracker.stop()
        
        total_designs = 90  # 30 of each type
        concurrent_results = {
            'total_time': metrics['execution_time'],
            'total_designs': total_designs,
            'avg_time_per_design': metrics['execution_time'] / total_designs,
            'overall_throughput': total_designs / metrics['execution_time'],
            'memory_usage': metrics['memory_usage']
        }
        
        print(f"  {total_designs} total designs: {metrics['execution_time']:.3f}s")
        print(f"  Overall throughput: {concurrent_results['overall_throughput']:.1f} designs/s")
        print(f"  Average per design: {concurrent_results['avg_time_per_design']*1000:.1f}ms")
        
        # Performance targets for concurrent operations
        assert concurrent_results['avg_time_per_design'] < 0.2, \
            f"Concurrent performance too slow: {concurrent_results['avg_time_per_design']:.3f}s"
        assert concurrent_results['overall_throughput'] > 5, \
            f"Concurrent throughput too low: {concurrent_results['overall_throughput']:.1f} designs/s"
        
        return concurrent_results


@pytest.mark.aci
@pytest.mark.benchmark
@pytest.mark.slow
class TestACIComparisonBenchmarks:
    """Comparison benchmarks between different approaches"""
    
    @pytest.fixture(scope="class")
    def materials(self):
        """Standard materials"""
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        return {'concrete': concrete, 'steel': steel}
    
    def test_material_strength_performance(self, materials):
        """Test performance across different material strengths"""
        print("\n🧪 Benchmarking Material Strength Performance")
        
        # Different concrete strengths
        concrete_strengths = [21, 28, 35, 42]  # MPa
        
        benchmark_results = {}
        
        for fc in concrete_strengths:
            concrete = ACI318M25Concrete(fc_prime=fc)
            beam_designer = ACI318M25BeamDesign(concrete, materials['steel'])
            
            geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
            loads = BeamLoads(dead_load=5.0, live_load=8.0)
            
            start_time = time.time()
            
            # Run designs
            for _ in range(20):
                result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
            
            execution_time = time.time() - start_time
            
            benchmark_results[fc] = {
                'avg_time': execution_time / 20,
                'total_time': execution_time
            }
            
            print(f"  fc'={fc} MPa: {execution_time:.3f}s total, {benchmark_results[fc]['avg_time']*1000:.1f}ms avg")
        
        # Performance should be consistent across material strengths
        times = [result['avg_time'] for result in benchmark_results.values()]
        max_time = max(times)
        min_time = min(times)
        variation = (max_time - min_time) / min_time
        
        assert variation < 0.3, f"Performance variation too high: {variation:.2f}"
        print(f"  ✅ Performance variation: {variation:.2%}")
        
        return benchmark_results
    
    def test_load_level_performance(self, materials):
        """Test performance across different load levels"""
        print("\n📏 Benchmarking Load Level Performance")
        
        beam_designer = ACI318M25BeamDesign(materials['concrete'], materials['steel'])
        
        # Different load levels
        load_multipliers = [0.5, 1.0, 2.0, 4.0]
        
        benchmark_results = {}
        
        for multiplier in load_multipliers:
            geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
            loads = BeamLoads(
                dead_load=5.0 * multiplier,
                live_load=8.0 * multiplier
            )
            
            start_time = time.time()
            
            # Run designs
            for _ in range(15):
                result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
            
            execution_time = time.time() - start_time
            
            benchmark_results[multiplier] = {
                'avg_time': execution_time / 15,
                'total_time': execution_time,
                'load_level': f"{5.0 * multiplier:.1f} + {8.0 * multiplier:.1f} kN/m"
            }
            
            print(f"  Load {multiplier:.1f}x: {execution_time:.3f}s total, "
                  f"{benchmark_results[multiplier]['avg_time']*1000:.1f}ms avg")
        
        # Performance should be relatively consistent
        times = [result['avg_time'] for result in benchmark_results.values()]
        max_time = max(times)
        min_time = min(times)
        variation = (max_time - min_time) / min_time
        
        assert variation < 0.5, f"Load level performance variation too high: {variation:.2f}"
        print(f"  ✅ Load level variation: {variation:.2%}")
        
        return benchmark_results


@pytest.mark.benchmark
@pytest.mark.slow
@pytest.mark.integration
class TestSystemWideBenchmarks:
    """System-wide performance benchmarks"""
    
    def test_complete_building_benchmark(self, performance_monitor):
        """Benchmark complete building design workflow"""
        print("\n🏗️ Benchmarking Complete Building Design")
        
        # Setup materials
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        
        # Create all designers
        beam_designer = ACI318M25BeamDesign(concrete, steel)
        column_designer = ACI318M25ColumnDesign(concrete, steel)
        slab_designer = ACI318M25SlabDesign(concrete, steel)
        
        performance_monitor.start()
        
        # Design complete building (simplified)
        building_results = []
        
        for floor in range(3):  # 3-story building
            floor_results = {}
            
            # Design beams for this floor
            beam_geometry = BeamGeometry(width=300, height=600, effective_depth=550, span_length=6000)
            beam_loads = BeamLoads(dead_load=5.0 + floor * 0.5, live_load=8.0)
            
            for beam_num in range(4):  # 4 beams per floor
                beam_result = beam_designer.design(beam_geometry, beam_loads, BeamType.SIMPLY_SUPPORTED)
                floor_results[f'beam_{beam_num}'] = beam_result
            
            # Design columns for this floor
            column_geometry = ColumnGeometry(width=400, depth=400, length=3000)
            column_loads = ColumnLoads(
                axial_dead=200 + floor * 100,
                axial_live=150 + floor * 75,
                moment_x_dead=15,
                moment_x_live=10
            )
            
            for column_num in range(2):  # 2 columns per floor
                column_result = column_designer.design(column_geometry, column_loads, ColumnType.TIED)
                floor_results[f'column_{column_num}'] = column_result
            
            # Design slab for this floor
            slab_geometry = SlabGeometry(length_x=6000, length_y=6000, thickness=200, span_x=6000, span_y=6000)
            slab_loads = SlabLoads(dead_load=4.0, live_load=2.5)
            slab_result = slab_designer.design(slab_geometry, slab_loads, SlabType.TWO_WAY)
            floor_results['slab'] = slab_result
            
            building_results.append(floor_results)
        
        total_time = performance_monitor.stop()
        
        # Calculate statistics
        total_members = 3 * (4 + 2 + 1)  # 3 floors × (4 beams + 2 columns + 1 slab)
        avg_time_per_member = total_time / total_members
        
        benchmark_summary = {
            'total_time': total_time,
            'total_members': total_members,
            'avg_time_per_member': avg_time_per_member,
            'members_per_second': total_members / total_time,
            'floors_designed': 3
        }
        
        print(f"  Total building design: {total_time:.3f}s")
        print(f"  {total_members} members: {avg_time_per_member*1000:.1f}ms avg")
        print(f"  Throughput: {benchmark_summary['members_per_second']:.1f} members/s")
        
        # Performance targets for complete building
        assert total_time < 10.0, f"Building design too slow: {total_time:.3f}s"
        assert avg_time_per_member < 0.5, f"Average member design too slow: {avg_time_per_member:.3f}s"
        
        return benchmark_summary