# -*- coding: utf-8 -*-

"""
ACI 318M-25 Column Design Library
Building Code Requirements for Structural Concrete - Column Design

Based on:
- ACI CODE-318M-25 International System of Units
- Chapter 10: Axial Force and Combined Bending and Axial Force
- Chapter 21: Special Provisions for Seismic Design
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

class ColumnType(Enum):
    """Types of columns for design"""
    TIED = "tied"              # Tied columns with rectangular ties
    SPIRAL = "spiral"          # Spiral columns with spiral reinforcement
    COMPOSITE = "composite"    # Composite columns with structural steel

class ColumnShape(Enum):
    """Column cross-sectional shapes"""
    RECTANGULAR = "rectangular"
    CIRCULAR = "circular"
    L_SHAPED = "l_shaped"
    T_SHAPED = "t_shaped"

class LoadCondition(Enum):
    """Load conditions for column design"""
    AXIAL_ONLY = "axial_only"
    UNIAXIAL_BENDING = "uniaxial_bending"
    BIAXIAL_BENDING = "biaxial_bending"

@dataclass
class ColumnGeometry:
    """Column geometry properties"""
    width: float              # Column width or diameter (mm)
    depth: float              # Column depth (mm) - equals width for circular
    height: float             # Column height (mm)
    cover: float              # Concrete cover (mm)
    shape: ColumnShape        # Cross-sectional shape
    column_type: ColumnType   # Type of column
    effective_length: float   # Effective length for buckling (mm)

@dataclass
class ColumnLoads:
    """Column load conditions"""
    axial_force: float        # Factored axial force Pu (kN) - compression positive
    moment_x: float           # Factored moment about x-axis Mux (kN⋅m)
    moment_y: float           # Factored moment about y-axis Muy (kN⋅m)
    shear_x: float            # Factored shear in x-direction Vux (kN)
    shear_y: float            # Factored shear in y-direction Vuy (kN)
    load_condition: LoadCondition

@dataclass
class ColumnReinforcement:
    """Column reinforcement design"""
    longitudinal_bars: List[str]    # Longitudinal bar sizes
    longitudinal_area: float        # Total longitudinal steel area (mm²)
    tie_bars: str                   # Tie bar size for tied columns
    tie_spacing: float              # Tie spacing (mm)
    spiral_bar: str                 # Spiral bar size for spiral columns
    spiral_pitch: float             # Spiral pitch (mm)
    confinement_ratio: float        # Volumetric ratio of confinement steel

@dataclass
class ColumnCapacity:
    """Column capacity results"""
    axial_capacity: float           # Nominal axial capacity Pn (kN)
    moment_capacity_x: float        # Moment capacity about x-axis Mnx (kN⋅m)
    moment_capacity_y: float        # Moment capacity about y-axis Mny (kN⋅m)
    interaction_ratio: float        # P-M interaction ratio
    slenderness_effects: bool       # Whether slenderness effects considered

@dataclass
class ColumnAnalysisResult:
    """Complete column analysis results"""
    capacity: ColumnCapacity
    reinforcement: ColumnReinforcement
    utilization_ratio: float       # Demand/Capacity ratio
    stability_index: float         # Stability index for sway analysis
    design_notes: List[str]         # Design notes and warnings

class ACI318M25ColumnDesign:
    """
    ACI 318M-25 Column Design Library
    
    Comprehensive column design according to ACI 318M-25:
    - Axial and combined loading (Chapter 10)
    - Slenderness effects (Chapter 6)
    - Seismic provisions (Chapter 18)
    - Confinement design
    - P-M interaction analysis
    """
    
    def __init__(self):
        """Initialize column design calculator"""
        self.aci = ACI318M25()
        
        # Strength reduction factors φ - ACI 318M-25 Section 21.2
        self.phi_factors = {
            'compression_tied': 0.65,
            'compression_spiral': 0.75,
            'flexure': 0.90,
            'shear': 0.75
        }
        
        # Minimum and maximum reinforcement ratios - ACI 318M-25 Section 10.6
        self.reinforcement_limits = {
            'min_ratio': 0.01,      # Minimum ρg = 0.01
            'max_ratio': 0.08,      # Maximum ρg = 0.08 (0.06 for lap splices)
            'min_bars': 4,          # Minimum number of longitudinal bars
            'min_bar_size': '15M'   # Minimum bar size
        }
        
        # Tie and spiral requirements
        self.confinement_requirements = {
            'min_tie_size': '10M',
            'max_tie_spacing_factor': 16,  # 16 times longitudinal bar diameter
            'min_spiral_ratio': 0.45,      # Minimum spiral reinforcement ratio factor
            'spiral_clear_spacing': 25     # Minimum clear spacing between spiral turns (mm)
        }
    
    def calculate_required_longitudinal_steel(self, loads: ColumnLoads, 
                                            geometry: ColumnGeometry,
                                            material_props: MaterialProperties) -> float:
        """
        Calculate required longitudinal steel area
        ACI 318M-25 Section 10.6
        
        Args:
            loads: Column load conditions
            geometry: Column geometric properties
            material_props: Material properties
            
        Returns:
            Required longitudinal steel area (mm²)
        """
        # Gross cross-sectional area
        if geometry.shape == ColumnShape.RECTANGULAR:
            Ag = geometry.width * geometry.depth
        elif geometry.shape == ColumnShape.CIRCULAR:
            Ag = math.pi * (geometry.width / 2) ** 2
        else:
            # Simplified for other shapes
            Ag = geometry.width * geometry.depth
        
        # Minimum steel area
        As_min = self.reinforcement_limits['min_ratio'] * Ag
        
        # For compression-controlled sections, start with minimum
        # More detailed P-M interaction analysis needed for precise sizing
        As_required = As_min
        
        # Check if additional steel needed for moment
        if loads.load_condition != LoadCondition.AXIAL_ONLY:
            # Simplified approach - detailed interaction diagram needed
            moment_ratio = abs(loads.moment_x) / (loads.axial_force * geometry.width / 6)
            if moment_ratio > 1.0:  # Tension exists
                As_additional = self._calculate_additional_steel_for_moment(
                    loads, geometry, material_props
                )
                As_required = max(As_required, As_additional)
        
        # Maximum steel area
        As_max = self.reinforcement_limits['max_ratio'] * Ag
        As_required = min(As_required, As_max)
        
        return As_required
    
    def design_tie_reinforcement(self, geometry: ColumnGeometry, 
                               longitudinal_bars: List[str]) -> Tuple[str, float]:
        """
        Design tie reinforcement for tied columns
        ACI 318M-25 Section 25.7.2
        
        Args:
            geometry: Column geometric properties
            longitudinal_bars: List of longitudinal bar sizes
            
        Returns:
            Tuple of (tie_size, spacing_mm)
        """
        # Tie size requirements
        if longitudinal_bars:
            long_bar_size = longitudinal_bars[0]
            long_bar_diameter = self.aci.get_bar_diameter(long_bar_size)
        else:
            long_bar_diameter = 20.0  # Default assumption
        
        # Minimum tie size - ACI 318M-25 Section 25.7.2.1
        if long_bar_diameter <= 32.0:
            tie_size = '10M'
        else:
            tie_size = '15M'
        
        # Tie spacing requirements - ACI 318M-25 Section 25.7.2.2
        spacing_limits = [
            16 * long_bar_diameter,           # 16 times longitudinal bar diameter
            48 * self.aci.get_bar_diameter(tie_size),  # 48 times tie bar diameter
            min(geometry.width, geometry.depth)       # Least dimension of column
        ]
        
        tie_spacing = min(spacing_limits)
        
        # Additional spacing requirements for seismic design
        # ACI 318M-25 Chapter 18 (if applicable)
        
        return tie_size, tie_spacing
    
    def design_spiral_reinforcement(self, geometry: ColumnGeometry,
                                  material_props: MaterialProperties) -> Tuple[str, float, float]:
        """
        Design spiral reinforcement for spiral columns
        ACI 318M-25 Section 25.7.3
        
        Args:
            geometry: Column geometric properties
            material_props: Material properties
            
        Returns:
            Tuple of (spiral_bar_size, pitch_mm, volumetric_ratio)
        """
        if geometry.shape != ColumnShape.CIRCULAR:
            raise ValueError("Spiral reinforcement only applicable to circular columns")
        
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        
        # Core dimensions
        dc = geometry.width - 2 * geometry.cover  # Core diameter
        Ac = math.pi * (dc / 2) ** 2  # Core area
        Ag = math.pi * (geometry.width / 2) ** 2  # Gross area
        
        # Required volumetric ratio - ACI 318M-25 Eq. (25.7.3.3)
        rho_s = 0.45 * (Ag / Ac - 1) * (fc_prime / fy)
        
        # Minimum volumetric ratio
        rho_s_min = self.confinement_requirements['min_spiral_ratio'] * (fc_prime / fy)
        rho_s = max(rho_s, rho_s_min)
        
        # Select spiral bar size
        spiral_bar = '10M'  # Start with minimum practical size
        As_spiral = self.aci.get_bar_area(spiral_bar)
        
        # Calculate required pitch
        # rho_s = 4 * As / (dc * s)
        s_required = 4 * As_spiral / (dc * rho_s)
        
        # Check minimum clear spacing
        min_clear_spacing = self.confinement_requirements['spiral_clear_spacing']
        spiral_diameter = self.aci.get_bar_diameter(spiral_bar)
        s_min = min_clear_spacing + spiral_diameter
        
        if s_required < s_min:
            # Try larger spiral bar
            spiral_bar = '15M'
            As_spiral = self.aci.get_bar_area(spiral_bar)
            s_required = 4 * As_spiral / (dc * rho_s)
        
        spiral_pitch = max(s_required, s_min)
        
        # Maximum pitch - ACI 318M-25 Section 25.7.3.1
        s_max = min(75.0, dc / 6)
        spiral_pitch = min(spiral_pitch, s_max)
        
        return spiral_bar, spiral_pitch, rho_s
    
    def calculate_axial_capacity(self, geometry: ColumnGeometry,
                               material_props: MaterialProperties,
                               steel_area: float) -> float:
        """
        Calculate nominal axial capacity
        ACI 318M-25 Section 22.4.2
        
        Args:
            geometry: Column geometric properties
            material_props: Material properties
            steel_area: Longitudinal steel area (mm²)
            
        Returns:
            Nominal axial capacity Pn (kN)
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        
        # Gross cross-sectional area
        if geometry.shape == ColumnShape.RECTANGULAR:
            Ag = geometry.width * geometry.depth
        elif geometry.shape == ColumnShape.CIRCULAR:
            Ag = math.pi * (geometry.width / 2) ** 2
        else:
            Ag = geometry.width * geometry.depth
        
        # Nominal axial capacity - ACI 318M-25 Eq. (22.4.2.2)
        if geometry.column_type == ColumnType.TIED:
            Pn = 0.80 * (0.85 * fc_prime * (Ag - steel_area) + fy * steel_area)
        else:  # Spiral column
            Pn = 0.85 * (0.85 * fc_prime * (Ag - steel_area) + fy * steel_area)
        
        # Convert to kN
        Pn = Pn / 1000
        
        return Pn
    
    def check_slenderness_effects(self, geometry: ColumnGeometry,
                                loads: ColumnLoads) -> Tuple[bool, float]:
        """
        Check if slenderness effects need to be considered
        ACI 318M-25 Section 6.2
        
        Args:
            geometry: Column geometric properties
            loads: Column load conditions
            
        Returns:
            Tuple of (slenderness_required, magnification_factor)
        """
        # Effective length factor k (assumed as 1.0 for pinned-pinned)
        k = 1.0  # This should be calculated based on frame analysis
        
        # Radius of gyration
        if geometry.shape == ColumnShape.RECTANGULAR:
            r = geometry.depth / (2 * math.sqrt(3))  # For rectangular section
        elif geometry.shape == ColumnShape.CIRCULAR:
            r = geometry.width / 4  # For circular section
        else:
            r = min(geometry.width, geometry.depth) / (2 * math.sqrt(3))
        
        # Slenderness ratio
        kl_r = k * geometry.effective_length / r
        
        # Slenderness limits - ACI 318M-25 Section 6.2.5
        if loads.load_condition == LoadCondition.AXIAL_ONLY:
            limit = 22
        else:
            # For columns with moments
            M1 = min(abs(loads.moment_x), abs(loads.moment_y))
            M2 = max(abs(loads.moment_x), abs(loads.moment_y))
            M1_M2 = M1 / M2 if M2 > 0 else 0
            limit = 34 - 12 * M1_M2
            limit = max(limit, 22)
        
        slenderness_required = kl_r > limit
        
        # Simplified magnification factor (detailed analysis needed)
        if slenderness_required:
            magnification_factor = 1.0 + 0.1 * (kl_r - limit) / limit
        else:
            magnification_factor = 1.0
        
        return slenderness_required, magnification_factor
    
    def calculate_pm_interaction(self, geometry: ColumnGeometry,
                               material_props: MaterialProperties,
                               steel_area: float,
                               loads: ColumnLoads) -> float:
        """
        Calculate P-M interaction ratio
        Simplified approach - full interaction diagram needed for precise analysis
        
        Args:
            geometry: Column geometric properties
            material_props: Material properties
            steel_area: Longitudinal steel area (mm²)
            loads: Column load conditions
            
        Returns:
            Interaction ratio (demand/capacity)
        """
        # Calculate capacities
        Pn = self.calculate_axial_capacity(geometry, material_props, steel_area)
        
        # Simplified moment capacity (detailed analysis needed)
        # This is a very simplified approach
        if geometry.shape == ColumnShape.RECTANGULAR:
            Ag = geometry.width * geometry.depth
            Mnx = steel_area * material_props.fy * geometry.depth * 0.8 / 1e6  # Very simplified
            Mny = steel_area * material_props.fy * geometry.width * 0.8 / 1e6
        else:
            Ag = math.pi * (geometry.width / 2) ** 2
            Mnx = Mny = steel_area * material_props.fy * geometry.width * 0.6 / 1e6
        
        # Get appropriate phi factor
        if geometry.column_type == ColumnType.TIED:
            phi = self.phi_factors['compression_tied']
        else:
            phi = self.phi_factors['compression_spiral']
        
        # Interaction check (simplified)
        P_ratio = loads.axial_force / (phi * Pn)
        Mx_ratio = abs(loads.moment_x) / (phi * Mnx) if Mnx > 0 else 0
        My_ratio = abs(loads.moment_y) / (phi * Mny) if Mny > 0 else 0
        
        # Simplified interaction equation
        if P_ratio >= 0.1:
            interaction_ratio = P_ratio + (8.0/9.0) * (Mx_ratio + My_ratio)
        else:
            interaction_ratio = P_ratio / 2.0 + Mx_ratio + My_ratio
        
        return interaction_ratio
    
    def _calculate_additional_steel_for_moment(self, loads: ColumnLoads,
                                             geometry: ColumnGeometry,
                                             material_props: MaterialProperties) -> float:
        """Calculate additional steel needed for moment resistance"""
        # Simplified calculation - detailed P-M interaction needed
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        
        # Approximate additional steel for moment
        if geometry.shape == ColumnShape.RECTANGULAR:
            lever_arm = 0.8 * geometry.depth
            As_moment = abs(loads.moment_x) * 1e6 / (fy * lever_arm)
        else:
            lever_arm = 0.6 * geometry.width
            As_moment = max(abs(loads.moment_x), abs(loads.moment_y)) * 1e6 / (fy * lever_arm)
        
        return As_moment
    
    def select_longitudinal_reinforcement(self, As_required: float) -> List[str]:
        """Select longitudinal reinforcement bars"""
        # Available bar sizes and areas
        bar_data = [
            ('20M', 300), ('25M', 500), ('30M', 700),
            ('35M', 1000), ('45M', 1500), ('55M', 2500)
        ]
        
        selected_bars = []
        min_bars = self.reinforcement_limits['min_bars']
        
        # Try to use uniform bar sizes
        for bar_size, area in bar_data:
            num_bars = round(As_required / area)
            if num_bars >= min_bars and abs(num_bars * area - As_required) / As_required < 0.1:
                selected_bars = [bar_size] * num_bars
                break
        
        # If no good match, use combination
        if not selected_bars:
            remaining_area = As_required
            for bar_size, area in reversed(bar_data):
                num_bars = int(remaining_area / area)
                if num_bars > 0:
                    selected_bars.extend([bar_size] * num_bars)
                    remaining_area -= num_bars * area
                    if remaining_area <= 0:
                        break
            
            # Ensure minimum number of bars
            while len(selected_bars) < min_bars:
                selected_bars.append('20M')
        
        return selected_bars
    
    def perform_complete_column_design(self, loads: ColumnLoads,
                                     geometry: ColumnGeometry,
                                     material_props: MaterialProperties) -> ColumnAnalysisResult:
        """
        Perform complete column design analysis
        
        Args:
            loads: Column load conditions
            geometry: Column geometric properties
            material_props: Material properties
            
        Returns:
            Complete column analysis results
        """
        design_notes = []
        
        # Calculate required longitudinal steel
        As_required = self.calculate_required_longitudinal_steel(loads, geometry, material_props)
        longitudinal_bars = self.select_longitudinal_reinforcement(As_required)
        As_provided = sum(self.aci.get_bar_area(bar) for bar in longitudinal_bars)
        
        # Design confinement reinforcement
        if geometry.column_type == ColumnType.TIED:
            tie_size, tie_spacing = self.design_tie_reinforcement(geometry, longitudinal_bars)
            spiral_bar, spiral_pitch, volumetric_ratio = "", 0.0, 0.0
        else:
            spiral_bar, spiral_pitch, volumetric_ratio = self.design_spiral_reinforcement(
                geometry, material_props
            )
            tie_size, tie_spacing = "", 0.0
        
        # Check slenderness effects
        slenderness_required, magnification_factor = self.check_slenderness_effects(geometry, loads)
        
        # Calculate capacities
        axial_capacity = self.calculate_axial_capacity(geometry, material_props, As_provided)
        
        # P-M interaction analysis
        interaction_ratio = self.calculate_pm_interaction(
            geometry, material_props, As_provided, loads
        )
        
        # Apply magnification for slenderness if needed
        if slenderness_required:
            adjusted_loads = ColumnLoads(
                axial_force=loads.axial_force,
                moment_x=loads.moment_x * magnification_factor,
                moment_y=loads.moment_y * magnification_factor,
                shear_x=loads.shear_x,
                shear_y=loads.shear_y,
                load_condition=loads.load_condition
            )
            interaction_ratio = self.calculate_pm_interaction(
                geometry, material_props, As_provided, adjusted_loads
            )
        
        # Design notes
        if slenderness_required:
            design_notes.append(f"Slenderness effects considered (λ = {magnification_factor:.2f})")
        
        if As_provided > As_required * 1.5:
            design_notes.append("Consider reducing steel area or increasing section size")
        
        if interaction_ratio > 1.0:
            design_notes.append("Section inadequate - increase size or steel")
        
        # Create result objects
        reinforcement = ColumnReinforcement(
            longitudinal_bars=longitudinal_bars,
            longitudinal_area=As_provided,
            tie_bars=tie_size,
            tie_spacing=tie_spacing,
            spiral_bar=spiral_bar,
            spiral_pitch=spiral_pitch,
            confinement_ratio=volumetric_ratio
        )
        
        capacity = ColumnCapacity(
            axial_capacity=axial_capacity,
            moment_capacity_x=0.0,  # Simplified - needs detailed analysis
            moment_capacity_y=0.0,  # Simplified - needs detailed analysis
            interaction_ratio=interaction_ratio,
            slenderness_effects=slenderness_required
        )
        
        return ColumnAnalysisResult(
            capacity=capacity,
            reinforcement=reinforcement,
            utilization_ratio=interaction_ratio,
            stability_index=0.0,  # Would need frame analysis
            design_notes=design_notes
        )