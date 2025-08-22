"""
Tests for ACI 318M-25 Material Models
====================================

Comprehensive test suite for ACI concrete and steel materials.
"""

import pytest
import math
from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25Steel, ACI318M25ReinforcementSteel

@pytest.mark.aci
class TestACI318M25Concrete:
    """Test ACI 318M-25 concrete material"""
    
    def test_standard_strength_creation(self):
        """Test creation with standard strength classes"""
        concrete = ACI318M25Concrete(strength_class='FC28')
        
        assert concrete.fc_prime == 28.0
        assert concrete.strength_class == 'FC28'
        assert concrete.standard == "ACI 318M-25"
    
    def test_elastic_modulus_calculation(self):
        """Test elastic modulus calculation"""
        concrete = ACI318M25Concrete(fc_prime=28.0)
        
        expected_ec = 4700 * math.sqrt(28.0)
        actual_ec = concrete.elastic_modulus()
        
        assert abs(actual_ec - expected_ec) < 1.0
    
    def test_beta1_factor(self):
        """Test β₁ factor calculation"""
        # Test fc' ≤ 28 MPa
        concrete1 = ACI318M25Concrete(fc_prime=21.0)
        assert concrete1.beta1() == 0.85
        
        # Test 28 < fc' ≤ 55 MPa
        concrete2 = ACI318M25Concrete(fc_prime=35.0)
        expected_beta1 = 0.85 - 0.05 * (35.0 - 28.0) / 7.0
        assert abs(concrete2.beta1() - expected_beta1) < 0.001
        
        # Test fc' > 55 MPa
        concrete3 = ACI318M25Concrete(fc_prime=70.0)
        assert concrete3.beta1() == 0.65

@pytest.mark.aci  
class TestACI318M25Steel:
    """Test ACI 318M-25 steel material"""
    
    def test_grade_creation(self):
        """Test creation with standard grades"""
        steel = ACI318M25Steel(grade='GRADE420')
        
        assert steel.fy == 420.0
        assert steel.fu == 620.0
        assert steel.grade == 'GRADE420'
    
    def test_elastic_modulus(self):
        """Test elastic modulus"""
        steel = ACI318M25Steel(grade='GRADE420')
        assert steel.elastic_modulus() == 200000.0

@pytest.mark.aci
class TestACI318M25ReinforcementSteel:
    """Test ACI reinforcement steel"""
    
    def test_bar_properties(self):
        """Test bar area and diameter"""
        rebar = ACI318M25ReinforcementSteel('20M', 'GRADE420')
        
        assert rebar.bar_area() == 300  # mm²
        assert rebar.bar_diameter() == 19.5  # mm
        assert rebar.fy == 420.0
    
    def test_area_per_meter(self):
        """Test area per meter calculation"""
        rebar = ACI318M25ReinforcementSteel('20M', 'GRADE420')
        
        # 20M @ 200mm spacing
        area_per_m = rebar.calculate_area_per_meter(200.0)
        expected = 300 * 1000 / 200  # 1500 mm²/m
        
        assert abs(area_per_m - expected) < 1.0