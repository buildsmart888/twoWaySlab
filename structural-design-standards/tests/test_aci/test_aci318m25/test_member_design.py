"""
Tests for ACI 318M-25 Member Design and Load Combinations
=========================================================

Comprehensive test suite for beam design, column design, and load combinations
according to ACI 318M-25.

การทดสอบสำหรับการออกแบบส่วนประกอบตาม ACI 318M-25
"""

import pytest
import math
from typing import Dict, Any

from structural_standards.aci.aci318m25 import (
    ACI318M25Concrete,
    ACI318M25ReinforcementSteel,
    ACI318M25BeamDesign,
    ACI318M25ColumnDesign,
    ACI318M25LoadCombinations,
    BeamGeometry,
    BeamLoads,
    ColumnGeometry,
    ColumnLoads,
    LoadType,
    CombinationType
)


class TestACI318M25BeamDesign:
    """Test suite for ACI 318M-25 beam design"""
    
    @pytest.fixture
    def concrete(self):
        """Standard concrete material"""
        return ACI318M25Concrete(fc_prime=28.0)  # 28 MPa
    
    @pytest.fixture
    def reinforcement(self):
        """Standard reinforcement steel"""
        return ACI318M25ReinforcementSteel(fy=420.0, bar_designation="DB20")
    
    @pytest.fixture
    def beam_designer(self, concrete, reinforcement):
        """Beam designer instance"""
        return ACI318M25BeamDesign(concrete, reinforcement)
    
    @pytest.fixture
    def standard_geometry(self):
        """Standard beam geometry"""
        return BeamGeometry(
            width=300.0,      # mm
            height=500.0,     # mm
            effective_depth=450.0,  # mm
            span_length=6000.0     # mm
        )
    
    def test_flexural_design_basic(self, beam_designer, standard_geometry):
        """Test basic flexural reinforcement design"""
        # Design for moderate moment
        result = beam_designer.design_flexural_reinforcement(
            geometry=standard_geometry,
            moment_ultimate=100.0  # kN⋅m
        )
        
        assert result.is_adequate
        assert result.design_details['As_required_mm2'] > 0
        assert result.design_details['reinforcement_ratio'] > 0.001  # Above minimum
        assert result.design_details['section_type'] == "tension-controlled"
        assert result.capacity_ratio >= 1.0
    
    def test_flexural_design_high_moment(self, beam_designer, standard_geometry):
        """Test flexural design with high moment"""
        # Design for high moment
        result = beam_designer.design_flexural_reinforcement(
            geometry=standard_geometry,
            moment_ultimate=300.0  # kN⋅m (high moment)
        )
        
        # Should still be feasible but with higher reinforcement
        assert result.is_adequate
        assert result.design_details['As_required_mm2'] > 1000  # Significant steel area
        
        # Check that it doesn't exceed maximum reinforcement ratio
        rho_max = beam_designer.maximum_flexural_reinforcement_ratio()
        assert result.design_details['reinforcement_ratio'] <= rho_max
    
    def test_minimum_reinforcement_control(self, beam_designer, standard_geometry):
        """Test that minimum reinforcement controls for low moments"""
        # Very low moment
        result = beam_designer.design_flexural_reinforcement(
            geometry=standard_geometry,
            moment_ultimate=10.0  # kN⋅m (very low)
        )
        
        assert result.is_adequate
        
        # Should be controlled by minimum reinforcement
        rho_min = beam_designer.minimum_flexural_reinforcement_ratio(
            standard_geometry.width, standard_geometry.effective_depth
        )
        expected_As_min = rho_min * standard_geometry.width * standard_geometry.effective_depth
        
        assert result.design_details['As_required_mm2'] >= expected_As_min * 0.95  # Allow small tolerance
    
    def test_shear_design(self, beam_designer, standard_geometry):
        """Test shear reinforcement design"""
        # Design for moderate shear
        result = beam_designer.design_shear_reinforcement(
            geometry=standard_geometry,
            shear_ultimate=100.0,  # kN
            longitudinal_steel=1500.0  # mm²
        )
        
        assert result.is_adequate
        assert result.design_details['shear_capacity_kN'] >= 100.0
        assert result.design_details['stirrup_spacing_mm'] > 0
        assert result.design_details['stirrup_area_mm2'] > 0
    
    def test_shear_design_high_shear(self, beam_designer, standard_geometry):
        """Test shear design with high shear force"""
        # High shear force
        result = beam_designer.design_shear_reinforcement(
            geometry=standard_geometry,
            shear_ultimate=200.0,  # kN (high shear)
            longitudinal_steel=2000.0  # mm²
        )
        
        assert result.is_adequate
        assert result.design_details['shear_reinforcement_required']
        assert result.design_details['stirrup_spacing_mm'] <= standard_geometry.effective_depth / 2
    
    def test_deflection_check(self, beam_designer, standard_geometry):
        """Test deflection calculations"""
        from structural_standards.aci.aci318m25.members.beam_design import BeamType, BeamReinforcement
        
        loads = BeamLoads(
            dead_load=10.0,  # kN/m
            live_load=8.0    # kN/m
        )
        
        reinforcement = BeamReinforcement(
            tension_bars=["DB20", "DB20", "DB20"]  # 3 bars
        )
        
        result = beam_designer.check_deflection(
            geometry=standard_geometry,
            loads=loads,
            reinforcement=reinforcement,
            beam_type=BeamType.SIMPLY_SUPPORTED
        )
        
        assert 'immediate_deflection_mm' in result.design_details
        assert 'longterm_deflection_mm' in result.design_details
        assert result.design_details['immediate_deflection_mm'] > 0
        assert result.design_details['longterm_deflection_mm'] >= result.design_details['immediate_deflection_mm']
    
    def test_material_validation(self):
        """Test validation of material inputs"""
        # Invalid concrete strength
        with pytest.raises(ValueError):
            ACI318M25Concrete(fc_prime=-10.0)
        
        # Invalid steel yield strength
        with pytest.raises(ValueError):
            ACI318M25ReinforcementSteel(fy=-400.0, bar_designation="DB20")


class TestACI318M25ColumnDesign:
    """Test suite for ACI 318M-25 column design"""
    
    @pytest.fixture
    def concrete(self):
        """Standard concrete material"""
        return ACI318M25Concrete(fc_prime=28.0)  # 28 MPa
    
    @pytest.fixture
    def reinforcement(self):
        """Standard reinforcement steel"""
        return ACI318M25ReinforcementSteel(fy=420.0, bar_designation="DB25")
    
    @pytest.fixture
    def column_designer(self, concrete, reinforcement):
        """Column designer instance"""
        return ACI318M25ColumnDesign(concrete, reinforcement)
    
    @pytest.fixture
    def standard_geometry(self):
        """Standard column geometry"""
        return ColumnGeometry(
            width=400.0,   # mm
            depth=400.0,   # mm
            length=3000.0, # mm
            cross_section="rectangular"
        )
    
    @pytest.fixture
    def standard_loads(self):
        """Standard column loads"""
        return ColumnLoads(
            axial_dead=500.0,   # kN
            axial_live=300.0,   # kN
            moment_x_dead=50.0, # kN⋅m
            moment_x_live=30.0  # kN⋅m
        )
    
    def test_axial_design_basic(self, column_designer, standard_geometry, standard_loads):
        """Test basic axial reinforcement design"""
        result = column_designer.design_axial_reinforcement(
            geometry=standard_geometry,
            loads=standard_loads,
            reinforcement_ratio=0.02
        )
        
        assert result.is_adequate
        assert result.design_details['As_required_mm2'] > 0
        assert 0.01 <= result.design_details['reinforcement_ratio'] <= 0.08
        assert result.design_details['num_longitudinal_bars'] >= 4  # Minimum for rectangular
        assert result.capacity_ratio >= 1.0
    
    def test_high_axial_load(self, column_designer, standard_geometry):
        """Test design with high axial load"""
        high_loads = ColumnLoads(
            axial_dead=1000.0,  # kN (high load)
            axial_live=600.0    # kN
        )
        
        result = column_designer.design_axial_reinforcement(
            geometry=standard_geometry,
            loads=high_loads,
            reinforcement_ratio=0.04  # Higher reinforcement ratio
        )
        
        assert result.is_adequate
        assert result.design_details['reinforcement_ratio'] >= 0.03  # Should use higher ratio
    
    def test_tie_design(self, column_designer, standard_geometry):
        """Test tie reinforcement design"""
        result = column_designer.design_tie_reinforcement(
            geometry=standard_geometry,
            longitudinal_bars=8,
            bar_size="DB25"
        )
        
        assert result.is_adequate
        assert result.design_details['tie_diameter_mm'] >= 10  # Minimum tie size
        assert result.design_details['tie_spacing_mm'] <= 300  # Maximum spacing
        assert result.design_details['tie_spacing_mm'] <= 16 * 25  # 16db limit
    
    def test_biaxial_bending(self, column_designer, standard_geometry):
        """Test biaxial bending check"""
        from structural_standards.aci.aci318m25.members.column_design import ColumnReinforcement
        
        biaxial_loads = ColumnLoads(
            axial_dead=400.0,
            axial_live=200.0,
            moment_x_dead=60.0,
            moment_x_live=40.0,
            moment_y_dead=30.0,
            moment_y_live=20.0
        )
        
        reinforcement = ColumnReinforcement(
            longitudinal_bars=["DB25"] * 8  # 8 bars
        )
        
        result = column_designer.check_biaxial_bending(
            geometry=standard_geometry,
            reinforcement=reinforcement,
            loads=biaxial_loads
        )
        
        assert 'interaction_ratio' in result.design_details
        assert result.design_details['interaction_ratio'] > 0
    
    def test_slenderness_classification(self, column_designer):
        """Test column slenderness classification"""
        from structural_standards.aci.aci318m25.members.column_design import ColumnType
        
        # Short column
        short_geometry = ColumnGeometry(
            width=400.0, depth=400.0, length=1000.0  # Low slenderness
        )
        assert column_designer.classify_column_slenderness(short_geometry) == ColumnType.SHORT
        
        # Slender column
        slender_geometry = ColumnGeometry(
            width=300.0, depth=300.0, length=8000.0  # High slenderness
        )
        column_type = column_designer.classify_column_slenderness(slender_geometry)
        assert column_type in [ColumnType.INTERMEDIATE, ColumnType.SLENDER]
    
    def test_circular_column(self, column_designer, reinforcement):
        """Test circular column design"""
        circular_geometry = ColumnGeometry(
            width=450.0,  # diameter
            depth=450.0,  # same as width for circular
            length=3000.0,
            cross_section="circular"
        )
        
        loads = ColumnLoads(axial_dead=600.0, axial_live=400.0)
        
        result = column_designer.design_axial_reinforcement(
            geometry=circular_geometry,
            loads=loads,
            reinforcement_ratio=0.02
        )
        
        assert result.is_adequate
        assert result.design_details['num_longitudinal_bars'] >= 6  # Minimum for circular


class TestACI318M25LoadCombinations:
    """Test suite for ACI 318M-25 load combinations"""
    
    @pytest.fixture
    def load_combos(self):
        """Load combinations instance"""
        return ACI318M25LoadCombinations()
    
    @pytest.fixture
    def sample_loads(self):
        """Sample load values"""
        return {
            LoadType.DEAD: 10.0,    # kN/m²
            LoadType.LIVE: 5.0,     # kN/m²
            LoadType.WIND: 3.0,     # kN/m²
            LoadType.SNOW: 2.0      # kN/m²
        }
    
    def test_strength_combinations(self, load_combos, sample_loads):
        """Test strength design load combinations"""
        combinations = load_combos.get_strength_combinations()
        
        assert len(combinations) >= 7  # Should have all ASCE 7 combinations
        
        # Test specific combinations
        combo_1_4D = next((c for c in combinations if c.name == "1.4D"), None)
        assert combo_1_4D is not None
        assert combo_1_4D.calculate_load_effect(sample_loads) == 1.4 * 10.0
        
        combo_basic = next((c for c in combinations if "1.2D + 1.6L" in c.name), None)
        assert combo_basic is not None
        effect = combo_basic.calculate_load_effect(sample_loads)
        expected = 1.2 * 10.0 + 1.6 * 5.0  # 1.2D + 1.6L portion
        assert abs(effect - expected) <= 1.0  # Allow for other load terms
    
    def test_service_combinations(self, load_combos, sample_loads):
        """Test service load combinations"""
        combinations = load_combos.get_service_combinations()
        
        assert len(combinations) >= 5  # Should have service and deflection combinations
        
        # Test service combination
        combo_DL = next((c for c in combinations if c.name == "D + L"), None)
        assert combo_DL is not None
        assert combo_DL.calculate_load_effect(sample_loads) == 10.0 + 5.0
    
    def test_critical_combination(self, load_combos, sample_loads):
        """Test finding critical load combination"""
        critical_combo, max_effect = load_combos.find_critical_combination(
            sample_loads, CombinationType.STRENGTH
        )
        
        assert critical_combo is not None
        assert max_effect > 0
        
        # Critical should be higher than basic D+L
        basic_effect = 1.0 * sample_loads[LoadType.DEAD] + 1.0 * sample_loads[LoadType.LIVE]
        assert max_effect > basic_effect
    
    def test_phi_factors(self, load_combos):
        """Test strength reduction factors"""
        # Test standard phi factors
        assert load_combos.get_strength_reduction_factor('flexure_tension_controlled') == 0.90
        assert load_combos.get_strength_reduction_factor('shear_and_torsion') == 0.75
        assert load_combos.get_strength_reduction_factor('compression_axial_ties') == 0.65
        
        # Test invalid phi factor
        with pytest.raises(ValueError):
            load_combos.get_strength_reduction_factor('invalid_mode')
    
    def test_transition_phi_factor(self, load_combos):
        """Test phi factor in transition zone"""
        # Tension-controlled (high strain)
        phi_tension = load_combos.get_transition_phi_factor(0.006, "ties")
        assert phi_tension == 0.90
        
        # Compression-controlled (low strain)
        phi_compression = load_combos.get_transition_phi_factor(0.001, "ties")
        assert phi_compression == 0.65
        
        # Transition zone
        phi_transition = load_combos.get_transition_phi_factor(0.003, "ties")
        assert 0.65 < phi_transition < 0.90
        
        # Spiral columns should have higher phi
        phi_spiral = load_combos.get_transition_phi_factor(0.001, "spiral")
        assert phi_spiral == 0.75
    
    def test_custom_combination(self, load_combos):
        """Test creating custom load combinations"""
        custom_combo = load_combos.create_custom_combination(
            name="1.0D + 1.5L",
            factors={LoadType.DEAD: 1.0, LoadType.LIVE: 1.5},
            combination_type=CombinationType.STRENGTH,
            description="Custom combination"
        )
        
        assert custom_combo.name == "1.0D + 1.5L"
        assert custom_combo.factors[LoadType.DEAD] == 1.0
        assert custom_combo.factors[LoadType.LIVE] == 1.5
        
        # Test calculation
        loads = {LoadType.DEAD: 10.0, LoadType.LIVE: 5.0}
        effect = custom_combo.calculate_load_effect(loads)
        assert effect == 1.0 * 10.0 + 1.5 * 5.0
    
    def test_load_validation(self, load_combos):
        """Test load validation"""
        # Valid loads
        valid_loads = {LoadType.DEAD: 10.0, LoadType.LIVE: 5.0}
        assert load_combos.validate_loads(valid_loads)
        
        # Invalid loads (negative)
        invalid_loads = {LoadType.DEAD: -10.0, LoadType.LIVE: 5.0}
        assert not load_combos.validate_loads(invalid_loads)
    
    def test_combination_equations(self, load_combos):
        """Test load combination equation strings"""
        combinations = load_combos.get_strength_combinations()
        
        # Find 1.4D combination
        combo_1_4D = next((c for c in combinations if c.name == "1.4D"), None)
        assert combo_1_4D is not None
        equation = combo_1_4D.get_equation()
        assert "1.4dead" in equation.lower() or "dead" in equation
    
    def test_export_combinations(self, load_combos):
        """Test exporting combinations to dictionary"""
        export_data = load_combos.export_combinations_to_dict()
        
        assert 'strength_combinations' in export_data
        assert 'service_combinations' in export_data
        assert 'phi_factors' in export_data
        
        # Check that we have reasonable number of combinations
        assert len(export_data['strength_combinations']) >= 7
        assert len(export_data['service_combinations']) >= 5
        
        # Check phi factors
        assert 'flexure_tension_controlled' in export_data['phi_factors']
        assert export_data['phi_factors']['flexure_tension_controlled'] == 0.90


# Integration tests
class TestACI318M25Integration:
    """Integration tests combining multiple modules"""
    
    def test_complete_beam_design_workflow(self):
        """Test complete beam design workflow"""
        # Create materials
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(fy=420.0, bar_designation="DB20")
        
        # Create designers
        beam_designer = ACI318M25BeamDesign(concrete, steel)
        load_combos = ACI318M25LoadCombinations()
        
        # Define geometry
        geometry = BeamGeometry(
            width=300.0,
            height=500.0,
            effective_depth=450.0,
            span_length=6000.0
        )
        
        # Define service loads
        service_loads = {
            LoadType.DEAD: 8.0,   # kN/m
            LoadType.LIVE: 6.0    # kN/m
        }
        
        # Calculate factored loads
        critical_combo, factored_load = load_combos.find_critical_combination(
            service_loads, CombinationType.STRENGTH
        )
        
        # Calculate factored moment (simple beam)
        factored_moment = factored_load * (geometry.span_length/1000)**2 / 8  # kN⋅m
        
        # Design reinforcement
        flexural_result = beam_designer.design_flexural_reinforcement(
            geometry=geometry,
            moment_ultimate=factored_moment
        )
        
        assert flexural_result.is_adequate
        assert flexural_result.design_details['As_required_mm2'] > 0
        
        # Design shear reinforcement
        factored_shear = factored_load * geometry.span_length / 1000 / 2  # kN
        shear_result = beam_designer.design_shear_reinforcement(
            geometry=geometry,
            shear_ultimate=factored_shear,
            longitudinal_steel=flexural_result.design_details['As_required_mm2']
        )
        
        assert shear_result.is_adequate
    
    def test_complete_column_design_workflow(self):
        """Test complete column design workflow"""
        # Create materials
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(fy=420.0, bar_designation="DB25")
        
        # Create designers
        column_designer = ACI318M25ColumnDesign(concrete, steel)
        load_combos = ACI318M25LoadCombinations()
        
        # Define geometry
        geometry = ColumnGeometry(
            width=400.0,
            depth=400.0,
            length=3000.0,
            cross_section="rectangular"
        )
        
        # Define service loads
        service_loads = {
            LoadType.DEAD: 400.0,   # kN
            LoadType.LIVE: 250.0    # kN
        }
        
        # Calculate factored loads
        critical_combo, factored_axial = load_combos.find_critical_combination(
            service_loads, CombinationType.STRENGTH
        )
        
        # Create column loads
        column_loads = ColumnLoads(
            axial_dead=service_loads[LoadType.DEAD],
            axial_live=service_loads[LoadType.LIVE],
            moment_x_dead=40.0,  # kN⋅m
            moment_x_live=25.0   # kN⋅m
        )
        
        # Design reinforcement
        axial_result = column_designer.design_axial_reinforcement(
            geometry=geometry,
            loads=column_loads,
            reinforcement_ratio=0.02
        )
        
        assert axial_result.is_adequate
        assert axial_result.design_details['num_longitudinal_bars'] >= 4
        
        # Design ties
        tie_result = column_designer.design_tie_reinforcement(
            geometry=geometry,
            longitudinal_bars=axial_result.design_details['num_longitudinal_bars'],
            bar_size="DB25"
        )
        
        assert tie_result.is_adequate


if __name__ == "__main__":
    # Run tests if file is executed directly
    pytest.main([__file__, "-v", "--tb=short"])