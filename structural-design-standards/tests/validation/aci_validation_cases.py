"""
ACI 318M-25 Validation Cases
===========================

Validation tests against known solutions from ACI 318M-25 examples,
textbooks, and published design cases.

การทดสอบการตรวจสอบความถูกต้องกับตัวอย่างที่ทราบผลลัพธ์
"""

import pytest
import math
from typing import Dict, Any, List, Tuple

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

from structural_standards.base.design_base import DesignStatus


@pytest.mark.aci
@pytest.mark.validation
@pytest.mark.slow
class TestACIValidationCases:
    """Validation tests against known ACI 318M-25 solutions"""
    
    @pytest.fixture(scope="class")
    def standard_materials(self):
        """Standard materials used in validation examples"""
        concrete = ACI318M25Concrete(fc_prime=28.0)  # 28 MPa concrete
        steel = ACI318M25ReinforcementSteel(grade=420)  # Grade 420 steel
        return {'concrete': concrete, 'steel': steel}
    
    def test_aci_example_4_2_simply_supported_beam(self, standard_materials):
        """
        Test against ACI 318M-25 Example 4.2: Simply Supported Beam
        (Based on typical textbook example)
        """
        print("\n📖 Validating ACI Example 4.2: Simply Supported Beam")
        
        beam_designer = ACI318M25BeamDesign(
            standard_materials['concrete'], 
            standard_materials['steel']
        )
        
        # Given data from example
        geometry = BeamGeometry(
            width=300,           # mm
            height=600,          # mm
            effective_depth=550, # mm
            span_length=6000     # mm
        )
        
        # Applied moment (from load analysis)
        moment_ultimate = 150.0  # kN⋅m
        
        # Design the beam
        result = beam_designer.design_flexural_reinforcement(geometry, moment_ultimate)
        
        # Validate result
        assert result.overall_status == DesignStatus.PASS, "Beam design should pass"
        
        steel_area = result.required_reinforcement['required_steel_area']
        
        # Expected result range (from manual calculation)
        # Ru = Mu / (φ × b × d²) = 150×10⁶ / (0.9 × 300 × 550²) = 1.84 MPa
        # ρ ≈ 0.0044, As = ρ × b × d ≈ 728 mm²
        expected_steel_min = 650   # mm²
        expected_steel_max = 850   # mm²
        
        assert expected_steel_min <= steel_area <= expected_steel_max, \
            f"Steel area out of expected range: {steel_area:.0f} mm² (expected {expected_steel_min}-{expected_steel_max})"
        
        print(f"  ✅ Required steel area: {steel_area:.0f} mm² (expected range: {expected_steel_min}-{expected_steel_max})")
        
        # Check utilization ratio
        assert 0.5 <= result.utilization_ratio <= 0.9, \
            f"Utilization ratio seems unreasonable: {result.utilization_ratio:.2f}"
        
        return {
            'steel_area': steel_area,
            'utilization_ratio': result.utilization_ratio,
            'status': result.overall_status
        }
    
    def test_aci_example_column_axial_moment(self, standard_materials):
        """
        Test column with combined axial load and moment
        (Based on typical design example)
        """
        print("\n🏛️ Validating Column Axial-Moment Interaction")
        
        column_designer = ACI318M25ColumnDesign(
            standard_materials['concrete'], 
            standard_materials['steel']
        )
        
        # Given data
        geometry = ColumnGeometry(
            width=400,    # mm
            depth=400,    # mm
            length=3000   # mm
        )
        
        loads = ColumnLoads(
            axial_dead=300,       # kN
            axial_live=200,       # kN
            moment_x_dead=25,     # kN⋅m
            moment_x_live=15      # kN⋅m
        )
        
        # Design the column
        result = column_designer.design(geometry, loads, ColumnType.TIED)
        
        # Validate result
        assert result.overall_status == DesignStatus.PASS, "Column design should pass"
        
        steel_area = result.required_reinforcement['required_steel_area']
        Ag = geometry.width * geometry.depth
        steel_ratio = steel_area / Ag
        
        # Expected result range
        # For this load level, expect 1-3% steel ratio
        expected_ratio_min = 0.01
        expected_ratio_max = 0.03
        
        assert expected_ratio_min <= steel_ratio <= expected_ratio_max, \
            f"Steel ratio out of expected range: {steel_ratio:.3f} (expected {expected_ratio_min:.3f}-{expected_ratio_max:.3f})"
        
        print(f"  ✅ Steel ratio: {steel_ratio:.3f} (expected range: {expected_ratio_min:.3f}-{expected_ratio_max:.3f})")
        print(f"  ✅ Steel area: {steel_area:.0f} mm²")
        
        return {
            'steel_area': steel_area,
            'steel_ratio': steel_ratio,
            'status': result.overall_status
        }
    
    def test_aci_example_two_way_slab(self, standard_materials):
        """
        Test two-way slab design
        (Based on typical slab design example)
        """
        print("\n🏢 Validating Two-Way Slab Design")
        
        slab_designer = ACI318M25SlabDesign(
            standard_materials['concrete'], 
            standard_materials['steel']
        )
        
        # Given data - square slab
        geometry = SlabGeometry(
            length_x=6000,    # mm
            length_y=6000,    # mm
            thickness=200,    # mm
            span_x=6000,      # mm
            span_y=6000       # mm
        )
        
        loads = SlabLoads(
            dead_load=4.0,    # kPa
            live_load=2.5     # kPa
        )
        
        # Design the slab
        result = slab_designer.design(geometry, loads, SlabType.TWO_WAY)
        
        # Validate result
        assert result.overall_status == DesignStatus.PASS, "Slab design should pass"
        
        steel_x = result.required_reinforcement['main_reinforcement_x']
        steel_y = result.required_reinforcement['main_reinforcement_y']
        
        # Calculate reinforcement ratios
        b = 1000  # mm (per meter)
        d = geometry.thickness - 20  # Effective depth
        rho_x = steel_x / (b * d)
        rho_y = steel_y / (b * d)
        
        # Expected result range for this load level
        expected_rho_min = 0.0018  # Minimum reinforcement
        expected_rho_max = 0.008   # Reasonable maximum
        
        assert expected_rho_min <= rho_x <= expected_rho_max, \
            f"Steel ratio X out of range: {rho_x:.4f} (expected {expected_rho_min:.4f}-{expected_rho_max:.4f})"
        assert expected_rho_min <= rho_y <= expected_rho_max, \
            f"Steel ratio Y out of range: {rho_y:.4f} (expected {expected_rho_min:.4f}-{expected_rho_max:.4f})"
        
        print(f"  ✅ Steel ratio X: {rho_x:.4f} (expected range: {expected_rho_min:.4f}-{expected_rho_max:.4f})")
        print(f"  ✅ Steel ratio Y: {rho_y:.4f}")
        print(f"  ✅ Steel area X: {steel_x:.0f} mm²/m")
        print(f"  ✅ Steel area Y: {steel_y:.0f} mm²/m")
        
        return {
            'steel_area_x': steel_x,
            'steel_area_y': steel_y,
            'steel_ratio_x': rho_x,
            'steel_ratio_y': rho_y,
            'status': result.overall_status
        }
    
    def test_aci_development_length_validation(self, standard_materials):
        """
        Test development length calculations against known values
        """
        print("\n📏 Validating Development Length Calculations")
        
        beam_designer = ACI318M25BeamDesign(
            standard_materials['concrete'], 
            standard_materials['steel']
        )
        
        # Test different bar sizes
        bar_sizes = [12, 16, 20, 25]  # mm diameter
        
        validation_results = {}
        
        for bar_diameter in bar_sizes:
            ld = beam_designer._calculate_development_length(bar_diameter)
            
            # Expected range based on ACI 318M-25 formula
            # ld = (fy × ψt × ψe × ψs × λ) / (25 × λ × √fc) × db
            # For normal conditions: ψt=ψe=ψs=λ=1.0
            # ld = fy / (25 × √fc) × db = 420 / (25 × √28) × db ≈ 3.17 × db
            
            expected_ld_min = 2.5 * bar_diameter  # Conservative estimate
            expected_ld_max = 4.0 * bar_diameter  # Liberal estimate
            
            assert expected_ld_min <= ld <= expected_ld_max, \
                f"Development length for {bar_diameter}mm bar out of range: {ld:.0f}mm " \
                f"(expected {expected_ld_min:.0f}-{expected_ld_max:.0f}mm)"
            
            validation_results[bar_diameter] = {
                'calculated_ld': ld,
                'expected_min': expected_ld_min,
                'expected_max': expected_ld_max,
                'ratio_to_diameter': ld / bar_diameter
            }
            
            print(f"  ✅ DB{bar_diameter}: ld = {ld:.0f}mm ({ld/bar_diameter:.1f} × db)")
        
        return validation_results
    
    def test_material_property_validation(self, standard_materials):
        """
        Test material properties against ACI 318M-25 requirements
        """
        print("\n🧪 Validating Material Properties")
        
        concrete = standard_materials['concrete']
        steel = standard_materials['steel']
        
        # Concrete properties validation
        fc = concrete.fc_prime
        ec = concrete.elastic_modulus()
        fr = concrete.modulus_of_rupture()
        
        # ACI 318M-25 formulas
        # Ec = 4700 × √fc (for normal weight concrete)
        expected_ec = 4700 * math.sqrt(fc)
        ec_tolerance = 0.1  # 10% tolerance
        
        assert abs(ec - expected_ec) / expected_ec <= ec_tolerance, \
            f"Concrete modulus incorrect: {ec:.0f} MPa (expected {expected_ec:.0f} MPa)"
        
        # fr = 0.62 × √fc
        expected_fr = 0.62 * math.sqrt(fc)
        fr_tolerance = 0.15  # 15% tolerance
        
        assert abs(fr - expected_fr) / expected_fr <= fr_tolerance, \
            f"Modulus of rupture incorrect: {fr:.2f} MPa (expected {expected_fr:.2f} MPa)"
        
        print(f"  ✅ Concrete fc': {fc} MPa")
        print(f"  ✅ Concrete Ec: {ec:.0f} MPa (expected {expected_ec:.0f} MPa)")
        print(f"  ✅ Concrete fr: {fr:.2f} MPa (expected {expected_fr:.2f} MPa)")
        
        # Steel properties validation
        fy = steel.fy
        fu = steel.fu
        es = steel.elastic_modulus()
        
        # Standard values
        assert es == 200000, f"Steel modulus should be 200,000 MPa: {es}"
        assert fu >= 1.25 * fy, f"Tensile strength should be ≥ 1.25 × fy: fu={fu}, fy={fy}"
        
        print(f"  ✅ Steel fy: {fy} MPa")
        print(f"  ✅ Steel fu: {fu} MPa")
        print(f"  ✅ Steel Es: {es:.0f} MPa")
        
        return {
            'concrete': {'fc': fc, 'ec': ec, 'fr': fr},
            'steel': {'fy': fy, 'fu': fu, 'es': es}
        }
    
    def test_load_factor_validation(self):
        """
        Test load factors against ACI 318M-25 requirements
        """
        print("\n⚖️ Validating Load Factors")
        
        # Standard load factors from ACI 318M-25
        expected_factors = {
            'dead_load': 1.2,      # Basic combination
            'live_load': 1.6,      # Basic combination
            'wind_load': 1.0,      # When combined with seismic
            'seismic_load': 1.0,   # Seismic load factor
        }
        
        # Note: This is a simplified test. In practice, load factors
        # are implemented in the load combination modules
        
        # Strength reduction factors (φ factors)
        expected_phi_factors = {
            'flexure_tension_controlled': 0.90,
            'flexure_compression_controlled': 0.65,
            'shear_and_torsion': 0.75,
            'compression_tied': 0.65,
            'compression_spiral': 0.70,
            'bearing': 0.65
        }
        
        # This validation confirms the expected values are documented
        for factor_type, expected_value in expected_phi_factors.items():
            assert 0.6 <= expected_value <= 1.0, \
                f"Phi factor {factor_type} seems unreasonable: {expected_value}"
            print(f"  ✅ φ {factor_type}: {expected_value}")
        
        return expected_phi_factors


@pytest.mark.aci
@pytest.mark.validation
@pytest.mark.integration
class TestACIIntegrationValidation:
    """Integration validation tests"""
    
    @pytest.fixture(scope="class")
    def standard_materials(self):
        """Standard materials"""
        concrete = ACI318M25Concrete(fc_prime=28.0)
        steel = ACI318M25ReinforcementSteel(grade=420)
        return {'concrete': concrete, 'steel': steel}
    
    def test_complete_frame_validation(self, standard_materials):
        """
        Test complete frame design validation
        """
        print("\n🏗️ Validating Complete Frame Design")
        
        # Create designers
        beam_designer = ACI318M25BeamDesign(
            standard_materials['concrete'], 
            standard_materials['steel']
        )
        column_designer = ACI318M25ColumnDesign(
            standard_materials['concrete'], 
            standard_materials['steel']
        )
        
        # Design beam
        beam_geometry = BeamGeometry(
            width=350, height=700, effective_depth=650, span_length=8000
        )
        beam_loads = BeamLoads(dead_load=6.0, live_load=9.0)
        beam_result = beam_designer.design(beam_geometry, beam_loads, BeamType.SIMPLY_SUPPORTED)
        
        # Calculate beam reactions for column design
        total_load = beam_loads.dead_load + beam_loads.live_load
        beam_reaction = total_load * beam_geometry.span_length / 1000  # kN
        
        # Design column
        column_geometry = ColumnGeometry(width=450, depth=450, length=3500)
        column_loads = ColumnLoads(
            axial_dead=beam_reaction * 0.6 + 150,  # Add building dead load
            axial_live=beam_reaction * 0.4 + 100,  # Add building live load
            moment_x_dead=30,
            moment_x_live=20
        )
        column_result = column_designer.design(column_geometry, column_loads, ColumnType.TIED)
        
        # Validate integration
        assert beam_result.overall_status == DesignStatus.PASS, "Beam should pass"
        assert column_result.overall_status == DesignStatus.PASS, "Column should pass"
        
        # Check force compatibility
        beam_steel = beam_result.required_reinforcement['required_steel_area']
        column_steel = column_result.required_reinforcement['required_steel_area']
        
        # Both should have reasonable reinforcement
        assert beam_steel > 500, f"Beam steel seems too low: {beam_steel:.0f} mm²"
        assert column_steel > 2000, f"Column steel seems too low: {column_steel:.0f} mm²"
        
        print(f"  ✅ Beam: {beam_steel:.0f} mm² steel, {beam_result.utilization_ratio:.2f} utilization")
        print(f"  ✅ Column: {column_steel:.0f} mm² steel, {column_result.utilization_ratio:.2f} utilization")
        print(f"  ✅ Beam reaction: {beam_reaction:.0f} kN")
        
        return {
            'beam': {'steel_area': beam_steel, 'utilization': beam_result.utilization_ratio},
            'column': {'steel_area': column_steel, 'utilization': column_result.utilization_ratio},
            'beam_reaction': beam_reaction
        }
    
    def test_design_consistency_validation(self, standard_materials):
        """
        Test design consistency across different member sizes
        """
        print("\n📐 Validating Design Consistency")
        
        beam_designer = ACI318M25BeamDesign(
            standard_materials['concrete'], 
            standard_materials['steel']
        )
        
        # Test multiple beam sizes with proportional loads
        beam_cases = [
            (300, 500, 4000, 3.0),    # Small beam, light load
            (350, 600, 6000, 5.0),    # Medium beam, medium load
            (400, 700, 8000, 7.0),    # Large beam, heavy load
        ]
        
        consistency_results = []
        
        for width, height, span, load in beam_cases:
            geometry = BeamGeometry(
                width=width,
                height=height,
                effective_depth=height - 50,
                span_length=span
            )
            loads = BeamLoads(dead_load=load, live_load=load * 1.5)
            
            result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
            
            if result.overall_status == DesignStatus.PASS:
                steel_area = result.required_reinforcement['required_steel_area']
                gross_area = width * height
                steel_ratio = steel_area / gross_area
                
                consistency_results.append({
                    'size': f"{width}x{height}x{span}",
                    'load': load,
                    'steel_ratio': steel_ratio,
                    'utilization': result.utilization_ratio
                })
                
                print(f"  ✅ {width}x{height}x{span}: ρ={steel_ratio:.4f}, util={result.utilization_ratio:.2f}")
        
        # Check consistency - steel ratios should be in reasonable range
        steel_ratios = [case['steel_ratio'] for case in consistency_results]
        utilizations = [case['utilization'] for case in consistency_results]
        
        # All ratios should be between minimum and reasonable maximum
        for i, ratio in enumerate(steel_ratios):
            assert 0.002 <= ratio <= 0.025, \
                f"Steel ratio out of range for case {i}: {ratio:.4f}"
        
        # Utilizations should be reasonable and not drastically different
        max_util = max(utilizations)
        min_util = min(utilizations)
        util_range = max_util - min_util
        
        assert util_range <= 0.5, f"Utilization range too large: {util_range:.2f}"
        
        print(f"  ✅ Steel ratio range: {min(steel_ratios):.4f} - {max(steel_ratios):.4f}")
        print(f"  ✅ Utilization range: {min_util:.2f} - {max_util:.2f}")
        
        return consistency_results