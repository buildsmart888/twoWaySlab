#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Thai Earthquake/Seismic Load Calculation Library
ไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย

Based on:
- มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1) มาตรฐานการออกแบบอาคารต้านทานการสั่นสะเทือนของแผ่นดินไหว
- TIS 1301/1302-61 (Revised Edition 1) - Standard for Earthquake Resistant Building Design

@author: Enhanced by AI Assistant  
@date: 2024
@version: 1.0
"""

import math
from typing import Dict, Tuple, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

class SeismicZone(Enum):
    """โซนแผ่นดินไหวในประเทศไทยตาม มยผ. 1301/1302-61 / Seismic zones in Thailand according to TIS 1301/1302-61"""
    ZONE_A = "A"  # โซน A - พื้นที่เสี่ยงต่ำ / Zone A - Low risk areas
    ZONE_B = "B"  # โซน B - พื้นที่เสี่ยงปานกลาง / Zone B - Moderate risk areas
    ZONE_C = "C"  # โซน C - พื้นที่เสี่ยงสูง / Zone C - High risk areas

class SoilType(Enum):
    """ประเภทชั้นดินตาม มยผ. 1301/1302-61 / Soil types according to TIS 1301/1302-61"""
    TYPE_A = "A"  # หินแข็ง / Hard rock
    TYPE_B = "B"  # หินอ่อน / Rock  
    TYPE_C = "C"  # ดินแน่นมาก / Very dense soil
    TYPE_D = "D"  # ดินแน่นปานกลาง / Stiff soil
    TYPE_E = "E"  # ดินอ่อน / Soft soil
    TYPE_F = "F"  # ดินพิเศษ / Special soil

class BuildingImportance(Enum):
    """ระดับความสำคัญของอาคารตามแผ่นดินไหว / Building importance levels for seismic design"""
    STANDARD = "I"       # อาคารทั่วไป / Standard buildings (I = 1.0)
    IMPORTANT = "II"     # อาคารสำคัญ / Important buildings (I = 1.25)
    ESSENTIAL = "III"    # อาคารจำเป็น / Essential facilities (I = 1.5)

class StructuralSystem(Enum):
    """ระบบโครงสร้างต้านทานแผ่นดินไหว / Structural systems for seismic resistance"""
    MOMENT_FRAME = "moment_frame"           # โครงข้อแข็ง / Moment resisting frame
    SHEAR_WALL = "shear_wall"              # กำแพงรับแรงเฉือน / Shear wall
    DUAL_SYSTEM = "dual_system"            # ระบบผสม / Dual system
    BRACED_FRAME = "braced_frame"          # โครงค้ำยัน / Braced frame

@dataclass
class SeismicLoadResult:
    """ผลลัพธ์การคำนวณแรงแผ่นดินไหว / Seismic load calculation result"""
    design_base_shear: float         # แรงเฉือนฐานออกแบบ kN / Design base shear (kN)
    seismic_coefficient: float       # ค่าสัมประสิทธิ์แผ่นดินไหว / Seismic coefficient
    peak_ground_acceleration: float  # ความเร่งพื้นดินสูงสุด g / Peak ground acceleration (g)
    site_coefficient_fa: float       # ค่าประกอบดิน Fa / Site coefficient Fa
    site_coefficient_fv: float       # ค่าประกอบดิน Fv / Site coefficient Fv
    importance_factor: float         # ค่าประกอบความสำคัญ / Importance factor
    response_modification: float     # ค่าปรับลดแรง R / Response modification factor
    fundamental_period: float        # คาบธรรมชาติ วินาที / Fundamental period (sec)
    story_forces: Dict[int, float]   # แรงแผ่นดินไหวแต่ละชั้น kN / Story forces by floor (kN)
    lateral_displacement: Dict[int, float]  # การเคลื่อนตัวด้านข้าง mm / Lateral displacement by floor (mm)
    drift_ratio: Dict[int, float]    # อัตราส่วนการเอียง / Drift ratio by floor
    description: str                 # คำอธิบาย / Description
    calculation_method: str          # วิธีการคำนวณ / Calculation method

@dataclass
class BuildingGeometrySeismic:
    """ข้อมูลรูปทรงอาคารสำหรับการคำนวณแผ่นดินไหว / Building geometry for seismic analysis"""
    total_height: float              # ความสูงรวม m / Total height (m)
    story_heights: List[float]       # ความสูงแต่ละชั้น m / Story heights (m)
    story_weights: List[float]       # น้ำหนักแต่ละชั้น kN / Story weights (kN)
    plan_dimensions: Tuple[float, float]  # ขนาดผัง (ยาว, กว้าง) m / Plan dimensions (length, width) (m)
    structural_system: StructuralSystem   # ระบบโครงสร้าง / Structural system
    building_type: str               # ประเภทอาคาร / Building type
    irregularity_factors: Dict[str, float]  # ค่าประกอบความผิดปกติ / Irregularity factors

class ThaiEarthquakeLoad:
    """ไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย / Thai Earthquake Load Calculation Library
    
    ตามมาตรฐาน:
    - มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1) มาตรฐานการออกแบบอาคารต้านทานการสั่นสะเทือนของแผ่นดินไหว
    
    Based on Standards:
    - TIS 1301/1302-61 (Revised Edition 1) - Standard for Earthquake Resistant Building Design
    """
    
    def __init__(self):
        """เริ่มต้นเครื่องคำนวณแรงแผ่นดินไหวตามมาตรฐานไทย / Initialize earthquake load calculator with Thai standards"""
        
        # ความเร่งพื้นดินสูงสุดแยกตามโซน (g) / Peak ground acceleration by seismic zone (g)
        self.peak_ground_accelerations = {
            SeismicZone.ZONE_A: 0.15,  # โซน A - 0.15g
            SeismicZone.ZONE_B: 0.25,  # โซน B - 0.25g  
            SeismicZone.ZONE_C: 0.40   # โซน C - 0.40g
        }
        
        # ค่าสัมประสิทธิ์ดิน Fa (Short period) ตาม มยผ. 1301/1302-61
        self.site_coefficient_fa = {
            SoilType.TYPE_A: {0.15: 0.8, 0.25: 0.8, 0.40: 0.8},
            SoilType.TYPE_B: {0.15: 1.0, 0.25: 1.0, 0.40: 1.0},  
            SoilType.TYPE_C: {0.15: 1.2, 0.25: 1.2, 0.40: 1.1},
            SoilType.TYPE_D: {0.15: 1.6, 0.25: 1.4, 0.40: 1.2},
            SoilType.TYPE_E: {0.15: 2.5, 0.25: 1.7, 0.40: 1.2},
            SoilType.TYPE_F: {0.15: 0.0, 0.25: 0.0, 0.40: 0.0}  # ต้องศึกษาเฉพาะ / Site-specific study required
        }
        
        # ค่าสัมประสิทธิ์ดิน Fv (Long period) ตาม มยผ. 1301/1302-61
        self.site_coefficient_fv = {
            SoilType.TYPE_A: {0.15: 0.8, 0.25: 0.8, 0.40: 0.8},
            SoilType.TYPE_B: {0.15: 1.0, 0.25: 1.0, 0.40: 1.0},
            SoilType.TYPE_C: {0.15: 1.8, 0.25: 1.6, 0.40: 1.5},
            SoilType.TYPE_D: {0.15: 2.4, 0.25: 2.0, 0.40: 1.8},
            SoilType.TYPE_E: {0.15: 3.5, 0.25: 3.2, 0.40: 3.0},
            SoilType.TYPE_F: {0.15: 0.0, 0.25: 0.0, 0.40: 0.0}  # ต้องศึกษาเฉพาะ / Site-specific study required
        }
        
        # ค่าประกอบความสำคัญ I ตามการใช้งานอาคาร / Importance factors by building usage
        self.importance_factors = {
            BuildingImportance.STANDARD: {
                'factor': 1.0,
                'description': 'อาคารทั่วไป',
                'description_en': 'Standard buildings',
                'examples': 'อาคารที่อยู่อาศัย อาคารสำนักงาน โรงงาน'
            },
            BuildingImportance.IMPORTANT: {
                'factor': 1.25,
                'description': 'อาคารสำคัญ', 
                'description_en': 'Important buildings',
                'examples': 'โรงเรียน โรงพยาบาล อาคารชุมนุมคน'
            },
            BuildingImportance.ESSENTIAL: {
                'factor': 1.5,
                'description': 'อาคารจำเป็น',
                'description_en': 'Essential facilities', 
                'examples': 'สถานีตำรวจ สถานีดับเพลิง โรงพยาบาลฉุกเฉิน'
            }
        }
        
        # ค่าปรับลดแรง R และค่าขยายการเคลื่อนตัว Cd ตามระบบโครงสร้าง / Response modification factors R and deflection amplification Cd
        self.structural_system_factors = {
            StructuralSystem.MOMENT_FRAME: {
                'steel': {'R': 8, 'Cd': 5.5, 'description': 'โครงข้อแข็งเหล็ก'},
                'concrete': {'R': 8, 'Cd': 5.5, 'description': 'โครงข้อแข็งคอนกรีต'},
                'description_en': 'Moment resisting frame'
            },
            StructuralSystem.SHEAR_WALL: {
                'concrete': {'R': 5, 'Cd': 5.0, 'description': 'กำแพงรับแรงเฉือนคอนกรีต'},
                'masonry': {'R': 2, 'Cd': 2.5, 'description': 'กำแพงรับแรงเฉือนก่ออิฐ'},
                'description_en': 'Shear wall system'
            },
            StructuralSystem.DUAL_SYSTEM: {
                'steel': {'R': 8, 'Cd': 6.5, 'description': 'ระบบผสมเหล็ก'},
                'concrete': {'R': 7, 'Cd': 5.5, 'description': 'ระบบผสมคอนกรีต'},
                'description_en': 'Dual system'
            },
            StructuralSystem.BRACED_FRAME: {
                'steel': {'R': 6, 'Cd': 5.0, 'description': 'โครงค้ำยันเหล็ก'},
                'concrete': {'R': 6, 'Cd': 5.0, 'description': 'โครงค้ำยันคอนกรีต'},
                'description_en': 'Braced frame system'
            }
        }
        
        # ขีดจำกัดการเอียง (Drift limits) ตาม มยผ. 1301/1302-61 / Drift limits according to TIS 1301/1302-61
        self.drift_limits = {
            'residential': 0.02,      # อาคารที่อยู่อาศัย 2%
            'office': 0.02,          # อาคารสำนักงาน 2%
            'industrial': 0.025,     # อาคารอุตสาหกรรม 2.5%
            'warehouse': 0.025       # โกดัง 2.5%
        }
        
        # จังหวัดไทยและโซนแผ่นดินไหวที่สอดคล้อง / Thai provinces and their seismic zones
        self.province_seismic_zones = {
            # Northern Thailand - Higher seismic risk
            'เชียงใหม่': SeismicZone.ZONE_C, 'เชียงราย': SeismicZone.ZONE_C,
            'ลำปาง': SeismicZone.ZONE_B, 'ลำพูน': SeismicZone.ZONE_B,
            'แม่ฮ่องสอน': SeismicZone.ZONE_C, 'น่าน': SeismicZone.ZONE_B,
            'พะเยา': SeismicZone.ZONE_B, 'แพร่': SeismicZone.ZONE_B,
            
            # Western Thailand - Moderate to high risk
            'กาญจนบุรี': SeismicZone.ZONE_B, 'ตาก': SeismicZone.ZONE_B,
            'เพชรบุรี': SeismicZone.ZONE_A, 'ประจวบคีรีขันธ์': SeismicZone.ZONE_A,
            
            # Central Thailand - Lower seismic risk
            'กรุงเทพมหานคร': SeismicZone.ZONE_A, 'นนทบุรี': SeismicZone.ZONE_A,
            'ปทุมธานี': SeismicZone.ZONE_A, 'สมุทรปราการ': SeismicZone.ZONE_A,
            'นครปฐม': SeismicZone.ZONE_A, 'ราชบุรี': SeismicZone.ZONE_A,
            
            # Northeastern Thailand - Low to moderate risk
            'นครราชสีมา': SeismicZone.ZONE_A, 'ขอนแก่น': SeismicZone.ZONE_A,
            'อุดรธานี': SeismicZone.ZONE_A, 'อุบลราชธานี': SeismicZone.ZONE_A,
            
            # Eastern Thailand - Low risk
            'ชลบุรี': SeismicZone.ZONE_A, 'ระยอง': SeismicZone.ZONE_A,
            'จันทบุรี': SeismicZone.ZONE_A, 'ตราด': SeismicZone.ZONE_A,
            
            # Southern Thailand - Low risk
            'ภูเก็ต': SeismicZone.ZONE_A, 'สงขลา': SeismicZone.ZONE_A,
            'สุราษฎร์ธานี': SeismicZone.ZONE_A, 'นครศรีธรรมราช': SeismicZone.ZONE_A
        }

    def get_seismic_zone_info(self, location: Union[str, SeismicZone]) -> Tuple[SeismicZone, float, str]:
        """ดึงข้อมูลโซนแผ่นดินไหวสำหรับตำแหน่งที่ตั้ง / Get seismic zone information for location
        
        Args:
            location: ชื่อจังหวัด (ไทย) หรือ SeismicZone enum / Province name (Thai) or SeismicZone enum
            
        Returns:
            Tuple ของ (SeismicZone, ความเร่งพื้นดิน_g, คำอธิบาย) / Tuple of (SeismicZone, PGA_g, description)
        """
        if isinstance(location, str):
            if location in self.province_seismic_zones:
                zone = self.province_seismic_zones[location]
                pga = self.peak_ground_accelerations[zone]
                description = f"Zone {zone.value} - {location}"
            else:
                # Default to Zone A for unknown locations
                zone = SeismicZone.ZONE_A
                pga = self.peak_ground_accelerations[zone]
                description = f"Zone {zone.value} - ไม่ทราบจังหวัด (Unknown province)"
        else:
            zone = location
            pga = self.peak_ground_accelerations[zone]
            description = f"Zone {zone.value}"
        
        return zone, pga, description

    def get_site_coefficients(self, pga: float, soil_type: SoilType) -> Tuple[float, float]:
        """ค่าสัมประสิทธิ์ดิน Fa และ Fv / Get site coefficients Fa and Fv
        
        Args:
            pga: ความเร่งพื้นดินสูงสุด g / Peak ground acceleration (g)
            soil_type: ประเภทชั้นดิน / Soil type
            
        Returns:
            Tuple ของ (Fa, Fv) / Tuple of (Fa, Fv)
        """
        # ปัดเศษ PGA ให้ตรงกับตารางมาตรฐาน / Round PGA to match standard table values
        pga_rounded = min(self.site_coefficient_fa[soil_type].keys(), 
                         key=lambda x: abs(x - pga))
        
        fa = self.site_coefficient_fa[soil_type][pga_rounded]
        fv = self.site_coefficient_fv[soil_type][pga_rounded]
        
        return fa, fv

    def calculate_design_response_spectrum_parameters(self, pga: float, fa: float, fv: float) -> Tuple[float, float, float, float, float]:
        """คำนวณพารามิเตอร์สเปกตรัมการตอบสนองออกแบบ / Calculate design response spectrum parameters
        
        Args:
            pga: ความเร่งพื้นดินสูงสุด g / Peak ground acceleration (g)
            fa: ค่าสัมประสิทธิ์ดิน Fa / Site coefficient Fa  
            fv: ค่าสัมประสิทธิ์ดิน Fv / Site coefficient Fv
            
        Returns:
            Tuple ของ (Sms, Sm1, Sds, Sd1, Ts) / Tuple of design spectrum parameters
        """
        # Site-Modified Spectral Acceleration Parameters
        Sms = fa * pga  # Site-modified short period acceleration
        Sm1 = fv * pga  # Site-modified 1-second period acceleration
        
        # Design Spectral Acceleration Parameters
        Sds = (2.0/3.0) * Sms  # Design short period acceleration
        Sd1 = (2.0/3.0) * Sm1  # Design 1-second period acceleration
        
        # Transition periods
        Ts = Sd1 / Sds if Sds > 0 else 0.0  # Short period transition
        
        return Sms, Sm1, Sds, Sd1, Ts

    def calculate_fundamental_period(self, building_geometry: BuildingGeometrySeismic, 
                                  material: str = 'concrete') -> float:
        """คำนวณคาบธรรมชาติพื้นฐานของอาคาร / Calculate fundamental period of building
        
        Args:
            building_geometry: ข้อมูลรูปทรงอาคาร / Building geometry
            material: วัสดุโครงสร้าง / Structural material ('concrete', 'steel')
            
        Returns:
            คาบธรรมชาติ วินาที / Fundamental period (seconds)
        """
        height = building_geometry.total_height
        
        # ค่าคงที่ Ct และ x ตามประเภทโครงสร้างและวัสดุ / Constants Ct and x by structure type and material
        if building_geometry.structural_system == StructuralSystem.MOMENT_FRAME:
            if material == 'steel':
                Ct, x = 0.035, 0.8
            else:  # concrete
                Ct, x = 0.030, 0.9
        elif building_geometry.structural_system == StructuralSystem.SHEAR_WALL:
            Ct, x = 0.020, 0.9
        elif building_geometry.structural_system == StructuralSystem.BRACED_FRAME:
            if material == 'steel':
                Ct, x = 0.030, 0.8  
            else:  # concrete
                Ct, x = 0.030, 0.9
        else:  # dual system
            Ct, x = 0.030, 0.9
        
        # สูตรประมาณคาบธรรมชาติ / Approximate period formula: Ta = Ct * hn^x
        Ta = Ct * (height ** x)
        
        return Ta

    def calculate_seismic_coefficient(self, Sds: float, R: float, I: float, Ta: float = None, Sd1: float = None) -> float:
        """คำนวณค่าสัมประสิทธิ์แผ่นดินไหว / Calculate seismic coefficient
        
        Args:
            Sds: ความเร่งสเปกตรัมออกแบบคาบสั้น / Design short period spectral acceleration
            R: ค่าปรับลดแรง / Response modification factor
            I: ค่าประกอบความสำคัญ / Importance factor
            Ta: คาบธรรมชาติ วินาที / Fundamental period (optional)
            Sd1: ความเร่งสเปกตรัมออกแบบคาบ 1 วินาที / Design 1-sec spectral acceleration (optional)
            
        Returns:
            ค่าสัมประสิทธิ์แผ่นดินไหว / Seismic coefficient
        """
        # สูตรพื้นฐาน / Basic formula
        Cs = Sds / (R / I)
        
        # ขีดจำกัดต่ำสุด / Minimum limit
        Cs_min = 0.01
        
        # ขีดจำกัดสูงสุดตามคาบธรรมชาติ / Maximum limit based on period
        if Ta and Sd1 and Ta > 0:
            Cs_max = Sd1 / (Ta * (R / I))
        else:
            Cs_max = Sds / 2.0
        
        return max(Cs_min, min(Cs, Cs_max))

    def calculate_base_shear(self, total_weight: float, seismic_coefficient: float) -> float:
        """คำนวณแรงเฉือนฐาน / Calculate base shear
        
        Args:
            total_weight: น้ำหนักรวมของอาคาร kN / Total building weight (kN)
            seismic_coefficient: ค่าสัมประสิทธิ์แผ่นดินไหว / Seismic coefficient
            
        Returns:
            แรงเฉือนฐาน kN / Base shear (kN)
        """
        return total_weight * seismic_coefficient

    def distribute_lateral_forces(self, base_shear: float, building_geometry: BuildingGeometrySeismic, 
                                period: float) -> Dict[int, float]:
        """กระจายแรงด้านข้างไปยังแต่ละชั้น / Distribute lateral forces to each floor
        
        Args:
            base_shear: แรงเฉือนฐาน kN / Base shear (kN)
            building_geometry: ข้อมูลรูปทรงอาคาร / Building geometry
            period: คาบธรรมชาติ วินาที / Fundamental period (seconds)
            
        Returns:
            Dict ของแรงด้านข้างแต่ละชั้น {ชั้น: แรง_kN} / Dict of lateral forces by floor {floor: force_kN}
        """
        story_forces = {}
        
        # คำนวณค่า k สำหรับการกระจายแรง / Calculate k factor for force distribution
        if period <= 0.5:
            k = 1.0
        elif period >= 2.5:
            k = 2.0
        else:
            k = 1.0 + (period - 0.5) / 2.0
        
        # คำนวณความสูงสะสมแต่ละชั้น / Calculate cumulative heights
        heights = []
        cumulative_height = 0
        for story_height in building_geometry.story_heights:
            cumulative_height += story_height
            heights.append(cumulative_height)
        
        # คำนวณตัวส่วนรวม / Calculate total denominator
        weights = building_geometry.story_weights
        total_wh_k = sum(w * (h ** k) for w, h in zip(weights, heights))
        
        # กระจายแรงไปยังแต่ละชั้น / Distribute forces to each floor
        for i, (weight, height) in enumerate(zip(weights, heights), 1):
            force = base_shear * (weight * (height ** k)) / total_wh_k
            story_forces[i] = force
        
        return story_forces

    def calculate_lateral_displacement(self, story_forces: Dict[int, float], 
                                    building_geometry: BuildingGeometrySeismic,
                                    structural_properties: Dict) -> Tuple[Dict[int, float], Dict[int, float]]:
        """คำนวณการเคลื่อนตัวด้านข้างและอัตราส่วนการเอียง / Calculate lateral displacement and drift ratios"""
        Cd = structural_properties.get('Cd', 5.0)
        
        # Simplified displacement calculation (for detailed analysis, use structural software)
        displacements = {}
        drift_ratios = {}
        
        # Approximate story stiffness (simplified)
        story_heights = building_geometry.story_heights
        
        for i, (story_force, story_height) in enumerate(zip(story_forces.values(), story_heights), 1):
            # Simplified elastic displacement (mm)
            elastic_displacement = story_force * story_height * 0.001  # Simplified formula
            # Amplified displacement
            total_displacement = elastic_displacement * Cd
            displacements[i] = total_displacement
            
            # Drift ratio calculation
            if i == 1:
                story_drift = total_displacement
            else:
                story_drift = total_displacement - displacements[i-1]
            
            drift_ratio = story_drift / (story_height * 1000)  # Convert to ratio
            drift_ratios[i] = drift_ratio
        
        return displacements, drift_ratios

    def get_seismic_load_summary(self, location: str, building_height: float, 
                               soil_type: SoilType = SoilType.TYPE_C) -> Dict[str, Union[str, float]]:
        """สรุปแรงแผ่นดินไหวอย่างรวดเร็ว / Quick seismic load summary"""
        zone, pga, zone_desc = self.get_seismic_zone_info(location)
        fa, fv = self.get_site_coefficients(pga, soil_type)
        Sms, Sm1, Sds, Sd1, Ts = self.calculate_design_response_spectrum_parameters(pga, fa, fv)
        
        # Basic building properties for quick analysis
        estimated_weight = building_height * 15.0  # Rough estimate: 15 kN/m²/m height
        R = 8.0  # Moment frame default
        I = 1.0  # Standard building
        
        # Fundamental period (approximate)
        Ta = 0.03 * (building_height ** 0.9)  # Concrete moment frame
        
        # Seismic coefficient
        Cs = self.calculate_seismic_coefficient(Sds, R, I, Ta, Sd1)
        
        # Base shear
        base_shear = estimated_weight * Cs
        
        return {
            'location': location,
            'zone': zone_desc,
            'peak_ground_acceleration_g': pga,
            'site_coefficient_fa': fa,
            'site_coefficient_fv': fv,
            'design_spectrum_sds': Sds,
            'seismic_coefficient': Cs,
            'fundamental_period_sec': Ta,
            'base_shear_per_height_kn_m': base_shear / building_height,
            'estimated_base_shear_kn': base_shear
        }

    def calculate_complete_seismic_analysis(self, location: str, 
                                          building_geometry: BuildingGeometrySeismic,
                                          soil_type: SoilType,
                                          building_importance: BuildingImportance,
                                          material: str = 'concrete') -> SeismicLoadResult:
        """การวิเคราะห์แรงแผ่นดินไหวครบถ้วน / Complete seismic analysis"""
        
        # Get seismic zone information
        zone, pga, zone_desc = self.get_seismic_zone_info(location)
        
        # Site coefficients
        fa, fv = self.get_site_coefficients(pga, soil_type)
        
        # Design response spectrum parameters
        Sms, Sm1, Sds, Sd1, Ts = self.calculate_design_response_spectrum_parameters(pga, fa, fv)
        
        # Building properties
        total_weight = sum(building_geometry.story_weights)
        I = self.importance_factors[building_importance]['factor']
        
        # Structural system factors
        system_factors = self.structural_system_factors[building_geometry.structural_system][material]
        R = system_factors['R']
        Cd = system_factors['Cd']
        
        # Fundamental period
        Ta = self.calculate_fundamental_period(building_geometry, material)
        
        # Seismic coefficient
        Cs = self.calculate_seismic_coefficient(Sds, R, I, Ta, Sd1)
        
        # Base shear
        base_shear = self.calculate_base_shear(total_weight, Cs)
        
        # Distribute lateral forces
        story_forces = self.distribute_lateral_forces(base_shear, building_geometry, Ta)
        
        # Calculate displacements and drift
        structural_props = {'Cd': Cd, 'R': R}
        displacements, drift_ratios = self.calculate_lateral_displacement(
            story_forces, building_geometry, structural_props)
        
        # Create result
        result = SeismicLoadResult(
            design_base_shear=base_shear,
            seismic_coefficient=Cs,
            peak_ground_acceleration=pga,
            site_coefficient_fa=fa,
            site_coefficient_fv=fv,
            importance_factor=I,
            response_modification=R,
            fundamental_period=Ta,
            story_forces=story_forces,
            lateral_displacement=displacements,
            drift_ratio=drift_ratios,
            description=f"การวิเคราะห์แรงแผ่นดินไหว {zone_desc} ตาม มยผ. 1301/1302-61",
            calculation_method="TIS 1301/1302-61 Equivalent Lateral Force Method"
        )
        
        return result

    def generate_seismic_load_report(self, result: SeismicLoadResult, 
                                   building_info: Dict[str, str]) -> str:
        """สร้างรายงานการคำนวณแรงแผ่นดินไหว / Generate seismic load calculation report"""
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                            รายงานการคำนวณแรงแผ่นดินไหว                            ║
║                         THAI SEISMIC LOAD CALCULATION REPORT                         ║
║                        ตาม มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1)                  ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

ข้อมูลโครงการ / Project Information:
{'='*80}
ชื่อโครงการ / Project Name: {building_info.get('project_name', 'N/A')}
ตำแหน่ง / Location: {building_info.get('location', 'N/A')}
วันที่ / Date: {building_info.get('date', 'N/A')}
วิศวกร / Engineer: {building_info.get('engineer', 'N/A')}

พารามิเตอร์แผ่นดินไหว / Seismic Parameters:
{'='*80}
ความเร่งพื้นดินสูงสุด / Peak Ground Acceleration (PGA): {result.peak_ground_acceleration:.3f} g
ค่าสัมประสิทธิ์ดิน Fa / Site Coefficient Fa: {result.site_coefficient_fa:.2f}
ค่าสัมประสิทธิ์ดิน Fv / Site Coefficient Fv: {result.site_coefficient_fv:.2f}
ค่าประกอบความสำคัญ / Importance Factor (I): {result.importance_factor:.2f}
ค่าปรับลดแรง / Response Modification Factor (R): {result.response_modification:.1f}

การวิเคราะห์โครงสร้าง / Structural Analysis:
{'='*80}
คาบธรรมชาติ / Fundamental Period (Ta): {result.fundamental_period:.3f} วินาที / seconds
ค่าสัมประสิทธิ์แผ่นดินไหว / Seismic Coefficient (Cs): {result.seismic_coefficient:.4f}
แรงเฉือนฐาน / Design Base Shear (V): {result.design_base_shear:.1f} kN

แรงด้านข้างแต่ละชั้น / Lateral Forces by Floor:
{'='*80}
{'ชั้น':<8} {'แรงแผ่นดินไหว':<15} {'การเคลื่อนตัว':<15} {'อัตราส่วนเอียง':<15}
{'Floor':<8} {'Force (kN)':<15} {'Displacement (mm)':<15} {'Drift Ratio':<15}
{'-'*60}"""
        
        for floor in sorted(result.story_forces.keys()):
            force = result.story_forces[floor]
            displacement = result.lateral_displacement.get(floor, 0)
            drift = result.drift_ratio.get(floor, 0)
            report += f"\n{floor:<8} {force:<15.1f} {displacement:<15.1f} {drift:<15.4f}"
        
        report += f"""

สรุปผลการวิเคราะห์ / Analysis Summary:
{'='*80}
วิธีการคำนวณ / Calculation Method: {result.calculation_method}
คำอธิบาย / Description: {result.description}

การตรวจสอบขีดจำกัดการเอียง / Drift Limit Check:
{'='*80}
"""
        
        # Check drift limits
        building_type = building_info.get('building_type', 'office')
        drift_limit = self.drift_limits.get(building_type, 0.02)
        
        max_drift = max(result.drift_ratio.values()) if result.drift_ratio else 0
        drift_check = "ผ่าน / PASS" if max_drift <= drift_limit else "ไม่ผ่าน / FAIL"
        
        report += f"ขีดจำกัดการเอียง / Drift Limit: {drift_limit:.1%}\n"
        report += f"การเอียงสูงสุด / Maximum Drift: {max_drift:.1%}\n"
        report += f"ผลการตรวจสอบ / Check Result: {drift_check}\n"
        
        report += f"""

หมายเหตุ / Notes:
{'='*80}
1. การคำนวณนี้เป็นไปตามมาตรฐาน มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1)
2. ใช้วิธี Equivalent Lateral Force Method
3. ควรตรวจสอบรายละเอียดเพิ่มเติมด้วยโปรแกรมวิเคราะห์โครงสร้าง
4. This calculation is based on TIS 1301/1302-61 (Revised Edition 1)
5. Equivalent Lateral Force Method is used
6. Detailed analysis with structural software is recommended

รายงานนี้สร้างโดย Thai Earthquake Load Library v1.0
Generated by Thai Earthquake Load Library v1.0
{'-'*80}
"""
        
        return report