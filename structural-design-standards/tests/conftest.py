"""
Test Configuration for Structural Design Standards Library
==========================================================

Pytest configuration and fixtures for comprehensive testing.
"""

import pytest
import math
import sys
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add structural_standards to Python path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test data fixtures
@pytest.fixture
def sample_concrete_properties():
    """Sample concrete properties for testing"""
    return {
        'fc_prime': 28.0,  # MPa
        'unit_weight': 24.0,  # kN/m³
        'aggregate_size': 25.0,  # mm
        'elastic_modulus': 24847.0,  # MPa (calculated)
        'modulus_of_rupture': 3.31,  # MPa (calculated)
    }

@pytest.fixture
def sample_steel_properties():
    """Sample steel properties for testing"""
    return {
        'fy': 420.0,  # MPa
        'fu': 620.0,  # MPa
        'elastic_modulus': 200000.0,  # MPa
        'unit_weight': 77.0,  # kN/m³
    }

@pytest.fixture
def sample_thai_concrete():
    """Sample Thai concrete properties"""
    return {
        'grade': 'Fc210',
        'fc_prime': 21.0,  # MPa
        'fc_ksc': 214.1,   # ksc (calculated)
        'unit_weight': 24.0,  # kN/m³
    }

@pytest.fixture  
def sample_beam_geometry():
    """Sample beam geometry for testing"""
    return {
        'width': 300.0,     # mm
        'depth': 500.0,     # mm
        'effective_depth': 450.0,  # mm
        'cover': 40.0,      # mm
        'span': 6.0,        # m
    }

@pytest.fixture
def sample_slab_geometry():
    """Sample slab geometry for testing"""
    return {
        'length_x': 4.0,    # m
        'length_y': 6.0,    # m
        'thickness': 150.0, # mm
        'effective_depth': 120.0,  # mm
        'cover': 20.0,      # mm
    }

@pytest.fixture
def sample_loads():
    """Sample load combinations for testing"""
    return {
        'dead_load': 5.0,    # kN/m²
        'live_load': 3.0,    # kN/m²
        'wind_load': 1.5,    # kN/m²
        'seismic_load': 2.0, # kN/m²
    }

@pytest.fixture
def tolerance():
    """Standard tolerance for floating point comparisons"""
    return 1e-6

@pytest.fixture
def engineering_tolerance():
    """Engineering tolerance for practical calculations"""
    return 0.01  # 1%

# Helper functions for tests
def approx_equal(a: float, b: float, tolerance: float = 1e-6) -> bool:
    """Check if two values are approximately equal"""
    if math.isnan(a) or math.isnan(b):
        return False
    if math.isinf(a) or math.isinf(b):
        return a == b
    return abs(a - b) <= tolerance

def validate_design_result(result: Dict[str, Any]) -> bool:
    """Validate that a design result has required fields"""
    required_fields = [
        'member_type',
        'design_method', 
        'overall_status',
        'utilization_ratio'
    ]
    
    return all(field in result for field in required_fields)

def validate_material_properties(props: Dict[str, float]) -> bool:
    """Validate material properties"""
    required_props = ['fc_prime', 'unit_weight']  # Basic required properties
    
    # Check required properties exist and are positive
    for prop in required_props:
        if prop not in props:
            return False
        if props[prop] <= 0:
            return False
    
    return True

@pytest.fixture
def aci_concrete():
    """ACI 318M-25 concrete fixture"""
    try:
        from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
        return ACI318M25Concrete(fc_prime=28.0)
    except ImportError:
        pytest.skip("ACI 318M-25 concrete module not available")

@pytest.fixture
def aci_steel():
    """ACI 318M-25 steel fixture"""
    try:
        from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
        return ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')
    except ImportError:
        pytest.skip("ACI 318M-25 steel module not available")

@pytest.fixture
def thai_load_combinations():
    """Thai Ministry Regulation B.E. 2566 load combinations fixture"""
    try:
        from structural_standards.thai.ministry_2566.load_combinations import ThaiMinistryLoadCombinations
        return ThaiMinistryLoadCombinations()
    except ImportError:
        pytest.skip("Thai Ministry Regulation B.E. 2566 module not available")

@pytest.fixture
def sample_column_geometry():
    """Sample column geometry for testing"""
    return {
        'width': 400.0,     # mm
        'depth': 400.0,     # mm
        'length': 3000.0,   # mm
        'cover': 40.0,      # mm
        'effective_depth': 350.0,  # mm
    }

@pytest.fixture
def sample_wall_geometry():
    """Sample wall geometry for testing"""
    return {
        'length': 4000.0,   # mm
        'height': 3000.0,   # mm
        'thickness': 200.0, # mm
        'cover': 40.0,      # mm
    }

@pytest.fixture
def sample_footing_geometry():
    """Sample footing geometry for testing"""
    return {
        'length': 2000.0,   # mm
        'width': 2000.0,    # mm
        'thickness': 500.0, # mm
        'cover_bottom': 75.0,  # mm
        'cover_top': 40.0,     # mm
    }

@pytest.fixture
def sample_soil_properties():
    """Sample soil properties for testing"""
    return {
        'bearing_capacity': 200.0,  # kPa
        'unit_weight': 18.0,        # kN/m³
        'friction_angle': 30.0,     # degrees
        'cohesion': 0.0,           # kPa
    }

@pytest.fixture
def performance_benchmark_data():
    """Performance benchmark data for testing"""
    return {
        'max_execution_time': {
            'beam_design': 0.1,      # seconds
            'column_design': 0.15,   # seconds
            'slab_design': 0.2,      # seconds
            'wall_design': 0.1,      # seconds
            'footing_design': 0.15,  # seconds
            'load_combinations': 0.05,  # seconds
        },
        'memory_usage_limit': 50,    # MB
        'iterations_per_test': 100   # for performance tests
    }

# Enhanced helper functions
def validate_aci_design_result(result) -> bool:
    """Validate ACI design result structure"""
    try:
        # Check basic structure
        assert hasattr(result, 'member_type')
        assert hasattr(result, 'design_method')
        assert hasattr(result, 'overall_status')
        assert hasattr(result, 'utilization_ratio')
        
        # Check design method
        assert result.design_method == "ACI 318M-25"
        
        # Check utilization ratio
        assert 0.0 <= result.utilization_ratio <= 10.0  # Allow very high ratios for failing designs
        
        return True
    except (AssertionError, AttributeError):
        return False

def validate_thai_load_combination(combination) -> bool:
    """Validate Thai load combination structure"""
    try:
        # Check required attributes
        assert hasattr(combination, 'name')
        assert hasattr(combination, 'combination_type')
        assert hasattr(combination, 'factors')
        assert hasattr(combination, 'get_equation')
        
        # Check factors are valid
        for load_type, factor in combination.factors.items():
            assert isinstance(factor, (int, float))
            assert -2.0 <= factor <= 2.0  # Reasonable range for load factors
        
        return True
    except (AssertionError, AttributeError):
        return False

# Test data validation
def pytest_runtest_setup(item):
    """Setup for each test run"""
    # Mark slow tests
    if "benchmark" in item.name or "performance" in item.name:
        if item.get_closest_marker("slow") is None:
            item.add_marker(pytest.mark.slow)

# Custom pytest markers
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "aci: mark test as ACI standard related"
    )
    config.addinivalue_line(
        "markers", "thai: mark test as Thai standard related"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "validation: mark test as validation/verification test"
    )
    config.addinivalue_line(
        "markers", "benchmark: mark test as performance benchmark"
    )
    config.addinivalue_line(
        "markers", "materials: mark test as materials related"
    )
    config.addinivalue_line(
        "markers", "beam: mark test as beam design related"
    )
    config.addinivalue_line(
        "markers", "column: mark test as column design related"
    )
    config.addinivalue_line(
        "markers", "slab: mark test as slab design related"
    )
    config.addinivalue_line(
        "markers", "wall: mark test as wall design related"
    )
    config.addinivalue_line(
        "markers", "footing: mark test as footing design related"
    )
    config.addinivalue_line(
        "markers", "diaphragm: mark test as diaphragm design related"
    )
    config.addinivalue_line(
        "markers", "load_combinations: mark test as load combinations related"
    )
    config.addinivalue_line(
        "markers", "ministry_2566: mark test as Thai Ministry Regulation B.E. 2566 related"
    )

# Test collection and reporting
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Auto-mark tests based on file location
        test_path = str(item.fspath)
        
        if "test_aci" in test_path:
            item.add_marker(pytest.mark.aci)
            
        if "test_thai" in test_path:
            item.add_marker(pytest.mark.thai)
            
        if "test_materials" in test_path:
            item.add_marker(pytest.mark.materials)
            
        if "test_integration" in test_path:
            item.add_marker(pytest.mark.integration)
            
        if "benchmark" in test_path:
            item.add_marker(pytest.mark.benchmark)
            item.add_marker(pytest.mark.slow)
            
        if "validation" in test_path:
            item.add_marker(pytest.mark.validation)

# Performance monitoring
@pytest.fixture(scope="session")
def performance_monitor():
    """Performance monitoring fixture"""
    import time
    import psutil
    import os
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.process = psutil.Process(os.getpid())
            
        def start(self):
            self.start_time = time.time()
            
        def stop(self):
            if self.start_time:
                return time.time() - self.start_time
            return 0
            
        def memory_usage(self):
            return self.process.memory_info().rss / 1024 / 1024  # MB
    
    return PerformanceMonitor()