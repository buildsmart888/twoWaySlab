"""
Utilities Package
=================

Common utilities for structural design standards including:
- Unit conversions
- Input validation  
- Mathematical calculations
- Exception handling

เครื่องมือช่วยทั่วไปสำหรับมาตรฐานการออกแบบโครงสร้าง รวมถึง:
- การแปลงหน่วย
- การตรวจสอบข้อมูลนำเข้า
- การคำนวณทางคณิตศาสตร์
- การจัดการข้อผิดพลาด
"""

from structural_standards.utils.validation import (
    ValidationError,
    validate_positive,
    validate_range,
    validate_type,
    validate_in_list
)

from structural_standards.utils.units import (
    UnitConverter,
    UnitSystem,
    convert_pressure,
    convert_force,
    convert_length,
    convert_moment
)

from structural_standards.utils.calculations import (
    moment_area_rectangular,
    moment_area_circular,
    section_modulus_rectangular,
    elastic_deflection_simple_beam_udl
)

__all__ = [
    # Validation
    'ValidationError',
    'validate_positive',
    'validate_range', 
    'validate_type',
    'validate_in_list',
    
    # Units
    'UnitConverter',
    'UnitSystem',
    'convert_pressure',
    'convert_force',
    'convert_length',
    'convert_moment',
    
    # Calculations
    'moment_area_rectangular',
    'moment_area_circular',
    'section_modulus_rectangular',
    'elastic_deflection_simple_beam_udl'
]