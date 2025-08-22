# -*- coding: utf-8 -*-

"""
ACI 318M-25 Wall Design Library
Building Code Requirements for Structural Concrete - Wall Design

Based on:
- ACI CODE-318M-25 International System of Units
- Chapter 11: Wall Design
- Chapter 14: Walls
- Chapter 18: Earthquake-Resistant Structures

@author: Enhanced by AI Assistant  
@date: 2024
@version: 1.0
"""

import math
from typing import Dict, Tuple, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from aci318m25 import ACI318M25, ConcreteStrengthClass, ReinforcementGrade, MaterialProperties

class WallType(Enum):
    """Types of walls"""
    BEARING_WALL = "bearing_wall"
    SHEAR_WALL = "shear_wall"
    RETAINING_WALL = "retaining_wall"
    BASEMENT_WALL = "basement_wall"
    TILT_UP_WALL = "tilt_up_wall"
    PRECAST_WALL = "precast_wall"

class WallSupportCondition(Enum):
    """Wall support conditions"""
    FIXED_TOP_BOTTOM = "fixed_top_bottom"
    PINNED_TOP_BOTTOM = "pinned_top_bottom"
    FIXED_BOTTOM_FREE_TOP = "fixed_bottom_free_top"
    CANTILEVER = "cantilever"

class LoadType(Enum):
    """Load types for wall design"""
    GRAVITY_ONLY = "gravity_only"
    LATERAL_WIND = "lateral_wind"
    LATERAL_SEISMIC = "lateral_seismic"
    SOIL_PRESSURE = "soil_pressure"
    COMBINED = "combined"

@dataclass
class WallGeometry:
    """Wall geometry properties"""
    length: float             # Wall length (mm)
    height: float             # Wall height (mm)
    thickness: float          # Wall thickness (mm)
    cover: float              # Concrete cover (mm)
    effective_length: float   # Effective length for buckling (mm)
    wall_type: WallType       # Type of wall
    support_condition: WallSupportCondition

@dataclass
class WallLoads:
    """Wall loading conditions"""
    axial_force: float        # Factored axial force per unit length (kN/m)
    in_plane_shear: float     # Factored in-plane shear (kN)
    out_plane_moment: float   # Factored out-of-plane moment (kN⋅m/m)
    out_plane_shear: float    # Factored out-of-plane shear (kN/m)
    lateral_pressure: float   # Lateral pressure (kPa)
    load_type: LoadType       # Type of loading

@dataclass
class WallReinforcement:
    """Wall reinforcement design"""
    vertical_bars: str        # Vertical reinforcement bar size
    vertical_spacing: float   # Vertical bar spacing (mm)
    horizontal_bars: str      # Horizontal reinforcement bar size
    horizontal_spacing: float # Horizontal bar spacing (mm)
    boundary_elements: bool   # Whether boundary elements required
    boundary_bars: str        # Boundary element longitudinal bars
    boundary_ties: str        # Boundary element ties
    tie_spacing: float        # Tie spacing in boundary elements (mm)

@dataclass
class WallAnalysisResult:
    """Complete wall analysis results"""
    axial_capacity: float     # Axial capacity (kN/m)
    shear_capacity: float     # Shear capacity (kN)
    moment_capacity: float    # Moment capacity (kN⋅m/m)
    buckling_capacity: float  # Buckling capacity (kN/m)
    reinforcement: WallReinforcement
    utilization_ratio: float # Maximum utilization ratio
    stability_ok: bool       # Stability check result
    design_notes: List[str]   # Design notes and warnings

class ACI318M25WallDesign:
    """
    ACI 318M-25 Wall Design Library
    
    Comprehensive wall design according to ACI 318M-25:
    - Bearing wall design (Chapter 11)
    - Shear wall design (Chapter 11)
    - Retaining wall design
    - Buckling and stability checks
    - Seismic design provisions (Chapter 18)
    """
    
    def __init__(self):
        """Initialize wall design calculator"""
        self.aci = ACI318M25()
        
        # Strength reduction factors φ - ACI 318M-25 Section 21.2
        self.phi_factors = {
            'compression_tied': 0.65,
            'compression_spiral': 0.75,
            'flexure': 0.90,
            'shear': 0.75,
            'bearing': 0.65
        }
        
        # Minimum reinforcement requirements - ACI 318M-25 Section 11.6
        self.min_reinforcement = {
            'vertical_ratio_grade420': 0.0012,      # For fy = 420 MPa
            'vertical_ratio_grade520': 0.0015,      # For fy = 520 MPa
            'horizontal_ratio': 0.0020,             # Horizontal reinforcement
            'max_spacing_vertical': 450,            # Maximum vertical bar spacing (mm)
            'max_spacing_horizontal': 450,          # Maximum horizontal bar spacing (mm)
            'min_bar_size': '15M'                   # Minimum bar size
        }
        
        # Slenderness limits
        self.slenderness_limits = {
            'bearing_wall': 30,       # kl_u/r limit for bearing walls
            'shear_wall': 30,         # Height-to-thickness ratio for shear walls
            'cantilever_wall': 22     # Special limit for cantilever walls
        }
        
        # Boundary element requirements
        self.boundary_requirements = {
            'compression_strain_limit': 0.003,
            'neutral_axis_limit': 0.1,  # c/lw limit for boundary elements
            'min_length': 300,          # Minimum boundary element length (mm)
            'min_confinement_ratio': 0.09
        }
    
    def calculate_minimum_wall_thickness(self, geometry: WallGeometry,
                                       material_props: MaterialProperties) -> float:
        """
        Calculate minimum wall thickness requirements
        ACI 318M-25 Section 14.5
        
        Args:
            geometry: Wall geometric properties
            material_props: Material properties
            
        Returns:
            Minimum required thickness (mm)
        """
        height = geometry.height
        
        if geometry.wall_type == WallType.BEARING_WALL:
            # Bearing wall minimum thickness - ACI 318M-25 Section 14.5.3.1
            t_min_bearing = height / 25  # h/25 for bearing walls
            t_min_abs = 100              # Absolute minimum 100mm
            
        elif geometry.wall_type == WallType.SHEAR_WALL:
            # Shear wall minimum thickness - ACI 318M-25 Section 11.5.1
            t_min_shear = height / 16    # hw/16 for shear walls
            t_min_abs = 150              # Absolute minimum 150mm
            
        elif geometry.wall_type == WallType.RETAINING_WALL:
            # Retaining wall - based on height and soil pressure
            t_min_retaining = height / 12  # More conservative for lateral loads
            t_min_abs = 200              # Minimum 200mm for retaining walls
            
        else:
            # General wall requirements
            t_min_bearing = height / 30
            t_min_abs = 100
        
        t_min = max(t_min_bearing if 't_min_bearing' in locals() else t_min_shear,
                   t_min_abs)
        
        return t_min
    
    def calculate_axial_capacity(self, geometry: WallGeometry,
                               material_props: MaterialProperties,
                               vertical_steel_ratio: float) -> float:
        """
        Calculate axial capacity of wall
        ACI 318M-25 Section 11.5.2
        
        Args:
            geometry: Wall geometric properties
            material_props: Material properties
            vertical_steel_ratio: Ratio of vertical reinforcement
            
        Returns:
            Axial capacity per unit length (kN/m)
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        t = geometry.thickness
        
        # Gross cross-sectional area per unit length
        Ag = t * 1000  # mm²/m
        
        # Steel area per unit length
        As = vertical_steel_ratio * Ag
        
        # Check slenderness effects
        slenderness_factor = self._calculate_slenderness_factor(geometry)
        
        # Nominal axial capacity - ACI 318M-25 Eq. (11.5.2.1)
        # For walls with slenderness effects
        Pn_wall = 0.55 * fc_prime * Ag * (1 - (geometry.effective_length / (32 * t))**2) + As * fy
        
        # Apply slenderness factor
        Pn_wall *= slenderness_factor
        
        # Convert to kN/m
        Pn = Pn_wall / 1000
        
        return max(Pn, 0)
    
    def calculate_shear_capacity(self, geometry: WallGeometry,
                               material_props: MaterialProperties,
                               horizontal_steel_ratio: float) -> float:
        """
        Calculate in-plane shear capacity of wall
        ACI 318M-25 Section 11.5.4
        
        Args:
            geometry: Wall geometric properties
            material_props: Material properties
            horizontal_steel_ratio: Ratio of horizontal reinforcement
            
        Returns:
            Shear capacity (kN)
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        lw = geometry.length
        t = geometry.thickness
        
        # Effective area
        Acv = lw * t  # mm²
        
        # Concrete contribution to shear strength
        if geometry.wall_type == WallType.SHEAR_WALL:
            # For shear walls - ACI 318M-25 Section 11.5.4.6
            alpha_c = 0.25  # Conservative value
            Vc = alpha_c * math.sqrt(fc_prime) * Acv / 1000  # kN
        else:
            # For bearing walls
            Vc = 0.17 * math.sqrt(fc_prime) * Acv / 1000  # kN
        
        # Steel contribution (horizontal reinforcement)
        As_h = horizontal_steel_ratio * Acv
        Vs = As_h * fy / 1000  # kN
        
        # Total shear capacity
        Vn = Vc + Vs
        
        # Maximum shear capacity limit
        Vn_max = 0.83 * math.sqrt(fc_prime) * Acv / 1000  # kN
        Vn = min(Vn, Vn_max)
        
        return Vn
    
    def calculate_out_of_plane_moment_capacity(self, geometry: WallGeometry,
                                             material_props: MaterialProperties,
                                             vertical_steel_ratio: float) -> float:
        """
        Calculate out-of-plane moment capacity
        ACI 318M-25 Chapter 9
        
        Args:
            geometry: Wall geometric properties
            material_props: Material properties
            vertical_steel_ratio: Ratio of vertical reinforcement
            
        Returns:
            Moment capacity per unit length (kN⋅m/m)
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        t = geometry.thickness
        cover = geometry.cover
        
        # Effective depth
        d = t - cover - 10  # Assume 10mm bar radius
        
        # Steel area per unit length
        As = vertical_steel_ratio * t * 1000  # mm²/m
        
        # Neutral axis depth
        a = As * fy / (0.85 * fc_prime * 1000)  # mm
        
        # Check if tension-controlled
        c = a / 0.85
        epsilon_t = 0.003 * (d - c) / c
        
        if epsilon_t >= 0.005:  # Tension-controlled
            phi = self.phi_factors['flexure']
        else:
            phi = 0.65 + (epsilon_t - 0.002) * (0.25 / 0.003)  # Transition zone
            phi = max(phi, 0.65)
        
        # Nominal moment capacity
        Mn = As * fy * (d - a/2) / 1e6  # kN⋅m/m
        
        return phi * Mn
    
    def design_vertical_reinforcement(self, geometry: WallGeometry,
                                    loads: WallLoads,
                                    material_props: MaterialProperties) -> Tuple[str, float]:
        """
        Design vertical reinforcement for wall
        
        Args:
            geometry: Wall geometric properties
            loads: Wall loading conditions
            material_props: Material properties
            
        Returns:
            Tuple of (bar_size, spacing_mm)
        """
        fy = material_props.fy
        
        # Calculate required steel ratio
        if loads.load_type == LoadType.GRAVITY_ONLY:
            # Minimum reinforcement for gravity loads
            if fy <= 420:
                rho_required = self.min_reinforcement['vertical_ratio_grade420']
            else:
                rho_required = self.min_reinforcement['vertical_ratio_grade520']
        else:
            # Additional reinforcement for lateral loads
            # Simplified approach - detailed analysis needed
            additional_ratio = abs(loads.out_plane_moment) * 0.0001  # Simplified
            if fy <= 420:
                rho_required = self.min_reinforcement['vertical_ratio_grade420'] + additional_ratio
            else:
                rho_required = self.min_reinforcement['vertical_ratio_grade520'] + additional_ratio
        
        # Calculate required area per unit length
        As_required = rho_required * geometry.thickness * 1000  # mm²/m
        
        # Select bar size and spacing
        return self._select_wall_reinforcement(As_required, 'vertical')
    
    def design_horizontal_reinforcement(self, geometry: WallGeometry,
                                      loads: WallLoads,
                                      material_props: MaterialProperties) -> Tuple[str, float]:
        """
        Design horizontal reinforcement for wall
        
        Args:
            geometry: Wall geometric properties
            loads: Wall loading conditions
            material_props: Material properties
            
        Returns:
            Tuple of (bar_size, spacing_mm)
        """
        fy = material_props.fy
        
        # Minimum horizontal reinforcement - ACI 318M-25 Section 11.6.2
        rho_min = self.min_reinforcement['horizontal_ratio']
        
        # Additional reinforcement for shear if required
        if loads.in_plane_shear > 0:
            # Calculate additional steel for shear
            Vu = loads.in_plane_shear
            fc_prime = material_props.fc_prime
            Acv = geometry.length * geometry.thickness
            
            # Concrete shear strength
            Vc = 0.17 * math.sqrt(fc_prime) * Acv / 1000  # kN
            
            # Required steel shear strength
            Vs_required = max(0, Vu / self.phi_factors['shear'] - Vc)
            
            # Required horizontal steel area
            As_shear = Vs_required * 1000 / fy  # mm²
            As_shear_ratio = As_shear / Acv
            
            rho_required = max(rho_min, As_shear_ratio)
        else:
            rho_required = rho_min
        
        # Calculate required area per unit length
        As_required = rho_required * geometry.thickness * 1000  # mm²/m
        
        # Select bar size and spacing
        return self._select_wall_reinforcement(As_required, 'horizontal')
    
    def check_boundary_elements(self, geometry: WallGeometry,
                              loads: WallLoads,
                              material_props: MaterialProperties) -> bool:
        """
        Check if boundary elements are required
        ACI 318M-25 Section 18.10.6
        
        Args:
            geometry: Wall geometric properties
            loads: Wall loading conditions
            material_props: Material properties
            
        Returns:
            True if boundary elements required
        """
        if geometry.wall_type != WallType.SHEAR_WALL:
            return False
        
        if loads.load_type not in [LoadType.LATERAL_SEISMIC, LoadType.COMBINED]:
            return False
        
        # Simplified check - detailed analysis needed
        # Check compression strain and neutral axis location
        
        # Estimate neutral axis location
        P = loads.axial_force * geometry.length  # Total axial force
        M = loads.out_plane_moment * geometry.length  # Total moment
        
        if M > 0:
            # Estimate c/lw ratio
            c_lw_ratio = P / (0.85 * material_props.fc_prime * geometry.thickness * geometry.length)
            
            if c_lw_ratio > self.boundary_requirements['neutral_axis_limit']:
                return True
        
        # Additional checks based on displacement ductility (simplified)
        return False
    
    def _calculate_slenderness_factor(self, geometry: WallGeometry) -> float:
        """Calculate slenderness reduction factor"""
        klu_r = geometry.effective_length / (geometry.thickness / 3.46)  # k*lu/r
        
        if geometry.wall_type == WallType.BEARING_WALL:
            limit = self.slenderness_limits['bearing_wall']
        elif geometry.wall_type == WallType.SHEAR_WALL:
            # For shear walls, use height-to-thickness ratio
            ht_ratio = geometry.height / geometry.thickness
            if ht_ratio <= self.slenderness_limits['shear_wall']:
                return 1.0
            else:
                return max(0.7, 1.0 - (ht_ratio - 30) * 0.01)
        else:
            limit = self.slenderness_limits['cantilever_wall']
        
        if klu_r <= limit:
            return 1.0
        else:
            # Simplified reduction factor
            return max(0.5, 1.0 - (klu_r - limit) / (2 * limit))
    
    def _select_wall_reinforcement(self, As_required: float, 
                                 direction: str) -> Tuple[str, float]:
        """Select appropriate bar size and spacing for wall"""
        # Common wall bar sizes
        bar_sizes = ['10M', '15M', '20M', '25M']
        
        for bar_size in bar_sizes:
            bar_area = self.aci.get_bar_area(bar_size)
            spacing = bar_area * 1000 / As_required  # Spacing for 1m length
            
            # Check spacing limits
            if direction == 'vertical':
                max_spacing = self.min_reinforcement['max_spacing_vertical']
            else:
                max_spacing = self.min_reinforcement['max_spacing_horizontal']
            
            min_spacing = 75  # Minimum practical spacing
            
            if min_spacing <= spacing <= max_spacing:
                return bar_size, spacing
        
        # If no suitable spacing, use maximum allowed
        bar_size = '15M'
        bar_area = self.aci.get_bar_area(bar_size)
        spacing = min(max_spacing, bar_area * 1000 / As_required)
        
        return bar_size, spacing
    
    def perform_complete_wall_design(self, geometry: WallGeometry,
                                   loads: WallLoads,
                                   material_props: MaterialProperties) -> WallAnalysisResult:
        """
        Perform complete wall design analysis
        
        Args:
            geometry: Wall geometric properties
            loads: Wall loading conditions
            material_props: Material properties
            
        Returns:
            Complete wall analysis results
        """
        design_notes = []
        
        # Check minimum thickness
        t_min = self.calculate_minimum_wall_thickness(geometry, material_props)
        if geometry.thickness < t_min:
            design_notes.append(f"Increase thickness to minimum {t_min:.0f}mm")
        
        # Design reinforcement
        vert_bar, vert_spacing = self.design_vertical_reinforcement(geometry, loads, material_props)
        horiz_bar, horiz_spacing = self.design_horizontal_reinforcement(geometry, loads, material_props)
        
        # Calculate steel ratios
        vert_steel_ratio = self.aci.get_bar_area(vert_bar) / (vert_spacing * geometry.thickness)
        horiz_steel_ratio = self.aci.get_bar_area(horiz_bar) / (horiz_spacing * geometry.thickness)
        
        # Calculate capacities
        axial_capacity = self.calculate_axial_capacity(geometry, material_props, vert_steel_ratio)
        shear_capacity = self.calculate_shear_capacity(geometry, material_props, horiz_steel_ratio)
        moment_capacity = self.calculate_out_of_plane_moment_capacity(geometry, material_props, vert_steel_ratio)
        
        # Buckling capacity (simplified)
        slenderness_factor = self._calculate_slenderness_factor(geometry)
        buckling_capacity = axial_capacity * slenderness_factor
        
        # Check boundary elements
        boundary_required = self.check_boundary_elements(geometry, loads, material_props)
        
        # Design boundary elements if required
        if boundary_required:
            boundary_bars = '25M'  # Simplified
            boundary_ties = '10M'
            tie_spacing = 100.0    # Close spacing for confinement
            design_notes.append("Boundary elements required for seismic design")
        else:
            boundary_bars = 'None'
            boundary_ties = 'None'
            tie_spacing = 0.0
        
        # Calculate utilization ratios
        utilization_axial = abs(loads.axial_force) / axial_capacity if axial_capacity > 0 else 0
        utilization_shear = abs(loads.in_plane_shear) / (self.phi_factors['shear'] * shear_capacity) if shear_capacity > 0 else 0
        utilization_moment = abs(loads.out_plane_moment) / moment_capacity if moment_capacity > 0 else 0
        
        utilization_ratio = max(utilization_axial, utilization_shear, utilization_moment)
        
        # Stability check
        stability_ok = utilization_ratio <= 1.0 and slenderness_factor > 0.5
        
        if not stability_ok:
            design_notes.append("Stability concerns - check slenderness and loading")
        
        if utilization_ratio > 1.0:
            design_notes.append("Design inadequate - increase section or reinforcement")
        
        # Create result objects
        reinforcement = WallReinforcement(
            vertical_bars=vert_bar,
            vertical_spacing=vert_spacing,
            horizontal_bars=horiz_bar,
            horizontal_spacing=horiz_spacing,
            boundary_elements=boundary_required,
            boundary_bars=boundary_bars,
            boundary_ties=boundary_ties,
            tie_spacing=tie_spacing
        )
        
        return WallAnalysisResult(
            axial_capacity=axial_capacity,
            shear_capacity=shear_capacity,
            moment_capacity=moment_capacity,
            buckling_capacity=buckling_capacity,
            reinforcement=reinforcement,
            utilization_ratio=utilization_ratio,
            stability_ok=stability_ok,
            design_notes=design_notes
        )