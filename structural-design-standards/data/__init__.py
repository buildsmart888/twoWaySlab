"""
Data Package
============

Contains material databases, validation data, and reference solutions
for structural design standards verification and benchmarking.

Structure:
- material_databases/: Standard material property databases
- validation_data/: Test data for validation
- reference_solutions/: Known solutions for verification
"""

from .material_databases import *
from .validation_data import *
from .reference_solutions import *

__all__ = [
    # Material databases
    'ACI_CONCRETE_GRADES',
    'ACI_STEEL_GRADES',
    'THAI_CONCRETE_GRADES',
    'THAI_STEEL_GRADES',
    
    # Validation data
    'BEAM_TEST_CASES',
    'COLUMN_TEST_CASES',
    'LOAD_COMBINATION_CASES',
    
    # Reference solutions
    'ACI_REFERENCE_SOLUTIONS',
    'THAI_REFERENCE_SOLUTIONS'
]