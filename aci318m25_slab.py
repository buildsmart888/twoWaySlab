# -*- coding: utf-8 -*-

"""
ACI 318M-25 Slab Design Library
Building Code Requirements for Structural Concrete - Slab Design

Based on:
- ACI CODE-318M-25 International System of Units
- Chapter 8: Two-Way Slab Systems
- Chapter 9: Flexural Design
- Chapter 24: Deflection Control

@author: Enhanced by AI Assistant  
@date: 2024
@version: 1.0
"""

import math
from typing import Dict, Tuple, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from aci318m25 import ACI318M25, ConcreteStrengthClass, ReinforcementGrade, MaterialProperties

class SlabType(Enum):
    """Types of slab systems"""
    ONE_WAY = "one_way"
    TWO_WAY_FLAT = "two_way_flat"
    TWO_WAY_BEAMS = "two_way_with_beams"
    FLAT_PLATE = "flat_plate"
    FLAT_SLAB = "flat_slab"
    WAFFLE_SLAB = "waffle_slab"

class SupportCondition(Enum):
    """Support conditions for slabs"""
    SIMPLY_SUPPORTED = "simply_supported"
    FIXED = "fixed"
    CONTINUOUS = "continuous"
    CANTILEVER = "cantilever"

class LoadPattern(Enum):
    """Load patterns for slab analysis"""
    UNIFORM = "uniform"
    POINT_LOAD = "point_load"
    LINE_LOAD = "line_load"
    PARTIAL_UNIFORM = "partial_uniform"

@dataclass
class SlabGeometry:
    """Slab geometry properties"""
    length_x: float           # Slab length in x-direction (mm)
    length_y: float           # Slab length in y-direction (mm)
    thickness: float          # Slab thickness (mm)
    cover: float              # Concrete cover (mm)
    effective_depth_x: float  # Effective depth for x-direction reinforcement (mm)
    effective_depth_y: float  # Effective depth for y-direction reinforcement (mm)
    slab_type: SlabType       # Type of slab system
    support_conditions: Dict[str, SupportCondition]  # Support conditions for each edge

@dataclass
class SlabLoads:
    """Slab loading conditions"""
    dead_load: float          # Dead load (kN/m²)
    live_load: float          # Live load (kN/m²)
    superimposed_dead: float  # Superimposed dead load (kN/m²)
    load_pattern: LoadPattern # Load distribution pattern
    load_factors: Dict[str, float]  # Load factors for combinations

@dataclass
class SlabReinforcement:
    """Slab reinforcement design"""
    main_bars_x: str          # Main reinforcement in x-direction
    main_spacing_x: float     # Spacing of x-direction bars (mm)
    main_bars_y: str          # Main reinforcement in y-direction
    main_spacing_y: float     # Spacing of y-direction bars (mm)
    shrinkage_bars: str       # Shrinkage and temperature reinforcement
    shrinkage_spacing: float  # Shrinkage reinforcement spacing (mm)
    top_bars: str             # Top reinforcement over supports
    top_spacing: float        # Top reinforcement spacing (mm)

@dataclass
class SlabMoments:
    """Slab moment results"""
    moment_x_positive: float  # Positive moment in x-direction (kN⋅m/m)
    moment_x_negative: float  # Negative moment in x-direction (kN⋅m/m)
    moment_y_positive: float  # Positive moment in y-direction (kN⋅m/m)
    moment_y_negative: float  # Negative moment in y-direction (kN⋅m/m)
    shear_x: float            # Shear in x-direction (kN/m)
    shear_y: float            # Shear in y-direction (kN/m)

@dataclass
class SlabAnalysisResult:
    """Complete slab analysis results"""
    moments: SlabMoments
    reinforcement: SlabReinforcement
    deflection: float         # Maximum deflection (mm)
    crack_width: float        # Maximum crack width (mm)
    punching_shear_ok: bool   # Punching shear check result
    utilization_ratio: float # Maximum utilization ratio
    design_notes: List[str]   # Design notes and warnings

class ACI318M25SlabDesign:
    """
    ACI 318M-25 Slab Design Library
    
    Comprehensive slab design according to ACI 318M-25:
    - One-way and two-way slab systems (Chapter 8)
    - Flexural design (Chapter 9)
    - Deflection control (Chapter 24)
    - Punching shear (Chapter 22)
    - Minimum reinforcement requirements
    """
    
    def __init__(self):
        """Initialize slab design calculator"""
        self.aci = ACI318M25()
        
        # Strength reduction factors φ - ACI 318M-25 Section 21.2
        self.phi_factors = {
            'flexure': 0.90,
            'shear': 0.75,
            'bearing': 0.65
        }
        
        # Minimum thickness requirements - ACI 318M-25 Table 7.3.1.1
        self.min_thickness_ratios = {
            SlabType.ONE_WAY: {
                SupportCondition.SIMPLY_SUPPORTED: 20,
                SupportCondition.FIXED: 28,
                SupportCondition.CONTINUOUS: 24,
                SupportCondition.CANTILEVER: 10
            },
            SlabType.TWO_WAY_FLAT: {
                SupportCondition.SIMPLY_SUPPORTED: 30,
                SupportCondition.FIXED: 36,
                SupportCondition.CONTINUOUS: 33
            }
        }
        
        # Deflection limits - ACI 318M-25 Table 24.2.2
        self.deflection_limits = {
            'immediate': {
                'flat_roof': 180,      # L/180
                'floor': 360,          # L/360
                'roof_floor': 240      # L/240
            },
            'long_term': {
                'supporting_nonstructural': 480,  # L/480
                'not_supporting': 240             # L/240
            }
        }
    
    def calculate_minimum_thickness(self, geometry: SlabGeometry, 
                                  material_props: MaterialProperties) -> float:
        """
        Calculate minimum slab thickness
        ACI 318M-25 Table 7.3.1.1 and Section 8.3.1
        
        Args:
            geometry: Slab geometric properties
            material_props: Material properties
            
        Returns:
            Minimum required thickness (mm)
        """
        # Get span ratios
        aspect_ratio = max(geometry.length_x, geometry.length_y) / min(geometry.length_x, geometry.length_y)
        longer_span = max(geometry.length_x, geometry.length_y)
        
        if geometry.slab_type == SlabType.ONE_WAY:
            # One-way slab thickness
            support_type = list(geometry.support_conditions.values())[0]
            ratio = self.min_thickness_ratios[SlabType.ONE_WAY][support_type]
            h_min = longer_span / ratio
            
        elif geometry.slab_type in [SlabType.TWO_WAY_FLAT, SlabType.FLAT_PLATE]:
            # Two-way slab without beams - ACI 318M-25 Section 8.3.1.1
            perimeter = 2 * (geometry.length_x + geometry.length_y)
            ln = longer_span - 200  # Assume 200mm support width
            
            # Basic minimum thickness
            h_min = ln * (0.8 + material_props.fy / 1400) / 36
            
            # Minimum absolute thickness
            h_min = max(h_min, 125)  # 125mm minimum for slabs without beams
            
        else:
            # Two-way slab with beams
            h_min = longer_span / 36  # Simplified approach
            h_min = max(h_min, 90)   # 90mm minimum for slabs with beams
        
        return h_min
    
    def calculate_slab_moments_one_way(self, geometry: SlabGeometry, 
                                     loads: SlabLoads) -> SlabMoments:
        """
        Calculate moments for one-way slabs
        ACI 318M-25 Chapter 7
        
        Args:
            geometry: Slab geometric properties
            loads: Loading conditions
            
        Returns:
            Slab moments
        """
        # Total factored load
        wu = (loads.dead_load + loads.superimposed_dead) * loads.load_factors.get('D', 1.4) + \
             loads.live_load * loads.load_factors.get('L', 1.6)
        
        # Convert span to meters for moment calculation
        span = max(geometry.length_x, geometry.length_y) / 1000  # Convert mm to m
        
        # Support conditions
        support_type = list(geometry.support_conditions.values())[0]
        
        if support_type == SupportCondition.SIMPLY_SUPPORTED:
            moment_positive = wu * span**2 / 8  # kN⋅m/m
            moment_negative = 0.0
        elif support_type == SupportCondition.FIXED:
            moment_positive = wu * span**2 / 24  # kN⋅m/m
            moment_negative = wu * span**2 / 12  # kN⋅m/m
        elif support_type == SupportCondition.CONTINUOUS:
            moment_positive = wu * span**2 / 16  # kN⋅m/m
            moment_negative = wu * span**2 / 12  # kN⋅m/m
        else:  # Cantilever
            moment_positive = 0.0
            moment_negative = wu * span**2 / 2  # kN⋅m/m
        
        return SlabMoments(
            moment_x_positive=moment_positive,
            moment_x_negative=moment_negative,
            moment_y_positive=0.0,  # No moment in y-direction for one-way
            moment_y_negative=0.0,
            shear_x=wu * span / 2,  # kN/m (wu in kN/m², span in m → kN/m)
            shear_y=0.0
        )
    
    def calculate_slab_moments_two_way(self, geometry: SlabGeometry,
                                     loads: SlabLoads) -> SlabMoments:
        """
        Calculate moments for two-way slabs using Direct Design Method
        ACI 318M-25 Section 8.10
        
        Args:
            geometry: Slab geometric properties
            loads: Loading conditions
            
        Returns:
            Slab moments
        """
        # Total factored load
        wu = (loads.dead_load + loads.superimposed_dead) * loads.load_factors.get('D', 1.4) + \
             loads.live_load * loads.load_factors.get('L', 1.6)
        
        # Convert dimensions to meters for moment calculation
        lx = min(geometry.length_x, geometry.length_y) / 1000  # Convert mm to m
        ly = max(geometry.length_x, geometry.length_y) / 1000  # Convert mm to m
        
        # Aspect ratio
        beta = ly / lx
        
        # Two-way action coefficients (simplified)
        if beta <= 1.5:
            # Square or nearly square panels
            alpha_x = 0.5
            alpha_y = 0.5
        elif beta <= 2.0:
            alpha_x = 0.6
            alpha_y = 0.4
        else:
            # Approaches one-way action
            alpha_x = 0.8
            alpha_y = 0.2
        
        # Total static moment for each direction (now in kN⋅m)
        # Formula: Mo = wu * l1 * l2^2 / 8 (where wu in kN/m², l1,l2 in m)
        Mo_x = wu * lx * ly**2 / 8  # kN⋅m
        Mo_y = wu * ly * lx**2 / 8  # kN⋅m
        
        # Distribute moments to positive and negative regions
        # Simplified distribution (detailed coefficients in ACI 318M-25)
        moment_x_positive = 0.35 * Mo_x * alpha_x
        moment_x_negative = 0.65 * Mo_x * alpha_x
        moment_y_positive = 0.35 * Mo_y * alpha_y
        moment_y_negative = 0.65 * Mo_y * alpha_y
        
        # Shear forces (kN/m)
        shear_x = wu * ly / 2  # kN/m (wu in kN/m², ly in m → kN/m)
        shear_y = wu * lx / 2  # kN/m (wu in kN/m², lx in m → kN/m)
        
        return SlabMoments(
            moment_x_positive=moment_x_positive,
            moment_x_negative=moment_x_negative,
            moment_y_positive=moment_y_positive,
            moment_y_negative=moment_y_negative,
            shear_x=shear_x,
            shear_y=shear_y
        )
    
    def design_flexural_reinforcement(self, moment: float, width: float,
                                    effective_depth: float,
                                    material_props: MaterialProperties) -> Tuple[str, float]:
        """
        Design flexural reinforcement for slab
        ACI 318M-25 Chapter 9
        
        Args:
            moment: Factored moment per unit width (kN⋅m/m)
            width: Design width (typically 1000mm for slabs)
            effective_depth: Effective depth (mm)
            material_props: Material properties
            
        Returns:
            Tuple of (bar_size, spacing_mm)
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        b = width
        d = effective_depth
        
        # Convert moment to N⋅mm
        Mu = moment * 1e6
        
        if Mu <= 0:
            # Minimum reinforcement only
            return self._design_minimum_reinforcement(b, d, fy)
        
        phi = self.phi_factors['flexure']
        
        # Calculate required reinforcement area
        # Using quadratic formula: Mu = φ * As * fy * (d - a/2)
        # where a = As * fy / (0.85 * fc_prime * b)
        
        A = phi * fy**2 / (2 * 0.85 * fc_prime * b)
        B = phi * fy * d
        C = -Mu
        
        discriminant = B**2 - 4*A*C
        if discriminant < 0:
            raise ValueError("Section inadequate for applied moment")
        
        As_required = (-B + math.sqrt(discriminant)) / (2*A)
        
        # Check minimum reinforcement
        As_min = self._calculate_minimum_slab_reinforcement(b, d, fy)
        As_required = max(As_required, As_min)
        
        # Check maximum reinforcement (temperature and shrinkage controls)
        As_max = 0.025 * b * d  # Practical maximum
        if As_required > As_max:
            raise ValueError("Required reinforcement exceeds practical maximum")
        
        # Select bar size and spacing
        return self._select_slab_reinforcement(As_required, b)
    
    def _design_minimum_reinforcement(self, width: float, thickness: float,
                                    fy: float) -> Tuple[str, float]:
        """Design minimum reinforcement for slabs"""
        # Minimum reinforcement for shrinkage and temperature - ACI 318M-25 Section 7.12
        if fy <= 420:
            rho_min = 0.0020
        elif fy <= 520:
            rho_min = 0.0018
        else:
            rho_min = 0.0018 * 420 / fy
        
        As_min = rho_min * width * thickness
        
        return self._select_slab_reinforcement(As_min, width)
    
    def _calculate_minimum_slab_reinforcement(self, width: float, 
                                            effective_depth: float,
                                            fy: float) -> float:
        """Calculate minimum flexural reinforcement for slabs"""
        # Minimum flexural reinforcement
        As_min_flexure = 1.4 * width * effective_depth / fy
        
        # Minimum shrinkage and temperature reinforcement
        if fy <= 420:
            rho_temp = 0.0020
        elif fy <= 520:
            rho_temp = 0.0018
        else:
            rho_temp = 0.0018 * 420 / fy
        
        As_min_temp = rho_temp * width * effective_depth
        
        return max(As_min_flexure, As_min_temp)
    
    def _select_slab_reinforcement(self, As_required: float, 
                                 width: float) -> Tuple[str, float]:
        """Select appropriate bar size and spacing for slab"""
        # Common slab bar sizes
        bar_sizes = ['10M', '15M', '20M', '25M']
        
        for bar_size in bar_sizes:
            bar_area = self.aci.get_bar_area(bar_size)
            spacing = bar_area * width / As_required
            
            # Check spacing limits
            max_spacing = min(3 * 200, 450)  # Assume 200mm slab thickness
            min_spacing = max(bar_area / 25, 75)  # Minimum practical spacing
            
            if min_spacing <= spacing <= max_spacing:
                return bar_size, spacing
        
        # If no suitable single size, use smallest bar with maximum spacing
        bar_size = '15M'
        bar_area = self.aci.get_bar_area(bar_size)
        spacing = min(max_spacing, bar_area * width / As_required)
        
        return bar_size, spacing
    
    def check_punching_shear(self, geometry: SlabGeometry,
                           material_props: MaterialProperties,
                           column_dimensions: Tuple[float, float],
                           punching_force: float) -> Tuple[bool, float]:
        """
        Check punching shear around columns
        ACI 318M-25 Section 22.6
        
        Args:
            geometry: Slab geometric properties
            material_props: Material properties
            column_dimensions: (width, depth) of column (mm)
            punching_force: Factored punching force (kN)
            
        Returns:
            Tuple of (is_adequate, utilization_ratio)
        """
        fc_prime = material_props.fc_prime
        d = min(geometry.effective_depth_x, geometry.effective_depth_y)
        
        col_width, col_depth = column_dimensions
        
        # Critical section perimeter at d/2 from column face
        bo = 2 * (col_width + d) + 2 * (col_depth + d)
        
        # Punching shear strength - ACI 318M-25 Section 22.6.5.2
        # Three controlling equations:
        
        # Equation 1: Basic punching shear
        vc1 = 0.17 * (1 + 2/1) * math.sqrt(fc_prime)  # Assume β = 1 (square column)
        
        # Equation 2: Based on column location (interior column)
        alphas = 40  # For interior columns
        vc2 = 0.083 * (alphas * d / bo + 2) * math.sqrt(fc_prime)
        
        # Equation 3: Maximum punching shear
        vc3 = 0.33 * math.sqrt(fc_prime)
        
        # Controlling punching shear strength
        vc = min(vc1, vc2, vc3)
        
        # Nominal punching shear capacity
        Vn = vc * bo * d / 1000  # Convert to kN
        
        # Design punching shear capacity
        phi = self.phi_factors['shear']
        phi_Vn = phi * Vn
        
        # Check adequacy
        is_adequate = punching_force <= phi_Vn
        utilization_ratio = punching_force / phi_Vn if phi_Vn > 0 else float('inf')
        
        return is_adequate, utilization_ratio
    
    def calculate_deflection(self, geometry: SlabGeometry,
                           material_props: MaterialProperties,
                           service_loads: SlabLoads,
                           reinforcement_x: float,
                           reinforcement_y: float) -> float:
        """
        Calculate slab deflection
        ACI 318M-25 Chapter 24
        
        Args:
            geometry: Slab geometric properties
            material_props: Material properties
            service_loads: Service load conditions
            reinforcement_x: Reinforcement area in x-direction (mm²/m)
            reinforcement_y: Reinforcement area in y-direction (mm²/m)
            
        Returns:
            Maximum deflection (mm)
        """
        # Service load
        w_service = service_loads.dead_load + service_loads.superimposed_dead + service_loads.live_load
        
        # Material properties
        Ec = material_props.ec
        fc_prime = material_props.fc_prime
        
        # Slab properties
        h = geometry.thickness
        lx = min(geometry.length_x, geometry.length_y)
        ly = max(geometry.length_x, geometry.length_y)
        
        # Gross moment of inertia per unit width
        Ig = h**3 / 12  # mm⁴/mm
        
        # Modulus of rupture
        fr = 0.62 * math.sqrt(fc_prime)
        
        # Cracking moment per unit width
        Mcr = fr * Ig / (h/2) / 1000  # kN⋅m/m
        
        # Service moment (simplified for uniformly loaded slab)
        if geometry.slab_type == SlabType.ONE_WAY:
            M_service = w_service * lx**2 / 8
        else:
            # Two-way slab approximation
            M_service = w_service * lx**2 / 16
        
        # Transform section properties
        n = 200000 / Ec  # Modular ratio
        As = max(reinforcement_x, reinforcement_y)  # Use larger reinforcement
        rho = As / (1000 * geometry.effective_depth_x)
        
        # Neutral axis depth (cracked section)
        k = math.sqrt(2 * rho * n + (rho * n)**2) - rho * n
        
        # Cracked moment of inertia per unit width
        d = geometry.effective_depth_x
        Icr = (1000 * k**3 * d**3) / 3 + n * As * (d * (1 - k))**2
        
        # Effective moment of inertia
        if M_service <= Mcr:
            Ie = Ig
        else:
            Ie = (Mcr / M_service)**3 * Ig + (1 - (Mcr / M_service)**3) * Icr
            Ie = max(Ie, Icr)
        
        # Deflection calculation (simplified for center of slab)
        if geometry.slab_type == SlabType.ONE_WAY:
            # One-way slab deflection
            deflection = 5 * w_service * lx**4 / (384 * Ec * Ie)
        else:
            # Two-way slab deflection (approximate)
            alpha = 0.001  # Deflection coefficient for two-way slabs
            deflection = alpha * w_service * lx**4 / (Ec * Ie)
        
        return deflection
    
    def perform_complete_slab_design(self, geometry: SlabGeometry,
                                   loads: SlabLoads,
                                   material_props: MaterialProperties,
                                   column_size: Tuple[float, float] = None) -> SlabAnalysisResult:
        """
        Perform complete slab design analysis
        
        Args:
            geometry: Slab geometric properties
            loads: Loading conditions
            material_props: Material properties
            column_size: Column dimensions for punching shear check
            
        Returns:
            Complete slab analysis results
        """
        design_notes = []
        
        # Check minimum thickness
        h_min = self.calculate_minimum_thickness(geometry, material_props)
        if geometry.thickness < h_min:
            design_notes.append(f"Increase thickness to minimum {h_min:.0f}mm")
        
        # Calculate moments
        if geometry.slab_type == SlabType.ONE_WAY:
            moments = self.calculate_slab_moments_one_way(geometry, loads)
        else:
            moments = self.calculate_slab_moments_two_way(geometry, loads)
        
        # Design reinforcement
        bar_x, spacing_x = self.design_flexural_reinforcement(
            moments.moment_x_positive, 1000, geometry.effective_depth_x, material_props
        )
        
        bar_y, spacing_y = self.design_flexural_reinforcement(
            moments.moment_y_positive, 1000, geometry.effective_depth_y, material_props
        )
        
        # Top reinforcement for negative moments
        if moments.moment_x_negative > 0:
            bar_top, spacing_top = self.design_flexural_reinforcement(
                moments.moment_x_negative, 1000, geometry.effective_depth_x, material_props
            )
        else:
            bar_top, spacing_top = self._design_minimum_reinforcement(
                1000, geometry.thickness, material_props.fy
            )
        
        # Shrinkage and temperature reinforcement
        bar_shrink, spacing_shrink = self._design_minimum_reinforcement(
            1000, geometry.thickness, material_props.fy
        )
        
        # Calculate reinforcement areas
        As_x = self.aci.get_bar_area(bar_x) * 1000 / spacing_x
        As_y = self.aci.get_bar_area(bar_y) * 1000 / spacing_y
        
        # Deflection calculation
        service_loads = SlabLoads(
            dead_load=loads.dead_load,
            live_load=loads.live_load,
            superimposed_dead=loads.superimposed_dead,
            load_pattern=loads.load_pattern,
            load_factors={'D': 1.0, 'L': 1.0}  # Service load factors
        )
        
        deflection = self.calculate_deflection(
            geometry, material_props, service_loads, As_x, As_y
        )
        
        # Check deflection limits
        span = max(geometry.length_x, geometry.length_y)
        deflection_limit = span / self.deflection_limits['immediate']['floor']
        
        if deflection > deflection_limit:
            design_notes.append(f"Deflection {deflection:.1f}mm exceeds limit {deflection_limit:.1f}mm")
        
        # Punching shear check
        punching_shear_ok = True
        if column_size and geometry.slab_type in [SlabType.FLAT_PLATE, SlabType.FLAT_SLAB]:
            punching_force = (loads.dead_load + loads.live_load) * \
                           geometry.length_x * geometry.length_y / 1000  # Approximate
            punching_shear_ok, punch_ratio = self.check_punching_shear(
                geometry, material_props, column_size, punching_force
            )
            if not punching_shear_ok:
                design_notes.append("Punching shear inadequate - increase slab thickness or add shear reinforcement")
        
        # Calculate utilization ratios
        moment_utilization = max(
            moments.moment_x_positive / (As_x * material_props.fy * geometry.effective_depth_x * 0.9 / 1e6),
            moments.moment_y_positive / (As_y * material_props.fy * geometry.effective_depth_y * 0.9 / 1e6)
        ) if As_x > 0 and As_y > 0 else 0
        
        utilization_ratio = min(moment_utilization, 1.0)
        
        # Create result objects
        reinforcement = SlabReinforcement(
            main_bars_x=bar_x,
            main_spacing_x=spacing_x,
            main_bars_y=bar_y,
            main_spacing_y=spacing_y,
            shrinkage_bars=bar_shrink,
            shrinkage_spacing=spacing_shrink,
            top_bars=bar_top,
            top_spacing=spacing_top
        )
        
        return SlabAnalysisResult(
            moments=moments,
            reinforcement=reinforcement,
            deflection=deflection,
            crack_width=0.0,  # Simplified - detailed crack analysis needed
            punching_shear_ok=punching_shear_ok,
            utilization_ratio=utilization_ratio,
            design_notes=design_notes
        )