"""
Benchmarking Module
===================

Performance benchmarking and analysis tools for structural design standards.
Provides comprehensive performance testing, profiling, and optimization guidance.
"""

import time
import gc
import psutil
import statistics
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import json

class BenchmarkType(Enum):
    """Types of benchmarks"""
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    SCALABILITY = "scalability"
    CONCURRENCY = "concurrency"
    ACCURACY = "accuracy"

class BenchmarkMode(Enum):
    """Benchmark execution modes"""
    SINGLE_THREAD = "single_thread"
    MULTI_THREAD = "multi_thread"
    MULTI_PROCESS = "multi_process"

@dataclass
class BenchmarkConfig:
    """Benchmark configuration"""
    iterations: int = 100
    warmup_iterations: int = 10
    timeout: float = 300.0  # seconds
    mode: BenchmarkMode = BenchmarkMode.SINGLE_THREAD
    workers: int = 4
    measure_memory: bool = True
    measure_cpu: bool = True
    save_individual_results: bool = False

@dataclass
class BenchmarkResult:
    """Single benchmark result"""
    name: str
    benchmark_type: BenchmarkType
    execution_time: float
    memory_usage: float
    peak_memory: float
    cpu_usage: float
    success_rate: float
    error_count: int
    config: BenchmarkConfig
    timestamp: float = field(default_factory=time.time)
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BenchmarkSuite:
    """Collection of benchmark results"""
    name: str
    results: List[BenchmarkResult]
    summary: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DesignBenchmark:
    """
    Benchmarks for structural design calculations
    """
    
    def __init__(self, config: BenchmarkConfig = None):
        """Initialize design benchmark"""
        self.config = config or BenchmarkConfig()
        self.process = psutil.Process()
    
    def benchmark_beam_design(self, 
                            beam_designer,
                            geometry_list: List[Any],
                            loads_list: List[Any]) -> BenchmarkResult:
        """
        Benchmark beam design performance
        
        Parameters:
        -----------
        beam_designer : BeamDesign
            Beam design instance
        geometry_list : list
            List of beam geometries to test
        loads_list : list
            List of beam loads to test
            
        Returns:
        --------
        BenchmarkResult
            Benchmark results
        """
        return self._benchmark_design_function(
            name="beam_design",
            design_func=beam_designer.design,
            test_cases=list(zip(geometry_list, loads_list)),
            benchmark_type=BenchmarkType.EXECUTION_TIME
        )
    
    def benchmark_column_design(self,
                              column_designer,
                              geometry_list: List[Any],
                              loads_list: List[Any]) -> BenchmarkResult:
        """
        Benchmark column design performance
        
        Parameters:
        -----------
        column_designer : ColumnDesign
            Column design instance
        geometry_list : list
            List of column geometries
        loads_list : list
            List of column loads
            
        Returns:
        --------
        BenchmarkResult
            Benchmark results
        """
        return self._benchmark_design_function(
            name="column_design",
            design_func=column_designer.design,
            test_cases=list(zip(geometry_list, loads_list)),
            benchmark_type=BenchmarkType.EXECUTION_TIME
        )
    
    def benchmark_slab_design(self,
                            slab_designer,
                            geometry_list: List[Any],
                            loads_list: List[Any]) -> BenchmarkResult:
        """
        Benchmark slab design performance
        """
        return self._benchmark_design_function(
            name="slab_design",
            design_func=slab_designer.design,
            test_cases=list(zip(geometry_list, loads_list)),
            benchmark_type=BenchmarkType.EXECUTION_TIME
        )
    
    def _benchmark_design_function(self,
                                 name: str,
                                 design_func: Callable,
                                 test_cases: List[tuple],
                                 benchmark_type: BenchmarkType) -> BenchmarkResult:
        """Generic design function benchmarking"""
        
        # Prepare for benchmark
        gc.collect()
        start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        # Warmup
        warmup_cases = test_cases[:self.config.warmup_iterations]
        for geometry, loads in warmup_cases:
            try:
                design_func(geometry, loads)
            except Exception:
                pass  # Ignore warmup errors
        
        # Actual benchmark
        execution_times = []
        memory_measurements = []
        error_count = 0
        success_count = 0
        
        start_time = time.perf_counter()
        
        for i in range(self.config.iterations):
            # Select test case (cycle through if more iterations than cases)
            geometry, loads = test_cases[i % len(test_cases)]
            
            # Measure execution time
            iter_start = time.perf_counter()
            
            try:
                result = design_func(geometry, loads)
                iter_end = time.perf_counter()
                
                execution_times.append(iter_end - iter_start)
                success_count += 1
                
                # Check if result indicates success
                if hasattr(result, 'overall_status'):
                    if result.overall_status not in ['PASS', 'WARNING']:
                        error_count += 1
                
            except Exception as e:
                iter_end = time.perf_counter()
                execution_times.append(iter_end - iter_start)
                error_count += 1
            
            # Memory measurement
            if self.config.measure_memory:
                current_memory = self.process.memory_info().rss / 1024 / 1024
                memory_measurements.append(current_memory)
        
        end_time = time.perf_counter()
        end_memory = self.process.memory_info().rss / 1024 / 1024
        
        # Calculate statistics
        total_time = end_time - start_time
        avg_execution_time = statistics.mean(execution_times) if execution_times else 0
        memory_usage = end_memory - start_memory
        peak_memory = max(memory_measurements) if memory_measurements else end_memory
        success_rate = success_count / self.config.iterations if self.config.iterations > 0 else 0
        
        # CPU usage (approximate)
        cpu_usage = self.process.cpu_percent() if self.config.measure_cpu else 0
        
        return BenchmarkResult(
            name=name,
            benchmark_type=benchmark_type,
            execution_time=avg_execution_time,
            memory_usage=memory_usage,
            peak_memory=peak_memory,
            cpu_usage=cpu_usage,
            success_rate=success_rate,
            error_count=error_count,
            config=self.config,
            details={
                "total_time": total_time,
                "iterations": self.config.iterations,
                "test_cases": len(test_cases),
                "execution_times": execution_times if self.config.save_individual_results else [],
                "memory_measurements": memory_measurements if self.config.save_individual_results else []
            }
        )


class MemoryBenchmark:
    """
    Memory usage analysis and profiling
    """
    
    def __init__(self, config: BenchmarkConfig = None):
        """Initialize memory benchmark"""
        self.config = config or BenchmarkConfig()
        self.process = psutil.Process()
    
    def profile_memory_usage(self, 
                           func: Callable,
                           args: tuple = (),
                           kwargs: dict = None) -> Dict[str, Any]:
        """
        Profile memory usage of a function
        
        Parameters:
        -----------
        func : callable
            Function to profile
        args : tuple
            Function arguments
        kwargs : dict
            Function keyword arguments
            
        Returns:
        --------
        dict
            Memory profiling results
        """
        if kwargs is None:
            kwargs = {}
        
        # Memory tracking
        gc.collect()
        initial_memory = self.process.memory_info().rss
        memory_samples = [initial_memory]
        
        # Execute function with memory sampling
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False
        
        end_time = time.perf_counter()
        final_memory = self.process.memory_info().rss
        
        # Additional memory sampling during execution would require threading
        # For simplicity, we're measuring start and end points
        
        memory_usage = (final_memory - initial_memory) / 1024 / 1024  # MB
        peak_memory = final_memory / 1024 / 1024  # MB
        
        return {
            "initial_memory_mb": initial_memory / 1024 / 1024,
            "final_memory_mb": final_memory / 1024 / 1024,
            "memory_usage_mb": memory_usage,
            "peak_memory_mb": peak_memory,
            "execution_time_s": end_time - start_time,
            "success": success,
            "function_name": func.__name__ if hasattr(func, '__name__') else str(func)
        }
    
    def memory_leak_test(self,
                        func: Callable,
                        iterations: int = 1000,
                        args: tuple = (),
                        kwargs: dict = None) -> Dict[str, Any]:
        """
        Test for memory leaks in repeated function calls
        
        Parameters:
        -----------
        func : callable
            Function to test
        iterations : int
            Number of iterations
        args : tuple
            Function arguments
        kwargs : dict
            Function keyword arguments
            
        Returns:
        --------
        dict
            Memory leak analysis
        """
        if kwargs is None:
            kwargs = {}
        
        memory_samples = []
        gc.collect()
        
        # Sample memory before starting
        initial_memory = self.process.memory_info().rss / 1024 / 1024
        
        # Run iterations with periodic memory sampling
        sample_interval = max(1, iterations // 20)  # Sample 20 times
        
        for i in range(iterations):
            func(*args, **kwargs)
            
            if i % sample_interval == 0:
                gc.collect()  # Force garbage collection
                current_memory = self.process.memory_info().rss / 1024 / 1024
                memory_samples.append(current_memory)
        
        # Final measurement
        gc.collect()
        final_memory = self.process.memory_info().rss / 1024 / 1024
        memory_samples.append(final_memory)
        
        # Analyze trend
        if len(memory_samples) >= 2:
            memory_trend = memory_samples[-1] - memory_samples[0]
            # Simple linear regression for trend analysis
            x_values = list(range(len(memory_samples)))
            y_values = memory_samples
            
            if len(x_values) > 1:
                slope = statistics.covariance(x_values, y_values) / statistics.variance(x_values)
            else:
                slope = 0
        else:
            memory_trend = 0
            slope = 0
        
        return {
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_trend_mb": memory_trend,
            "memory_slope_mb_per_iteration": slope,
            "iterations": iterations,
            "memory_samples": memory_samples,
            "potential_leak": abs(slope) > 0.001,  # Threshold for leak detection
            "leak_severity": "high" if abs(slope) > 0.01 else "low" if abs(slope) > 0.001 else "none"
        }


class ScalabilityBenchmark:
    """
    Scalability and performance analysis across different problem sizes
    """
    
    def __init__(self, config: BenchmarkConfig = None):
        """Initialize scalability benchmark"""
        self.config = config or BenchmarkConfig()
    
    def analyze_scalability(self,
                          func: Callable,
                          problem_sizes: List[int],
                          generate_data_func: Callable,
                          **kwargs) -> Dict[str, Any]:
        """
        Analyze how function performance scales with problem size
        
        Parameters:
        -----------
        func : callable
            Function to analyze
        problem_sizes : list
            List of problem sizes to test
        generate_data_func : callable
            Function that generates test data given a size
        **kwargs
            Additional arguments for generate_data_func
            
        Returns:
        --------
        dict
            Scalability analysis results
        """
        results = []
        
        for size in problem_sizes:
            # Generate test data for this size
            test_data = generate_data_func(size, **kwargs)
            
            # Benchmark the function
            execution_times = []
            memory_usages = []
            
            for _ in range(min(self.config.iterations, 20)):  # Limit iterations for large problems
                gc.collect()
                initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                start_time = time.perf_counter()
                try:
                    if isinstance(test_data, (list, tuple)):
                        result = func(*test_data)
                    elif isinstance(test_data, dict):
                        result = func(**test_data)
                    else:
                        result = func(test_data)
                    
                    end_time = time.perf_counter()
                    execution_times.append(end_time - start_time)
                    
                    final_memory = psutil.Process().memory_info().rss / 1024 / 1024
                    memory_usages.append(final_memory - initial_memory)
                    
                except Exception as e:
                    # Record failed attempt
                    end_time = time.perf_counter()
                    execution_times.append(end_time - start_time)
                    memory_usages.append(0)
            
            # Calculate statistics for this size
            avg_time = statistics.mean(execution_times) if execution_times else 0
            avg_memory = statistics.mean(memory_usages) if memory_usages else 0
            
            results.append({
                "problem_size": size,
                "avg_execution_time": avg_time,
                "avg_memory_usage": avg_memory,
                "min_execution_time": min(execution_times) if execution_times else 0,
                "max_execution_time": max(execution_times) if execution_times else 0,
                "iterations": len(execution_times)
            })
        
        # Analyze complexity
        complexity_analysis = self._analyze_complexity(results)
        
        return {
            "results": results,
            "complexity_analysis": complexity_analysis,
            "function_name": func.__name__ if hasattr(func, '__name__') else str(func),
            "problem_sizes": problem_sizes
        }
    
    def _analyze_complexity(self, results: List[Dict]) -> Dict[str, Any]:
        """Analyze computational complexity from results"""
        if len(results) < 3:
            return {"analysis": "insufficient_data"}
        
        sizes = [r["problem_size"] for r in results]
        times = [r["avg_execution_time"] for r in results]
        
        # Simple complexity analysis (could be more sophisticated)
        # Check for linear, quadratic, logarithmic patterns
        
        # Linear check: T(n) ∝ n
        linear_ratios = []
        for i in range(1, len(results)):
            if sizes[i-1] > 0 and times[i-1] > 0:
                size_ratio = sizes[i] / sizes[i-1]
                time_ratio = times[i] / times[i-1]
                linear_ratios.append(time_ratio / size_ratio)
        
        # Quadratic check: T(n) ∝ n²
        quadratic_ratios = []
        for i in range(1, len(results)):
            if sizes[i-1] > 0 and times[i-1] > 0:
                size_ratio = sizes[i] / sizes[i-1]
                time_ratio = times[i] / times[i-1]
                quadratic_ratios.append(time_ratio / (size_ratio ** 2))
        
        # Determine likely complexity
        linear_variance = statistics.variance(linear_ratios) if len(linear_ratios) > 1 else float('inf')
        quadratic_variance = statistics.variance(quadratic_ratios) if len(quadratic_ratios) > 1 else float('inf')
        
        if linear_variance < quadratic_variance and linear_variance < 0.1:
            complexity = "O(n) - Linear"
        elif quadratic_variance < 0.1:
            complexity = "O(n²) - Quadratic"
        else:
            complexity = "Unknown/Complex"
        
        return {
            "estimated_complexity": complexity,
            "linear_variance": linear_variance,
            "quadratic_variance": quadratic_variance,
            "performance_trend": "increasing" if times[-1] > times[0] else "stable"
        }


class ConcurrencyBenchmark:
    """
    Benchmarks for concurrent and parallel execution
    """
    
    def __init__(self, config: BenchmarkConfig = None):
        """Initialize concurrency benchmark"""
        self.config = config or BenchmarkConfig()
    
    def benchmark_threading(self,
                          func: Callable,
                          test_data_list: List[Any],
                          max_workers: int = None) -> Dict[str, Any]:
        """
        Benchmark function performance with threading
        
        Parameters:
        -----------
        func : callable
            Function to benchmark
        test_data_list : list
            List of test data for parallel execution
        max_workers : int
            Maximum number of worker threads
            
        Returns:
        --------
        dict
            Threading benchmark results
        """
        if max_workers is None:
            max_workers = min(self.config.workers, len(test_data_list))
        
        # Single-threaded baseline
        start_time = time.perf_counter()
        single_results = []
        for data in test_data_list:
            try:
                if isinstance(data, (list, tuple)):
                    result = func(*data)
                elif isinstance(data, dict):
                    result = func(**data)
                else:
                    result = func(data)
                single_results.append(result)
            except Exception as e:
                single_results.append(None)
        
        single_thread_time = time.perf_counter() - start_time
        
        # Multi-threaded execution
        start_time = time.perf_counter()
        multi_results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for data in test_data_list:
                if isinstance(data, (list, tuple)):
                    future = executor.submit(func, *data)
                elif isinstance(data, dict):
                    future = executor.submit(func, **data)
                else:
                    future = executor.submit(func, data)
                futures.append(future)
            
            for future in futures:
                try:
                    result = future.result(timeout=30)
                    multi_results.append(result)
                except Exception as e:
                    multi_results.append(None)
        
        multi_thread_time = time.perf_counter() - start_time
        
        # Calculate speedup
        speedup = single_thread_time / multi_thread_time if multi_thread_time > 0 else 0
        efficiency = speedup / max_workers if max_workers > 0 else 0
        
        return {
            "single_thread_time": single_thread_time,
            "multi_thread_time": multi_thread_time,
            "speedup": speedup,
            "efficiency": efficiency,
            "max_workers": max_workers,
            "test_cases": len(test_data_list),
            "successful_results": sum(1 for r in multi_results if r is not None)
        }


class BenchmarkReporter:
    """
    Generates comprehensive benchmark reports
    """
    
    def __init__(self):
        """Initialize benchmark reporter"""
        pass
    
    def generate_report(self, 
                       benchmark_suite: BenchmarkSuite,
                       output_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Generate comprehensive benchmark report
        
        Parameters:
        -----------
        benchmark_suite : BenchmarkSuite
            Collection of benchmark results
        output_path : Path, optional
            Path to save report
            
        Returns:
        --------
        dict
            Generated report
        """
        report = {
            "suite_name": benchmark_suite.name,
            "timestamp": time.time(),
            "summary": self._generate_summary(benchmark_suite.results),
            "detailed_results": [self._format_result(r) for r in benchmark_suite.results],
            "recommendations": self._generate_recommendations(benchmark_suite.results),
            "metadata": benchmark_suite.metadata
        }
        
        # Save to file if path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
        
        return report
    
    def _generate_summary(self, results: List[BenchmarkResult]) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not results:
            return {}
        
        execution_times = [r.execution_time for r in results]
        memory_usages = [r.memory_usage for r in results]
        success_rates = [r.success_rate for r in results]
        
        return {
            "total_benchmarks": len(results),
            "avg_execution_time": statistics.mean(execution_times),
            "median_execution_time": statistics.median(execution_times),
            "max_execution_time": max(execution_times),
            "min_execution_time": min(execution_times),
            "avg_memory_usage": statistics.mean(memory_usages),
            "max_memory_usage": max(memory_usages),
            "avg_success_rate": statistics.mean(success_rates),
            "total_errors": sum(r.error_count for r in results)
        }
    
    def _format_result(self, result: BenchmarkResult) -> Dict[str, Any]:
        """Format individual result for report"""
        return {
            "name": result.name,
            "type": result.benchmark_type.value,
            "execution_time_ms": result.execution_time * 1000,
            "memory_usage_mb": result.memory_usage,
            "peak_memory_mb": result.peak_memory,
            "cpu_usage_percent": result.cpu_usage,
            "success_rate": result.success_rate,
            "error_count": result.error_count,
            "timestamp": result.timestamp,
            "config": {
                "iterations": result.config.iterations,
                "mode": result.config.mode.value
            }
        }
    
    def _generate_recommendations(self, results: List[BenchmarkResult]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        for result in results:
            if result.execution_time > 1.0:  # Slow execution
                recommendations.append(f"Consider optimizing {result.name} - execution time {result.execution_time:.2f}s is high")
            
            if result.memory_usage > 100:  # High memory usage
                recommendations.append(f"Consider memory optimization for {result.name} - using {result.memory_usage:.1f}MB")
            
            if result.success_rate < 0.95:  # Low success rate
                recommendations.append(f"Investigate reliability issues in {result.name} - success rate {result.success_rate:.1%}")
            
            if result.error_count > result.config.iterations * 0.1:  # High error rate
                recommendations.append(f"High error rate in {result.name} - {result.error_count} errors in {result.config.iterations} iterations")
        
        return recommendations


# Convenience functions for quick benchmarking
def quick_benchmark(func: Callable, 
                   args: tuple = (), 
                   kwargs: dict = None,
                   iterations: int = 100) -> BenchmarkResult:
    """Quick benchmark of a function"""
    config = BenchmarkConfig(iterations=iterations)
    benchmark = DesignBenchmark(config)
    
    # Create a simple test case
    test_cases = [(args, kwargs or {})]
    
    return benchmark._benchmark_design_function(
        name=func.__name__ if hasattr(func, '__name__') else "function",
        design_func=lambda *a, **k: func(*a, **k),
        test_cases=test_cases,
        benchmark_type=BenchmarkType.EXECUTION_TIME
    )

def memory_profile(func: Callable, 
                  args: tuple = (), 
                  kwargs: dict = None) -> Dict[str, Any]:
    """Quick memory profiling"""
    benchmark = MemoryBenchmark()
    return benchmark.profile_memory_usage(func, args, kwargs or {})