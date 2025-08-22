"""
ACI Standards Package
=====================

Implementation of American Concrete Institute (ACI) design standards.

อิมพลีเมนเทชันของมาตรฐานการออกแบบสถาบันคอนกรีตอเมริกัน (ACI)
"""

# Import ACI 318M-25 components
try:
    from structural_standards.aci.aci318m25 import (
        ACI318M25Standard,
        ACI318M25Concrete,
        ACI318M25Steel,
        ACI318M25SlabDesign,
        ACI318M25BeamDesign,
        ACI318M25ColumnDesign
    )
    
    __all__ = [
        'ACI318M25Standard',
        'ACI318M25Concrete', 
        'ACI318M25Steel',
        'ACI318M25SlabDesign',
        'ACI318M25BeamDesign',
        'ACI318M25ColumnDesign'
    ]
    
except ImportError as e:
    # ACI modules not available
    __all__ = []

# Package metadata
__version__ = '1.0.0'
__author__ = 'Structural Design Standards Team'