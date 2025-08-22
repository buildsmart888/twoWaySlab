"""
Unit Conversion Utilities
=========================

Enhanced unit conversion system for structural engineering.
Supports metric, imperial, and mixed unit systems with Thai units.

ระบบการแปลงหน่วยที่ปรับปรุงแล้วสำหรับวิศวกรรมโครงสร้าง
รองรับระบบเมตริก อิมพีเรียล และหน่วยผสม รวมถึงหน่วยไทย
"""

import math
from typing import Dict, Union, Optional, Tuple
from enum import Enum

class UnitSystem(Enum):
    """Standard unit systems"""
    METRIC_SI = "metric_si"                 # Pure SI units
    METRIC_ENGINEERING = "metric_engineering"  # Engineering metric (mm, N/mm²)
    IMPERIAL = "imperial"                   # US customary units
    THAI_TRADITIONAL = "thai_traditional"  # Thai traditional units (ksc, kgf, tonf)
    MIXED_METRIC = "mixed_metric"          # Mixed metric units

class UnitConverter:
    """
    Comprehensive unit conversion system for structural engineering
    
    ระบบการแปลงหน่วยที่ครอบคลุมสำหรับวิศวกรรมโครงสร้าง
    """
    
    def __init__(self):
        """Initialize unit converter with conversion factors"""
        
        # Base unit conversion factors (to SI base units)
        self.length_factors = {
            # Base: meter (m)
            'm': 1.0,
            'mm': 1e-3,
            'cm': 1e-2,
            'km': 1e3,
            'ft': 0.3048,
            'in': 0.0254,
            'yd': 0.9144,
            # Thai units
            'wa': 2.0,      # วา = 2 meters
            'sok': 0.5,     # ศอก = 0.5 meters
            'keub': 0.25,   # คืบ = 0.25 meters
        }
        
        self.area_factors = {
            # Base: square meter (m²)
            'm2': 1.0,
            'mm2': 1e-6,
            'cm2': 1e-4,
            'ft2': 0.092903,
            'in2': 0.00064516,
            # Thai units
            'rai': 1600.0,    # ไร่ = 1600 m²
            'ngan': 400.0,    # งาน = 400 m²
            'wa2': 4.0,       # ตารางวา = 4 m²
        }
        
        self.force_factors = {
            # Base: Newton (N)
            'N': 1.0,
            'kN': 1e3,
            'MN': 1e6,
            'lbf': 4.448222,
            'kip': 4448.222,
            'kgf': 9.80665,
            'tonf': 9806.65,  # metric ton-force
            # Thai traditional units
            'kgf_thai': 9.80665,  # Same as kgf but explicitly Thai
            'tonf_thai': 9806.65, # Thai ton-force
        }
        
        self.stress_factors = {
            # Base: Pascal (Pa = N/m²)
            'Pa': 1.0,
            'kPa': 1e3,
            'MPa': 1e6,
            'GPa': 1e9,
            'N/m2': 1.0,
            'N/mm2': 1e6,
            'kN/m2': 1e3,
            'psi': 6894.757,
            'ksi': 6.894757e6,
            'psf': 47.88026,  # pounds per square foot
            'kgf/cm2': 98066.5,
            'kgf/m2': 9.80665,
            'tonf/m2': 9806.65,
            # Thai traditional stress units
            'ksc': 98066.5,   # 1 ksc = 1 kgf/cm² = 98.0665 kPa ≈ 0.098 MPa
        }
        
        self.moment_factors = {
            # Base: Newton-meter (N⋅m)
            'N.m': 1.0,
            'N.mm': 1e-3,
            'kN.m': 1e3,
            'kN.mm': 1.0,
            'MN.m': 1e6,
            'lbf.ft': 1.355818,
            'lbf.in': 0.112985,
            'kip.ft': 1355.818,
            'kip.in': 112.985,
            'kgf.m': 9.80665,
            'kgf.cm': 0.0980665,
            'tonf.m': 9806.65,
        }
        
        self.density_factors = {
            # Base: kg/m³
            'kg/m3': 1.0,
            'g/cm3': 1000.0,
            'kN/m3': 101.971621,  # Assuming g = 9.80665 m/s²
            'lb/ft3': 16.01846,
            'pcf': 16.01846,  # pounds per cubic foot
        }
        
        # Unit system definitions
        self.unit_systems = {
            UnitSystem.METRIC_SI: {
                'name': 'Metric (SI)',
                'name_thai': 'เมตริก (SI)',
                'length': 'm',
                'area': 'm2', 
                'force': 'N',
                'stress': 'MPa',
                'moment': 'N.m',
                'density': 'kg/m3',
                'distributed_load': 'N/m',
                'moment_per_length': 'N.m/m',
            },
            UnitSystem.METRIC_ENGINEERING: {
                'name': 'Metric (Engineering)',
                'name_thai': 'เมตริก (วิศวกรรม)',
                'length': 'mm',
                'area': 'mm2',
                'force': 'kN', 
                'stress': 'N/mm2',
                'moment': 'kN.m',
                'density': 'kN/m3',
                'distributed_load': 'kN/m',
                'moment_per_length': 'kN.m/m',
            },
            UnitSystem.IMPERIAL: {
                'name': 'Imperial (US)',
                'name_thai': 'อิมพีเรียล (สหรัฐ)',
                'length': 'ft',
                'area': 'ft2',
                'force': 'kip',
                'stress': 'ksi', 
                'moment': 'kip.ft',
                'density': 'pcf',
                'distributed_load': 'kip/ft',
                'moment_per_length': 'kip.ft/ft',
            },
            UnitSystem.THAI_TRADITIONAL: {
                'name': 'Thai Traditional',
                'name_thai': 'หน่วยไทยดั้งเดิม',
                'length': 'm',
                'area': 'mm2',
                'force': 'tonf',
                'stress': 'ksc',  # kgf/cm²
                'moment': 'tonf.m',
                'density': 'kgf/m3',
                'distributed_load': 'tonf/m',
                'moment_per_length': 'tonf.m/m',
            },
            UnitSystem.MIXED_METRIC: {
                'name': 'Mixed Metric',
                'name_thai': 'เมตริกผสม',
                'length': 'm',
                'area': 'mm2',
                'force': 'kN',
                'stress': 'N/mm2',
                'moment': 'kN.m', 
                'density': 'kN/m3',
                'distributed_load': 'kN/m',
                'moment_per_length': 'kN.m/m',
            }
        }
        
        self.current_system = UnitSystem.METRIC_ENGINEERING
    
    def convert(self, 
                value: Union[float, int],
                from_unit: str,
                to_unit: str,
                quantity_type: str) -> float:
        """
        Convert value between units of the same quantity type
        
        Parameters:
        -----------
        value : Union[float, int]
            Value to convert
        from_unit : str
            Source unit
        to_unit : str
            Target unit
        quantity_type : str
            Type of quantity ('length', 'force', 'stress', etc.)
            
        Returns:
        --------
        float
            Converted value
            
        Raises:
        -------
        ValueError
            If units or quantity type are invalid
        """
        # Get appropriate conversion factors
        factor_map = {
            'length': self.length_factors,
            'area': self.area_factors,
            'force': self.force_factors,
            'stress': self.stress_factors,
            'moment': self.moment_factors,
            'density': self.density_factors,
        }
        
        if quantity_type not in factor_map:
            raise ValueError(f"Unknown quantity type: {quantity_type}")
        
        factors = factor_map[quantity_type]
        
        if from_unit not in factors:
            raise ValueError(f"Unknown {quantity_type} unit: {from_unit}")
        
        if to_unit not in factors:
            raise ValueError(f"Unknown {quantity_type} unit: {to_unit}")
        
        # Convert: value * from_factor / to_factor
        return value * factors[from_unit] / factors[to_unit]
    
    def convert_length(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert length units"""
        return self.convert(value, from_unit, to_unit, 'length')
    
    def convert_area(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert area units"""
        return self.convert(value, from_unit, to_unit, 'area')
    
    def convert_force(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert force units"""
        return self.convert(value, from_unit, to_unit, 'force')
    
    def convert_stress(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert stress/pressure units"""
        return self.convert(value, from_unit, to_unit, 'stress')
    
    def convert_moment(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert moment units"""
        return self.convert(value, from_unit, to_unit, 'moment')
    
    def convert_density(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert density units"""
        return self.convert(value, from_unit, to_unit, 'density')
    
    # Thai-specific conversions (commonly used in Thai engineering)
    def mpa_to_ksc(self, mpa_value: float) -> float:
        """Convert MPa to ksc (Thai traditional unit)"""
        return self.convert_stress(mpa_value, 'MPa', 'ksc')
    
    def ksc_to_mpa(self, ksc_value: float) -> float:
        """Convert ksc to MPa"""
        return self.convert_stress(ksc_value, 'ksc', 'MPa')
    
    def kn_to_tonf(self, kn_value: float) -> float:
        """Convert kN to tonf (Thai traditional unit)"""
        return self.convert_force(kn_value, 'kN', 'tonf')
    
    def tonf_to_kn(self, tonf_value: float) -> float:
        """Convert tonf to kN"""
        return self.convert_force(tonf_value, 'tonf', 'kN')
    
    def kgf_to_n(self, kgf_value: float) -> float:
        """Convert kgf to N"""
        return self.convert_force(kgf_value, 'kgf', 'N')
    
    def n_to_kgf(self, n_value: float) -> float:
        """Convert N to kgf"""
        return self.convert_force(n_value, 'N', 'kgf')
    
    # Unit system management
    def set_system(self, system: UnitSystem) -> None:
        """Set current unit system"""
        self.current_system = system
    
    def get_system(self) -> UnitSystem:
        """Get current unit system"""
        return self.current_system
    
    def get_system_info(self, system: Optional[UnitSystem] = None) -> Dict[str, str]:
        """Get unit system information"""
        if system is None:
            system = self.current_system
        return self.unit_systems.get(system, {})
    
    def get_unit_for_quantity(self, quantity_type: str, 
                             system: Optional[UnitSystem] = None) -> str:
        """Get unit for a specific quantity in given system"""
        if system is None:
            system = self.current_system
        
        system_info = self.get_system_info(system)
        return system_info.get(quantity_type, '')
    
    def format_value(self, value: float, quantity_type: str, 
                    precision: int = 2, 
                    system: Optional[UnitSystem] = None) -> str:
        """Format value with appropriate unit"""
        unit = self.get_unit_for_quantity(quantity_type, system)
        return f"{value:.{precision}f} {unit}"
    
    def convert_to_system(self, 
                         value: float,
                         quantity_type: str,
                         from_system: UnitSystem,
                         to_system: Optional[UnitSystem] = None) -> float:
        """Convert value from one unit system to another"""
        if to_system is None:
            to_system = self.current_system
        
        from_unit = self.get_unit_for_quantity(quantity_type, from_system)
        to_unit = self.get_unit_for_quantity(quantity_type, to_system)
        
        if not from_unit or not to_unit:
            raise ValueError(f"Cannot find units for {quantity_type}")
        
        return self.convert(value, from_unit, to_unit, quantity_type)
    
    def get_thai_conversion_table(self) -> Dict[str, Dict[str, float]]:
        """
        Get conversion table for Thai traditional units
        
        Returns:
        --------
        Dict[str, Dict[str, float]]
            Conversion factors from Thai units to SI/metric
        """
        return {
            'stress_conversions': {
                'ksc_to_mpa': 1.0 / 10.197,  # 1 ksc ≈ 0.098 MPa
                'mpa_to_ksc': 10.197,        # 1 MPa ≈ 10.197 ksc
            },
            'force_conversions': {
                'tonf_to_kn': 9.80665,       # 1 tonf = 9.80665 kN
                'kn_to_tonf': 1.0 / 9.80665, # 1 kN ≈ 0.102 tonf
                'kgf_to_n': 9.80665,         # 1 kgf = 9.80665 N
                'n_to_kgf': 1.0 / 9.80665,   # 1 N ≈ 0.102 kgf
            },
            'load_conversions': {
                'kgf_m2_to_kn_m2': 9.80665 / 1000,  # kgf/m² to kN/m²
                'kn_m2_to_kgf_m2': 1000 / 9.80665,  # kN/m² to kgf/m²
            }
        }

# Convenience functions for common conversions
def convert_pressure(value: float, from_unit: str, to_unit: str) -> float:
    """Convenience function for pressure/stress conversion"""
    converter = UnitConverter()
    return converter.convert_stress(value, from_unit, to_unit)

def convert_force(value: float, from_unit: str, to_unit: str) -> float:
    """Convenience function for force conversion"""
    converter = UnitConverter()
    return converter.convert_force(value, from_unit, to_unit)

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convenience function for length conversion"""
    converter = UnitConverter()
    return converter.convert_length(value, from_unit, to_unit)

def convert_moment(value: float, from_unit: str, to_unit: str) -> float:
    """Convenience function for moment conversion"""
    converter = UnitConverter()
    return converter.convert_moment(value, from_unit, to_unit)

# Global unit converter instance
_global_converter = UnitConverter()

def set_global_unit_system(system: UnitSystem) -> None:
    """Set global unit system"""
    _global_converter.set_system(system)

def get_global_unit_system() -> UnitSystem:
    """Get global unit system"""
    return _global_converter.get_system()