# -*- coding: utf-8 -*-

"""
ACI 318M-25 Diaphragm Design Library
Building Code Requirements for Structural Concrete - Diaphragm Design

Based on:
- ACI CODE-318M-25 International System of Units
- Chapter 12: Diaphragms and Collectors
- Chapter 18: Earthquake-Resistant Structures
- ASCE 7: Minimum Design Loads for Buildings

@author: Enhanced by AI Assistant  
@date: 2024
@version: 1.0
"""

import math
from typing import Dict, Tuple, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from aci318m25 import ACI318M25, ConcreteStrengthClass, ReinforcementGrade, MaterialProperties

class DiaphragmType(Enum):
    """Types of diaphragms for design"""
    CONCRETE_SLAB = "concrete_slab"
    CONCRETE_FILL = "concrete_fill"
    PRECAST_CONCRETE = "precast_concrete"
    COMPOSITE_DECK = "composite_deck"
    TOPPING_SLAB = "topping_slab"

class DiaphragmLoadType(Enum):
    """Load types for diaphragm design"""
    SEISMIC = "seismic"
    WIND = "wind"
    EXPLOSION = "explosion"
    PROGRESSIVE_COLLAPSE = "progressive_collapse"
    CONSTRUCTION_LOADS = "construction_loads"

class DiaphragmBehavior(Enum):
    """Diaphragm behavioral classifications"""
    FLEXIBLE = "flexible"
    RIGID = "rigid"
    SEMI_RIGID = "semi_rigid"

class CollectorType(Enum):
    """Types of collector elements"""
    CONCRETE_BEAM = "concrete_beam"
    STEEL_BEAM = "steel_beam"
    CONCRETE_SLAB_BAND = "concrete_slab_band"
    PRESTRESSED_BEAM = "prestressed_beam"

@dataclass
class DiaphragmGeometry:
    """Diaphragm geometry properties"""
    length: float             # Diaphragm length (mm)
    width: float              # Diaphragm width (mm)
    thickness: float          # Diaphragm thickness (mm)
    cover: float              # Concrete cover (mm)
    diaphragm_type: DiaphragmType
    openings: List[Tuple[float, float, float, float]]  # List of (x, y, width, height) for openings
    aspect_ratio: float       # Length to width ratio
    irregularities: List[str] # List of plan irregularities

@dataclass
class DiaphragmLoads:
    """Diaphragm loading conditions"""
    lateral_force: float      # Total lateral force on diaphragm (kN)
    force_distribution: str   # Distribution type ('uniform', 'triangular', 'concentrated')
    seismic_coefficient: float # Seismic design coefficient
    wind_pressure: float      # Wind pressure (kPa)
    load_type: DiaphragmLoadType
    force_direction: float    # Angle of force application (degrees)
    story_shear: float        # Story shear force (kN)

@dataclass
class CollectorDesign:
    """Collector element design"""
    collector_type: CollectorType
    length: float             # Collector length (mm)
    cross_section: Tuple[float, float]  # Width and height (mm)
    axial_force: float        # Axial tension/compression (kN)
    moment: float             # Moment in collector (kN⋅m)
    shear: float              # Shear in collector (kN)
    reinforcement: List[str]  # Required reinforcement
    connection_force: float   # Force transfer to vertical elements (kN)

@dataclass
class DiaphragmReinforcement:
    """Diaphragm reinforcement design"""
    main_bars_x: str          # Main reinforcement in x-direction
    main_spacing_x: float     # Main bar spacing x-direction (mm)
    main_bars_y: str          # Main reinforcement in y-direction
    main_spacing_y: float     # Main bar spacing y-direction (mm)
    chord_reinforcement: List[str]  # Chord reinforcement at edges
    collector_reinforcement: List[CollectorDesign]  # Collector elements
    shear_reinforcement: str  # Additional shear reinforcement if required
    connection_details: Dict[str, str]  # Connection to vertical elements

@dataclass
class DiaphragmAnalysisResult:
    """Complete diaphragm analysis results"""
    in_plane_shear_capacity: float    # In-plane shear capacity (kN)
    out_plane_moment_capacity: float  # Out-of-plane moment capacity (kN⋅m/m)
    chord_force: float                 # Maximum chord force (kN)
    deflection: float                  # Maximum diaphragm deflection (mm)
    flexibility_ratio: float           # Diaphragm flexibility ratio
    behavior_classification: DiaphragmBehavior
    reinforcement: DiaphragmReinforcement
    utilization_ratio: float          # Maximum utilization ratio
    design_notes: List[str]            # Design notes and warnings

class ACI318M25DiaphragmDesign:
    """
    ACI 318M-25 Diaphragm Design Library
    
    Comprehensive diaphragm design according to ACI 318M-25:
    - In-plane shear design (Chapter 12)
    - Diaphragm flexibility assessment
    - Collector element design
    - Chord reinforcement design
    - Seismic design provisions (Chapter 18)
    """
    
    def __init__(self):
        """Initialize diaphragm design calculator"""
        self.aci = ACI318M25()
        
        # Strength reduction factors φ - ACI 318M-25 Section 21.2
        self.phi_factors = {
            'flexure': 0.90,
            'shear': 0.75,
            'axial_tension': 0.90,
            'axial_compression': 0.65
        }
        
        # Diaphragm design requirements
        self.diaphragm_requirements = {
            'min_thickness': {
                'concrete_slab': 100,     # Minimum 100mm for concrete slabs
                'composite_deck': 65,     # Minimum 65mm over metal deck
                'topping_slab': 50        # Minimum 50mm topping
            },
            'min_reinforcement_ratio': 0.0012,  # Minimum reinforcement ratio
            'max_spacing': 450,                  # Maximum bar spacing (mm)
            'min_edge_reinforcement': 0.0015    # Minimum edge reinforcement ratio
        }
        
        # Flexibility criteria
        self.flexibility_criteria = {
            'rigid_limit': 2.0,          # L³/(EI) limit for rigid classification
            'flexible_limit': 10.0,      # L³/(EI) limit for flexible classification
            'deflection_limit_rigid': 'L/1000',     # Deflection limit for rigid diaphragms
            'deflection_limit_flexible': 'L/400'    # Deflection limit for flexible diaphragms
        }
        
        # Seismic design factors
        self.seismic_factors = {
            'amplification_factor': 1.0,    # Diaphragm design force amplification
            'irregularity_penalty': 1.25,   # Penalty for irregular diaphragms
            'collector_amplification': 1.25  # Collector force amplification
        }
    
    def calculate_diaphragm_forces(self, loads: DiaphragmLoads,
                                 geometry: DiaphragmGeometry) -> Dict[str, float]:
        """
        Calculate diaphragm design forces
        ACI 318M-25 Section 12.10
        
        Args:
            loads: Diaphragm loading conditions
            geometry: Diaphragm geometric properties
            
        Returns:
            Dictionary of design forces
        """
        # Basic design force
        if loads.load_type == DiaphragmLoadType.SEISMIC:
            # Seismic diaphragm force per ASCE 7
            base_force = loads.lateral_force
            
            # Apply amplification factors
            if geometry.aspect_ratio > 3.0:
                amplification = 1.25  # For high aspect ratio diaphragms
            else:
                amplification = 1.0
                
            design_force = base_force * amplification
            
        elif loads.load_type == DiaphragmLoadType.WIND:
            # Wind force on diaphragm
            tributary_area = geometry.length * geometry.width / 1e6  # m²
            design_force = loads.wind_pressure * tributary_area
            
        else:
            design_force = loads.lateral_force
        
        # Apply irregularity penalties
        if geometry.irregularities:
            design_force *= self.seismic_factors['irregularity_penalty']
        
        # Calculate unit shear
        effective_width = geometry.width
        if geometry.openings:
            # Reduce effective width for openings
            total_opening_width = sum(opening[2] for opening in geometry.openings)
            effective_width = max(geometry.width - total_opening_width, 0.5 * geometry.width)
        
        unit_shear = design_force / effective_width if effective_width > 0 else 0
        
        # Chord forces at diaphragm boundaries
        moment_arm = geometry.width * 0.9  # Approximate moment arm
        max_moment = design_force * geometry.length / 8  # Simplified for uniform load
        chord_force = max_moment / moment_arm if moment_arm > 0 else 0
        
        return {
            'design_force': design_force,
            'unit_shear': unit_shear,
            'chord_force': chord_force,
            'max_moment': max_moment,
            'effective_width': effective_width
        }
    
    def calculate_shear_capacity(self, geometry: DiaphragmGeometry,
                               material_props: MaterialProperties,
                               reinforcement_ratio: float) -> float:
        """
        Calculate diaphragm shear capacity
        ACI 318M-25 Section 12.10
        
        Args:
            geometry: Diaphragm geometric properties
            material_props: Material properties
            reinforcement_ratio: Reinforcement ratio in critical direction
            
        Returns:
            Nominal shear capacity per unit width (kN/m)
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        t = geometry.thickness
        
        # Concrete contribution to shear strength
        # For diaphragms, use reduced concrete capacity
        if geometry.diaphragm_type == DiaphragmType.CONCRETE_SLAB:
            Vc = 0.17 * math.sqrt(fc_prime) * t * 1000 / 1000  # kN/m
        elif geometry.diaphragm_type == DiaphragmType.COMPOSITE_DECK:
            # Reduced capacity for composite construction
            Vc = 0.12 * math.sqrt(fc_prime) * t * 1000 / 1000  # kN/m
        else:
            Vc = 0.15 * math.sqrt(fc_prime) * t * 1000 / 1000  # kN/m
        
        # Steel contribution (in-plane reinforcement)
        As_per_meter = reinforcement_ratio * t * 1000  # mm²/m
        Vs = As_per_meter * fy / 1000  # kN/m
        
        # Total shear capacity
        Vn = Vc + Vs
        
        # Limit maximum shear capacity
        Vn_max = 0.66 * math.sqrt(fc_prime) * t * 1000 / 1000  # kN/m
        Vn = min(Vn, Vn_max)
        
        return Vn
    
    def assess_diaphragm_flexibility(self, geometry: DiaphragmGeometry,
                                   material_props: MaterialProperties,
                                   loads: DiaphragmLoads) -> Tuple[DiaphragmBehavior, float]:
        """
        Assess diaphragm flexibility per ASCE 7
        
        Args:
            geometry: Diaphragm geometric properties
            material_props: Material properties
            loads: Loading conditions
            
        Returns:
            Tuple of (behavior_classification, flexibility_ratio)
        """
        # Diaphragm properties
        L = max(geometry.length, geometry.width)  # Maximum span
        E = material_props.ec  # Modulus of elasticity
        
        # Moment of inertia per unit width
        t = geometry.thickness
        I = t**3 / 12  # mm⁴/mm
        
        # Flexibility parameter
        flexibility_ratio = (L**3) / (E * I * t)  # Normalized flexibility
        
        # Classification based on flexibility
        if flexibility_ratio <= self.flexibility_criteria['rigid_limit']:
            behavior = DiaphragmBehavior.RIGID
        elif flexibility_ratio >= self.flexibility_criteria['flexible_limit']:
            behavior = DiaphragmBehavior.FLEXIBLE
        else:
            behavior = DiaphragmBehavior.SEMI_RIGID
        
        return behavior, flexibility_ratio
    
    def calculate_diaphragm_deflection(self, geometry: DiaphragmGeometry,
                                     material_props: MaterialProperties,
                                     loads: DiaphragmLoads) -> float:
        """
        Calculate maximum diaphragm deflection
        
        Args:
            geometry: Diaphragm geometric properties
            material_props: Material properties
            loads: Loading conditions
            
        Returns:
            Maximum deflection (mm)
        """
        # Simplified deflection calculation for uniformly loaded diaphragm
        L = max(geometry.length, geometry.width)
        w = loads.lateral_force / L  # Load per unit length
        E = material_props.ec
        t = geometry.thickness
        I = t**3 / 12  # Moment of inertia per unit width
        
        # For simply supported diaphragm with uniform load
        # δ = 5wL⁴/(384EI)
        deflection = (5 * w * L**4) / (384 * E * I)
        
        # Account for shear deformation (approximate)
        shear_deflection = deflection * 0.2  # Approximate 20% additional
        total_deflection = deflection + shear_deflection
        
        return total_deflection
    
    def design_chord_reinforcement(self, chord_force: float,
                                 geometry: DiaphragmGeometry,
                                 material_props: MaterialProperties) -> List[str]:
        """
        Design chord reinforcement at diaphragm edges
        
        Args:
            chord_force: Maximum chord force (kN)
            geometry: Diaphragm geometric properties
            material_props: Material properties
            
        Returns:
            List of required chord reinforcement
        """
        fy = material_props.fy
        
        # Required steel area for chord force
        if chord_force > 0:  # Tension
            phi = self.phi_factors['axial_tension']
            As_required = chord_force * 1000 / (phi * fy)  # mm²
        else:  # Compression
            phi = self.phi_factors['axial_compression']
            # For compression, consider concrete contribution
            fc_prime = material_props.fc_prime
            Ag_chord = geometry.thickness * 1000  # Assume 1m width chord
            Pn_concrete = 0.85 * fc_prime * Ag_chord
            
            if abs(chord_force) * 1000 <= phi * Pn_concrete:
                As_required = self.diaphragm_requirements['min_reinforcement_ratio'] * Ag_chord
            else:
                As_required = (abs(chord_force) * 1000 - phi * Pn_concrete) / (phi * fy)
        
        # Select reinforcement bars
        chord_bars = self._select_chord_reinforcement(As_required)
        
        return chord_bars
    
    def design_collector_elements(self, forces: Dict[str, float],
                                geometry: DiaphragmGeometry,
                                material_props: MaterialProperties) -> List[CollectorDesign]:
        """
        Design collector elements for force transfer
        
        Args:
            forces: Dictionary of design forces
            geometry: Diaphragm geometric properties
            material_props: Material properties
            
        Returns:
            List of collector element designs
        """
        collectors = []
        
        # Estimate collector requirements based on geometry
        if geometry.openings or geometry.aspect_ratio > 2.0:
            # Need collectors for force transfer around openings or in long diaphragms
            
            collector_force = forces['design_force'] * self.seismic_factors['collector_amplification']
            
            # Design typical collector
            collector = CollectorDesign(
                collector_type=CollectorType.CONCRETE_BEAM,
                length=min(geometry.length, geometry.width),
                cross_section=(300, 600),  # Typical beam size
                axial_force=collector_force,
                moment=collector_force * 0.1,  # Small moment due to eccentricity
                shear=collector_force * 0.05,
                reinforcement=self._design_collector_reinforcement(collector_force, material_props),
                connection_force=collector_force
            )
            
            collectors.append(collector)
        
        return collectors
    
    def design_diaphragm_reinforcement(self, forces: Dict[str, float],
                                     geometry: DiaphragmGeometry,
                                     material_props: MaterialProperties) -> DiaphragmReinforcement:
        """
        Design complete diaphragm reinforcement
        
        Args:
            forces: Dictionary of design forces
            geometry: Diaphragm geometric properties
            material_props: Material properties
            
        Returns:
            Complete diaphragm reinforcement design
        """
        fc_prime = material_props.fc_prime
        fy = material_props.fy
        t = geometry.thickness
        
        # Main reinforcement for in-plane shear
        required_shear_capacity = forces['unit_shear'] / self.phi_factors['shear']
        
        # Calculate required reinforcement ratio
        Vc = 0.17 * math.sqrt(fc_prime) * t / 1000  # kN/m
        Vs_required = max(0, required_shear_capacity - Vc)
        
        if Vs_required > 0:
            As_required = Vs_required * 1000 / fy  # mm²/m
            rho_required = As_required / (t * 1000)
        else:
            rho_required = 0
        
        # Check minimum reinforcement
        rho_min = self.diaphragm_requirements['min_reinforcement_ratio']
        rho_design = max(rho_required, rho_min)
        
        # Select reinforcement in both directions
        As_design = rho_design * t * 1000  # mm²/m
        
        main_bar_x, spacing_x = self._select_diaphragm_reinforcement(As_design)
        main_bar_y, spacing_y = self._select_diaphragm_reinforcement(As_design)
        
        # Chord reinforcement
        chord_bars = self.design_chord_reinforcement(
            forces['chord_force'], geometry, material_props
        )
        
        # Collector elements
        collectors = self.design_collector_elements(forces, geometry, material_props)
        
        # Additional shear reinforcement if needed
        if Vs_required > 0.5 * Vc:
            shear_reinforcement = main_bar_x  # Use same as main reinforcement
        else:
            shear_reinforcement = 'None'
        
        return DiaphragmReinforcement(
            main_bars_x=main_bar_x,
            main_spacing_x=spacing_x,
            main_bars_y=main_bar_y,
            main_spacing_y=spacing_y,
            chord_reinforcement=chord_bars,
            collector_reinforcement=collectors,
            shear_reinforcement=shear_reinforcement,
            connection_details={'type': 'standard_dowels', 'size': '20M'}
        )
    
    def _select_diaphragm_reinforcement(self, As_required: float) -> Tuple[str, float]:
        """Select appropriate bar size and spacing for diaphragm"""
        # Common diaphragm bar sizes
        bar_sizes = ['10M', '15M', '20M']
        
        for bar_size in bar_sizes:
            bar_area = self.aci.get_bar_area(bar_size)
            spacing = bar_area * 1000 / As_required  # Spacing for 1m width
            
            # Check spacing limits
            max_spacing = self.diaphragm_requirements['max_spacing']
            min_spacing = 100  # Minimum practical spacing
            
            if min_spacing <= spacing <= max_spacing:
                return bar_size, spacing
        
        # If no suitable spacing, use maximum allowed
        bar_size = '15M'
        bar_area = self.aci.get_bar_area(bar_size)
        spacing = min(max_spacing, bar_area * 1000 / As_required)
        
        return bar_size, spacing
    
    def _select_chord_reinforcement(self, As_required: float) -> List[str]:
        """Select chord reinforcement bars"""
        # Available bar sizes and areas
        bar_data = [
            ('20M', 300), ('25M', 500), ('30M', 700),
            ('35M', 1000), ('45M', 1500)
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
        
        # If we still need more area, add one more bar
        if remaining_area > 0:
            selected_bars.append('20M')
        
        return selected_bars if selected_bars else ['20M', '20M']  # Minimum
    
    def _design_collector_reinforcement(self, axial_force: float,
                                      material_props: MaterialProperties) -> List[str]:
        """Design reinforcement for collector element"""
        fy = material_props.fy
        
        # Required steel area
        phi = self.phi_factors['axial_tension']
        As_required = axial_force * 1000 / (phi * fy)  # mm²
        
        # Select bars
        return self._select_chord_reinforcement(As_required)
    
    def perform_complete_diaphragm_design(self, geometry: DiaphragmGeometry,
                                        loads: DiaphragmLoads,
                                        material_props: MaterialProperties) -> DiaphragmAnalysisResult:
        """
        Perform complete diaphragm design analysis
        
        Args:
            geometry: Diaphragm geometric properties
            loads: Loading conditions
            material_props: Material properties
            
        Returns:
            Complete diaphragm analysis results
        """
        design_notes = []
        
        # Check minimum thickness
        min_thickness = self.diaphragm_requirements['min_thickness'][geometry.diaphragm_type.value]
        if geometry.thickness < min_thickness:
            design_notes.append(f"Increase thickness to minimum {min_thickness}mm")
        
        # Calculate design forces
        forces = self.calculate_diaphragm_forces(loads, geometry)
        
        # Assess flexibility
        behavior, flexibility_ratio = self.assess_diaphragm_flexibility(geometry, material_props, loads)
        
        # Calculate deflection
        deflection = self.calculate_diaphragm_deflection(geometry, material_props, loads)
        
        # Check deflection limits
        L = max(geometry.length, geometry.width)
        if behavior == DiaphragmBehavior.RIGID:
            deflection_limit = L / 1000
        else:
            deflection_limit = L / 400
        
        if deflection > deflection_limit:
            design_notes.append(f"Deflection {deflection:.1f}mm exceeds limit {deflection_limit:.1f}mm")
        
        # Design reinforcement
        reinforcement = self.design_diaphragm_reinforcement(forces, geometry, material_props)
        
        # Calculate capacities
        rho_design = self.diaphragm_requirements['min_reinforcement_ratio']
        shear_capacity = self.calculate_shear_capacity(geometry, material_props, rho_design)
        
        # Out-of-plane moment capacity (simplified)
        As_out_plane = rho_design * geometry.thickness * 1000  # mm²/m
        d = geometry.thickness - geometry.cover - 10  # Effective depth
        a = As_out_plane * material_props.fy / (0.85 * material_props.fc_prime * 1000)
        moment_capacity = As_out_plane * material_props.fy * (d - a/2) / 1e6  # kN⋅m/m
        
        # Calculate utilization ratios
        shear_utilization = forces['unit_shear'] / (self.phi_factors['shear'] * shear_capacity)
        chord_utilization = forces['chord_force'] / (1000)  # Simplified
        
        utilization_ratio = max(shear_utilization, chord_utilization)
        
        # Additional design notes
        if geometry.aspect_ratio > 4.0:
            design_notes.append("High aspect ratio - consider flexible diaphragm analysis")
        
        if geometry.openings:
            design_notes.append("Openings present - verify force transfer around openings")
        
        if behavior == DiaphragmBehavior.FLEXIBLE:
            design_notes.append("Flexible diaphragm - use tributary area method for vertical elements")
        
        if utilization_ratio > 1.0:
            design_notes.append("Design inadequate - increase thickness or reinforcement")
        
        return DiaphragmAnalysisResult(
            in_plane_shear_capacity=shear_capacity,
            out_plane_moment_capacity=moment_capacity,
            chord_force=forces['chord_force'],
            deflection=deflection,
            flexibility_ratio=flexibility_ratio,
            behavior_classification=behavior,
            reinforcement=reinforcement,
            utilization_ratio=utilization_ratio,
            design_notes=design_notes
        )