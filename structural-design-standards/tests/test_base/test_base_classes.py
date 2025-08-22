"""
Tests for Base Classes
======================

Test suite for abstract base classes and interfaces.
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.base.standard_interface import (
    StructuralStandard, StandardInfo, LoadType, MemberType, DesignMethod
)
from structural_standards.base.material_base import (
    ConcreteMaterial, SteelMaterial, ReinforcementSteel, MaterialDatabase,
    MaterialType, ConcreteType, SteelType
)
from structural_standards.base.design_base import (
    DesignResult, DesignCheck, DesignStatus, FailureMode,
    BeamDesign, ColumnDesign, SlabDesign
)

# Concrete implementation for testing abstract classes
class TestConcreteMaterial(ConcreteMaterial):
    """Test implementation of ConcreteMaterial"""
    
    def elastic_modulus(self) -> float:
        """ACI 318M-25 formula: Ec = 4700√f'c"""
        return 4700 * math.sqrt(self.fc_prime)
    
    def modulus_of_rupture(self) -> float:
        """ACI 318M-25 formula: fr = 0.62√f'c"""
        return 0.62 * math.sqrt(self.fc_prime)

class TestSteelMaterial(SteelMaterial):
    """Test implementation of SteelMaterial"""
    pass

class TestReinforcementSteel(ReinforcementSteel):
    """Test implementation of ReinforcementSteel"""
    
    def bar_area(self) -> float:
        """Get area based on designation"""
        areas = {
            'DB10': 78.5,    # mm²
            'DB12': 113.1,   # mm²
            'DB20': 314.2,   # mm²
            'DB25': 490.9,   # mm²
        }
        return areas.get(self.bar_designation, 0.0)
    
    def bar_diameter(self) -> float:
        """Get diameter based on designation"""
        diameters = {
            'DB10': 10.0,    # mm
            'DB12': 12.0,    # mm
            'DB20': 20.0,    # mm
            'DB25': 25.0,    # mm
        }
        return diameters.get(self.bar_designation, 0.0)

class TestStructuralStandard(StructuralStandard):
    """Test implementation of StructuralStandard"""
    
    def get_material_properties(self, material_type: str, grade: str):
        """Mock implementation"""
        if material_type == 'concrete' and grade == 'FC28':
            return {
                'fc_prime': 28.0,
                'elastic_modulus': 24847.0,
                'unit_weight': 24.0
            }
        return {}
    
    def get_safety_factors(self):
        """Mock implementation"""
        return {
            'concrete': 1.5,
            'steel': 1.15,
            'dead_load': 1.4,
            'live_load': 1.6
        }
    
    def get_load_combinations(self, loads):
        """Mock implementation"""
        return {
            'combination_1': 1.4 * loads.get(LoadType.DEAD, 0),
            'combination_2': 1.2 * loads.get(LoadType.DEAD, 0) + 1.6 * loads.get(LoadType.LIVE, 0)
        }
    
    def calculate_design_strength(self, nominal_strength, member_type, failure_mode):
        """Mock implementation"""
        phi_factors = {
            'flexure': 0.90,
            'shear': 0.75,
            'compression': 0.65
        }
        phi = phi_factors.get(failure_mode, 0.75)
        return phi * nominal_strength
    
    def check_serviceability(self, deflection, span, member_type):
        """Mock implementation"""
        limit = span * 1000 / 250  # L/250 in mm
        return {
            'deflection_check': deflection <= limit
        }

class TestBaseClasses:
    """Test suite for base classes"""
    
    def test_standard_info_creation(self):
        """Test StandardInfo dataclass creation"""
        info = StandardInfo(
            name="Test Standard",
            version="1.0",
            country="Test Country",
            language="en",
            organization="Test Org",
            year_published=2024,
            design_method=DesignMethod.LIMIT_STATE,
            units_system="SI"
        )
        
        assert info.name == "Test Standard"
        assert info.version == "1.0"
        assert info.design_method == DesignMethod.LIMIT_STATE
        assert info.units_system == "SI"
    
    def test_structural_standard_interface(self):
        """Test StructuralStandard abstract interface"""
        info = StandardInfo(
            name="Test Standard",
            version="1.0", 
            country="Test",
            language="en",
            organization="Test Org",
            year_published=2024,
            design_method=DesignMethod.LIMIT_STATE,
            units_system="SI"
        )
        
        standard = TestStructuralStandard(info)
        
        # Test basic properties
        assert standard.name == "Test Standard"
        assert standard.version == "1.0"
        assert standard.country == "Test"
        assert standard.language == "en"
        
        # Test abstract method implementations
        props = standard.get_material_properties('concrete', 'FC28')
        assert props['fc_prime'] == 28.0
        
        sf = standard.get_safety_factors()
        assert sf['concrete'] == 1.5
        
        # Test load combinations
        loads = {LoadType.DEAD: 10.0, LoadType.LIVE: 5.0}
        combinations = standard.get_load_combinations(loads)
        assert 'combination_1' in combinations
        
        # Test design strength calculation
        design_strength = standard.calculate_design_strength(100.0, MemberType.BEAM, 'flexure')
        assert design_strength == 90.0  # 0.9 * 100
        
        # Test serviceability check
        serviceability = standard.check_serviceability(10.0, 6.0, MemberType.BEAM)
        assert 'deflection_check' in serviceability
    
    def test_concrete_material_creation(self):
        """Test ConcreteMaterial creation and properties"""
        concrete = TestConcreteMaterial(
            fc_prime=28.0,
            unit_weight=24.0,
            concrete_type=ConcreteType.NORMAL_WEIGHT
        )
        
        assert concrete.fc_prime == 28.0
        assert concrete.unit_weight == 24.0
        assert concrete.concrete_type == ConcreteType.NORMAL_WEIGHT
        assert concrete.material_type == MaterialType.CONCRETE
        
        # Test calculated properties
        ec = concrete.elastic_modulus()
        expected_ec = 4700 * math.sqrt(28.0)
        assert abs(ec - expected_ec) < 0.1
        
        fr = concrete.modulus_of_rupture()
        expected_fr = 0.62 * math.sqrt(28.0)
        assert abs(fr - expected_fr) < 0.01
        
        # Test design properties
        props = concrete.get_design_properties()
        assert 'fc_prime' in props
        assert 'elastic_modulus' in props
        assert props['fc_prime'] == 28.0
        
        # Test utility methods
        assert not concrete.is_lightweight()
        assert not concrete.is_high_strength()
        
        density = concrete.density()
        assert abs(density - 2446.7) < 1.0  # kg/m³
    
    def test_concrete_material_validation(self):
        """Test ConcreteMaterial input validation"""
        # Test invalid inputs
        with pytest.raises(ValueError):
            TestConcreteMaterial(fc_prime=-10.0)  # Negative strength
        
        with pytest.raises(ValueError):
            TestConcreteMaterial(fc_prime=28.0, unit_weight=0)  # Zero weight
        
        with pytest.raises(ValueError):
            TestConcreteMaterial(fc_prime=28.0, aggregate_size=-5.0)  # Negative size
    
    def test_steel_material_creation(self):
        """Test SteelMaterial creation and properties"""
        steel = TestSteelMaterial(
            fy=420.0,
            fu=620.0,
            steel_type=SteelType.HIGH_STRENGTH
        )
        
        assert steel.fy == 420.0
        assert steel.fu == 620.0
        assert steel.steel_type == SteelType.HIGH_STRENGTH
        assert steel.material_type == MaterialType.STEEL
        
        # Test design properties
        props = steel.get_design_properties()
        assert props['fy'] == 420.0
        assert props['fu'] == 620.0
        assert 'elastic_modulus' in props
        
        # Test utility methods
        assert steel.is_high_strength()
        
        ductility = steel.ductility_ratio()
        expected_ductility = 620.0 / 420.0
        assert abs(ductility - expected_ductility) < 0.01
    
    def test_steel_material_validation(self):
        """Test SteelMaterial input validation"""
        # Test invalid inputs
        with pytest.raises(ValueError):
            TestSteelMaterial(fy=-100.0)  # Negative yield strength
        
        with pytest.raises(ValueError):
            TestSteelMaterial(fy=420.0, fu=300.0)  # fu < fy
    
    def test_reinforcement_steel_creation(self):
        """Test ReinforcementSteel creation and properties"""
        rebar = TestReinforcementSteel(
            fy=390.0,
            bar_designation="DB20",
            surface_condition="deformed"
        )
        
        assert rebar.fy == 390.0
        assert rebar.bar_designation == "DB20"
        assert rebar.surface_condition == "deformed"
        assert rebar.material_type == MaterialType.REINFORCEMENT
        
        # Test bar properties
        area = rebar.bar_area()
        assert abs(area - 314.2) < 0.1  # mm²
        
        diameter = rebar.bar_diameter()
        assert abs(diameter - 20.0) < 0.1  # mm
        
        perimeter = rebar.bar_perimeter()
        expected_perimeter = math.pi * 20.0
        assert abs(perimeter - expected_perimeter) < 0.1
        
        # Test development length factor
        dev_factor = rebar.development_length_factor()
        assert dev_factor == 1.0  # For deformed bars
    
    def test_material_database(self):
        """Test MaterialDatabase functionality"""
        db = MaterialDatabase("Test Standard")
        
        # Create test materials
        concrete = TestConcreteMaterial(fc_prime=28.0)
        steel = TestSteelMaterial(fy=420.0)
        rebar = TestReinforcementSteel(fy=390.0, bar_designation="DB20")
        
        # Add materials to database
        db.add_concrete("FC28", concrete)
        db.add_steel("FY420", steel)
        db.add_reinforcement("DB20", rebar)
        
        # Test retrieval
        retrieved_concrete = db.get_concrete("FC28")
        assert retrieved_concrete.fc_prime == 28.0
        
        retrieved_steel = db.get_steel("FY420")
        assert retrieved_steel.fy == 420.0
        
        retrieved_rebar = db.get_reinforcement("DB20")
        assert retrieved_rebar.bar_designation == "DB20"
        
        # Test listing
        concrete_grades = db.list_concrete_grades()
        assert "FC28" in concrete_grades
        
        steel_grades = db.list_steel_grades()
        assert "FY420" in steel_grades
        
        rebar_designations = db.list_reinforcement_designations()
        assert "DB20" in rebar_designations
        
        # Test error handling
        with pytest.raises(ValueError):
            db.get_concrete("INVALID")
    
    def test_design_check_creation(self):
        """Test DesignCheck creation"""
        check = DesignCheck(
            name="Flexural Capacity",
            status=DesignStatus.PASS,
            value=90.0,
            limit=100.0,
            ratio=0.90,
            units="kN⋅m",
            description="Check flexural capacity",
            code_reference="ACI 318M-25 9.3"
        )
        
        assert check.name == "Flexural Capacity"
        assert check.status == DesignStatus.PASS
        assert check.value == 90.0
        assert check.ratio == 0.90
    
    def test_design_result_creation(self):
        """Test DesignResult creation and methods"""
        result = DesignResult(
            member_type="beam",
            design_method="ACI 318M-25",
            overall_status=DesignStatus.PASS,
            utilization_ratio=0.85
        )
        
        # Add design checks
        strength_check = DesignCheck(
            name="Flexure", status=DesignStatus.PASS,
            value=90.0, limit=100.0, ratio=0.90, units="kN⋅m"
        )
        
        serviceability_check = DesignCheck(
            name="Deflection", status=DesignStatus.PASS,
            value=15.0, limit=20.0, ratio=0.75, units="mm"
        )
        
        result.add_strength_check(strength_check)
        result.add_serviceability_check(serviceability_check)
        
        # Test methods
        assert len(result.strength_checks) == 1
        assert len(result.serviceability_checks) == 1
        
        critical_ratio = result.get_critical_ratio()
        assert critical_ratio == 0.90
        
        governing_check = result.get_governing_check()
        assert governing_check.name == "Flexure"
        
        assert result.is_adequate()

@pytest.mark.unit
class TestValidationIntegration:
    """Integration tests between base classes and validation"""
    
    def test_material_grade_validation(self):
        """Test material grade validation through base classes"""
        concrete = TestConcreteMaterial(fc_prime=28.0)
        
        # Test valid grade
        assert concrete.validate_grade("FC28")
        
        # Test invalid grade  
        assert not concrete.validate_grade("INVALID")
        
        # Test edge cases
        assert not concrete.validate_grade("")
        assert not concrete.validate_grade("FC999")  # Too high