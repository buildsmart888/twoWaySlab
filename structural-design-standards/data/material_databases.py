"""
Material Databases
==================

Comprehensive databases of material properties for various structural standards.
Contains concrete grades, steel grades, and other material data.
"""

from typing import Dict, List, Any

# ACI 318M-25 Material Properties
ACI_CONCRETE_GRADES = {
    "fc17": {
        "fc_prime": 17.0,  # MPa
        "unit_weight": 23.5,  # kN/m³
        "description": "Low strength concrete",
        "typical_uses": ["mass concrete", "unreinforced applications"],
        "elastic_modulus": 19684,  # MPa (calculated)
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,  # /°C
        "shrinkage_strain": 500e-6,
        "creep_coefficient": 2.5
    },
    "fc21": {
        "fc_prime": 21.0,
        "unit_weight": 24.0,
        "description": "Standard concrete",
        "typical_uses": ["residential", "light commercial"],
        "elastic_modulus": 21797,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 480e-6,
        "creep_coefficient": 2.3
    },
    "fc28": {
        "fc_prime": 28.0,
        "unit_weight": 24.0,
        "description": "High strength concrete",
        "typical_uses": ["commercial", "industrial"],
        "elastic_modulus": 25120,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 450e-6,
        "creep_coefficient": 2.0
    },
    "fc35": {
        "fc_prime": 35.0,
        "unit_weight": 24.0,
        "description": "High performance concrete",
        "typical_uses": ["high-rise", "precast"],
        "elastic_modulus": 28098,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 420e-6,
        "creep_coefficient": 1.8
    },
    "fc42": {
        "fc_prime": 42.0,
        "unit_weight": 24.0,
        "description": "Very high strength concrete",
        "typical_uses": ["special structures", "prestressed"],
        "elastic_modulus": 30672,
        "poisson_ratio": 0.18,
        "coefficient_thermal_expansion": 9e-6,
        "shrinkage_strain": 400e-6,
        "creep_coefficient": 1.6
    },
    "fc55": {
        "fc_prime": 55.0,
        "unit_weight": 24.5,
        "description": "Ultra high strength concrete",
        "typical_uses": ["bridges", "special applications"],
        "elastic_modulus": 35044,
        "poisson_ratio": 0.18,
        "coefficient_thermal_expansion": 9e-6,
        "shrinkage_strain": 380e-6,
        "creep_coefficient": 1.4
    },
    "fc69": {
        "fc_prime": 69.0,
        "unit_weight": 25.0,
        "description": "Ultra high performance concrete",
        "typical_uses": ["specialized structures"],
        "elastic_modulus": 39262,
        "poisson_ratio": 0.17,
        "coefficient_thermal_expansion": 8e-6,
        "shrinkage_strain": 350e-6,
        "creep_coefficient": 1.2
    },
    "fc83": {
        "fc_prime": 83.0,
        "unit_weight": 25.0,
        "description": "Maximum strength concrete per ACI",
        "typical_uses": ["research", "special applications"],
        "elastic_modulus": 43074,
        "poisson_ratio": 0.16,
        "coefficient_thermal_expansion": 8e-6,
        "shrinkage_strain": 320e-6,
        "creep_coefficient": 1.0
    }
}

ACI_STEEL_GRADES = {
    "GRADE280": {
        "fy": 280,  # MPa
        "fu": 420,  # MPa
        "es": 200000,  # MPa (elastic modulus)
        "description": "Standard grade reinforcement",
        "yield_strain": 0.0014,
        "ultimate_strain": 0.12,
        "bar_designations": ["10M", "15M", "20M", "25M", "30M"],
        "typical_uses": ["general construction", "residential"],
        "ductility_class": "normal",
        "weldability": "good"
    },
    "GRADE350": {
        "fy": 350,
        "fu": 520,
        "es": 200000,
        "description": "Intermediate grade reinforcement",
        "yield_strain": 0.00175,
        "ultimate_strain": 0.10,
        "bar_designations": ["10M", "15M", "20M", "25M", "30M", "35M"],
        "typical_uses": ["commercial", "industrial"],
        "ductility_class": "normal",
        "weldability": "good"
    },
    "GRADE420": {
        "fy": 420,
        "fu": 620,
        "es": 200000,
        "description": "High strength reinforcement",
        "yield_strain": 0.0021,
        "ultimate_strain": 0.09,
        "bar_designations": ["10M", "15M", "20M", "25M", "30M", "35M", "45M", "55M"],
        "typical_uses": ["high-rise", "heavy construction"],
        "ductility_class": "normal",
        "weldability": "fair"
    },
    "GRADE520": {
        "fy": 520,
        "fu": 690,
        "es": 200000,
        "description": "Very high strength reinforcement",
        "yield_strain": 0.0026,
        "ultimate_strain": 0.08,
        "bar_designations": ["15M", "20M", "25M", "30M", "35M", "45M", "55M"],
        "typical_uses": ["specialized applications", "prestressed"],
        "ductility_class": "low",
        "weldability": "poor"
    }
}

# Thai Material Properties (Ministry Regulation B.E. 2566)
THAI_CONCRETE_GRADES = {
    "Fc180": {
        "fc_prime": 18.0,  # MPa
        "fc_ksc": 180,     # ksc (Thai unit)
        "unit_weight": 24.0,
        "description": "มาตรฐานคอนกรีต Fc180",
        "description_english": "Standard concrete Fc180",
        "typical_uses": ["โครงสร้างทั่วไป", "อาคารพักอาศัย"],
        "typical_uses_english": ["general structures", "residential buildings"],
        "elastic_modulus": 19951,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 500e-6,
        "creep_coefficient": 2.5,
        "tis_standard": "TIS 1505",
        "ministry_approval": "มกท.2566"
    },
    "Fc210": {
        "fc_prime": 21.0,
        "fc_ksc": 210,
        "unit_weight": 24.0,
        "description": "มาตรฐานคอนกรีต Fc210",
        "description_english": "Standard concrete Fc210",
        "typical_uses": ["อาคารพาณิชย์", "โครงสร้างกลาง"],
        "typical_uses_english": ["commercial buildings", "medium structures"],
        "elastic_modulus": 21571,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 480e-6,
        "creep_coefficient": 2.3,
        "tis_standard": "TIS 1505",
        "ministry_approval": "มกท.2566"
    },
    "Fc240": {
        "fc_prime": 24.0,
        "fc_ksc": 240,
        "unit_weight": 24.0,
        "description": "คอนกรีตเกรดสูง Fc240",
        "description_english": "High grade concrete Fc240",
        "typical_uses": ["อาคารสูง", "โครงสร้างพิเศษ"],
        "typical_uses_english": ["high-rise buildings", "special structures"],
        "elastic_modulus": 23060,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 460e-6,
        "creep_coefficient": 2.1,
        "tis_standard": "TIS 1505",
        "ministry_approval": "มกท.2566"
    },
    "Fc280": {
        "fc_prime": 28.0,
        "fc_ksc": 280,
        "unit_weight": 24.0,
        "description": "คอนกรีตกำลังสูง Fc280",
        "description_english": "High strength concrete Fc280",
        "typical_uses": ["สะพาน", "อาคารพิเศษ"],
        "typical_uses_english": ["bridges", "special buildings"],
        "elastic_modulus": 24899,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 440e-6,
        "creep_coefficient": 1.9,
        "tis_standard": "TIS 1505",
        "ministry_approval": "มกท.2566"
    },
    "Fc320": {
        "fc_prime": 32.0,
        "fc_ksc": 320,
        "unit_weight": 24.0,
        "description": "คอนกรีตกำลังสูงพิเศษ Fc320",
        "description_english": "Special high strength concrete Fc320",
        "typical_uses": ["โครงสร้างพิเศษ", "งานก่อสร้างหนัก"],
        "typical_uses_english": ["special structures", "heavy construction"],
        "elastic_modulus": 26584,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 420e-6,
        "creep_coefficient": 1.7,
        "tis_standard": "TIS 1505",
        "ministry_approval": "มกท.2566"
    },
    "Fc350": {
        "fc_prime": 35.0,
        "fc_ksc": 350,
        "unit_weight": 24.0,
        "description": "คอนกรีตกำลังสูงสุด Fc350",
        "description_english": "Maximum strength concrete Fc350",
        "typical_uses": ["งานพิเศษ", "วิจัยและพัฒนา"],
        "typical_uses_english": ["special applications", "research and development"],
        "elastic_modulus": 27838,
        "poisson_ratio": 0.20,
        "coefficient_thermal_expansion": 10e-6,
        "shrinkage_strain": 400e-6,
        "creep_coefficient": 1.5,
        "tis_standard": "TIS 1505",
        "ministry_approval": "มกท.2566"
    }
}

THAI_STEEL_GRADES = {
    "SR24": {
        "fy": 235,  # MPa
        "fy_ksc": 2400,  # ksc
        "fu": 380,
        "es": 200000,
        "description": "เหล็กเสริมเกรด SR24",
        "description_english": "Reinforcement steel grade SR24",
        "yield_strain": 0.00118,
        "ultimate_strain": 0.14,
        "bar_designations": ["DB10", "DB12", "DB16", "DB20", "DB25"],
        "typical_uses": ["งานโครงสร้างทั่วไป", "อาคารพักอาศัย"],
        "typical_uses_english": ["general structures", "residential buildings"],
        "ductility_class": "สูง",
        "ductility_class_english": "high",
        "weldability": "ดี",
        "weldability_english": "good",
        "tis_standard": "TIS 24-2548",
        "ministry_approval": "มกท.2566"
    },
    "SD30": {
        "fy": 295,
        "fy_ksc": 3000,
        "fu": 440,
        "es": 200000,
        "description": "เหล็กเสริมเกรด SD30",
        "description_english": "Reinforcement steel grade SD30",
        "yield_strain": 0.00148,
        "ultimate_strain": 0.12,
        "bar_designations": ["DB10", "DB12", "DB16", "DB20", "DB25", "DB32"],
        "typical_uses": ["อาคารพาณิชย์", "โครงสร้างกลาง"],
        "typical_uses_english": ["commercial buildings", "medium structures"],
        "ductility_class": "สูง",
        "ductility_class_english": "high",
        "weldability": "ดี",
        "weldability_english": "good",
        "tis_standard": "TIS 24-2548",
        "ministry_approval": "มกท.2566"
    },
    "SD40": {
        "fy": 392,
        "fy_ksc": 4000,
        "fu": 560,
        "es": 200000,
        "description": "เหล็กเสริมเกรด SD40",
        "description_english": "Reinforcement steel grade SD40",
        "yield_strain": 0.00196,
        "ultimate_strain": 0.10,
        "bar_designations": ["DB10", "DB12", "DB16", "DB20", "DB25", "DB32", "DB40"],
        "typical_uses": ["อาคารสูง", "โครงสร้างหนัก"],
        "typical_uses_english": ["high-rise buildings", "heavy structures"],
        "ductility_class": "ปานกลาง",
        "ductility_class_english": "medium",
        "weldability": "พอใช้",
        "weldability_english": "fair",
        "tis_standard": "TIS 24-2548",
        "ministry_approval": "มกท.2566"
    },
    "SD50": {
        "fy": 490,
        "fy_ksc": 5000,
        "fu": 630,
        "es": 200000,
        "description": "เหล็กเสริมเกรดสูง SD50",
        "description_english": "High grade reinforcement steel SD50",
        "yield_strain": 0.00245,
        "ultimate_strain": 0.08,
        "bar_designations": ["DB12", "DB16", "DB20", "DB25", "DB32", "DB40"],
        "typical_uses": ["งานพิเศษ", "สะพาน"],
        "typical_uses_english": ["special applications", "bridges"],
        "ductility_class": "ต่ำ",
        "ductility_class_english": "low",
        "weldability": "ยาก",
        "weldability_english": "difficult",
        "tis_standard": "TIS 24-2548",
        "ministry_approval": "มกท.2566"
    }
}

# Bar area and weight data
ACI_BAR_DATA = {
    "10M": {
        "nominal_diameter": 11.3,  # mm
        "nominal_area": 100,       # mm²
        "mass_per_meter": 0.785,   # kg/m
        "imperial_equivalent": "#3"
    },
    "15M": {
        "nominal_diameter": 16.0,
        "nominal_area": 200,
        "mass_per_meter": 1.570,
        "imperial_equivalent": "#5"
    },
    "20M": {
        "nominal_diameter": 19.5,
        "nominal_area": 300,
        "mass_per_meter": 2.355,
        "imperial_equivalent": "#6"
    },
    "25M": {
        "nominal_diameter": 25.2,
        "nominal_area": 500,
        "mass_per_meter": 3.925,
        "imperial_equivalent": "#8"
    },
    "30M": {
        "nominal_diameter": 29.9,
        "nominal_area": 700,
        "mass_per_meter": 5.495,
        "imperial_equivalent": "#9"
    },
    "35M": {
        "nominal_diameter": 35.7,
        "nominal_area": 1000,
        "mass_per_meter": 7.850,
        "imperial_equivalent": "#11"
    },
    "45M": {
        "nominal_diameter": 43.7,
        "nominal_area": 1500,
        "mass_per_meter": 11.775,
        "imperial_equivalent": "#14"
    },
    "55M": {
        "nominal_diameter": 56.4,
        "nominal_area": 2500,
        "mass_per_meter": 19.625,
        "imperial_equivalent": "#18"
    }
}

THAI_BAR_DATA = {
    "DB9": {
        "nominal_diameter": 9.0,   # mm
        "nominal_area": 64,        # mm²
        "mass_per_meter": 0.502,   # kg/m
        "thai_designation": "เหล็กข้อต่อ 9 มม."
    },
    "DB10": {
        "nominal_diameter": 9.5,
        "nominal_area": 71,
        "mass_per_meter": 0.557,
        "thai_designation": "เหล็กข้อต่อ 10 มม."
    },
    "DB12": {
        "nominal_diameter": 11.9,
        "nominal_area": 113,
        "mass_per_meter": 0.888,
        "thai_designation": "เหล็กข้อต่อ 12 มม."
    },
    "DB16": {
        "nominal_diameter": 15.9,
        "nominal_area": 199,
        "mass_per_meter": 1.562,
        "thai_designation": "เหล็กข้อต่อ 16 มม."
    },
    "DB20": {
        "nominal_diameter": 19.5,
        "nominal_area": 387,
        "mass_per_meter": 2.466,
        "thai_designation": "เหล็กข้อต่อ 20 มม."
    },
    "DB25": {
        "nominal_diameter": 25.2,
        "nominal_area": 507,
        "mass_per_meter": 3.980,
        "thai_designation": "เหล็กข้อต่อ 25 มม."
    },
    "DB32": {
        "nominal_diameter": 31.8,
        "nominal_area": 794,
        "mass_per_meter": 6.225,
        "thai_designation": "เหล็กข้อต่อ 32 มม."
    },
    "DB40": {
        "nominal_diameter": 39.9,
        "nominal_area": 1257,
        "mass_per_meter": 9.870,
        "thai_designation": "เหล็กข้อต่อ 40 มม."
    }
}

# Regional material variations
REGIONAL_MATERIAL_MODIFICATIONS = {
    "thailand": {
        "concrete": {
            "tropical_climate_factor": 1.1,  # Increased cover requirements
            "humidity_adjustment": 0.95,     # Reduced strength due to humidity
            "temperature_factor": 1.05,      # High temperature effects
            "monsoon_durability": 1.2        # Enhanced durability requirements
        },
        "steel": {
            "corrosion_protection": 1.3,     # Enhanced corrosion protection
            "coating_requirements": "epoxy_or_galvanized",
            "inspection_frequency": "quarterly"
        }
    },
    "north_america": {
        "concrete": {
            "freeze_thaw_resistance": 1.15,
            "air_entrainment": "required_for_exterior",
            "winter_construction": "special_procedures"
        },
        "steel": {
            "cold_weather_factor": 1.05,
            "welding_procedures": "certified_only"
        }
    }
}

# Utility functions
def get_concrete_grade(standard: str, grade: str) -> Dict[str, Any]:
    """Get concrete grade properties"""
    if standard.lower() == "aci":
        return ACI_CONCRETE_GRADES.get(grade.lower(), {})
    elif standard.lower() == "thai":
        return THAI_CONCRETE_GRADES.get(grade, {})
    else:
        return {}

def get_steel_grade(standard: str, grade: str) -> Dict[str, Any]:
    """Get steel grade properties"""
    if standard.lower() == "aci":
        return ACI_STEEL_GRADES.get(grade.upper(), {})
    elif standard.lower() == "thai":
        return THAI_STEEL_GRADES.get(grade.upper(), {})
    else:
        return {}

def get_bar_properties(standard: str, designation: str) -> Dict[str, Any]:
    """Get reinforcement bar properties"""
    if standard.lower() == "aci":
        return ACI_BAR_DATA.get(designation.upper(), {})
    elif standard.lower() == "thai":
        return THAI_BAR_DATA.get(designation.upper(), {})
    else:
        return {}

def list_available_grades(standard: str, material_type: str) -> List[str]:
    """List available grades for a standard and material type"""
    if standard.lower() == "aci":
        if material_type.lower() == "concrete":
            return list(ACI_CONCRETE_GRADES.keys())
        elif material_type.lower() == "steel":
            return list(ACI_STEEL_GRADES.keys())
    elif standard.lower() == "thai":
        if material_type.lower() == "concrete":
            return list(THAI_CONCRETE_GRADES.keys())
        elif material_type.lower() == "steel":
            return list(THAI_STEEL_GRADES.keys())
    
    return []