"""
Utility Validation Tests
=======================

Tests for utility functions including validation, unit conversion, and helpers.

การทดสอบฟังก์ชันช่วยเหลือต่างๆ
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.utils.validation import (
    StructuralValidator, validate_positive, validate_range
)


@pytest.mark.unit
@pytest.mark.utils
class TestStructuralValidator:
    """Test structural validation utilities"""
    
    @pytest.fixture
    def validator(self):
        """Create validator fixture"""
        return StructuralValidator()
    
    def test_validator_initialization(self, validator):
        """Test validator initialization"""
        assert validator is not None
        assert hasattr(validator, 'validate_positive')
        assert hasattr(validator, 'validate_range')
    
    def test_positive_validation(self, validator):
        """Test positive value validation"""
        # Valid positive values
        assert validator.validate_positive(10.0, "test_value") == True
        assert validator.validate_positive(0.1, "test_value") == True
        assert validator.validate_positive(1000, "test_value") == True
        
        # Invalid values
        with pytest.raises(ValueError):
            validator.validate_positive(-1.0, "negative_value")
        
        with pytest.raises(ValueError):
            validator.validate_positive(0.0, "zero_value")
    
    def test_range_validation(self, validator):
        """Test range validation"""
        # Valid ranges
        assert validator.validate_range(5.0, 0, 10, "test_value") == True
        assert validator.validate_range(0.0, 0, 10, "boundary_min") == True
        assert validator.validate_range(10.0, 0, 10, "boundary_max") == True
        
        # Invalid ranges
        with pytest.raises(ValueError):
            validator.validate_range(-1.0, 0, 10, "below_min")
        
        with pytest.raises(ValueError):
            validator.validate_range(11.0, 0, 10, "above_max")
    
    def test_material_property_validation(self, validator):
        """Test material property validation"""
        # Valid concrete properties
        valid_concrete = {
            'fc_prime': 28.0,
            'unit_weight': 24.0,
            'elastic_modulus': 24000.0
        }
        
        # Should not raise exceptions
        validator.validate_positive(valid_concrete['fc_prime'], "fc_prime")
        validator.validate_positive(valid_concrete['unit_weight'], "unit_weight")
        validator.validate_positive(valid_concrete['elastic_modulus'], "elastic_modulus")
        
        # Test realistic ranges
        validator.validate_range(valid_concrete['fc_prime'], 15, 80, "fc_prime")
        validator.validate_range(valid_concrete['unit_weight'], 20, 30, "unit_weight")
    
    def test_geometry_validation(self, validator):
        """Test geometry validation"""
        # Valid beam geometry
        width = 300.0
        height = 600.0
        span = 6000.0
        
        validator.validate_positive(width, "beam_width")
        validator.validate_positive(height, "beam_height")
        validator.validate_positive(span, "beam_span")
        
        # Check reasonable ratios
        span_to_depth_ratio = span / height
        validator.validate_range(span_to_depth_ratio, 5, 30, "span_to_depth_ratio")
    
    def test_load_validation(self, validator):
        """Test load validation"""
        # Valid loads
        dead_load = 5.0  # kN/m
        live_load = 8.0  # kN/m
        
        validator.validate_positive(dead_load, "dead_load")
        validator.validate_positive(live_load, "live_load")
        
        # Check reasonable load ranges for buildings
        validator.validate_range(dead_load, 1, 50, "dead_load")
        validator.validate_range(live_load, 1, 50, "live_load")


@pytest.mark.unit
@pytest.mark.utils
class TestValidationHelpers:
    """Test validation helper functions"""
    
    def test_validate_positive_function(self):
        """Test standalone validate_positive function"""
        # Valid cases
        assert validate_positive(10.0, "test") == 10.0
        assert validate_positive(0.1, "test") == 0.1
        
        # Invalid cases
        with pytest.raises(ValueError, match="test must be positive"):
            validate_positive(-1.0, "test")
        
        with pytest.raises(ValueError, match="test must be positive"):
            validate_positive(0.0, "test")
    
    def test_validate_range_function(self):
        """Test standalone validate_range function"""
        # Valid cases
        assert validate_range(5.0, 0, 10, "test") == 5.0
        assert validate_range(0.0, 0, 10, "test") == 0.0
        assert validate_range(10.0, 0, 10, "test") == 10.0
        
        # Invalid cases
        with pytest.raises(ValueError, match="test must be between"):
            validate_range(-1.0, 0, 10, "test")
        
        with pytest.raises(ValueError, match="test must be between"):
            validate_range(11.0, 0, 10, "test")
    
    def test_validation_with_none_values(self):
        """Test validation with None values"""
        with pytest.raises((ValueError, TypeError)):
            validate_positive(None, "test")
        
        with pytest.raises((ValueError, TypeError)):
            validate_range(None, 0, 10, "test")
    
    def test_validation_with_string_values(self):
        """Test validation with string values"""
        with pytest.raises((ValueError, TypeError)):
            validate_positive("not_a_number", "test")
        
        with pytest.raises((ValueError, TypeError)):
            validate_range("not_a_number", 0, 10, "test")


@pytest.mark.unit
@pytest.mark.utils
class TestMathUtilities:
    """Test mathematical utility functions"""
    
    def test_engineering_tolerance(self, engineering_tolerance):
        """Test engineering tolerance fixture"""
        assert engineering_tolerance == 0.01
        
        # Test usage in comparisons
        value1 = 100.0
        value2 = 100.005
        
        assert abs(value1 - value2) <= engineering_tolerance * value1
    
    def test_floating_point_comparisons(self, tolerance):
        """Test floating point comparison utilities"""
        # Test approximate equality
        a = 1.0 / 3.0
        b = 0.333333333
        
        # Should be approximately equal within tolerance
        assert abs(a - b) <= tolerance * 10  # Allow larger tolerance for this case
    
    def test_unit_conversions(self):
        """Test unit conversion utilities"""
        # Length conversions
        mm_to_m = 1000.0  # mm
        m_value = mm_to_m / 1000.0
        assert abs(m_value - 1.0) < 1e-6
        
        # Force conversions
        kn_to_n = 100.0  # kN
        n_value = kn_to_n * 1000.0
        assert abs(n_value - 100000.0) < 1e-6
        
        # Stress conversions
        mpa_to_pa = 28.0  # MPa
        pa_value = mpa_to_pa * 1e6
        assert abs(pa_value - 28000000.0) < 1e-6


@pytest.mark.integration
@pytest.mark.utils
class TestValidationIntegration:
    """Integration tests for validation utilities"""
    
    def test_validation_in_design_workflow(self):
        """Test validation integration in design workflow"""
        # Simulate a design workflow with validation
        
        # Step 1: Validate material properties
        fc_prime = 28.0
        fy = 420.0
        
        validate_positive(fc_prime, "concrete_strength")
        validate_range(fc_prime, 15, 80, "concrete_strength")
        
        validate_positive(fy, "steel_strength")
        validate_range(fy, 300, 600, "steel_strength")
        
        # Step 2: Validate geometry
        beam_width = 300.0
        beam_height = 600.0
        beam_span = 6000.0
        
        validate_positive(beam_width, "beam_width")
        validate_positive(beam_height, "beam_height")
        validate_positive(beam_span, "beam_span")
        
        # Check geometric constraints
        min_width = 200.0
        max_width = 1000.0
        validate_range(beam_width, min_width, max_width, "beam_width")
        
        # Step 3: Validate loads
        dead_load = 5.0
        live_load = 8.0
        
        validate_positive(dead_load, "dead_load")
        validate_positive(live_load, "live_load")
        
        # All validations should pass for reasonable values
        assert True  # If we reach here, all validations passed
    
    def test_validation_error_handling(self):
        """Test proper error handling in validation"""
        error_cases = [
            (lambda: validate_positive(-1.0, "negative"), "negative must be positive"),
            (lambda: validate_range(15.0, 0, 10, "out_of_range"), "out_of_range must be between"),
        ]
        
        for error_func, expected_message in error_cases:
            with pytest.raises(ValueError) as exc_info:
                error_func()
            assert expected_message in str(exc_info.value)
    
    def test_validation_performance(self, performance_monitor):
        """Test validation performance"""
        performance_monitor.start()
        
        # Run many validation operations
        for i in range(1000):
            validate_positive(10.0 + i * 0.1, "test_value")
            validate_range(5.0 + i * 0.001, 0, 1000, "test_range")
        
        execution_time = performance_monitor.stop()
        
        # Validation should be very fast
        assert execution_time < 0.1, f"Validation too slow: {execution_time:.3f}s"
        
        print(f"✅ Validation performance: {execution_time:.3f}s for 2000 operations")


@pytest.mark.utils
@pytest.mark.benchmark
@pytest.mark.slow
class TestUtilityPerformance:
    """Performance tests for utility functions"""
    
    def test_validation_benchmark(self, performance_monitor, performance_benchmark_data):
        """Benchmark validation operations"""
        
        # Test data
        test_values = [i * 0.1 + 1.0 for i in range(1000)]
        
        performance_monitor.start()
        
        # Benchmark positive validation
        for value in test_values:
            validate_positive(value, "benchmark_value")
        
        # Benchmark range validation
        for value in test_values:
            validate_range(value, 0, 200, "benchmark_range")
        
        execution_time = performance_monitor.stop()
        
        # Should be very fast
        max_time = 0.05  # 50ms for 2000 operations
        assert execution_time <= max_time, f"Validation benchmark too slow: {execution_time:.3f}s"
        
        print(f"✅ Validation benchmark: {execution_time:.3f}s for 2000 operations")
        print(f"✅ Average per operation: {execution_time/2000*1000:.2f}ms")
        
        return execution_time