"""
Structural Calculations Utilities
=================================

Common structural engineering calculations and formulas.
คำนวณทางวิศวกรรมโครงสร้างทั่วไป
"""

import math
from typing import Union, Tuple, Optional


def moment_area_rectangular(width: float, height: float) -> float:
    """
    Calculate moment of inertia for rectangular section
    
    Parameters:
    -----------
    width : float
        Section width
    height : float
        Section height
        
    Returns:
    --------
    float
        Moment of inertia about centroidal axis
    """
    return width * height**3 / 12


def moment_area_circular(diameter: float) -> float:
    """
    Calculate moment of inertia for circular section
    
    Parameters:
    -----------
    diameter : float
        Circle diameter
        
    Returns:
    --------
    float
        Moment of inertia about centroidal axis
    """
    return math.pi * diameter**4 / 64


def section_modulus_rectangular(width: float, height: float) -> float:
    """
    Calculate section modulus for rectangular section
    
    Parameters:
    -----------
    width : float
        Section width
    height : float
        Section height
        
    Returns:
    --------
    float
        Section modulus
    """
    return width * height**2 / 6


def section_modulus_circular(diameter: float) -> float:
    """
    Calculate section modulus for circular section
    
    Parameters:
    -----------
    diameter : float
        Circle diameter
        
    Returns:
    --------
    float
        Section modulus
    """
    return math.pi * diameter**3 / 32


def radius_of_gyration_rectangular(width: float, height: float) -> float:
    """
    Calculate radius of gyration for rectangular section
    
    Parameters:
    -----------
    width : float
        Section width
    height : float
        Section height
        
    Returns:
    --------
    float
        Radius of gyration
    """
    area = width * height
    inertia = moment_area_rectangular(width, height)
    return math.sqrt(inertia / area)


def radius_of_gyration_circular(diameter: float) -> float:
    """
    Calculate radius of gyration for circular section
    
    Parameters:
    -----------
    diameter : float
        Circle diameter
        
    Returns:
    --------
    float
        Radius of gyration
    """
    return diameter / 4


def elastic_deflection_simple_beam_udl(
    load: float, 
    span: float, 
    elastic_modulus: float, 
    moment_inertia: float
) -> float:
    """
    Calculate elastic deflection for simply supported beam with UDL
    
    Parameters:
    -----------
    load : float
        Uniformly distributed load
    span : float
        Beam span
    elastic_modulus : float
        Elastic modulus
    moment_inertia : float
        Moment of inertia
        
    Returns:
    --------
    float
        Maximum deflection at midspan
    """
    return 5 * load * span**4 / (384 * elastic_modulus * moment_inertia)


def elastic_deflection_simple_beam_point_load(
    load: float, 
    span: float, 
    elastic_modulus: float, 
    moment_inertia: float
) -> float:
    """
    Calculate elastic deflection for simply supported beam with point load at midspan
    
    Parameters:
    -----------
    load : float
        Point load at midspan
    span : float
        Beam span
    elastic_modulus : float
        Elastic modulus
    moment_inertia : float
        Moment of inertia
        
    Returns:
    --------
    float
        Maximum deflection at midspan
    """
    return load * span**3 / (48 * elastic_modulus * moment_inertia)


def elastic_deflection_cantilever_udl(
    load: float, 
    span: float, 
    elastic_modulus: float, 
    moment_inertia: float
) -> float:
    """
    Calculate elastic deflection for cantilever with UDL
    
    Parameters:
    -----------
    load : float
        Uniformly distributed load
    span : float
        Cantilever length
    elastic_modulus : float
        Elastic modulus
    moment_inertia : float
        Moment of inertia
        
    Returns:
    --------
    float
        Maximum deflection at free end
    """
    return load * span**4 / (8 * elastic_modulus * moment_inertia)


def elastic_deflection_cantilever_point_load(
    load: float, 
    span: float, 
    elastic_modulus: float, 
    moment_inertia: float
) -> float:
    """
    Calculate elastic deflection for cantilever with point load at free end
    
    Parameters:
    -----------
    load : float
        Point load at free end
    span : float
        Cantilever length
    elastic_modulus : float
        Elastic modulus
    moment_inertia : float
        Moment of inertia
        
    Returns:
    --------
    float
        Maximum deflection at free end
    """
    return load * span**3 / (3 * elastic_modulus * moment_inertia)


def slenderness_ratio(length: float, radius_gyration: float) -> float:
    """
    Calculate slenderness ratio
    
    Parameters:
    -----------
    length : float
        Effective length
    radius_gyration : float
        Radius of gyration
        
    Returns:
    --------
    float
        Slenderness ratio
    """
    return length / radius_gyration


def buckling_load_euler(
    elastic_modulus: float, 
    moment_inertia: float, 
    length: float, 
    end_condition_factor: float = 1.0
) -> float:
    """
    Calculate Euler buckling load
    
    Parameters:
    -----------
    elastic_modulus : float
        Elastic modulus
    moment_inertia : float
        Moment of inertia
    length : float
        Column length
    end_condition_factor : float
        End condition factor (K factor)
        
    Returns:
    --------
    float
        Critical buckling load
    """
    effective_length = end_condition_factor * length
    return math.pi**2 * elastic_modulus * moment_inertia / effective_length**2


def interaction_ratio_biaxial(
    mx: float, mnx: float, 
    my: float, mny: float, 
    alpha: float = 1.0
) -> float:
    """
    Calculate biaxial interaction ratio
    
    Parameters:
    -----------
    mx : float
        Applied moment about x-axis
    mnx : float
        Nominal moment capacity about x-axis
    my : float
        Applied moment about y-axis
    mny : float
        Nominal moment capacity about y-axis
    alpha : float
        Interaction exponent
        
    Returns:
    --------
    float
        Interaction ratio
    """
    if mnx <= 0 or mny <= 0:
        return float('inf')
    
    return (abs(mx) / mnx)**alpha + (abs(my) / mny)**alpha


def effective_length_factor(end_condition: str) -> float:
    """
    Get effective length factor (K) based on end conditions
    
    Parameters:
    -----------
    end_condition : str
        End condition type:
        - "fixed_fixed": Both ends fixed
        - "pinned_pinned": Both ends pinned
        - "fixed_pinned": One fixed, one pinned
        - "fixed_free": One fixed, one free (cantilever)
        
    Returns:
    --------
    float
        Effective length factor (K)
    """
    factors = {
        "fixed_fixed": 0.5,
        "pinned_pinned": 1.0,
        "fixed_pinned": 0.7,
        "fixed_free": 2.0
    }
    
    return factors.get(end_condition, 1.0)


def natural_frequency_simple_beam(
    elastic_modulus: float,
    moment_inertia: float,
    mass_per_length: float,
    span: float,
    mode: int = 1
) -> float:
    """
    Calculate natural frequency of simply supported beam
    
    Parameters:
    -----------
    elastic_modulus : float
        Elastic modulus
    moment_inertia : float
        Moment of inertia
    mass_per_length : float
        Mass per unit length
    span : float
        Beam span
    mode : int
        Mode number (1, 2, 3, ...)
        
    Returns:
    --------
    float
        Natural frequency (Hz)
    """
    lambda_n = mode * math.pi
    omega = lambda_n**2 * math.sqrt(elastic_modulus * moment_inertia / mass_per_length) / span**2
    return omega / (2 * math.pi)


def shear_lag_factor(
    flange_width: float,
    web_spacing: float,
    span: float
) -> float:
    """
    Calculate shear lag factor for wide flange sections
    
    Parameters:
    -----------
    flange_width : float
        Total flange width
    web_spacing : float
        Distance between webs
    span : float
        Beam span
        
    Returns:
    --------
    float
        Shear lag factor
    """
    # Simplified shear lag factor calculation
    effective_width_ratio = min(1.0, span / (4 * flange_width))
    return effective_width_ratio


def punching_shear_perimeter(
    column_width: float,
    column_depth: float,
    slab_thickness: float
) -> float:
    """
    Calculate punching shear critical perimeter
    
    Parameters:
    -----------
    column_width : float
        Column width
    column_depth : float
        Column depth
    slab_thickness : float
        Slab thickness
        
    Returns:
    --------
    float
        Critical perimeter at d/2 from column face
    """
    d = slab_thickness * 0.9  # Approximate effective depth
    critical_perimeter = 2 * (column_width + column_depth) + 4 * math.pi * (d / 2)
    return critical_perimeter


def development_length_basic(
    bar_diameter: float,
    fy: float,
    fc_prime: float,
    modification_factors: float = 1.0
) -> float:
    """
    Calculate basic development length for reinforcement
    
    Parameters:
    -----------
    bar_diameter : float
        Bar diameter
    fy : float
        Yield strength of steel
    fc_prime : float
        Compressive strength of concrete
    modification_factors : float
        Combined modification factors
        
    Returns:
    --------
    float
        Development length
    """
    # Simplified formula - actual calculation depends on specific code
    sqrt_fc = math.sqrt(fc_prime)
    basic_length = (fy * bar_diameter) / (2.1 * sqrt_fc)
    return basic_length * modification_factors


# Constants for common calculations
STEEL_UNIT_WEIGHT = 77.0  # kN/m³
CONCRETE_UNIT_WEIGHT = 24.0  # kN/m³
STEEL_ELASTIC_MODULUS = 200000.0  # MPa