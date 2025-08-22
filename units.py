#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Unit Conversion System
Handles conversion between different unit systems (Metric, Imperial, etc.)

@author: Enhanced by AI Assistant
@date: 2024
"""

import math

class UnitConverter:
    """
    Unit conversion system for structural engineering
    Supports metric, imperial, and mixed unit systems
    """
    
    def __init__(self):
        # Conversion factors to base units (SI)
        self.length_conversions = {
            # Base unit: meter (m)
            'm': 1.0,
            'mm': 0.001,
            'cm': 0.01,
            'km': 1000.0,
            'ft': 0.3048,
            'in': 0.0254,
            'yd': 0.9144
        }
        
        self.area_conversions = {
            # Base unit: square meter (m²)
            'm2': 1.0,
            'mm2': 1e-6,
            'cm2': 1e-4,
            'ft2': 0.092903,
            'in2': 0.00064516
        }
        
        self.force_conversions = {
            # Base unit: Newton (N)
            'N': 1.0,
            'kN': 1000.0,
            'MN': 1e6,
            'lbf': 4.448222,
            'kip': 4448.222,
            'kgf': 9.80665
        }
        
        self.stress_conversions = {
            # Base unit: Pascal (Pa = N/m²)
            'Pa': 1.0,
            'kPa': 1000.0,
            'MPa': 1e6,
            'GPa': 1e9,
            'N/mm2': 1e6,
            'kN/m2': 1000.0,
            'psi': 6894.757,
            'ksi': 6.894757e6,
            'kgf/cm2': 98066.5
        }
        
        self.moment_conversions = {
            # Base unit: Newton-meter (N⋅m)
            'N.m': 1.0,
            'kN.m': 1000.0,
            'MN.m': 1e6,
            'N.mm': 0.001,
            'kN.mm': 1.0,
            'lbf.ft': 1.355818,
            'lbf.in': 0.112985,
            'kip.ft': 1355.818,
            'kip.in': 112.985,
            'kgf.m': 9.80665
        }
        
        self.density_conversions = {
            # Base unit: kg/m³
            'kg/m3': 1.0,
            'kN/m3': 101.971621,  # Assuming g = 9.80665 m/s²
            'g/cm3': 1000.0,
            'lb/ft3': 16.01846,
            'pcf': 16.01846  # pounds per cubic foot
        }
        
        # Unit system definitions
        self.unit_systems = {
            'metric_si': {
                'name': 'Metric (SI)',
                'length': 'm',
                'area': 'm2',
                'force': 'N',
                'stress': 'MPa',
                'moment': 'kN.m',
                'density': 'kN/m3',
                'moment_per_length': 'kN.m/m'
            },
            'metric_engineering': {
                'name': 'Metric (Engineering)',
                'length': 'mm',
                'area': 'mm2',
                'force': 'kN',
                'stress': 'N/mm2',
                'moment': 'kN.m',
                'density': 'kN/m3',
                'moment_per_length': 'kN.m/m'
            },
            'imperial': {
                'name': 'Imperial (US)',
                'length': 'ft',
                'area': 'ft2',
                'force': 'kip',
                'stress': 'ksi',
                'moment': 'kip.ft',
                'density': 'pcf',
                'moment_per_length': 'kip.ft/ft'
            },
            'mixed_metric': {
                'name': 'Mixed Metric',
                'length': 'm',
                'area': 'mm2',
                'force': 'kN',
                'stress': 'N/mm2',
                'moment': 'kN.m',
                'density': 'kN/m3',
                'moment_per_length': 'kN.m/m'
            }
        }
        
        self.current_system = 'metric_engineering'

    def convert_length(self, value, from_unit, to_unit):
        """Convert length between units"""
        return self._convert_value(value, from_unit, to_unit, self.length_conversions)

    def convert_area(self, value, from_unit, to_unit):
        """Convert area between units"""
        return self._convert_value(value, from_unit, to_unit, self.area_conversions)

    def convert_force(self, value, from_unit, to_unit):
        """Convert force between units"""
        return self._convert_value(value, from_unit, to_unit, self.force_conversions)

    def convert_stress(self, value, from_unit, to_unit):
        """Convert stress between units"""
        return self._convert_value(value, from_unit, to_unit, self.stress_conversions)

    def convert_moment(self, value, from_unit, to_unit):
        """Convert moment between units"""
        return self._convert_value(value, from_unit, to_unit, self.moment_conversions)

    def convert_density(self, value, from_unit, to_unit):
        """Convert density between units"""
        return self._convert_value(value, from_unit, to_unit, self.density_conversions)

    def _convert_value(self, value, from_unit, to_unit, conversion_dict):
        """Generic value conversion using conversion dictionary"""
        if from_unit not in conversion_dict:
            raise ValueError(f"Unknown source unit: {from_unit}")
        if to_unit not in conversion_dict:
            raise ValueError(f"Unknown target unit: {to_unit}")
        
        # Convert to base unit, then to target unit
        base_value = value * conversion_dict[from_unit]
        result = base_value / conversion_dict[to_unit]
        
        return result

    def set_unit_system(self, system_name):
        """Set current unit system"""
        if system_name in self.unit_systems:
            self.current_system = system_name
            return True
        return False

    def get_current_system(self):
        """Get current unit system"""
        return self.current_system

    def get_system_info(self, system_name=None):
        """Get unit system information"""
        if system_name is None:
            system_name = self.current_system
        return self.unit_systems.get(system_name, {})

    def get_unit_for_quantity(self, quantity_type):
        """Get unit for a specific quantity in current system"""
        system_info = self.get_system_info()
        return system_info.get(quantity_type, '')

    def format_value_with_unit(self, value, quantity_type, precision=2):
        """Format value with appropriate unit for current system"""
        unit = self.get_unit_for_quantity(quantity_type)
        return f"{value:.{precision}f} {unit}"

    def convert_to_system(self, value, quantity_type, from_system, to_system=None):
        """
        Convert value from one unit system to another
        
        Args:
            value: Numeric value to convert
            quantity_type: Type of quantity ('length', 'stress', etc.)
            from_system: Source unit system
            to_system: Target unit system (default: current system)
        """
        if to_system is None:
            to_system = self.current_system
        
        from_info = self.unit_systems.get(from_system, {})
        to_info = self.unit_systems.get(to_system, {})
        
        from_unit = from_info.get(quantity_type)
        to_unit = to_info.get(quantity_type)
        
        if not from_unit or not to_unit:
            raise ValueError(f"Cannot convert {quantity_type} between {from_system} and {to_system}")
        
        # Select appropriate conversion method
        if quantity_type == 'length':
            return self.convert_length(value, from_unit, to_unit)
        elif quantity_type == 'area':
            return self.convert_area(value, from_unit, to_unit)
        elif quantity_type == 'force':
            return self.convert_force(value, from_unit, to_unit)
        elif quantity_type == 'stress':
            return self.convert_stress(value, from_unit, to_unit)
        elif quantity_type == 'moment':
            return self.convert_moment(value, from_unit, to_unit)
        elif quantity_type == 'density':
            return self.convert_density(value, from_unit, to_unit)
        else:
            raise ValueError(f"Unknown quantity type: {quantity_type}")

    def get_available_systems(self):
        """Get list of available unit systems"""
        return list(self.unit_systems.keys())

    def get_conversion_factors(self, quantity_type):
        """Get all conversion factors for a quantity type"""
        if quantity_type == 'length':
            return self.length_conversions.copy()
        elif quantity_type == 'area':
            return self.area_conversions.copy()
        elif quantity_type == 'force':
            return self.force_conversions.copy()
        elif quantity_type == 'stress':
            return self.stress_conversions.copy()
        elif quantity_type == 'moment':
            return self.moment_conversions.copy()
        elif quantity_type == 'density':
            return self.density_conversions.copy()
        else:
            return {}

    def validate_unit(self, unit, quantity_type):
        """Validate if unit is available for quantity type"""
        conversions = self.get_conversion_factors(quantity_type)
        return unit in conversions

    def get_compatible_units(self, quantity_type):
        """Get list of units compatible with quantity type"""
        return list(self.get_conversion_factors(quantity_type).keys())


# Global unit converter instance
unit_converter = UnitConverter()

# Convenience functions
def convert_length(value, from_unit, to_unit):
    """Convert length units"""
    return unit_converter.convert_length(value, from_unit, to_unit)

def convert_stress(value, from_unit, to_unit):
    """Convert stress units"""
    return unit_converter.convert_stress(value, from_unit, to_unit)

def convert_moment(value, from_unit, to_unit):
    """Convert moment units"""
    return unit_converter.convert_moment(value, from_unit, to_unit)

def set_unit_system(system_name):
    """Set unit system"""
    return unit_converter.set_unit_system(system_name)

def get_unit_for_quantity(quantity_type):
    """Get unit for quantity in current system"""
    return unit_converter.get_unit_for_quantity(quantity_type)

def format_with_unit(value, quantity_type, precision=2):
    """Format value with unit"""
    return unit_converter.format_value_with_unit(value, quantity_type, precision)


# Test the unit conversion system
if __name__ == "__main__":
    print("=== Unit Conversion System Test ===")
    
    # Test basic conversions
    print(f"Length conversion: 1000 mm = {convert_length(1000, 'mm', 'm')} m")
    print(f"Stress conversion: 21 N/mm² = {convert_stress(21, 'N/mm2', 'MPa')} MPa")
    print(f"Moment conversion: 10 kN.m = {convert_moment(10, 'kN.m', 'kN.mm')} kN.mm")
    
    # Test unit systems
    print(f"\nAvailable unit systems: {unit_converter.get_available_systems()}")
    
    # Test system conversion
    print(f"\nTesting system conversions:")
    value = 21.0  # N/mm²
    
    # Convert from metric_engineering to imperial
    imperial_stress = unit_converter.convert_to_system(
        value, 'stress', 'metric_engineering', 'imperial'
    )
    print(f"21 N/mm² = {imperial_stress:.1f} ksi")
    
    # Test formatting
    print(f"\nFormatting tests:")
    unit_converter.set_unit_system('metric_engineering')
    print(f"Stress: {format_with_unit(21.0, 'stress')}")
    print(f"Length: {format_with_unit(3.5, 'length')}")
    
    unit_converter.set_unit_system('imperial')
    print(f"Stress (Imperial): {format_with_unit(3.0, 'stress')}")
    print(f"Length (Imperial): {format_with_unit(10.0, 'length')}")
    
    # Test compatible units
    print(f"\nCompatible stress units: {unit_converter.get_compatible_units('stress')}")