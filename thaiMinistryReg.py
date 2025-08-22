#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Thai Ministry Regulation for Building Structural Design
กฎกระทรวง กำหนดการออกแบบโครงสร้างอาคาร และลักษณะและคุณสมบัติของวัสดุที่ใช้ในงานโครงสร้างอาคาร พ.ศ. 2566

Based on:
- Ministry Regulation B.E. 2566 (2023)
- Thai Building Code Standards
- ASA (Association of Siamese Architects) Guidelines
- TIS (Thai Industrial Standards)

@author: Enhanced by AI Assistant
@date: 2024
"""

import math
from typing import Dict, Tuple, List, Optional, Union
from dataclasses import dataclass

@dataclass
class StructuralRequirement:
    """Data class for structural requirements"""
    parameter: str
    value: float
    unit: str
    description_th: str
    description_en: str
    reference: str

@dataclass
class MaterialProperty:
    """Data class for material properties"""
    material: str
    grade: str
    property_name: str
    value: float
    unit: str
    standard: str
    description_th: str

class ThaiMinistryRegulation2566:
    """
    Thai Ministry Regulation for Building Structural Design B.E. 2566 (2023)
    
    This class implements the requirements for:
    1. Structural design parameters
    2. Material properties and specifications  
    3. Safety factors and load combinations
    4. Quality control requirements
    5. Construction tolerances
    """
    
    def __init__(self):
        """Initialize the regulation system"""
        
        # Basic structural parameters per Ministry Regulation 2566
        self.structural_parameters = {
            'concrete_cover': {
                'normal_environment': {
                    'beam': (25, 'mm', 'คานธรรมดา'),
                    'column': (25, 'mm', 'เสาธรรมดา'),
                    'slab': (20, 'mm', 'พื้นธรรมดา'),
                    'foundation': (75, 'mm', 'ฐานรากธรรมดา')
                },
                'aggressive_environment': {
                    'beam': (40, 'mm', 'คานในสภาพแวดล้อมรุนแรง'),
                    'column': (40, 'mm', 'เสาในสภาพแวดล้อมรุนแรง'), 
                    'slab': (30, 'mm', 'พื้นในสภาพแวดล้อมรุนแรง'),
                    'foundation': (100, 'mm', 'ฐานรากในสภาพแวดล้อมรุนแรง')
                },
                'marine_environment': {
                    'beam': (50, 'mm', 'คานในสภาพแวดล้อมทางทะเล'),
                    'column': (50, 'mm', 'เสาในสภาพแวดล้อมทางทะเล'),
                    'slab': (40, 'mm', 'พื้นในสภาพแวดล้อมทางทะเล'),
                    'foundation': (125, 'mm', 'ฐานรากในสภาพแวดล้อมทางทะเล')
                }
            },
            
            # Safety factors per B.E. 2566
            'safety_factors': {
                'concrete': 1.5,        # γc for concrete
                'steel': 1.15,          # γs for steel  
                'dead_load': 1.4,       # Load factor for dead load
                'live_load': 1.6,       # Load factor for live load
                'wind_load': 1.6,       # Load factor for wind
                'seismic_load': 1.0     # Load factor for earthquake (special combination)
            },
            
            # Deflection limits per Ministry Regulation
            'deflection_limits': {
                'immediate': {
                    'cantilever': 250,      # L/250
                    'simply_supported': 300, # L/300
                    'continuous': 350       # L/350
                },
                'long_term': {
                    'cantilever': 125,      # L/125
                    'simply_supported': 200, # L/200
                    'continuous': 250       # L/250
                }
            }
        }
        
        # Material specifications per TIS standards referenced in B.E. 2566
        self.material_specifications = {
            'concrete': {
                # Standard concrete grades per มยผ. 1101
                'grades': {
                    'Fc180': {
                        'fc_ksc': 180, 'fc_mpa': 18.0,
                        'max_aggregate': 25, 'slump': (5, 12),
                        'w_c_ratio': 0.65, 'min_cement': 280,
                        'usage': 'งานทั่วไป', 'durability_class': 'XC1'
                    },
                    'Fc210': {
                        'fc_ksc': 210, 'fc_mpa': 21.0,
                        'max_aggregate': 25, 'slump': (5, 12),
                        'w_c_ratio': 0.60, 'min_cement': 300,
                        'usage': 'งานโครงสร้าง', 'durability_class': 'XC2'
                    },
                    'Fc240': {
                        'fc_ksc': 240, 'fc_mpa': 24.0,
                        'max_aggregate': 25, 'slump': (5, 12),
                        'w_c_ratio': 0.55, 'min_cement': 320,
                        'usage': 'งานโครงสร้าง', 'durability_class': 'XC3'
                    },
                    'Fc280': {
                        'fc_ksc': 280, 'fc_mpa': 28.0,
                        'max_aggregate': 20, 'slump': (5, 10),
                        'w_c_ratio': 0.50, 'min_cement': 350,
                        'usage': 'งานโครงสร้างแรงสูง', 'durability_class': 'XC4'
                    },
                    'Fc350': {
                        'fc_ksc': 350, 'fc_mpa': 35.0,
                        'max_aggregate': 20, 'slump': (8, 15),
                        'w_c_ratio': 0.45, 'min_cement': 380,
                        'usage': 'งานโครงสร้างพิเศษ', 'durability_class': 'XD1'
                    }
                },
                
                # Modulus calculation per Thai standards
                'modulus_formula': 'Ec = 4700 * sqrt(fc) * (γc/24)^1.5'
            },
            
            'steel': {
                # Steel grades per มยผ. 1103
                'reinforcement': {
                    'SD40': {
                        'fy_ksc': 4000, 'fy_mpa': 392.4,
                        'fu_ksc': 5600, 'fu_mpa': 549.4,
                        'elongation': 14.0, 'bend_test': '180°',
                        'carbon_max': 0.32, 'type': 'เหล็กข้ออ้อย'
                    },
                    'SD50': {
                        'fy_ksc': 5000, 'fy_mpa': 490.5,
                        'fu_ksc': 6300, 'fu_mpa': 618.0,
                        'elongation': 12.0, 'bend_test': '180°',
                        'carbon_max': 0.25, 'type': 'เหล็กข้ออ้อย'
                    },
                    'SR24': {
                        'fy_ksc': 2400, 'fy_mpa': 235.4,
                        'fu_ksc': 3800, 'fu_mpa': 372.8,
                        'elongation': 23.0, 'bend_test': '180°',
                        'carbon_max': 0.25, 'type': 'เหล็กเส้นกลม'
                    }
                }
            }
        }
        
        # Load combinations per B.E. 2566
        self.load_combinations = {
            'ultimate_limit_state': [
                {'name': 'ULS-1', 'formula': '1.4D + 1.6L', 'description': 'Dead + Live'},
                {'name': 'ULS-2', 'formula': '1.2D + 1.6L + 1.6W', 'description': 'Dead + Live + Wind'},
                {'name': 'ULS-3', 'formula': '1.2D + 1.0L + 1.0E', 'description': 'Dead + Live + Earthquake'},
                {'name': 'ULS-4', 'formula': '0.9D + 1.6W', 'description': 'Dead + Wind (minimum D)'},
                {'name': 'ULS-5', 'formula': '0.9D + 1.0E', 'description': 'Dead + Earthquake (minimum D)'}
            ],
            'serviceability_limit_state': [
                {'name': 'SLS-1', 'formula': '1.0D + 1.0L', 'description': 'Dead + Live (frequent)'},
                {'name': 'SLS-2', 'formula': '1.0D + 0.7L', 'description': 'Dead + Live (quasi-permanent)'},
                {'name': 'SLS-3', 'formula': '1.0D + 0.5L + 1.0W', 'description': 'Dead + Live + Wind'}
            ]
        }
        
        # Quality control requirements
        self.quality_control = {
            'concrete_testing': {
                'cylinder_strength': {
                    'frequency': '1 test per 100 m³ or per day',
                    'specimens': 3,
                    'age_days': [7, 28],
                    'acceptance_criteria': 'fc,avg ≥ fc + 1.64σ'
                },
                'slump_test': {
                    'frequency': 'Every truck or 100 m³',
                    'tolerance': '±25 mm from specified'
                }
            },
            'steel_testing': {
                'tensile_test': {
                    'frequency': '1 test per 40 tonnes',
                    'specimens': 2,
                    'requirements': ['yield strength', 'tensile strength', 'elongation']
                },
                'bend_test': {
                    'frequency': '1 test per 40 tonnes', 
                    'angle': '180°',
                    'mandrel_diameter': '4d for SD40, 5d for SD50'
                }
            }
        }

    def get_concrete_cover(self, element_type: str, environment: str = 'normal') -> Tuple[float, str, str]:
        """
        Get required concrete cover per Ministry Regulation B.E. 2566
        
        Args:
            element_type: 'beam', 'column', 'slab', 'foundation'
            environment: 'normal', 'aggressive', 'marine'
            
        Returns:
            Tuple of (cover_mm, unit, description_th)
        """
        env_key = f"{environment}_environment"
        if env_key in self.structural_parameters['concrete_cover']:
            if element_type in self.structural_parameters['concrete_cover'][env_key]:
                return self.structural_parameters['concrete_cover'][env_key][element_type]
        
        # Default to normal slab if not found
        return (20, 'mm', 'ค่าเริ่มต้น')

    def get_safety_factor(self, material_or_load: str) -> float:
        """
        Get safety factor per Ministry Regulation B.E. 2566
        
        Args:
            material_or_load: 'concrete', 'steel', 'dead_load', 'live_load', etc.
            
        Returns:
            Safety factor value
        """
        return self.structural_parameters['safety_factors'].get(material_or_load, 1.0)

    def get_deflection_limit(self, support_type: str, load_duration: str = 'immediate') -> int:
        """
        Get deflection limit per Ministry Regulation B.E. 2566
        
        Args:
            support_type: 'cantilever', 'simply_supported', 'continuous'
            load_duration: 'immediate', 'long_term'
            
        Returns:
            Deflection limit as L/x ratio
        """
        return self.structural_parameters['deflection_limits'][load_duration].get(support_type, 250)

    def calculate_design_strength(self, material: str, grade: str, 
                                nominal_strength: float, unit_system: str = 'mpa') -> Tuple[float, str]:
        """
        Calculate design strength including safety factors per B.E. 2566
        
        Args:
            material: 'concrete' or 'steel'
            grade: Material grade
            nominal_strength: Nominal strength value
            unit_system: 'mpa' or 'ksc'
            
        Returns:
            Tuple of (design_strength, description)
        """
        safety_factor = self.get_safety_factor(material)
        design_strength = nominal_strength / safety_factor
        
        description = f"Design strength = {nominal_strength}/{safety_factor} = {design_strength:.1f}"
        
        return design_strength, description

    def get_material_properties(self, material: str, grade: str) -> Dict:
        """
        Get comprehensive material properties per TIS standards
        
        Args:
            material: 'concrete' or 'steel'
            grade: Material grade
            
        Returns:
            Dictionary of material properties
        """
        if material == 'concrete' and grade in self.material_specifications['concrete']['grades']:
            return self.material_specifications['concrete']['grades'][grade]
        elif material == 'steel' and grade in self.material_specifications['steel']['reinforcement']:
            return self.material_specifications['steel']['reinforcement'][grade]
        else:
            return {}

    def check_load_combination(self, loads: Dict[str, float], combination_type: str = 'ultimate') -> List[Dict]:
        """
        Check load combinations per Ministry Regulation B.E. 2566
        
        Args:
            loads: Dictionary with 'D', 'L', 'W', 'E' values (kN or kN/m²)
            combination_type: 'ultimate' or 'serviceability'
            
        Returns:
            List of load combination results
        """
        results = []
        
        combinations_key = f"{combination_type}_limit_state"
        combinations = self.load_combinations.get(combinations_key, [])
        
        D = loads.get('D', 0)  # Dead load
        L = loads.get('L', 0)  # Live load  
        W = loads.get('W', 0)  # Wind load
        E = loads.get('E', 0)  # Earthquake load
        
        for combo in combinations:
            formula = combo['formula']
            
            # Parse and calculate combination
            try:
                # Replace variables in formula
                calc_formula = formula.replace('D', str(D)).replace('L', str(L)).replace('W', str(W)).replace('E', str(E))
                result_value = eval(calc_formula)
                
                results.append({
                    'name': combo['name'],
                    'formula': formula,
                    'calculation': calc_formula,
                    'result': result_value,
                    'description': combo['description']
                })
            except:
                results.append({
                    'name': combo['name'],
                    'formula': formula,
                    'calculation': 'Error in calculation',
                    'result': 0,
                    'description': combo['description']
                })
        
        return results

    def validate_concrete_mix(self, grade: str, w_c_ratio: float, 
                            cement_content: float, aggregate_size: float) -> Dict:
        """
        Validate concrete mix design per Ministry Regulation B.E. 2566
        
        Args:
            grade: Concrete grade (e.g., 'Fc210')
            w_c_ratio: Water-cement ratio
            cement_content: Cement content (kg/m³)
            aggregate_size: Maximum aggregate size (mm)
            
        Returns:
            Validation result dictionary
        """
        result = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'recommendations': []
        }
        
        if grade in self.material_specifications['concrete']['grades']:
            spec = self.material_specifications['concrete']['grades'][grade]
            
            # Check w/c ratio
            if w_c_ratio > spec['w_c_ratio']:
                result['errors'].append(f"W/C ratio {w_c_ratio:.2f} exceeds limit {spec['w_c_ratio']}")
                result['is_valid'] = False
            
            # Check minimum cement content
            if cement_content < spec['min_cement']:
                result['errors'].append(f"Cement content {cement_content} kg/m³ below minimum {spec['min_cement']} kg/m³")
                result['is_valid'] = False
            
            # Check aggregate size
            if aggregate_size > spec['max_aggregate']:
                result['warnings'].append(f"Aggregate size {aggregate_size}mm exceeds recommended {spec['max_aggregate']}mm")
            
            # Recommendations
            if cement_content > spec['min_cement'] + 100:
                result['recommendations'].append(f"Consider using admixtures to reduce cement content")
        
        else:
            result['errors'].append(f"Unknown concrete grade: {grade}")
            result['is_valid'] = False
        
        return result

    def get_construction_tolerances(self) -> Dict:
        """
        Get construction tolerances per Ministry Regulation B.E. 2566
        
        Returns:
            Dictionary of construction tolerances
        """
        return {
            'dimensional_tolerances': {
                'column_position': {'horizontal': '±12 mm', 'vertical': '±6 mm'},
                'beam_position': {'horizontal': '±10 mm', 'vertical': '±6 mm'},
                'slab_thickness': '±10 mm or ±5%',
                'concrete_cover': '+10mm/-5mm',
                'reinforcement_spacing': '±10 mm or ±5%'
            },
            'concrete_quality': {
                'surface_finish': 'หน้าผิวเรียบ ไม่มีรูพรุน',
                'color_uniformity': 'สีสม่ำเสมอ ไม่มีคราบสี',
                'crack_width': '≤ 0.3 mm สำหรับสภาพแวดล้อมปกติ'
            },
            'reinforcement_placement': {
                'bar_cutting_tolerance': '±25 mm',
                'bend_radius': 'ตาม มยผ. 1103',
                'lap_length': 'ตามการออกแบบ ± 50 mm',
                'hook_length': 'ตามมาตรฐาน'
            }
        }

    def generate_compliance_report(self, project_data: Dict) -> str:
        """
        Generate compliance report for Ministry Regulation B.E. 2566
        
        Args:
            project_data: Dictionary containing project information
            
        Returns:
            Formatted compliance report string
        """
        report = []
        report.append("=" * 80)
        report.append("รายงานการตรวจสอบตามกฎกระทรวง พ.ศ. 2566")
        report.append("Ministry Regulation B.E. 2566 Compliance Report")
        report.append("=" * 80)
        
        # Project information
        if 'project_name' in project_data:
            report.append(f"โครงการ/Project: {project_data['project_name']}")
        
        if 'date' in project_data:
            report.append(f"วันที่/Date: {project_data['date']}")
        
        report.append("")
        
        # Material compliance
        report.append("1. การตรวจสอบวัสดุ (Material Compliance)")
        report.append("-" * 50)
        
        if 'concrete_grade' in project_data:
            grade = project_data['concrete_grade']
            props = self.get_material_properties('concrete', grade)
            if props:
                report.append(f"เกรดคอนกรีต/Concrete Grade: {grade}")
                report.append(f"กำลังอัด/Compressive Strength: {props['fc_ksc']} ksc ({props['fc_mpa']} MPa)")
                report.append(f"การใช้งาน/Usage: {props['usage']}")
                report.append(f"W/C Ratio ≤ {props['w_c_ratio']}")
                report.append(f"ปูนซีเมนต์ขั้นต่ำ/Min Cement: {props['min_cement']} kg/m³")
        
        if 'steel_grade' in project_data:
            grade = project_data['steel_grade']  
            props = self.get_material_properties('steel', grade)
            if props:
                report.append(f"เกรดเหล็ก/Steel Grade: {grade}")
                report.append(f"จุดครากผล/Yield Strength: {props['fy_ksc']} ksc ({props['fy_mpa']} MPa)")
                report.append(f"ประเภท/Type: {props['type']}")
        
        report.append("")
        
        # Safety factors
        report.append("2. ค่าความปลอดภัย (Safety Factors)")
        report.append("-" * 50)
        report.append(f"คอนกรีต/Concrete (γc): {self.get_safety_factor('concrete')}")
        report.append(f"เหล็ก/Steel (γs): {self.get_safety_factor('steel')}")
        report.append(f"น้ำหนักตาย/Dead Load: {self.get_safety_factor('dead_load')}")
        report.append(f"น้ำหนักใช้สอย/Live Load: {self.get_safety_factor('live_load')}")
        
        report.append("")
        
        # Cover requirements
        report.append("3. ความหนาของคอนกรีตปิด (Concrete Cover)")
        report.append("-" * 50)
        
        environments = ['normal', 'aggressive', 'marine']
        elements = ['beam', 'column', 'slab', 'foundation']
        
        for env in environments:
            report.append(f"{env.title()} Environment:")
            for elem in elements:
                cover, unit, desc = self.get_concrete_cover(elem, env)
                report.append(f"  {elem.title()}: {cover} {unit} ({desc})")
        
        report.append("")
        report.append("=" * 80)
        report.append("หมายเหตุ: รายงานนี้จัดทำตามกฎกระทรวง พ.ศ. 2566")
        report.append("Note: This report is prepared according to Ministry Regulation B.E. 2566")
        report.append("=" * 80)
        
        return "\n".join(report)


# Test functions and examples
if __name__ == "__main__":
    print("=== Thai Ministry Regulation B.E. 2566 Implementation ===")
    
    # Initialize the regulation system
    reg = ThaiMinistryRegulation2566()
    
    # Test 1: Concrete cover requirements
    print("\n1. ความหนาคอนกรีตปิด (Concrete Cover Requirements)")
    print("-" * 60)
    
    elements = ['slab', 'beam', 'column']
    environments = ['normal', 'aggressive', 'marine']
    
    for env in environments:
        print(f"\n{env.title()} Environment:")
        for elem in elements:
            cover, unit, desc = reg.get_concrete_cover(elem, env)
            print(f"  {elem.title()}: {cover} {unit} - {desc}")
    
    # Test 2: Safety factors
    print(f"\n2. ค่าความปลอดภัย (Safety Factors)")
    print("-" * 60)
    factors = ['concrete', 'steel', 'dead_load', 'live_load', 'wind_load']
    for factor in factors:
        sf = reg.get_safety_factor(factor)
        print(f"{factor.replace('_', ' ').title()}: {sf}")
    
    # Test 3: Material properties
    print(f"\n3. คุณสมบัติวัสดุ (Material Properties)")
    print("-" * 60)
    
    # Concrete properties
    concrete_grades = ['Fc210', 'Fc240', 'Fc280']
    for grade in concrete_grades:
        props = reg.get_material_properties('concrete', grade)
        if props:
            print(f"\n{grade}: {props['fc_ksc']} ksc ({props['fc_mpa']} MPa)")
            print(f"  W/C Ratio: ≤ {props['w_c_ratio']}")
            print(f"  Min Cement: {props['min_cement']} kg/m³")
            print(f"  Usage: {props['usage']}")
    
    # Steel properties  
    steel_grades = ['SD40', 'SD50', 'SR24']
    for grade in steel_grades:
        props = reg.get_material_properties('steel', grade)
        if props:
            print(f"\n{grade}: {props['fy_ksc']} ksc ({props['fy_mpa']} MPa)")
            print(f"  Type: {props['type']}")
            print(f"  Elongation: {props['elongation']}%")
    
    # Test 4: Design strength calculation
    print(f"\n4. กำลังรับแรงออกแบบ (Design Strength)")
    print("-" * 60)
    
    # Concrete design strength
    fc_nominal = 21.0  # MPa
    fc_design, desc = reg.calculate_design_strength('concrete', 'Fc210', fc_nominal)
    print(f"Concrete: {desc}")
    
    # Steel design strength
    fy_nominal = 392.4  # MPa  
    fy_design, desc = reg.calculate_design_strength('steel', 'SD40', fy_nominal)
    print(f"Steel: {desc}")
    
    # Test 5: Load combinations
    print(f"\n5. การผสมน้ำหนัก (Load Combinations)")
    print("-" * 60)
    
    loads = {
        'D': 10.0,  # Dead load (kN/m²)
        'L': 5.0,   # Live load (kN/m²)  
        'W': 8.0,   # Wind load (kN/m²)
        'E': 6.0    # Earthquake load (kN/m²)
    }
    
    # Ultimate limit state combinations
    uls_results = reg.check_load_combination(loads, 'ultimate')
    print("\nUltimate Limit State:")
    for result in uls_results:
        print(f"  {result['name']}: {result['formula']} = {result['result']:.1f} kN/m²")
    
    # Serviceability limit state combinations
    sls_results = reg.check_load_combination(loads, 'serviceability')  
    print("\nServiceability Limit State:")
    for result in sls_results:
        print(f"  {result['name']}: {result['formula']} = {result['result']:.1f} kN/m²")
    
    # Test 6: Concrete mix validation
    print(f"\n6. การตรวจสอบส่วนผสมคอนกรีต (Concrete Mix Validation)")
    print("-" * 60)
    
    mix_validation = reg.validate_concrete_mix('Fc210', 0.55, 320, 25)
    print(f"Valid: {mix_validation['is_valid']}")
    if mix_validation['errors']:
        print(f"Errors: {mix_validation['errors']}")
    if mix_validation['warnings']:
        print(f"Warnings: {mix_validation['warnings']}")
    if mix_validation['recommendations']:
        print(f"Recommendations: {mix_validation['recommendations']}")
    
    # Test 7: Deflection limits
    print(f"\n7. ขีดจำกัดการโก่งตัว (Deflection Limits)")
    print("-" * 60)
    
    support_types = ['simply_supported', 'continuous', 'cantilever']
    for support in support_types:
        immediate = reg.get_deflection_limit(support, 'immediate')
        long_term = reg.get_deflection_limit(support, 'long_term')
        print(f"{support.replace('_', ' ').title()}: L/{immediate} (immediate), L/{long_term} (long-term)")
    
    # Test 8: Generate compliance report
    print(f"\n8. รายงานการตรวจสอบ (Compliance Report)")
    print("-" * 60)
    
    project_data = {
        'project_name': 'ตัวอย่างโครงการพื้น 2 ทิศทาง',
        'date': '2024-01-15',
        'concrete_grade': 'Fc210',
        'steel_grade': 'SD40'
    }
    
    report = reg.generate_compliance_report(project_data)
    print(report)