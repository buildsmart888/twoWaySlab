"""
Thai Loads Package - Ministry Regulation B.E. 2566
===================================================

Load calculation modules for Thai building standards including:
- Wind loads (TIS 1311-50)
- Seismic loads (TIS 1301/1302-61)
- Load combinations per Ministry Regulation B.E. 2566

โมดูลการคำนวณแรงตามมาตรฐานไทย รวมถึง:
- แรงลม (มยผ. 1311-50)
- แรงแผ่นดินไหว (มยผ. 1301/1302-61)
- การรวมแรงตามกฎกระทรวง พ.ศ. 2566
"""

from .wind_loads import (
    ThaiWindLoads,
    ThaiWindZone,
    ThaiTerrainCategory,
    ThaiBuildingImportance,
    ThaiTopographyType,
    ThaiBuildingGeometry,
    ThaiWindLoadResult
)

from .seismic_loads import (
    ThaiSeismicLoads,
    ThaiSeismicZone,
    ThaiSoilType,
    ThaiSeismicImportance,
    ThaiStructuralSystem,
    ThaiSeismicForces,
    ThaiBuildingGeometry as ThaiSeismicBuildingGeometry,
    get_seismic_zone,
    quick_seismic_analysis
)

__version__ = '1.0.0'
__author__ = 'Thai Structural Design Standards Team'

__all__ = [
    # Wind loads
    'ThaiWindLoads',
    'ThaiWindZone',
    'ThaiTerrainCategory',
    'ThaiBuildingImportance', 
    'ThaiTopographyType',
    'ThaiBuildingGeometry',
    'ThaiWindLoadResult',
    
    # Seismic loads
    'ThaiSeismicLoads',
    'ThaiSeismicZone',
    'ThaiSoilType',
    'ThaiSeismicImportance',
    'ThaiStructuralSystem',
    'ThaiSeismicForces',
    'ThaiSeismicBuildingGeometry',
    'get_seismic_zone',
    'quick_seismic_analysis'
]

# Package information
PACKAGE_INFO = {
    'name': 'Thai Loads Package',
    'description': 'Load calculation modules for Thai building standards',
    'standards': [
        'TIS 1311-50: Wind Load Calculation',
        'TIS 1301/1302-61: Seismic Load Calculation',
        'Ministry Regulation B.E. 2566: Load Combinations'
    ],
    'version': __version__
}

def get_available_load_types():
    """Get available load calculation types"""
    return {
        'wind_loads': 'Thai wind loads per TIS 1311-50',
        'seismic_loads': 'Thai seismic loads per TIS 1301/1302-61',
        'load_combinations': 'Load combinations per Ministry Regulation B.E. 2566'
    }