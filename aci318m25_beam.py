# -*- coding: utf-8 -*-

"""
ACI 318M-25 Beam Design Library
Building Code Requirements for Structural Concrete - Beam Design

Based on:
- ACI CODE-318M-25 International System of Units
- Chapter 9: Flexural Design
- Chapter 22: Shear and Torsion Design
- Chapter 25: Development and Splices of Reinforcement

@author: Enhanced by AI Assistant  
@date: 2024
@version: 1.0
"""

import math
from typing import Dict, Tuple, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from aci318m25 import ACI318M25, ConcreteStrengthClass, ReinforcementGrade, MaterialProperties

class BeamType(Enum):
    """Types of beams for design"""
    RECTANGULAR = "rectangular"
    T_BEAM = "t_beam"
    L_BEAM = "l_beam"
    INVERTED_T = "inverted_t"

class LoadType(Enum):
    """Types of loads on beams"""
    POINT_LOAD = "point_load"
    UNIFORMLY_DISTRIBUTED = "uniformly_distributed"
    TRIANGULAR = "triangular"
    TRAPEZOIDAL = "trapezoidal"

@dataclass
class BeamGeometry:
    """Beam geometry properties"""
    length: float              # Beam length (mm)
    width: float              # Beam width (mm)
    height: float             # Beam total height (mm)
    effective_depth: float    # Effective depth to tension reinforcement (mm)
    cover: float              # Concrete cover (mm)
    flange_width: float       # Effective flange width for T-beams (mm)
    flange_thickness: float   # Flange thickness for T-beams (mm)
    beam_type: BeamType       # Type of beam cross-section

@dataclass
class ReinforcementDesign:
    """Reinforcement design results"""
    main_bars: List[str]      # Main tension reinforcement bar sizes
    main_area: float          # Total area of main reinforcement (mm²)
    compression_bars: List[str] # Compression reinforcement if required
    compression_area: float   # Total compression reinforcement area (mm²)
    stirrups: str             # Stirrup bar size
    stirrup_spacing: float    # Stirrup spacing (mm)
    development_length: float # Development length (mm)

@dataclass
class BeamAnalysisResult:
    """Complete beam analysis results"""
    moment_capacity: float     # Nominal moment capacity Mn (kN⋅m)
    shear_capacity: float      # Nominal shear capacity Vn (kN)
    deflection: float          # Maximum deflection (mm)
    crack_width: float         # Maximum crack width (mm)
    reinforcement: ReinforcementDesign
    utilization_ratio: float  # Demand/Capacity ratio
    design_notes: List[str]    # Design notes and warnings

class ACI318M25BeamDesign:
    """
    ACI 318M-25 Beam Design Library
    
    Comprehensive beam design according to ACI 318M-25:
    - Flexural design (Chapter 9)
    - Shear and torsion design (Chapter 22)
    - Development lengths (Chapter 25)
    - Deflection control (Chapter 24)
    - Crack control (Chapter 24)
    """
    
    def __init__(self):
        """Initialize beam design calculator"""
        self.aci = ACI318M25()
        
        # Strength reduction factors φ - ACI 318M-25 Section 21.2
        self.phi_factors = {
            'flexure_tension_controlled': 0.90,
            'flexure_compression_controlled_tied': 0.65,
            'flexure_compression_controlled_spiral': 0.75,
            'shear': 0.75,
            'torsion': 0.75,
            'bearing': 0.65
        }
        
        # Minimum reinforcement ratios - ACI 318M-25 Section 9.6.1
        self.rho_min_factors = {
            'normal': 1.4,  # 1.4/fy for normal sections
            'flanged': 1.4  # Special provisions for flanged sections
        }
        
        # Maximum aggregate size factors for development length
        self.development_factors = {
            'clear_spacing_factor': 1.0,    # Based on clear spacing
            'transverse_reinforcement': 1.0, # Based on transverse steel
            'confinement_factor': 1.0        # Confinement effects
        }
    
    def calculate_effective_flange_width(self, beam_geometry: BeamGeometry, 
                                       span_length: float) -> float:
        """
        Calculate effective flange width for T-beams
        ACI 318M-25 Section 6.3.2
        
        Args:
            beam_geometry: Beam geometric properties
            span_length: Clear span length (mm)
            
        Returns:
            Effective flange width (mm)
        """
        bw = beam_geometry.width
        hf = beam_geometry.flange_thickness
        
        # ACI 318M-25 Section 6.3.2.1 - effective width limitations
        be1 = span_length / 4.0  # One-quarter of span length
        be2 = bw + 16 * hf       # Beam width plus 16 times flange thickness
        be3 = beam_geometry.flange_width  # Given flange width
        
        effective_width = min(be1, be2, be3)
        return effective_width
    
    def calculate_minimum_reinforcement_ratio(self, fc_prime: float, fy: float,
                                            beam_type: BeamType = BeamType.RECTANGULAR) -> float:
        """
        Calculate minimum reinforcement ratio
        ACI 318M-25 Section 9.6.1
        
        Args:
            fc_prime: Concrete compressive strength (MPa)
            fy: Steel yield strength (MPa)
            beam_type: Type of beam section
            
        Returns:
            Minimum reinforcement ratio
        """
        # Basic minimum reinforcement ratio
        rho_min_basic = 1.4 / fy
        
        # Alternative minimum based on concrete strength
        rho_min_alt = 0.25 * math.sqrt(fc_prime) / fy
        
        # Use the larger value
        rho_min = max(rho_min_basic, rho_min_alt)
        
        # Special provisions for flanged sections
        if beam_type in [BeamType.T_BEAM, BeamType.L_BEAM]:
            # For flanged sections, apply to web area only
            pass  # Implementation depends on specific geometry
        
        return rho_min
    
    def calculate_maximum_reinforcement_ratio(self, fc_prime: float, fy: float,
                                            beam_geometry: BeamGeometry) -> float:
        """
        Calculate maximum reinforcement ratio for tension-controlled sections
        ACI 318M-25 Section 21.2.2
        
        Args:
            fc_prime: Concrete compressive strength (MPa)
            fy: Steel yield strength (MPa)
            beam_geometry: Beam geometric properties
            
        Returns:
            Maximum reinforcement ratio for tension-controlled sections
        """
        # Material properties
        Es = 200000.0  # Steel modulus (MPa)
        beta1 = self._calculate_beta1(fc_prime)
        
        # Strain limits for tension-controlled sections
        epsilon_t_min = 0.005  # Minimum tensile strain for tension-controlled
        epsilon_cu = 0.003     # Ultimate concrete strain
        
        # Balanced reinforcement ratio
        rho_b = (0.85 * fc_prime * beta1 / fy) * (epsilon_cu / (epsilon_cu + epsilon_t_min))
        
        # Maximum reinforcement ratio (75% of balanced for tension-controlled)
        rho_max = 0.75 * rho_b
        
        return rho_max
    
    def design_flexural_reinforcement(self, mu: float, beam_geometry: BeamGeometry,
                                    material_props: MaterialProperties) -> ReinforcementDesign:
        """
        Design flexural reinforcement for rectangular or T-beam sections
        ACI 318M-25 Chapter 9
        
        Args:
            mu: Factored moment (kN⋅m)
            beam_geometry: Beam geometric properties
            material_props: Material properties
            
        Returns:
            Reinforcement design results
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        b = beam_geometry.width
        d = beam_geometry.effective_depth
        
        # Convert moment to N⋅mm
        Mu = mu * 1e6
        
        # Check if compression reinforcement is needed
        phi = self.phi_factors['flexure_tension_controlled']
        
        # Maximum moment capacity with tension reinforcement only
        rho_max = self.calculate_maximum_reinforcement_ratio(fc_prime, fy, beam_geometry)
        As_max = rho_max * b * d
        
        # Calculate moment capacity with maximum tension reinforcement
        a_max = As_max * fy / (0.85 * fc_prime * b)
        Mn_max = As_max * fy * (d - a_max / 2)
        phi_Mn_max = phi * Mn_max
        
        if Mu <= phi_Mn_max:
            # Tension reinforcement only
            return self._design_tension_reinforcement_only(Mu, beam_geometry, material_props)
        else:
            # Compression reinforcement required
            return self._design_doubly_reinforced_section(Mu, beam_geometry, material_props)
    
    def _design_tension_reinforcement_only(self, Mu: float, beam_geometry: BeamGeometry,
                                         material_props: MaterialProperties) -> ReinforcementDesign:
        """Design tension reinforcement only"""
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        b = beam_geometry.width
        d = beam_geometry.effective_depth
        
        phi = self.phi_factors['flexure_tension_controlled']
        
        # Calculate required reinforcement area
        # Mu = φ * As * fy * (d - a/2)
        # a = As * fy / (0.85 * fc_prime * b)
        
        # Quadratic equation coefficients
        # φ * As * fy * d - φ * As² * fy² / (2 * 0.85 * fc_prime * b) = Mu
        A = phi * fy**2 / (2 * 0.85 * fc_prime * b)
        B = phi * fy * d
        C = -Mu
        
        # Solve quadratic equation
        discriminant = B**2 - 4*A*C
        As_required = (-B + math.sqrt(discriminant)) / (2*A)
        
        # Check minimum reinforcement
        rho_min = self.calculate_minimum_reinforcement_ratio(fc_prime, fy)
        As_min = rho_min * b * d
        As_required = max(As_required, As_min)
        
        # Select reinforcement bars
        main_bars = self._select_reinforcement_bars(As_required)
        
        # Calculate development length
        main_bar_size = main_bars[0] if main_bars else '20M'
        ld = self.aci.calculate_development_length(main_bar_size, fc_prime, fy)
        
        return ReinforcementDesign(
            main_bars=main_bars,
            main_area=As_required,
            compression_bars=[],
            compression_area=0.0,
            stirrups='10M',  # Default stirrup size
            stirrup_spacing=200.0,  # Default spacing
            development_length=ld
        )
    
    def _design_doubly_reinforced_section(self, Mu: float, beam_geometry: BeamGeometry,
                                        material_props: MaterialProperties) -> ReinforcementDesign:
        """Design doubly reinforced section with compression reinforcement"""
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        b = beam_geometry.width
        d = beam_geometry.effective_depth
        d_prime = beam_geometry.cover + 20  # Assume 20mm to center of compression bars
        
        phi = self.phi_factors['flexure_tension_controlled']
        
        # Maximum tension reinforcement without compression steel
        rho_max = self.calculate_maximum_reinforcement_ratio(fc_prime, fy, beam_geometry)
        As1 = rho_max * b * d
        
        # Moment capacity with As1 only
        a1 = As1 * fy / (0.85 * fc_prime * b)
        Mn1 = As1 * fy * (d - a1/2)
        
        # Additional moment requiring compression reinforcement
        Mu2 = Mu - phi * Mn1
        
        # Design compression reinforcement
        # Assume compression steel yields
        As2_prime = Mu2 / (phi * fy * (d - d_prime))
        As2 = As2_prime  # Additional tension reinforcement to balance As2_prime
        
        # Total tension reinforcement
        As_total = As1 + As2
        
        # Select reinforcement
        main_bars = self._select_reinforcement_bars(As_total)
        comp_bars = self._select_reinforcement_bars(As2_prime)
        
        # Development length
        main_bar_size = main_bars[0] if main_bars else '25M'
        ld = self.aci.calculate_development_length(main_bar_size, fc_prime, fy)
        
        return ReinforcementDesign(
            main_bars=main_bars,
            main_area=As_total,
            compression_bars=comp_bars,
            compression_area=As2_prime,
            stirrups='10M',
            stirrup_spacing=150.0,  # Closer spacing for doubly reinforced
            development_length=ld
        )
    
    def design_shear_reinforcement(self, vu: float, beam_geometry: BeamGeometry,
                                 material_props: MaterialProperties,
                                 main_reinforcement_area: float) -> Tuple[str, float]:
        """
        Design shear reinforcement (stirrups)
        ACI 318M-25 Chapter 22
        
        Args:
            vu: Factored shear force (kN)
            beam_geometry: Beam geometric properties
            material_props: Material properties
            main_reinforcement_area: Area of tension reinforcement (mm²)
            
        Returns:
            Tuple of (stirrup_size, spacing_mm)
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        b = beam_geometry.width
        d = beam_geometry.effective_depth
        
        # Convert shear to N
        Vu = vu * 1000
        
        # Concrete shear strength - ACI 318M-25 Section 22.5.5.1
        lambda_factor = 1.0  # Normal weight concrete
        Vc = lambda_factor * 0.17 * math.sqrt(fc_prime) * b * d  # N
        
        phi_v = self.phi_factors['shear']
        phi_Vc = phi_v * Vc
        
        # Check if shear reinforcement is required
        if Vu <= phi_Vc / 2:
            # No shear reinforcement required
            return 'None', 0.0
        elif Vu <= phi_Vc:
            # Minimum shear reinforcement required
            return self._design_minimum_stirrups(beam_geometry, fy)
        else:
            # Calculate required stirrup area
            Vs_required = Vu / phi_v - Vc  # Required shear from stirrups
            return self._design_stirrups_for_shear(Vs_required, beam_geometry, fy)
    
    def _design_minimum_stirrups(self, beam_geometry: BeamGeometry, fy: float) -> Tuple[str, float]:
        """Design minimum stirrups - ACI 318M-25 Section 9.7.6.2.2"""
        b = beam_geometry.width
        
        # Minimum stirrup area: Av,min = 0.062√fc' bw s / fy (but not less than 0.35 bw s / fy)
        fc_prime = 28.0  # Assume typical strength for minimum calculation
        Av_min_1 = 0.062 * math.sqrt(fc_prime) * b / fy  # mm²/mm
        Av_min_2 = 0.35 * b / fy  # mm²/mm
        Av_min = max(Av_min_1, Av_min_2)
        
        # Select stirrup size and calculate spacing
        stirrup_size = '10M'
        Av_stirrup = 2 * self.aci.get_bar_area(stirrup_size)  # Two legs
        s_max = Av_stirrup / Av_min
        
        # Maximum spacing limits
        s_max_limit = min(beam_geometry.effective_depth / 2, 600.0)
        s_actual = min(s_max, s_max_limit)
        
        return stirrup_size, s_actual
    
    def _design_stirrups_for_shear(self, Vs_required: float, beam_geometry: BeamGeometry,
                                 fy: float) -> Tuple[str, float]:
        """Design stirrups for required shear strength"""
        d = beam_geometry.effective_depth
        
        # Select stirrup size
        stirrup_size = '10M'
        Av = 2 * self.aci.get_bar_area(stirrup_size)  # Two legs
        
        # Calculate required spacing
        # Vs = Av * fy * d / s
        s_required = Av * fy * d / Vs_required
        
        # Maximum spacing limits - ACI 318M-25 Section 9.7.6.2.2
        s_max = min(d / 2, 600.0)
        s_actual = min(s_required, s_max)
        
        # Check if larger stirrups are needed
        if s_actual < 75.0:  # Minimum practical spacing
            stirrup_size = '15M'
            Av = 2 * self.aci.get_bar_area(stirrup_size)
            s_actual = min(Av * fy * d / Vs_required, s_max)
        
        return stirrup_size, s_actual
    
    def calculate_deflection(self, beam_geometry: BeamGeometry, material_props: MaterialProperties,
                           service_moment: float, reinforcement_area: float) -> float:
        """
        Calculate beam deflection - ACI 318M-25 Chapter 24
        
        Args:
            beam_geometry: Beam geometric properties
            material_props: Material properties
            service_moment: Service load moment (kN⋅m)
            reinforcement_area: Tension reinforcement area (mm²)
            
        Returns:
            Maximum deflection (mm)
        """
        # Simplified deflection calculation for uniformly loaded simply supported beam
        # More detailed analysis would require moment-curvature integration
        
        L = beam_geometry.length
        b = beam_geometry.width
        h = beam_geometry.height
        d = beam_geometry.effective_depth
        As = reinforcement_area
        
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        Ec = material_props.ec
        
        # Transform section properties
        n = 200000 / Ec  # Modular ratio
        rho = As / (b * d)
        
        # Neutral axis depth (cracked section)
        k = math.sqrt(2 * rho * n + (rho * n)**2) - rho * n
        
        # Moment of inertia (cracked section)
        Icr = (b * k**3 * d**3) / 3 + n * As * (d * (1 - k))**2
        
        # Effective moment of inertia - ACI 318M-25 Eq. (24.2.3.5)
        Ig = b * h**3 / 12  # Gross moment of inertia
        
        # Cracking moment
        fr = 0.62 * math.sqrt(fc_prime)  # Modulus of rupture
        yt = h / 2  # Distance to extreme tension fiber
        Mcr = fr * Ig / yt / 1e6  # Convert to kN⋅m
        
        # Effective moment of inertia
        if service_moment <= Mcr:
            Ie = Ig
        else:
            Ie = (Mcr / service_moment)**3 * Ig + (1 - (Mcr / service_moment)**3) * Icr
            Ie = max(Ie, Icr)
        
        # Deflection for simply supported beam with uniform load
        # Δ = 5ML²/(48EI) - simplified assumption
        deflection = (5 * service_moment * 1e6 * L**2) / (48 * Ec * Ie)
        
        return deflection
    
    def _select_reinforcement_bars(self, As_required: float) -> List[str]:
        """Select reinforcement bars to provide required area"""
        # Available bar sizes and areas
        bar_data = [
            ('15M', 200), ('20M', 300), ('25M', 500), ('30M', 700),
            ('35M', 1000), ('45M', 1500), ('55M', 2500)
        ]
        
        selected_bars = []
        remaining_area = As_required
        
        # Start with largest bars and work down
        for bar_size, area in reversed(bar_data):
            if remaining_area <= 0:
                break
            
            num_bars = int(remaining_area / area)
            if num_bars > 0:
                for _ in range(num_bars):
                    selected_bars.append(bar_size)
                remaining_area -= num_bars * area
        
        # If we still need more area, add one more bar of the smallest practical size
        if remaining_area > 0:
            selected_bars.append('15M')
        
        return selected_bars if selected_bars else ['15M']
    
    def _calculate_beta1(self, fc_prime: float) -> float:
        """Calculate β₁ factor for concrete - ACI 318M-25 Section 22.2.2.4.3"""
        if fc_prime <= 28.0:
            return 0.85
        elif fc_prime <= 55.0:
            return 0.85 - 0.05 * (fc_prime - 28.0) / 7.0
        else:
            return 0.65
    
    def perform_complete_beam_design(self, mu: float, vu: float, beam_geometry: BeamGeometry,
                                   material_props: MaterialProperties,
                                   service_moment: float = None) -> BeamAnalysisResult:
        """
        Perform complete beam design analysis
        
        Args:
            mu: Factored moment (kN⋅m)
            vu: Factored shear (kN)
            beam_geometry: Beam geometric properties
            material_props: Material properties
            service_moment: Service moment for deflection (kN⋅m)
            
        Returns:
            Complete beam analysis results
        """
        design_notes = []
        
        # Flexural design
        flexural_design = self.design_flexural_reinforcement(mu, beam_geometry, material_props)
        
        # Shear design
        stirrup_size, stirrup_spacing = self.design_shear_reinforcement(
            vu, beam_geometry, material_props, flexural_design.main_area
        )
        
        flexural_design.stirrups = stirrup_size
        flexural_design.stirrup_spacing = stirrup_spacing
        
        # Calculate capacities
        moment_capacity = self._calculate_moment_capacity(
            flexural_design.main_area, beam_geometry, material_props
        )
        
        shear_capacity = self._calculate_shear_capacity(
            beam_geometry, material_props, stirrup_size, stirrup_spacing
        )
        
        # Deflection calculation
        deflection = 0.0
        if service_moment:
            deflection = self.calculate_deflection(
                beam_geometry, material_props, service_moment, flexural_design.main_area
            )
        
        # Utilization ratio
        utilization_moment = mu / moment_capacity if moment_capacity > 0 else 1.0
        utilization_shear = vu / shear_capacity if shear_capacity > 0 else 1.0
        utilization_ratio = max(utilization_moment, utilization_shear)
        
        # Design notes
        if flexural_design.compression_area > 0:
            design_notes.append("Compression reinforcement required")
        
        if stirrup_size == 'None':
            design_notes.append("No shear reinforcement required")
        
        if deflection > beam_geometry.length / 360:
            design_notes.append("Deflection may exceed typical limits")
        
        return BeamAnalysisResult(
            moment_capacity=moment_capacity,
            shear_capacity=shear_capacity,
            deflection=deflection,
            crack_width=0.0,  # Simplified - detailed crack analysis needed
            reinforcement=flexural_design,
            utilization_ratio=utilization_ratio,
            design_notes=design_notes
        )
    
    def _calculate_moment_capacity(self, As: float, beam_geometry: BeamGeometry,
                                 material_props: MaterialProperties) -> float:
        """Calculate nominal moment capacity"""
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        b = beam_geometry.width
        d = beam_geometry.effective_depth
        
        # Calculate neutral axis depth
        a = As * fy / (0.85 * fc_prime * b)
        
        # Nominal moment capacity
        Mn = As * fy * (d - a/2) / 1e6  # Convert to kN⋅m
        
        return Mn
    
    def _calculate_shear_capacity(self, beam_geometry: BeamGeometry,
                                material_props: MaterialProperties,
                                stirrup_size: str, stirrup_spacing: float) -> float:
        """Calculate nominal shear capacity"""
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        b = beam_geometry.width
        d = beam_geometry.effective_depth
        
        # Concrete contribution
        Vc = 0.17 * math.sqrt(fc_prime) * b * d / 1000  # Convert to kN
        
        # Steel contribution
        if stirrup_size != 'None' and stirrup_spacing > 0:
            Av = 2 * self.aci.get_bar_area(stirrup_size)
            Vs = Av * fy * d / stirrup_spacing / 1000  # Convert to kN
        else:
            Vs = 0
        
        # Total shear capacity
        Vn = Vc + Vs
        
        return Vn