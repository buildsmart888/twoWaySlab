"""
Thai Ministry Regulation B.E. 2566 Package
==========================================

Complete implementation of Thai Ministry Regulation for Building Structural Design B.E. 2566 (2023)

กฎกระทรวง กำหนดการออกแบบโครงสร้างอาคาร และลักษณะและคุณสมบัติของวัสดุที่ใช้ในงานโครงสร้างอาคาร พ.ศ. 2566

Components:
- Load combinations and safety factors
- Design requirements (cover, deflection, tolerances)
- Material specifications integration
- Quality control requirements
- Compliance validation and reporting

องค์ประกอบ:
- การรวมแรงและค่าความปลอดภัย
- ข้อกำหนดการออกแบบ (คอนกรีตปิด, การโก่งตัว, ค่าเผื่อ)
- การบูรณาการข้อกำหนดวัสดุ
- ข้อกำหนดการควบคุมคุณภาพ
- การตรวจสอบการปฏิบัติตามและการรายงาน
"""

from .ministry_regulation import (
    ThaiMinistryRegulation2566,
    ThaiProjectData,
    ThaiComplianceResult
)

from .load_combinations import (
    ThaiMinistryLoadCombinations,
    ThaiLoadType,
    ThaiCombinationType,
    ThaiLoadCombination
)

from .design_requirements import (
    ThaiMinistryDesignRequirements,
    ThaiEnvironmentType,
    ThaiElementType,
    ThaiSupportType,
    ThaiCoverRequirement,
    ThaiDeflectionLimit
)

from .materials.concrete import (
    ThaiConcrete,
    ThaiConcreteGrade,
    ThaiConcreteProperties,
    create_fc180,
    create_fc210,
    create_fc240,
    create_fc280,
    create_fc350,
    mpa_to_ksc,
    ksc_to_mpa
)

from .materials.steel import (
    ThaiReinforcementSteel,
    ThaiSteelGrade,
    ThaiRebarDesignation,
    ThaiRebarProperties,
    ThaiSteelProperties
)

from .units.thai_units import (
    ThaiUnitConverter,
    ThaiPressureUnit,
    ThaiLengthUnit,
    ThaiAreaUnit,
    ThaiWeightUnit,
    ksc_to_mpa,
    mpa_to_ksc,
    convert_thai_length,
    convert_thai_area,
    convert_thai_weight
)

__version__ = '1.0.0'
__author__ = 'Thai Structural Design Standards Team'
__date__ = '2024'

# Package metadata
__title__ = 'Thai Ministry Regulation B.E. 2566'
__description__ = 'Complete implementation of Thai Ministry Regulation for Building Structural Design B.E. 2566 (2023)'
__url__ = 'https://github.com/structural-design-standards'
__license__ = 'MIT'

# Export main classes for easy import
__all__ = [
    # Main regulation class
    'ThaiMinistryRegulation2566',
    
    # Data structures
    'ThaiProjectData',
    'ThaiComplianceResult',
    
    # Load combinations
    'ThaiMinistryLoadCombinations',
    'ThaiLoadType',
    'ThaiCombinationType', 
    'ThaiLoadCombination',
    
    # Design requirements
    'ThaiMinistryDesignRequirements',
    'ThaiEnvironmentType',
    'ThaiElementType',
    'ThaiSupportType',
    'ThaiCoverRequirement',
    'ThaiDeflectionLimit',
    
    # Materials
    'ThaiConcrete',
    'ThaiConcreteGrade',
    'ThaiConcreteProperties',
    'ThaiReinforcementSteel',
    'ThaiSteelGrade',
    'ThaiRebarDesignation',
    'ThaiRebarProperties',
    'ThaiSteelProperties',
    
    # Convenience functions
    'create_fc180',
    'create_fc210',
    'create_fc240',
    'create_fc280',
    'create_fc350',
    'mpa_to_ksc',
    'ksc_to_mpa',
    
    # Thai units
    'ThaiUnitConverter',
    'ThaiPressureUnit',
    'ThaiLengthUnit',
    'ThaiAreaUnit',
    'ThaiWeightUnit',
    'convert_thai_length',
    'convert_thai_area',
    'convert_thai_weight'
]

# Version info
version_info = (1, 0, 0)

def get_regulation_summary():
    """Get summary of the Thai Ministry Regulation implementation"""
    return {
        'name_thai': 'กฎกระทรวง กำหนดการออกแบบโครงสร้างอาคาร และลักษณะและคุณสมบัติของวัสดุที่ใช้ในงานโครงสร้างอาคาร พ.ศ. 2566',
        'name_english': 'Ministry Regulation for Building Structural Design and Material Properties B.E. 2566 (2023)',
        'effective_date': '2023-12-01',
        'authority': 'กระทรวงมหาดไทย (Ministry of Interior)',
        'scope': 'Building structural design standards for Thailand',
        'version': __version__,
        'components': [
            'Load combinations and safety factors',
            'Concrete cover requirements',
            'Deflection limits',
            'Material specifications (concrete and steel)',
            'Quality control requirements',
            'Construction tolerances',
            'Wind and seismic loads (TIS standards)',
            'Thai unit conversion systems (ksc ↔ MPa)',
            'Compliance checking and reporting'
        ],
        'supported_materials': [
            'Thai concrete grades: Fc180, Fc210, Fc240, Fc280, Fc350',
            'Thai steel grades: SR24, SD40, SD50',
            'Thai rebar designations: DB10-DB40, RB6-RB9'
        ],
        'supported_environments': [
            'Normal environment (สภาพแวดล้อมปกติ)',
            'Aggressive environment (สภาพแวดล้อมรุนแรง)',
            'Marine environment (สภาพแวดล้อมทางทะเล)'
        ]
    }

def create_thai_regulation():
    """
    Convenience function to create Thai Ministry Regulation instance
    
    Returns:
    --------
    ThaiMinistryRegulation2566
        Thai regulation instance
    """
    return ThaiMinistryRegulation2566()

# Quick access functions
def get_concrete_cover(element_type: str, environment: str = 'normal'):
    """
    Quick function to get concrete cover requirement
    
    Parameters:
    -----------
    element_type : str
        Element type ('slab', 'beam', 'column', 'foundation')
    environment : str
        Environment type ('normal', 'aggressive', 'marine')
        
    Returns:
    --------
    float
        Required cover in mm
    """
    regulation = ThaiMinistryRegulation2566()
    
    # Convert string to enum
    element_enum = {
        'slab': ThaiElementType.SLAB,
        'beam': ThaiElementType.BEAM,
        'column': ThaiElementType.COLUMN,
        'foundation': ThaiElementType.FOUNDATION
    }.get(element_type.lower())
    
    env_enum = {
        'normal': ThaiEnvironmentType.NORMAL,
        'aggressive': ThaiEnvironmentType.AGGRESSIVE,
        'marine': ThaiEnvironmentType.MARINE
    }.get(environment.lower())
    
    if element_enum and env_enum:
        cover_req = regulation.get_concrete_cover(element_enum, env_enum)
        return cover_req.cover_mm if cover_req else None
    
    return None

def get_safety_factor(material_or_load: str):
    """
    Quick function to get safety factor
    
    Parameters:
    -----------
    material_or_load : str
        Material or load type
        
    Returns:
    --------
    float
        Safety factor
    """
    regulation = ThaiMinistryRegulation2566()
    return regulation.get_safety_factor(material_or_load)

# Module-level constants
REGULATION_NAME_THAI = 'กฎกระทรวง พ.ศ. 2566'
REGULATION_NAME_ENGLISH = 'Ministry Regulation B.E. 2566'
EFFECTIVE_DATE = '2023-12-01'
AUTHORITY = 'กระทรวงมหาดไทย'

# Display package information when imported
print(f"📋 {REGULATION_NAME_THAI}")
print(f"📋 {REGULATION_NAME_ENGLISH}")
print(f"✅ Thai Ministry Regulation B.E. 2566 Package v{__version__} loaded successfully")
print(f"🏗️  Ready for Thai structural design standards compliance checking")