"""
Thai Unit Conversion System
===========================

Comprehensive unit conversion system for Thai engineering applications including:
- Pressure units (ksc ↔ MPa conversions)
- Traditional Thai length, area, weight units
- Engineering units commonly used in Thailand
"""

import math
from typing import Dict, Tuple, Union, Optional
from dataclasses import dataclass
from enum import Enum

from ....utils.validation import StructuralValidator, validate_positive


class ThaiPressureUnit(Enum):
    """Thai pressure units"""
    KSC = "ksc"           # กิโลกรัมต่อตารางเซนติเมตร (kg/cm²)
    MPA = "MPa"           # เมกะปาสคัล
    KPA = "kPa"           # กิโลปาสคัล
    BAR = "bar"           # บาร์
    PSI = "psi"           # ปอนด์ต่อตารางนิ้ว


class ThaiLengthUnit(Enum):
    """Thai length units"""
    M = "m"               # เมตร
    CM = "cm"             # เซนติเมตร
    MM = "mm"             # มิลลิเมตร
    WA = "wa"             # วา (2 meters)
    SEN = "sen"           # เส้น (20 meters)
    CUBIT = "cubit"       # ศอก (0.5 meters)
    FT = "ft"             # ฟุต
    IN = "in"             # นิ้ว


class ThaiAreaUnit(Enum):
    """Thai area units"""
    M2 = "m²"             # ตารางเมตร
    RAI = "rai"           # ไร่ (1,600 m²)
    NGAN = "ngan"         # งาน (400 m²)
    WA2 = "wa²"           # ตารางวา (4 m²)
    HA = "ha"             # เฮกตาร์
    FT2 = "ft²"           # ตารางฟุต


class ThaiWeightUnit(Enum):
    """Thai weight units"""
    KG = "kg"             # กิโลกรัม
    T = "t"               # ตัน (1,000 kg)
    CHANG = "chang"       # ช้าง (60 kg)
    PICUL = "picul"       # ปิกุล (60 kg, same as chang)
    LB = "lb"             # ปอนด์


@dataclass
class ThaiConversionResult:
    """Result of Thai unit conversion"""
    original_value: float
    original_unit: str
    converted_value: float
    converted_unit: str
    conversion_factor: float
    formula: str
    description_thai: str
    description_english: str


class ThaiUnitConverter:
    """
    Thai Unit Conversion System
    
    ระบบการแปลงหน่วยไทยสำหรับงานวิศวกรรม
    """
    
    def __init__(self):
        """Initialize Thai unit converter"""
        self.validator = StructuralValidator()
        
        # Pressure conversion factors to Pa
        self.pressure_factors = {
            ThaiPressureUnit.KSC: 98066.5,       # 1 ksc = 98,066.5 Pa
            ThaiPressureUnit.MPA: 1000000.0,
            ThaiPressureUnit.KPA: 1000.0,
            ThaiPressureUnit.BAR: 100000.0,
            ThaiPressureUnit.PSI: 6894.757
        }
        
        # Length conversion factors to meters
        self.length_factors = {
            ThaiLengthUnit.M: 1.0,
            ThaiLengthUnit.CM: 0.01,
            ThaiLengthUnit.MM: 0.001,
            ThaiLengthUnit.WA: 2.0,              # 1 วา = 2 เมตร
            ThaiLengthUnit.SEN: 20.0,            # 1 เส้น = 20 เมตร
            ThaiLengthUnit.CUBIT: 0.5,           # 1 ศอก = 0.5 เมตร
            ThaiLengthUnit.FT: 0.3048,
            ThaiLengthUnit.IN: 0.0254
        }
        
        # Area conversion factors to m²
        self.area_factors = {
            ThaiAreaUnit.M2: 1.0,
            ThaiAreaUnit.RAI: 1600.0,            # 1 ไร่ = 1,600 ตารางเมตร
            ThaiAreaUnit.NGAN: 400.0,            # 1 งาน = 400 ตารางเมตร
            ThaiAreaUnit.WA2: 4.0,               # 1 ตารางวา = 4 ตารางเมตร
            ThaiAreaUnit.HA: 10000.0,
            ThaiAreaUnit.FT2: 0.092903
        }
        
        # Weight conversion factors to kg
        self.weight_factors = {
            ThaiWeightUnit.KG: 1.0,
            ThaiWeightUnit.T: 1000.0,
            ThaiWeightUnit.CHANG: 60.0,          # 1 ช้าง = 60 กิโลกรัม
            ThaiWeightUnit.PICUL: 60.0,          # 1 ปิกุล = 60 กิโลกรัม
            ThaiWeightUnit.LB: 0.453592
        }
    
    def ksc_to_mpa(self, ksc_value: float) -> ThaiConversionResult:
        """Convert ksc (kg/cm²) to MPa"""
        validate_positive(ksc_value, "ksc value")
        
        conversion_factor = 98066.5 / 1000000.0  # ksc to MPa factor
        mpa_value = ksc_value * conversion_factor
        
        return ThaiConversionResult(
            original_value=ksc_value,
            original_unit="ksc",
            converted_value=mpa_value,
            converted_unit="MPa",
            conversion_factor=conversion_factor,
            formula=f"{ksc_value} ksc × {conversion_factor:.6f} = {mpa_value:.3f} MPa",
            description_thai=f"แปลง {ksc_value} กิโลกรัมต่อตารางเซนติเมตร เป็น {mpa_value:.3f} เมกะปาสคัล",
            description_english=f"Convert {ksc_value} kg/cm² to {mpa_value:.3f} MPa"
        )
    
    def mpa_to_ksc(self, mpa_value: float) -> ThaiConversionResult:
        """Convert MPa to ksc (kg/cm²)"""
        validate_positive(mpa_value, "MPa value")
        
        conversion_factor = 1000000.0 / 98066.5  # MPa to ksc factor
        ksc_value = mpa_value * conversion_factor
        
        return ThaiConversionResult(
            original_value=mpa_value,
            original_unit="MPa",
            converted_value=ksc_value,
            converted_unit="ksc",
            conversion_factor=conversion_factor,
            formula=f"{mpa_value} MPa × {conversion_factor:.3f} = {ksc_value:.2f} ksc",
            description_thai=f"แปลง {mpa_value} เมกะปาสคัล เป็น {ksc_value:.2f} กิโลกรัมต่อตารางเซนติเมตร",
            description_english=f"Convert {mpa_value} MPa to {ksc_value:.2f} kg/cm²"
        )
    
    def convert_length(self, value: float, from_unit: ThaiLengthUnit, 
                      to_unit: ThaiLengthUnit) -> ThaiConversionResult:
        """Convert between length units"""
        validate_positive(value, "length value")
        
        # Convert to meters first, then to target unit
        m_value = value * self.length_factors[from_unit]
        converted_value = m_value / self.length_factors[to_unit]
        conversion_factor = self.length_factors[from_unit] / self.length_factors[to_unit]
        
        return ThaiConversionResult(
            original_value=value,
            original_unit=from_unit.value,
            converted_value=converted_value,
            converted_unit=to_unit.value,
            conversion_factor=conversion_factor,
            formula=f"{value} {from_unit.value} × {conversion_factor:.6f} = {converted_value:.3f} {to_unit.value}",
            description_thai=f"แปลง {value} {from_unit.value} เป็น {converted_value:.3f} {to_unit.value}",
            description_english=f"Convert {value} {from_unit.value} to {converted_value:.3f} {to_unit.value}"
        )
    
    def convert_area(self, value: float, from_unit: ThaiAreaUnit, 
                    to_unit: ThaiAreaUnit) -> ThaiConversionResult:
        """Convert between area units"""
        validate_positive(value, "area value")
        
        # Convert to m² first, then to target unit
        m2_value = value * self.area_factors[from_unit]
        converted_value = m2_value / self.area_factors[to_unit]
        conversion_factor = self.area_factors[from_unit] / self.area_factors[to_unit]
        
        return ThaiConversionResult(
            original_value=value,
            original_unit=from_unit.value,
            converted_value=converted_value,
            converted_unit=to_unit.value,
            conversion_factor=conversion_factor,
            formula=f"{value} {from_unit.value} × {conversion_factor:.6f} = {converted_value:.3f} {to_unit.value}",
            description_thai=f"แปลง {value} {from_unit.value} เป็น {converted_value:.3f} {to_unit.value}",
            description_english=f"Convert {value} {from_unit.value} to {converted_value:.3f} {to_unit.value}"
        )
    
    def get_thai_concrete_conversions(self) -> Dict[str, Dict[str, float]]:
        """Get Thai concrete grade conversions"""
        return {
            'Fc180': {'ksc': 180, 'mpa': 180 * 98066.5 / 1000000.0},
            'Fc210': {'ksc': 210, 'mpa': 210 * 98066.5 / 1000000.0},
            'Fc240': {'ksc': 240, 'mpa': 240 * 98066.5 / 1000000.0},
            'Fc280': {'ksc': 280, 'mpa': 280 * 98066.5 / 1000000.0},
            'Fc350': {'ksc': 350, 'mpa': 350 * 98066.5 / 1000000.0}
        }
    
    def get_thai_steel_conversions(self) -> Dict[str, Dict[str, float]]:
        """Get Thai steel grade conversions"""
        return {
            'SR24': {'ksc': 2400, 'mpa': 2400 * 98066.5 / 1000000.0},
            'SD40': {'ksc': 4000, 'mpa': 4000 * 98066.5 / 1000000.0},
            'SD50': {'ksc': 5000, 'mpa': 5000 * 98066.5 / 1000000.0}
        }
    
    def generate_conversion_report(self, conversions: list) -> str:
        """Generate conversion report"""
        report = f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                         รายงานการแปลงหน่วยไทย                               ║
║                       THAI UNIT CONVERSION REPORT                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

การแปลงหน่วย / Unit Conversions:
{'-'*80}
"""
        
        for i, conversion in enumerate(conversions, 1):
            report += f"""
{i}. {conversion.formula}
   ไทย: {conversion.description_thai}
   English: {conversion.description_english}
"""
        
        report += f"""
หมายเหตุ / Notes:
{'-'*80}
1. การแปลงนี้ใช้ค่ามาตรฐานสากล
2. 1 ksc = 98,066.5 Pa = 0.0980665 MPa
3. 1 วา = 2 เมตร, 1 ไร่ = 1,600 ตารางเมตร
4. These conversions use international standards
5. Commonly used in Thai engineering practice

รายงานสร้างโดย Thai Unit Converter v1.0
Generated by Thai Unit Converter v1.0
{'-'*80}
"""
        return report


# Convenience functions for quick conversions
def ksc_to_mpa(ksc_value: float) -> float:
    """Quick ksc to MPa conversion"""
    return ksc_value * 98066.5 / 1000000.0

def mpa_to_ksc(mpa_value: float) -> float:
    """Quick MPa to ksc conversion"""
    return mpa_value * 1000000.0 / 98066.5

def convert_thai_length(value: float, from_unit: str, to_unit: str) -> float:
    """Quick Thai length conversion"""
    converter = ThaiUnitConverter()
    from_enum = ThaiLengthUnit(from_unit)
    to_enum = ThaiLengthUnit(to_unit)
    result = converter.convert_length(value, from_enum, to_enum)
    return result.converted_value

def convert_thai_area(value: float, from_unit: str, to_unit: str) -> float:
    """Quick Thai area conversion"""
    converter = ThaiUnitConverter()
    from_enum = ThaiAreaUnit(from_unit)
    to_enum = ThaiAreaUnit(to_unit)
    result = converter.convert_area(value, from_enum, to_enum)
    return result.converted_value

def convert_thai_weight(value: float, from_unit: str, to_unit: str) -> float:
    """Quick Thai weight conversion"""
    converter = ThaiUnitConverter()
    weight_factors = converter.weight_factors
    from_enum = ThaiWeightUnit(from_unit)
    to_enum = ThaiWeightUnit(to_unit)
    
    # Convert to kg first, then to target unit
    kg_value = value * weight_factors[from_enum]
    return kg_value / weight_factors[to_enum]


# Common Thai engineering conversion constants
KSC_TO_MPA_FACTOR = 98066.5 / 1000000.0  # 0.0980665
MPA_TO_KSC_FACTOR = 1000000.0 / 98066.5   # 10.197162
WA_TO_METER = 2.0
RAI_TO_M2 = 1600.0
CHANG_TO_KG = 60.0