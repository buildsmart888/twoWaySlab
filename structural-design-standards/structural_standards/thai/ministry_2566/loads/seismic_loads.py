"""
Thai Seismic/Earthquake Load Calculations per TIS 1301/1302-61
=============================================================

Implementation of Thai seismic load calculations according to:
- TIS 1301/1302-61 (Revised Edition 1) - Standard for Earthquake Resistant Building Design
- Ministry Regulation B.E. 2566

การคำนวณแรงแผ่นดินไหวประเทศไทยตาม:
- มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1) มาตรฐานการออกแบบอาคารต้านทานการสั่นสะเทือนของแผ่นดินไหว
- กฎกระทรวง พ.ศ. 2566
"""

import math
from typing import Dict, Tuple, List, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum

from ....utils.validation import StructuralValidator, validate_positive


class ThaiSeismicZone(Enum):
    """Thai seismic zones per TIS 1301/1302-61"""
    ZONE_A = "A"  # Low risk areas (PGA = 0.15g)
    ZONE_B = "B"  # Moderate risk areas (PGA = 0.25g)
    ZONE_C = "C"  # High risk areas (PGA = 0.40g)


class ThaiSoilType(Enum):
    """Thai soil types per TIS 1301/1302-61"""
    TYPE_A = "A"  # Hard rock
    TYPE_B = "B"  # Rock
    TYPE_C = "C"  # Very dense soil
    TYPE_D = "D"  # Stiff soil
    TYPE_E = "E"  # Soft soil
    TYPE_F = "F"  # Special soil (requires site-specific study)


class ThaiSeismicImportance(Enum):
    """Building importance categories for seismic design"""
    STANDARD = "I"    # Standard buildings (I = 1.0)
    IMPORTANT = "II"  # Important buildings (I = 1.25)
    ESSENTIAL = "III" # Essential facilities (I = 1.5)


class ThaiStructuralSystem(Enum):
    """Structural systems for seismic resistance"""
    MOMENT_FRAME = "moment_frame"      # Moment resisting frame
    SHEAR_WALL = "shear_wall"          # Shear wall system
    DUAL_SYSTEM = "dual_system"        # Dual system
    BRACED_FRAME = "braced_frame"      # Braced frame system


@dataclass
class ThaiSeismicForces:
    """Thai seismic force results"""
    base_shear: float                    # Design base shear (kN)
    seismic_coefficient: float          # Seismic coefficient Cs
    fundamental_period: float           # Fundamental period Ta (sec)
    peak_ground_acceleration: float     # PGA (g)
    site_coefficient_fa: float          # Site coefficient Fa
    site_coefficient_fv: float          # Site coefficient Fv
    importance_factor: float            # Importance factor I
    response_modification: float        # Response modification factor R
    story_forces: Dict[int, float]      # Story forces by floor (kN)
    calculation_method: str = "TIS 1301/1302-61 Equivalent Lateral Force Method"


@dataclass
class ThaiBuildingGeometry:
    """Thai building geometry for seismic analysis"""
    total_height: float                    # Total height (m)
    story_heights: List[float]             # Story heights (m)
    story_weights: List[float]             # Story weights (kN)
    structural_system: ThaiStructuralSystem
    structural_material: str = "concrete"  # "concrete", "steel"


class ThaiSeismicLoads:
    """
    Thai Seismic/Earthquake Load Calculations per TIS 1301/1302-61
    
    ไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทยตาม มยผ. 1301/1302-61
    """
    
    def __init__(self):
        """Initialize Thai seismic loads calculator"""
        self.validator = StructuralValidator()
        
        # Peak ground accelerations by seismic zone
        self.peak_ground_accelerations = {
            ThaiSeismicZone.ZONE_A: 0.15,  # Low risk - 0.15g
            ThaiSeismicZone.ZONE_B: 0.25,  # Moderate risk - 0.25g
            ThaiSeismicZone.ZONE_C: 0.40   # High risk - 0.40g
        }
        
        # Site coefficient Fa (short period) tables
        self.site_coefficient_fa = {
            ThaiSoilType.TYPE_A: {0.15: 0.8, 0.25: 0.8, 0.40: 0.8},
            ThaiSoilType.TYPE_B: {0.15: 1.0, 0.25: 1.0, 0.40: 1.0},
            ThaiSoilType.TYPE_C: {0.15: 1.2, 0.25: 1.2, 0.40: 1.1},
            ThaiSoilType.TYPE_D: {0.15: 1.6, 0.25: 1.4, 0.40: 1.2},
            ThaiSoilType.TYPE_E: {0.15: 2.5, 0.25: 1.7, 0.40: 1.2}
        }
        
        # Site coefficient Fv (long period) tables
        self.site_coefficient_fv = {
            ThaiSoilType.TYPE_A: {0.15: 0.8, 0.25: 0.8, 0.40: 0.8},
            ThaiSoilType.TYPE_B: {0.15: 1.0, 0.25: 1.0, 0.40: 1.0},
            ThaiSoilType.TYPE_C: {0.15: 1.8, 0.25: 1.6, 0.40: 1.5},
            ThaiSoilType.TYPE_D: {0.15: 2.4, 0.25: 2.0, 0.40: 1.8},
            ThaiSoilType.TYPE_E: {0.15: 3.5, 0.25: 3.2, 0.40: 3.0}
        }
        
        # Importance factors by building category
        self.importance_factors = {
            ThaiSeismicImportance.STANDARD: 1.0,
            ThaiSeismicImportance.IMPORTANT: 1.25,
            ThaiSeismicImportance.ESSENTIAL: 1.5
        }
        
        # Structural system factors (R and Cd values)
        self.structural_system_factors = {
            ThaiStructuralSystem.MOMENT_FRAME: {
                'steel': {'R': 8, 'Cd': 5.5},
                'concrete': {'R': 8, 'Cd': 5.5}
            },
            ThaiStructuralSystem.SHEAR_WALL: {
                'concrete': {'R': 5, 'Cd': 5.0},
                'masonry': {'R': 2, 'Cd': 2.5}
            },
            ThaiStructuralSystem.DUAL_SYSTEM: {
                'steel': {'R': 8, 'Cd': 6.5},
                'concrete': {'R': 7, 'Cd': 5.5}
            },
            ThaiStructuralSystem.BRACED_FRAME: {
                'steel': {'R': 6, 'Cd': 5.0},
                'concrete': {'R': 6, 'Cd': 5.0}
            }
        }
        
        # Provincial seismic zone mapping
        self.provincial_zones = {
            # Northern Thailand - Higher seismic risk
            'เชียงใหม่': ThaiSeismicZone.ZONE_C, 'เชียงราย': ThaiSeismicZone.ZONE_C,
            'ลำปาง': ThaiSeismicZone.ZONE_B, 'ลำพูน': ThaiSeismicZone.ZONE_B,
            'แม่ฮ่องสอน': ThaiSeismicZone.ZONE_C, 'น่าน': ThaiSeismicZone.ZONE_B,
            'พะเยา': ThaiSeismicZone.ZONE_B, 'แพร่': ThaiSeismicZone.ZONE_B,
            
            # Western Thailand - Moderate to high risk  
            'กาญจนบุรี': ThaiSeismicZone.ZONE_B, 'ตาก': ThaiSeismicZone.ZONE_B,
            'สุพรรณบุรี': ThaiSeismicZone.ZONE_B, 'ราชบุรี': ThaiSeismicZone.ZONE_A,
            'เพชรบุรี': ThaiSeismicZone.ZONE_A, 'ประจวบคีรีขันธ์': ThaiSeismicZone.ZONE_A,
            
            # Central Thailand - Lower seismic risk
            'กรุงเทพมหานคร': ThaiSeismicZone.ZONE_A, 'นนทบุรี': ThaiSeismicZone.ZONE_A,
            'ปทุมธานี': ThaiSeismicZone.ZONE_A, 'สมุทรปราการ': ThaiSeismicZone.ZONE_A,
            'นครปฐม': ThaiSeismicZone.ZONE_A, 'สมุทรสาคร': ThaiSeismicZone.ZONE_A,
            
            # Eastern Thailand - Low risk
            'ชลบุรี': ThaiSeismicZone.ZONE_A, 'ระยอง': ThaiSeismicZone.ZONE_A,
            'จันทบุรี': ThaiSeismicZone.ZONE_A, 'ตราด': ThaiSeismicZone.ZONE_A,
            
            # Southern Thailand - Low risk
            'ภูเก็ต': ThaiSeismicZone.ZONE_A, 'สงขลา': ThaiSeismicZone.ZONE_A,
            'สุราษฎร์ธานี': ThaiSeismicZone.ZONE_A, 'นครศรีธรรมราช': ThaiSeismicZone.ZONE_A
        }
    
    def get_seismic_zone_data(self, location: Union[str, ThaiSeismicZone]) -> Dict[str, Any]:
        """Get seismic zone data for location"""
        if isinstance(location, str):
            zone = self.provincial_zones.get(location, ThaiSeismicZone.ZONE_A)
            location_desc = location
        else:
            zone = location
            location_desc = f"Zone {zone.value}"
        
        pga = self.peak_ground_accelerations[zone]
        
        return {
            'seismic_zone': zone,
            'peak_ground_acceleration': pga,
            'location': location_desc,
            'zone_description': f"Zone {zone.value} - PGA {pga}g"
        }
    
    def get_site_coefficients(self, pga: float, soil_type: ThaiSoilType) -> Tuple[float, float]:
        """Get site coefficients Fa and Fv"""
        validate_positive(pga, "Peak ground acceleration")
        
        # Find closest PGA value in tables
        available_pgas = list(self.site_coefficient_fa[soil_type].keys())
        closest_pga = min(available_pgas, key=lambda x: abs(x - pga))
        
        fa = self.site_coefficient_fa[soil_type][closest_pga]
        fv = self.site_coefficient_fv[soil_type][closest_pga]
        
        return fa, fv
    
    def calculate_fundamental_period(self, building_geometry: ThaiBuildingGeometry) -> float:
        """Calculate fundamental period of building"""
        validate_positive(building_geometry.total_height, "Building height")
        
        height = building_geometry.total_height
        system = building_geometry.structural_system
        material = building_geometry.structural_material
        
        # Constants Ct and x by structural system and material
        if system == ThaiStructuralSystem.MOMENT_FRAME:
            ct, x = (0.035, 0.8) if material == 'steel' else (0.030, 0.9)
        elif system == ThaiStructuralSystem.SHEAR_WALL:
            ct, x = 0.020, 0.9
        elif system == ThaiStructuralSystem.BRACED_FRAME:
            ct, x = (0.030, 0.8) if material == 'steel' else (0.030, 0.9)
        else:  # dual system
            ct, x = 0.030, 0.9
        
        # Approximate period formula: Ta = Ct * hn^x
        return ct * (height ** x)
    
    def calculate_seismic_coefficient(self, sds: float, r_factor: float, 
                                    importance_factor: float, ta: Optional[float] = None,
                                    sd1: Optional[float] = None) -> float:
        """Calculate seismic coefficient Cs"""
        validate_positive(sds, "Design spectral acceleration Sds")
        validate_positive(r_factor, "Response modification factor R")
        validate_positive(importance_factor, "Importance factor I")
        
        # Basic seismic coefficient
        cs = sds / (r_factor / importance_factor)
        
        # Apply limits
        cs_min = 0.01
        if ta and sd1 and ta > 0:
            cs_max = sd1 / (ta * (r_factor / importance_factor))
        else:
            cs_max = sds / 2.0
        
        return max(cs_min, min(cs, cs_max))
    
    def calculate_complete_seismic_analysis(self, 
                                          location: Union[str, ThaiSeismicZone],
                                          building_geometry: ThaiBuildingGeometry,
                                          soil_type: ThaiSoilType,
                                          importance_category: ThaiSeismicImportance) -> ThaiSeismicForces:
        """Complete seismic analysis per TIS 1301/1302-61"""
        
        # Get seismic zone data
        zone_data = self.get_seismic_zone_data(location)
        pga = zone_data['peak_ground_acceleration']
        
        # Site coefficients
        fa, fv = self.get_site_coefficients(pga, soil_type)
        
        # Design response spectrum parameters
        sms = fa * pga
        sm1 = fv * pga
        sds = (2.0/3.0) * sms
        sd1 = (2.0/3.0) * sm1
        
        # Building properties
        total_weight = sum(building_geometry.story_weights)
        importance_factor = self.importance_factors[importance_category]
        
        # Structural system factors
        material = building_geometry.structural_material
        system_factors = self.structural_system_factors[building_geometry.structural_system][material]
        r_factor = system_factors['R']
        
        # Fundamental period
        ta = self.calculate_fundamental_period(building_geometry)
        
        # Seismic coefficient
        cs = self.calculate_seismic_coefficient(sds, r_factor, importance_factor, ta, sd1)
        
        # Base shear
        base_shear = total_weight * cs
        
        # Distribute lateral forces
        # Calculate k factor for force distribution
        k = 1.0 if ta <= 0.5 else (2.0 if ta >= 2.5 else 1.0 + (ta - 0.5) / 2.0)
        
        # Calculate cumulative heights and distribute forces
        heights = []
        cumulative_height = 0.0
        for story_height in building_geometry.story_heights:
            cumulative_height += story_height
            heights.append(cumulative_height)
        
        weights = building_geometry.story_weights
        total_wh_k = sum(w * (h ** k) for w, h in zip(weights, heights))
        
        story_forces = {}
        for i, (weight, height) in enumerate(zip(weights, heights), 1):
            force = base_shear * (weight * (height ** k)) / total_wh_k
            story_forces[i] = force
        
        return ThaiSeismicForces(
            base_shear=base_shear,
            seismic_coefficient=cs,
            fundamental_period=ta,
            peak_ground_acceleration=pga,
            site_coefficient_fa=fa,
            site_coefficient_fv=fv,
            importance_factor=importance_factor,
            response_modification=r_factor,
            story_forces=story_forces
        )
    
    def generate_seismic_report(self, result: ThaiSeismicForces, 
                              project_info: Dict[str, str]) -> str:
        """Generate seismic load calculation report"""
        
        report = f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                     รายงานการคำนวณแรงแผ่นดินไหว                             ║
║                   THAI SEISMIC LOAD CALCULATION REPORT                        ║
║                     ตาม มยผ. 1301/1302-61 (ฉบับปรับปรุง)                      ║
╚════════════════════════════════════════════════════════════════════════════════╝

ข้อมูลโครงการ / Project Information:
{'-'*80}
ชื่อโครงการ / Project: {project_info.get('project_name', 'N/A')}
ตำแหน่ง / Location: {project_info.get('location', 'N/A')}
วันที่ / Date: {project_info.get('date', 'N/A')}

พารามิเตอร์แผ่นดินไหว / Seismic Parameters:
{'-'*80}
ความเร่งพื้นดินสูงสุด / PGA: {result.peak_ground_acceleration:.3f} g
ค่าสัมประสิทธิ์ดิน Fa: {result.site_coefficient_fa:.2f}
ค่าสัมประสิทธิ์ดิน Fv: {result.site_coefficient_fv:.2f}
ค่าประกอบความสำคัญ I: {result.importance_factor:.2f}
ค่าปรับลดแรง R: {result.response_modification:.1f}

ผลการวิเคราะห์ / Analysis Results:
{'-'*80}
คาบธรรมชาติ Ta: {result.fundamental_period:.3f} วินาที
ค่าสัมประสิทธิ์แผ่นดินไหว Cs: {result.seismic_coefficient:.4f}
แรงเฉือนฐาน V: {result.base_shear:.1f} kN

แรงด้านข้างแต่ละชั้น / Story Forces:
{'-'*80}
{'ชั้น':<8} {'แรงแผ่นดินไหว (kN)':<20}
{'Floor':<8} {'Seismic Force (kN)':<20}
{'-'*30}"""

        for floor, force in sorted(result.story_forces.items()):
            report += f"\n{floor:<8} {force:<20.1f}"
        
        report += f"""

วิธีการคำนวณ / Method: {result.calculation_method}

หมายเหตุ / Notes:
{'-'*80}
1. การคำนวณตาม มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1)
2. ใช้วิธี Equivalent Lateral Force Method
3. ควรตรวจสอบด้วยโปรแกรมวิเคราะห์โครงสร้าง
4. Based on TIS 1301/1302-61 (Revised Edition 1)
5. Equivalent Lateral Force Method used
6. Detailed structural analysis software recommended

รายงานสร้างโดย Thai Seismic Loads v1.0
Generated by Thai Seismic Loads v1.0
{'-'*80}
"""
        return report


# Convenience functions for quick calculations
def get_seismic_zone(province: str) -> ThaiSeismicZone:
    """Get seismic zone for Thai province"""
    seismic_calc = ThaiSeismicLoads()
    return seismic_calc.provincial_zones.get(province, ThaiSeismicZone.ZONE_A)


def quick_seismic_analysis(location: str, building_height: float, 
                          total_weight: float, soil_type: ThaiSoilType = ThaiSoilType.TYPE_C) -> Dict[str, float]:
    """Quick seismic load analysis for preliminary design"""
    seismic_calc = ThaiSeismicLoads()
    
    zone_data = seismic_calc.get_seismic_zone_data(location)
    pga = zone_data['peak_ground_acceleration']
    
    fa, fv = seismic_calc.get_site_coefficients(pga, soil_type)
    sds = (2.0/3.0) * fa * pga
    
    # Default parameters for quick analysis
    ta = 0.03 * (building_height ** 0.9)  # Concrete moment frame
    cs = seismic_calc.calculate_seismic_coefficient(sds, 8.0, 1.0, ta)  # R=8, I=1.0
    base_shear = total_weight * cs
    
    return {
        'seismic_zone': zone_data['seismic_zone'].value,
        'peak_ground_acceleration': pga,
        'seismic_coefficient': cs,
        'base_shear_kn': base_shear,
        'base_shear_per_weight': cs
    }