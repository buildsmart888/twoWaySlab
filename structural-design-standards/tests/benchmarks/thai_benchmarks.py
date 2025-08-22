"""
Thai Standards Performance Benchmarks
=====================================

Performance benchmarks for Thai Ministry Regulation B.E. 2566 and other Thai standards.
Tests load combination calculations, material property access, and integration performance.

การทดสอบประสิทธิภาพการทำงานของมาตรฐานไทย
"""

import pytest
import time
import psutil
import os
from typing import Dict, Any, List

from structural_standards.thai.ministry_2566.load_combinations import (
    ThaiMinistryLoadCombinations, ThaiLoadType, ThaiCombinationType
)


@pytest.mark.thai
@pytest.mark.benchmark
@pytest.mark.slow
class TestThaiStandardsBenchmarks:
    """Performance benchmarks for Thai standards"""
    
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
    
    def test_load_combinations_benchmark(self, performance_tracker):
        """Benchmark Thai load combinations performance"""
        print("\n⚖️ Benchmarking Thai Load Combinations")
        
        thai_loads = ThaiMinistryLoadCombinations()
        
        # Test load cases
        load_cases = [
            {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0},
            {ThaiLoadType.DEAD: 80.0, ThaiLoadType.LIVE: 60.0, ThaiLoadType.WIND: 30.0},
            {ThaiLoadType.DEAD: 120.0, ThaiLoadType.LIVE: 40.0, ThaiLoadType.EARTHQUAKE: 25.0},
            {ThaiLoadType.DEAD: 90.0, ThaiLoadType.LIVE: 70.0, ThaiLoadType.WIND: 35.0, ThaiLoadType.EARTHQUAKE: 20.0},
            {ThaiLoadType.DEAD: 110.0, ThaiLoadType.LIVE: 45.0, ThaiLoadType.LATERAL_EARTH: 20.0, ThaiLoadType.FLUID: 15.0}
        ]
        
        benchmark_results = {}
        
        for i, loads in enumerate(load_cases):
            case_name = f"case_{i+1}"
            
            performance_tracker.start()
            
            # Run multiple load combination calculations
            for _ in range(500):  # 500 iterations
                # Calculate all ULS combinations
                uls_results = thai_loads.calculate_all_combinations(
                    loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
                
                # Calculate all SLS combinations
                sls_results = thai_loads.calculate_all_combinations(
                    loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
                )
                
                # Find critical combinations
                critical_uls, max_uls = thai_loads.find_critical_combination(
                    loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
                critical_sls, max_sls = thai_loads.find_critical_combination(
                    loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
                )
            
            metrics = performance_tracker.stop()
            
            benchmark_results[case_name] = {
                'avg_time_per_calculation': metrics['execution_time'] / 500,
                'total_time': metrics['execution_time'],
                'calculations_per_second': 500 / metrics['execution_time'],
                'memory_usage': metrics['memory_usage'],
                'load_types': len(loads)
            }
            
            print(f"  {case_name} ({len(loads)} loads): {metrics['execution_time']:.3f}s total, "
                  f"{benchmark_results[case_name]['avg_time_per_calculation']*1000:.2f}ms avg")
        
        # Performance targets
        for case_name, metrics in benchmark_results.items():
            assert metrics['avg_time_per_calculation'] < 0.01, \
                f"Load combination too slow: {case_name} = {metrics['avg_time_per_calculation']:.4f}s"
            assert metrics['calculations_per_second'] > 100, \
                f"Load combination throughput too low: {case_name} = {metrics['calculations_per_second']:.1f} calc/s"
        
        return benchmark_results
    
    def test_load_combination_scalability(self, performance_tracker):
        """Test scalability with increasing number of load types"""
        print("\n📈 Benchmarking Load Combination Scalability")
        
        thai_loads = ThaiMinistryLoadCombinations()
        
        # Progressive load complexity
        load_progressions = [
            {ThaiLoadType.DEAD: 100.0},  # 1 load type
            {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0},  # 2 load types
            {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0, ThaiLoadType.WIND: 30.0},  # 3 load types
            {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0, ThaiLoadType.WIND: 30.0, ThaiLoadType.EARTHQUAKE: 25.0},  # 4 load types
            {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0, ThaiLoadType.WIND: 30.0, ThaiLoadType.EARTHQUAKE: 25.0, ThaiLoadType.LATERAL_EARTH: 20.0},  # 5 load types
            {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0, ThaiLoadType.WIND: 30.0, ThaiLoadType.EARTHQUAKE: 25.0, ThaiLoadType.LATERAL_EARTH: 20.0, ThaiLoadType.FLUID: 15.0}  # 6 load types
        ]
        
        scalability_results = {}
        
        for loads in load_progressions:
            num_loads = len(loads)
            
            performance_tracker.start()
            
            # Run calculations
            for _ in range(200):  # 200 iterations
                uls_results = thai_loads.calculate_all_combinations(
                    loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
                critical_uls, max_uls = thai_loads.find_critical_combination(
                    loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
            
            metrics = performance_tracker.stop()
            
            scalability_results[num_loads] = {
                'avg_time': metrics['execution_time'] / 200,
                'total_time': metrics['execution_time'],
                'throughput': 200 / metrics['execution_time'],
                'memory_usage': metrics['memory_usage']
            }
            
            print(f"  {num_loads} load types: {metrics['execution_time']:.3f}s total, "
                  f"{scalability_results[num_loads]['avg_time']*1000:.2f}ms avg")
        
        # Check scalability
        times = [result['avg_time'] for result in scalability_results.values()]
        first_time = times[0]
        last_time = times[-1]
        scalability_factor = last_time / first_time
        
        # Should scale reasonably (not exponentially)
        assert scalability_factor < 10, f"Scalability too poor: {scalability_factor:.1f}x slower"
        print(f"  ✅ Scalability factor: {scalability_factor:.1f}x")
        
        return scalability_results
    
    def test_combination_comparison_benchmark(self, performance_tracker):
        """Benchmark comparison between ULS and SLS combinations"""
        print("\n🔄 Benchmarking ULS vs SLS Performance")
        
        thai_loads = ThaiMinistryLoadCombinations()
        
        test_loads = {
            ThaiLoadType.DEAD: 100.0,
            ThaiLoadType.LIVE: 50.0,
            ThaiLoadType.WIND: 30.0,
            ThaiLoadType.EARTHQUAKE: 25.0
        }
        
        comparison_results = {}
        
        # Test ULS performance
        performance_tracker.start()
        for _ in range(1000):
            uls_results = thai_loads.calculate_all_combinations(
                test_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
            )
            critical_uls, max_uls = thai_loads.find_critical_combination(
                test_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
            )
        uls_metrics = performance_tracker.stop()
        
        comparison_results['ULS'] = {
            'avg_time': uls_metrics['execution_time'] / 1000,
            'total_time': uls_metrics['execution_time'],
            'throughput': 1000 / uls_metrics['execution_time']
        }
        
        # Test SLS performance
        performance_tracker.start()
        for _ in range(1000):
            sls_results = thai_loads.calculate_all_combinations(
                test_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
            )
            critical_sls, max_sls = thai_loads.find_critical_combination(
                test_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
            )
        sls_metrics = performance_tracker.stop()
        
        comparison_results['SLS'] = {
            'avg_time': sls_metrics['execution_time'] / 1000,
            'total_time': sls_metrics['execution_time'],
            'throughput': 1000 / sls_metrics['execution_time']
        }
        
        print(f"  ULS: {uls_metrics['execution_time']:.3f}s total, "
              f"{comparison_results['ULS']['avg_time']*1000:.2f}ms avg")
        print(f"  SLS: {sls_metrics['execution_time']:.3f}s total, "
              f"{comparison_results['SLS']['avg_time']*1000:.2f}ms avg")
        
        # Performance should be similar
        uls_time = comparison_results['ULS']['avg_time']
        sls_time = comparison_results['SLS']['avg_time']
        time_ratio = max(uls_time, sls_time) / min(uls_time, sls_time)
        
        assert time_ratio < 2.0, f"Performance difference too large: {time_ratio:.1f}x"
        print(f"  ✅ Performance ratio: {time_ratio:.1f}x")
        
        return comparison_results
    
    def test_memory_efficiency_benchmark(self, performance_tracker):
        """Test memory efficiency of Thai load combinations"""
        print("\n💾 Benchmarking Memory Efficiency")
        
        thai_loads = ThaiMinistryLoadCombinations()
        
        # Various load scenarios
        load_scenarios = [
            ("Simple", {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0}),
            ("Wind", {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0, ThaiLoadType.WIND: 30.0}),
            ("Seismic", {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0, ThaiLoadType.EARTHQUAKE: 25.0}),
            ("Complex", {ThaiLoadType.DEAD: 100.0, ThaiLoadType.LIVE: 50.0, ThaiLoadType.WIND: 30.0, 
                        ThaiLoadType.EARTHQUAKE: 25.0, ThaiLoadType.LATERAL_EARTH: 20.0, ThaiLoadType.FLUID: 15.0})
        ]
        
        memory_results = {}
        
        for scenario_name, loads in load_scenarios:
            performance_tracker.start()
            
            # Intensive calculations to test memory usage
            results_storage = []
            for i in range(500):
                uls_results = thai_loads.calculate_all_combinations(
                    loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
                sls_results = thai_loads.calculate_all_combinations(
                    loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
                )
                
                # Store results to prevent garbage collection
                results_storage.append((uls_results, sls_results))
                
                # Clear periodically to test memory management
                if i % 100 == 99:
                    results_storage.clear()
            
            metrics = performance_tracker.stop()
            
            memory_results[scenario_name] = {
                'final_memory': metrics['memory_usage'],
                'memory_delta': metrics['memory_delta'],
                'execution_time': metrics['execution_time']
            }
            
            print(f"  {scenario_name}: {metrics['memory_usage']:.1f}MB final, "
                  f"Δ{metrics['memory_delta']:.1f}MB")
        
        # Memory usage should be reasonable and not grow excessively
        for scenario_name, metrics in memory_results.items():
            assert metrics['final_memory'] < 150, \
                f"Memory usage too high for {scenario_name}: {metrics['final_memory']:.1f}MB"
            
            # Memory delta should be controlled (no major leaks)
            if metrics['memory_delta'] > 0:
                assert metrics['memory_delta'] < 30, \
                    f"Memory delta too high for {scenario_name}: {metrics['memory_delta']:.1f}MB"
        
        return memory_results
    
    def test_load_validation_benchmark(self, performance_tracker):
        """Benchmark load validation performance"""
        print("\n✅ Benchmarking Load Validation Performance")
        
        thai_loads = ThaiMinistryLoadCombinations()
        
        # Test cases for validation
        valid_loads = {
            ThaiLoadType.DEAD: 100.0,
            ThaiLoadType.LIVE: 50.0,
            ThaiLoadType.WIND: 30.0
        }
        
        invalid_loads = {
            ThaiLoadType.DEAD: -10.0,  # Invalid negative
            ThaiLoadType.LIVE: 50.0
        }
        
        performance_tracker.start()
        
        # Test validation performance
        for _ in range(5000):  # 5000 validations
            # Valid case
            is_valid = thai_loads.validate_loads(valid_loads)
            
            # Invalid case
            is_invalid = thai_loads.validate_loads(invalid_loads)
        
        metrics = performance_tracker.stop()
        
        validation_results = {
            'total_time': metrics['execution_time'],
            'avg_time_per_validation': metrics['execution_time'] / 10000,  # 5000 × 2
            'validations_per_second': 10000 / metrics['execution_time'],
            'memory_usage': metrics['memory_usage']
        }
        
        print(f"  {metrics['execution_time']:.3f}s for 10,000 validations")
        print(f"  {validation_results['avg_time_per_validation']*1000000:.1f}μs per validation")
        print(f"  {validation_results['validations_per_second']:.0f} validations/s")
        
        # Validation should be very fast
        assert validation_results['avg_time_per_validation'] < 0.001, \
            f"Validation too slow: {validation_results['avg_time_per_validation']:.4f}s"
        assert validation_results['validations_per_second'] > 1000, \
            f"Validation throughput too low: {validation_results['validations_per_second']:.0f}/s"
        
        return validation_results


@pytest.mark.thai
@pytest.mark.benchmark
@pytest.mark.slow
class TestThaiIntegrationBenchmarks:
    """Integration benchmarks for Thai standards"""
    
    def test_building_analysis_benchmark(self, performance_tracker):
        """Benchmark complete building analysis with Thai standards"""
        print("\n🏢 Benchmarking Thai Building Analysis")
        
        thai_loads = ThaiMinistryLoadCombinations()
        
        # Simulate multi-story building loads
        building_floors = 5
        
        performance_tracker.start()
        
        building_results = []
        
        for floor in range(building_floors):
            floor_loads = {
                ThaiLoadType.DEAD: 80.0 + floor * 10.0,      # Increasing dead load
                ThaiLoadType.LIVE: 50.0,                      # Constant live load
                ThaiLoadType.WIND: 25.0 + floor * 5.0,       # Increasing wind load
                ThaiLoadType.EARTHQUAKE: 20.0 + floor * 3.0  # Increasing seismic load
            }
            
            # Multiple load cases per floor
            floor_analyses = []
            
            for load_case in range(10):  # 10 load cases per floor
                # Vary loads slightly for each case
                varied_loads = {
                    load_type: value * (1.0 + load_case * 0.05)
                    for load_type, value in floor_loads.items()
                }
                
                # Calculate all combinations
                uls_results = thai_loads.calculate_all_combinations(
                    varied_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
                sls_results = thai_loads.calculate_all_combinations(
                    varied_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
                )
                
                # Find critical combinations
                critical_uls, max_uls = thai_loads.find_critical_combination(
                    varied_loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
                critical_sls, max_sls = thai_loads.find_critical_combination(
                    varied_loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
                )
                
                floor_analyses.append({
                    'uls_results': uls_results,
                    'sls_results': sls_results,
                    'critical_uls': (critical_uls.name, max_uls),
                    'critical_sls': (critical_sls.name, max_sls)
                })
            
            building_results.append(floor_analyses)
        
        metrics = performance_tracker.stop()
        
        total_analyses = building_floors * 10
        building_benchmark = {
            'total_time': metrics['execution_time'],
            'total_analyses': total_analyses,
            'avg_time_per_analysis': metrics['execution_time'] / total_analyses,
            'analyses_per_second': total_analyses / metrics['execution_time'],
            'floors_analyzed': building_floors,
            'memory_usage': metrics['memory_usage']
        }
        
        print(f"  {total_analyses} total analyses: {metrics['execution_time']:.3f}s")
        print(f"  {building_benchmark['avg_time_per_analysis']*1000:.1f}ms per analysis")
        print(f"  {building_benchmark['analyses_per_second']:.1f} analyses/s")
        
        # Performance targets for building analysis
        assert building_benchmark['avg_time_per_analysis'] < 0.1, \
            f"Building analysis too slow: {building_benchmark['avg_time_per_analysis']:.3f}s"
        assert building_benchmark['analyses_per_second'] > 10, \
            f"Building analysis throughput too low: {building_benchmark['analyses_per_second']:.1f}/s"
        
        return building_benchmark
    
    def test_concurrent_thai_operations(self, performance_tracker):
        """Test concurrent Thai operations performance"""
        print("\n⚡ Benchmarking Concurrent Thai Operations")
        
        thai_loads = ThaiMinistryLoadCombinations()
        
        # Simulate concurrent operations
        operation_types = [
            "residential", "office", "industrial", "mixed_use"
        ]
        
        load_profiles = {
            "residential": {ThaiLoadType.DEAD: 60.0, ThaiLoadType.LIVE: 40.0, ThaiLoadType.WIND: 20.0},
            "office": {ThaiLoadType.DEAD: 80.0, ThaiLoadType.LIVE: 60.0, ThaiLoadType.WIND: 30.0},
            "industrial": {ThaiLoadType.DEAD: 120.0, ThaiLoadType.LIVE: 80.0, ThaiLoadType.WIND: 35.0},
            "mixed_use": {ThaiLoadType.DEAD: 90.0, ThaiLoadType.LIVE: 50.0, ThaiLoadType.WIND: 25.0, ThaiLoadType.EARTHQUAKE: 20.0}
        }
        
        performance_tracker.start()
        
        # Simulate concurrent operations by rapid switching
        for round_num in range(25):  # 25 rounds
            for operation_type in operation_types:
                loads = load_profiles[operation_type]
                
                # Perform full analysis
                uls_results = thai_loads.calculate_all_combinations(
                    loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
                sls_results = thai_loads.calculate_all_combinations(
                    loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
                )
                critical_uls, max_uls = thai_loads.find_critical_combination(
                    loads, ThaiCombinationType.ULTIMATE_LIMIT_STATE
                )
                critical_sls, max_sls = thai_loads.find_critical_combination(
                    loads, ThaiCombinationType.SERVICEABILITY_LIMIT_STATE
                )
        
        metrics = performance_tracker.stop()
        
        total_operations = 25 * len(operation_types)
        concurrent_results = {
            'total_time': metrics['execution_time'],
            'total_operations': total_operations,
            'avg_time_per_operation': metrics['execution_time'] / total_operations,
            'operations_per_second': total_operations / metrics['execution_time'],
            'operation_types': len(operation_types),
            'memory_usage': metrics['memory_usage']
        }
        
        print(f"  {total_operations} concurrent operations: {metrics['execution_time']:.3f}s")
        print(f"  {concurrent_results['avg_time_per_operation']*1000:.1f}ms per operation")
        print(f"  {concurrent_results['operations_per_second']:.1f} operations/s")
        
        # Performance targets
        assert concurrent_results['avg_time_per_operation'] < 0.05, \
            f"Concurrent operations too slow: {concurrent_results['avg_time_per_operation']:.3f}s"
        assert concurrent_results['operations_per_second'] > 20, \
            f"Concurrent throughput too low: {concurrent_results['operations_per_second']:.1f}/s"
        
        return concurrent_results