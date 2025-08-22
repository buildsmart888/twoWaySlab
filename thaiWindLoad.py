#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Thai Wind Load Calculation Library
ไลบรารีการคำนวณแรงลมประเทศไทย

Based on:
- กฎกระทรวง กำหนดการออกแบบโครงสร้างอาคาร พ.ศ. 2566 หมวด 4
- มยผ. 1311-50 มาตรฐานการคำนวณแรงลมและการตอบสนองของอาคาร

@author: Enhanced by AI Assistant
@date: 2024
@version: 1.0
"""

import math
from typing import Dict, Tuple, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

class TerrainCategory(Enum):
    """ประเภทภูมิประเทศตาม มยผ. 1311-50 / Terrain categories according to TIS 1311-50"""
    CATEGORY_I = "I"      # ภูมิประเทศเปิด / Open terrain
    CATEGORY_II = "II"    # ภูมิประเทศขรุขระ / Rough terrain
    CATEGORY_III = "III"  # ภูมิประเทศเมือง / Urban terrain
    CATEGORY_IV = "IV"    # ภูมิประเทศเมืองหนาแน่น / Dense urban terrain

class WindZone(Enum):
    """โซนลมในประเทศไทยตาม มยผ. 1311-50 / Wind zones in Thailand according to TIS 1311-50"""
    ZONE_1 = "1"  # ภาคเหนือ / Northern regions
    ZONE_2 = "2"  # ภาคกลาง / Central regions
    ZONE_3 = "3"  # ภาคใต้ / Southern regions
    ZONE_4 = "4"  # พื้นที่ชายฝั่ง / Coastal areas

class BuildingType(Enum):
    """ประเภทความสำคัญของอาคาร / Building importance categories"""
    STANDARD = "standard"      # อาคารทั่วไป / Standard buildings
    IMPORTANT = "important"    # อาคารสำคัญ / Important buildings
    ESSENTIAL = "essential"    # อาคารจำเป็น / Essential facilities
    HAZARDOUS = "hazardous"    # อาคารอันตราย / Hazardous facilities

@dataclass
class WindLoadResult:
    """ผลลัพธ์การคำนวณแรงลม / Wind load calculation result"""
    design_wind_pressure: float  # แรงดันลมออกแบบ Pa / Design wind pressure (Pa)
    design_wind_speed: float     # ความเร็วลมออกแบบ m/s / Design wind speed (m/s)
    basic_wind_speed: float      # ความเร็วลมพื้นฐาน m/s / Basic wind speed (m/s)
    terrain_factor: float        # ค่าประกอบภูมิประเทศ / Terrain factor
    topographic_factor: float    # ค่าประกอบภูมิทัศน์ / Topographic factor
    importance_factor: float     # ค่าประกอบความสำคัญ / Importance factor
    pressure_coefficients: Dict[str, float]  # ค่าสัมประสิทธิ์แรงดัน / Pressure coefficients
    total_wind_force: float      # แรงลมรวม N / Total wind force (N)
    description: str             # คำอธิบาย / Description
    calculation_method: str      # วิธีการคำนวณ / Calculation method

@dataclass
class BuildingGeometry:
    """ข้อมูลรูปทรงอาคาร / Building geometry parameters"""
    height: float           # ความสูง m / Height (m)
    width: float           # ความกว้าง m / Width (m)
    depth: float           # ความลึก m / Depth (m)
    roof_angle: float      # มุมหลังคา องศา / Roof angle (degrees)
    building_type: str     # ประเภทอาคาร / Building type
    exposure_category: TerrainCategory  # ประเภทภูมิประเทศ / Terrain category

class ThaiWindLoad:
    """ไลบรารีการคำนวณแรงลมประเทศไทย / Thai Wind Load Calculation Library
    
    ตามมาตรฐาน:
    - กฎกระทรวง พ.ศ. 2566 หมวด 4
    - มยผ. 1311-50 มาตรฐานการคำนวณแรงลมและการตอบสนองของอาคาร
    
    Based on Standards:
    - Ministry Regulation B.E. 2566 Chapter 4
    - TIS 1311-50 Wind Load and Building Response Calculation Standard
    """
    
    def __init__(self):
        """เริ่มต้นเครื่องคำนวณแรงลมตามมาตรฐานไทย / Initialize wind load calculator with Thai standards"""
        
        # ความเร็วลมพื้นฐานแยกตามโซน (m/s) / Basic wind speeds by zone (m/s)
        self.basic_wind_speeds = {
            WindZone.ZONE_1: 30.0,  # ภาคเหนือ / Northern Thailand
            WindZone.ZONE_2: 25.0,  # ภาคกลาง / Central Thailand
            WindZone.ZONE_3: 35.0,  # ภาคใต้ / Southern Thailand
            WindZone.ZONE_4: 40.0   # พื้นที่ชายฝั่ง / Coastal areas
        }
        
        # พารามิเตอร์ภูมิประเทศตาม มยผ. 1311-50 / Terrain parameters according to TIS 1311-50
        self.terrain_parameters = {
            TerrainCategory.CATEGORY_I: {
                'name': 'ภูมิประเทศเปิด',
                'name_en': 'Open terrain',
                'description': 'แหล่งน้ำขนาดใหญ่ พื้นที่เปิดโล่ง',
                'z0': 0.03, 'zmin': 10, 'alpha': 0.12
            },
            TerrainCategory.CATEGORY_II: {
                'name': 'ภูมิประเทศขรุขระ',
                'name_en': 'Rough terrain',
                'description': 'ที่โล่งมีสิ่งกีดขวางกระจายอยู่',
                'z0': 0.3, 'zmin': 15, 'alpha': 0.16
            },
            TerrainCategory.CATEGORY_III: {
                'name': 'ภูมิประเทศเมือง',
                'name_en': 'Urban terrain',
                'description': 'ชานเมือง เมืองเล็ก',
                'z0': 1.0, 'zmin': 20, 'alpha': 0.22
            },
            TerrainCategory.CATEGORY_IV: {
                'name': 'ภูมิประเทศเมืองหนาแน่น',
                'name_en': 'Dense urban terrain',
                'description': 'เขตเมืองหนาแน่น ใจกลางเมือง',
                'z0': 2.5, 'zmin': 30, 'alpha': 0.30
            }
        }
        
        # ค่าประกอบความสำคัญตามกฎกระทรวง พ.ศ. 2566 / Importance factors according to Ministry Regulation B.E. 2566
        self.importance_factors = {
            BuildingType.STANDARD: {
                'factor': 1.0, 
                'description': 'อาคารทั่วไป',
                'description_en': 'Standard buildings',
                'examples': 'อาคารที่อยู่อาศัย อาคารสำนักงาน'
            },
            BuildingType.IMPORTANT: {
                'factor': 1.15, 
                'description': 'อาคารสำคัญ',
                'description_en': 'Important buildings', 
                'examples': 'โรงเรียน โรงพยาบาล อาคารชุมนุม'
            },
            BuildingType.ESSENTIAL: {
                'factor': 1.25, 
                'description': 'อาคารจำเป็น',
                'description_en': 'Essential facilities',
                'examples': 'สิ่งอำนวยความสะดวกฉุกเฉิน โรงไฟฟ้า'
            },
            BuildingType.HAZARDOUS: {
                'factor': 1.25, 
                'description': 'อาคารอันตราย',
                'description_en': 'Hazardous facilities',
                'examples': 'โรงงานเคมี คลังเก็บสารพิษ'
            }
        }
        
        # ค่าสัมประสิทธิ์แรงดันสำหรับรูปทรงอาคารต่างๆ / Pressure coefficients for different building shapes
        self.pressure_coefficients = {
            'rectangular_building': {
                'windward_wall': 0.8,     # ผนังรับลม / Windward wall
                'leeward_wall': -0.5,     # ผนังหลังลม / Leeward wall  
                'side_walls': -0.7,       # ผนังข้าง / Side walls
                'flat_roof': -0.7         # หลังคาเรียบ / Flat roof
            },
            'low_rise_building': {
                'windward_wall': 0.8,     # ผนังรับลม / Windward wall
                'leeward_wall': -0.5,     # ผนังหลังลม / Leeward wall
                'side_walls': -0.7,       # ผนังข้าง / Side walls
                'roof_windward': -0.7,    # หลังคาด้านรับลม / Windward roof
                'roof_leeward': -0.3      # หลังคาด้านหลังลม / Leeward roof
            }
        }
        
        # จังหวัดไทยและโซนลมที่สอดคล้อง / Thai provinces and their wind zones
        self.province_wind_zones = {
            # Northern Thailand (Zone 1)
            'เชียงใหม่': WindZone.ZONE_1, 'เชียงราย': WindZone.ZONE_1,
            'ลำปาง': WindZone.ZONE_1, 'ลำพูน': WindZone.ZONE_1,
            'แม่ฮ่องสอน': WindZone.ZONE_1, 'น่าน': WindZone.ZONE_1,
            
            # Central Thailand (Zone 2)
            'กรุงเทพมหานคร': WindZone.ZONE_2, 'นนทบุรี': WindZone.ZONE_2,
            'ปทุมธานี': WindZone.ZONE_2, 'สมุทรปราการ': WindZone.ZONE_2,
            'นครปฐม': WindZone.ZONE_2, 'ราชบุรี': WindZone.ZONE_2,
            
            # Northeastern Thailand (Zone 2)
            'นครราชสีมา': WindZone.ZONE_2, 'ขอนแก่น': WindZone.ZONE_2,
            'อุดรธานี': WindZone.ZONE_2, 'อุบลราชธานี': WindZone.ZONE_2,
            
            # Southern Thailand & Coastal (Zone 3 & 4)
            'ชลบุรี': WindZone.ZONE_4, 'ระยอง': WindZone.ZONE_4,
            'ภูเก็ต': WindZone.ZONE_4, 'สงขลา': WindZone.ZONE_4,
            'สุราษฎร์ธานี': WindZone.ZONE_3, 'นครศรีธรรมราช': WindZone.ZONE_3
        }

    def get_basic_wind_speed(self, location: Union[str, WindZone]) -> Tuple[float, str]:
        """ดึงความเร็วลมพื้นฐานสำหรับตำแหน่งที่ตั้ง / Get basic wind speed for location
        
        Args:
            location: ชื่อจังหวัด (ไทย) หรือ WindZone enum / Province name (Thai) or WindZone enum
            
        Returns:
            Tuple ของ (ความเร็วลม_m_s, คำอธิบายโซน) / Tuple of (wind_speed_m_s, zone_description)
        """
        if isinstance(location, str):
            if location in self.province_wind_zones:
                zone = self.province_wind_zones[location]
                wind_speed = self.basic_wind_speeds[zone]
                zone_desc = f"Zone {zone.value} - {location}"
            else:
                zone = WindZone.ZONE_2
                wind_speed = self.basic_wind_speeds[zone]
                zone_desc = f"Zone {zone.value} - Default"
        else:
            zone = location
            wind_speed = self.basic_wind_speeds[zone]
            zone_desc = f"Zone {zone.value}"
        
        return wind_speed, zone_desc

    def calculate_terrain_factor(self, height: float, terrain: TerrainCategory) -> float:
        """คำนวณค่าประกอบภูมิประเทศตาม มยผ. 1311-50 / Calculate terrain exposure factor according to TIS 1311-50
        
        Args:
            height: ความสูงอาคาร (m) / Building height (m)
            terrain: ประเภทภูมิประเทศ / Terrain category
            
        Returns:
            ค่าประกอบภูมิประเทศ / Terrain factor
        """
        params = self.terrain_parameters[terrain]
        h = max(height, params['zmin'])
        
        if terrain == TerrainCategory.CATEGORY_I:
            kr = (h / 10.0) ** params['alpha']
        else:
            z0 = params['z0']
            kr = 0.85 * (h / 10.0) ** (0.22 + 0.07 * math.log(z0))
        
        return min(kr, 2.0)

    def calculate_topographic_factor(self, topography_type: str = 'flat') -> float:
        """คำนวณค่าประกอบภูมิทัศน์ตาม มยผ. 1311-50 / Calculate topographic factor according to TIS 1311-50
        
        Args:
            topography_type: ประเภทภูมิทัศน์ / Topography type
                'flat': ที่ราบ / Flat terrain
                'hill': เนินเขา / Hill
                'ridge': สันเขา / Ridge
                'escarpment': หน้าผา / Escarpment
                'valley': หุบเขา / Valley
            
        Returns:
            ค่าประกอบภูมิทัศน์ / Topographic factor
        """
        factors = {
            'flat': 1.0, 'hill': 1.1, 'ridge': 1.15,
            'escarpment': 1.2, 'valley': 0.9
        }
        return factors.get(topography_type, 1.0)

    def calculate_design_wind_pressure(self, 
                                     basic_wind_speed: float,
                                     height: float,
                                     terrain: TerrainCategory,
                                     building_type: BuildingType,
                                     topography: str = 'flat') -> float:
        """คำนวณแรงดันลมออกแบบตามกฎกระทรวง พ.ศ. 2566 / Calculate design wind pressure according to Ministry Regulation B.E. 2566
        
        Args:
            basic_wind_speed: ความเร็วลมพื้นฐาน (m/s) / Basic wind speed (m/s)
            height: ความสูงอาคาร (m) / Building height (m) 
            terrain: ประเภทภูมิประเทศ / Terrain category
            building_type: ประเภทความสำคัญอาคาร / Building importance type
            topography: สภาพภูมิทัศน์ / Topographic condition
            
        Returns:
            แรงดันลมออกแบบ (Pa) / Design wind pressure (Pa)
        """
        kr = self.calculate_terrain_factor(height, terrain)
        kt = self.calculate_topographic_factor(topography)
        ki = self.importance_factors[building_type]['factor']
        
        # Design wind speed: Vz = Vb × Kr × Kt × Ki
        design_wind_speed = basic_wind_speed * kr * kt * ki
        
        # Design wind pressure: qz = 0.5 × ρ × Vz²
        air_density = 1.225  # kg/m³
        design_pressure = 0.5 * air_density * (design_wind_speed ** 2)
        
        return design_pressure

    def calculate_wind_force_on_surface(self,
                                      design_pressure: float,
                                      area: float,
                                      pressure_coefficient: float,
                                      internal_pressure_coeff: float = 0.0) -> float:
        """คำนวณแรงลมที่กระทำต่อพื้นผิว / Calculate wind force on a surface
        
        Args:
            design_pressure: แรงดันลมออกแบบ (Pa) / Design wind pressure (Pa)
            area: พื้นที่หน้าตัด (m²) / Surface area (m²)
            pressure_coefficient: ค่าสัมประสิทธิ์แรงดันภายนอก / External pressure coefficient
            internal_pressure_coeff: ค่าสัมประสิทธิ์แรงดันภายใน / Internal pressure coefficient
            
        Returns:
            แรงลม (N) / Wind force (N)
        """
        net_cp = pressure_coefficient - internal_pressure_coeff
        wind_force = design_pressure * net_cp * area
        return wind_force

    def calculate_complete_wind_analysis(self,
                                       location: Union[str, WindZone],
                                       building_geometry: BuildingGeometry,
                                       building_type: BuildingType,
                                       topography: str = 'flat',
                                       internal_pressure_coeff: float = 0.0) -> WindLoadResult:
        """การวิเคราะห์แรงลมครบถ้วนตามมาตรฐานไทย / Complete wind load analysis according to Thai standards
        
        Args:
            location: ตำแหน่งที่ตั้ง (จังหวัดหรือโซนลม) / Location (province or wind zone)
            building_geometry: ข้อมูลรูปทรงอาคาร / Building geometry parameters
            building_type: ประเภทความสำคัญอาคาร / Building importance type
            topography: สภาพภูมิทัศน์ / Topographic condition
            internal_pressure_coeff: ค่าสัมประสิทธิ์แรงดันภายใน / Internal pressure coefficient
            
        Returns:
            ผลลัพธ์การวิเคราะห์แรงลมครบถ้วน / Complete wind load analysis result
        """
        # ดึงความเร็วลมพื้นฐาน / Get basic wind speed
        basic_wind_speed, zone_desc = self.get_basic_wind_speed(location)
        
        # คำนวณแรงดันลมออกแบบ / Calculate design wind pressure
        design_pressure = self.calculate_design_wind_pressure(
            basic_wind_speed,
            building_geometry.height,
            building_geometry.exposure_category,
            building_type,
            topography
        )
        
        # คำนวณค่าประกอบต่างๆ / Calculate factors
        kr = self.calculate_terrain_factor(building_geometry.height, 
                                         building_geometry.exposure_category)
        kt = self.calculate_topographic_factor(topography)
        ki = self.importance_factors[building_type]['factor']
        
        # ความเร็วลมออกแบบ / Design wind speed
        design_wind_speed = basic_wind_speed * kr * kt * ki
        
        # ดึงค่าสัมประสิทธิ์แรงดัน / Get pressure coefficients
        building_shape = 'low_rise_building' if building_geometry.height <= 18 else 'rectangular_building'
        pressure_coeffs = self.pressure_coefficients[building_shape].copy()
        
        # คำนวณแรงลมรวม (ผนังรับลม) / Calculate total wind force (windward wall)
        windward_area = building_geometry.height * building_geometry.width
        cp_windward = pressure_coeffs.get('windward_wall', 0.8)
        
        total_force = self.calculate_wind_force_on_surface(
            design_pressure, windward_area, cp_windward, internal_pressure_coeff
        )
        
        return WindLoadResult(
            design_wind_pressure=design_pressure,
            design_wind_speed=design_wind_speed,
            basic_wind_speed=basic_wind_speed,
            terrain_factor=kr,
            topographic_factor=kt,
            importance_factor=ki,
            pressure_coefficients=pressure_coeffs,
            total_wind_force=total_force,
            description=f"Wind analysis for {zone_desc}, {building_type.value} building",
            calculation_method="Ministry Regulation B.E. 2566 + TIS 1311-50"
        )

    def generate_wind_load_report(self, result: WindLoadResult, building_info: Dict) -> str:
        """สร้างรายงานการคำนวณแรงลมอย่างครบถ้วน / Generate comprehensive wind load report
        
        Args:
            result: ผลลัพธ์การคำนวณแรงลม / Wind load calculation result
            building_info: ข้อมูลอาคารเพิ่มเติม / Additional building information
            
        Returns:
            รายงานในรูปแบบข้อความ / Formatted report string
        """
        report = []
        report.append("=" * 80)
        report.append("รายงานการคำนวณแรงลมประเทศไทย")
        report.append("Thai Wind Load Calculation Report")
        report.append("=" * 80)
        report.append("ตามกฎกระทรวง พ.ศ. 2566 และ มยผ. 1311-50")
        report.append("=" * 80)
        
        if 'project_name' in building_info:
            report.append(f"โครงการ: {building_info['project_name']}")
        
        report.append("\n1. พารามิเตอร์แรงลม (Wind Parameters)")
        report.append("-" * 50)
        report.append(f"ความเร็วลมพื้นฐาน: {result.basic_wind_speed:.1f} m/s")
        report.append(f"ความเร็วลมออกแบบ: {result.design_wind_speed:.1f} m/s")
        report.append(f"แรงดันลมออกแบบ: {result.design_wind_pressure:.1f} Pa")
        
        report.append("\n2. ค่าประกอบการคำนวณ (Factors)")
        report.append("-" * 50)
        report.append(f"ค่าประกอบภูมิประเทศ (Kr): {result.terrain_factor:.3f}")
        report.append(f"ค่าประกอบภูมิทัศน์ (Kt): {result.topographic_factor:.3f}")
        report.append(f"ค่าประกอบความสำคัญ (Ki): {result.importance_factor:.3f}")
        
        report.append("\n3. ค่าสัมประสิทธิ์แรงดัน (Pressure Coefficients)")
        report.append("-" * 50)
        surface_translations = {
            'windward_wall': 'ผนังรับลม (Windward Wall)',
            'leeward_wall': 'ผนังหลังลม (Leeward Wall)',
            'side_walls': 'ผนังข้าง (Side Walls)',
            'flat_roof': 'หลังคาเรียบ (Flat Roof)',
            'roof_windward': 'หลังคาด้านรับลม (Windward Roof)',
            'roof_leeward': 'หลังคาด้านหลังลม (Leeward Roof)'
        }
        for surface, cp in result.pressure_coefficients.items():
            surface_name = surface_translations.get(surface, surface)
            report.append(f"{surface_name}: Cp = {cp:+.2f}")
        
        report.append(f"\n4. แรงลมรวม: {result.total_wind_force:.0f} N ({result.total_wind_force/1000:.1f} kN)")
        report.append("=" * 80)
        
        return "\n".join(report)

    def get_wind_load_summary(self, location: str, building_height: float, 
                            building_type: BuildingType = BuildingType.STANDARD) -> Dict:
        """ดึงสรุปแรงลมอย่างรวดเร็วสำหรับตำแหน่งที่ตั้ง / Get quick wind load summary for a location
        
        Args:
            location: ตำแหน่งที่ตั้ง (จังหวัดไทย) / Location (Thai province)
            building_height: ความสูงอาคาร (m) / Building height (m)
            building_type: ประเภทความสำคัญอาคาร / Building importance type
            
        Returns:
            พจนานุกรมข้อมูลสรุปแรงลม / Dictionary with wind load summary
        """
        basic_speed, zone_desc = self.get_basic_wind_speed(location)
        terrain = TerrainCategory.CATEGORY_III  # Default urban
        
        design_pressure = self.calculate_design_wind_pressure(
            basic_speed, building_height, terrain, building_type
        )
        
        force_per_sqm = design_pressure * 0.8  # Cp = 0.8
        
        return {
            'location': location,
            'zone': zone_desc,
            'basic_wind_speed_ms': basic_speed,
            'basic_wind_speed_kmh': basic_speed * 3.6,
            'design_pressure_pa': design_pressure,
            'design_pressure_kpa': design_pressure / 1000,
            'force_per_sqm_n': force_per_sqm,
            'force_per_sqm_kgf': force_per_sqm / 9.80665
        }

# ฟังก์ชันทดสอบ / Test functions
if __name__ == "__main__":
    print("=== การทดสอบไลบรารีการคำนวณแรงลมไทย / Thai Wind Load Library Test ===")
    
    wind_calc = ThaiWindLoad()
    
    # Test 1: การทดสอบความเร็วลมพื้นฐาน / Basic wind speed lookup
    print("\n1. การทดสอบความเร็วลมพื้นฐาน / Basic Wind Speed Test")
    locations = ['กรุงเทพมหานคร', 'เชียงใหม่', 'ภูเก็ต', 'สงขลา']
    for location in locations:
        speed, desc = wind_calc.get_basic_wind_speed(location)
        print(f"{location}: {speed} m/s ({desc})")
    
    # Test 2: การวิเคราะห์แรงลมครบถ้วน / Complete analysis
    print("\n2. ตัวอย่างการวิเคราะห์แรงลมครบถ้วน / Complete Wind Analysis Example")
    building = BuildingGeometry(
        height=30.0, width=20.0, depth=15.0, roof_angle=0,
        building_type="อาคารสำนักงาน/office", exposure_category=TerrainCategory.CATEGORY_III
    )
    
    result = wind_calc.calculate_complete_wind_analysis(
        location='กรุงเทพมหานคร',
        building_geometry=building,
        building_type=BuildingType.STANDARD
    )
    
    print(f"แรงดันลมออกแบบ / Design Wind Pressure: {result.design_wind_pressure:.1f} Pa")
    print(f"แรงลมรวม / Total Wind Force: {result.total_wind_force:.0f} N")
    
    # Test 3: สรุปแรงลมอย่างรวดเร็ว / Quick summary
    print("\n3. สรุปแรงลม / Wind Load Summary")
    summary = wind_calc.get_wind_load_summary('กรุงเทพมหานคร', 25.0)
    print(f"ตำแหน่งที่ตั้ง / Location: {summary['location']}")
    print(f"แรงดันออกแบบ / Design Pressure: {summary['design_pressure_kpa']:.1f} kPa")
    print(f"แรงต่อตารางเมตร / Force per m²: {summary['force_per_sqm_kgf']:.1f} kgf/m²")
    
    print("\n✓ การทดสอบไลบรารีการคำนวณแรงลมไทยเสร็จสิ้นเรียบร้อย!")
    print("✓ Thai Wind Load Library test completed successfully!")