#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Thailand Building Code Implementation (TIS Standards)
Based on Thai Industrial Standards for Reinforced Concrete Design
- มยผ. 1103: มาตรฐานเหล็กเส้นเสริมคอนกรีต (Reinforcement Steel Standards)
- มยผ. 1101: มาตรฐานงานคอนกรีตและคอนกรีตเสริมเหล็ก (Concrete and RC Standards)
- กฎกระทรวง พ.ศ. 2566: กำหนดการออกแบบโครงสร้างอาคาร (Ministry Regulation B.E. 2566)

@author: Enhanced by AI Assistant
@date: 2024
"""

try:
    from thaiMinistryReg import ThaiMinistryRegulation2566
except ImportError:
    # Handle case where Ministry Regulation module is not available
    ThaiMinistryRegulation2566 = None

class ThaiRc_set():
    """
    Thailand Building Code Implementation
    Based on TIS (Thai Industrial Standards) for reinforced concrete design
    Supports both traditional Thai units (kgf, tonf, ksc) and SI units (N, kN, MPa)
    """
    
    def __init__(self):
        # Thai concrete strength grades - Available in both ksc and N/mm² (MPa)
        # Based on มยผ. 1101 ตารางที่ 3
        self.concrete_grades = {
            # Grade: (ksc, MPa, usage)
            'Fc180': (180, 18.0, 'คอนกรีตงานทั่วไป'),     # 180 ksc = 18 MPa
            'Fc210': (210, 21.0, 'คอนกรีตงานทั่วไป'),     # 210 ksc = 21 MPa
            'Fc240': (240, 24.0, 'คอนกรีตงานโครงสร้าง'),   # 240 ksc = 24 MPa
            'Fc280': (280, 28.0, 'คอนกรีตงานโครงสร้าง'),   # 280 ksc = 28 MPa
            'Fc350': (350, 35.0, 'คอนกรีตงานโครงสร้างแรงสูง'), # 350 ksc = 35 MPa
            'Fc420': (420, 42.0, 'คอนกรีตงานโครงสร้างแรงสูง'), # 420 ksc = 42 MPa
            'Fc500': (500, 50.0, 'คอนกรีตงานโครงสร้างแรงสูงพิเศษ') # 500 ksc = 50 MPa
        }
        
        # Thai steel grades - Available in both ksc and N/mm² (MPa)
        # Based on มยผ. 1103
        self.steel_grades = {
            # เหล็กข้ออ้อย (Deformed Bar) - ตาม มยผ. 1103 ข้อ 4.2
            'SD40': {
                'yield_ksc': 4000,    # 4000 ksc
                'yield_mpa': 392.4,   # 4000 × 0.0981 = 392.4 MPa
                'tensile_ksc': 5600,  # 5600 ksc
                'tensile_mpa': 549.4, # 5600 × 0.0981 = 549.4 MPa
                'type': 'เหล็กข้ออ้อย (Deformed Bar)'
            },
            'SD50': {
                'yield_ksc': 5000,    # 5000 ksc
                'yield_mpa': 490.5,   # 5000 × 0.0981 = 490.5 MPa
                'tensile_ksc': 6300,  # 6300 ksc
                'tensile_mpa': 618.0, # 6300 × 0.0981 = 618.0 MPa
                'type': 'เหล็กข้ออ้อย (Deformed Bar)'
            },
            # เหล็กเส้นกลม (Round Bar) - ตาม มยผ. 1103 ข้อ 4.1
            'SR24': {
                'yield_ksc': 2400,    # 2400 ksc (as you specified)
                'yield_mpa': 235.44,  # 2400 × 0.0981 = 235.44 MPa
                'tensile_ksc': 3800,  # 3800 ksc
                'tensile_mpa': 372.8, # 3800 × 0.0981 = 372.8 MPa
                'type': 'เหล็กเส้นกลม (Round Bar)'
            }
        }
        
        # Unit conversion factors
        self.unit_conversions = {
            # Force conversions
            'kgf_to_n': 9.80665,      # 1 kgf = 9.80665 N
            'tonf_to_kn': 9.80665,     # 1 tonf = 9.80665 kN
            'tonf_to_kgf': 1000.0,     # 1 tonf = 1000 kgf
            
            # Stress conversions
            'ksc_to_mpa': 0.0980665,   # 1 ksc = 0.0980665 MPa
            'ksc_to_kpa': 98.0665,     # 1 ksc = 98.0665 kPa
            'mpa_to_ksc': 10.1972,     # 1 MPa = 10.1972 ksc
            
            # Load conversions (weight per area)
            'kgf_m2_to_kn_m2': 0.00980665,  # 1 kgf/m² = 0.00980665 kN/m²
            'tonf_m2_to_kn_m2': 9.80665      # 1 tonf/m² = 9.80665 kN/m²
        }
        
        # Thai rebar areas (mm²) - Based on มยผ. 1103
        self.bar_areas = {
            # เหล็กข้ออ้อย (Deformed Bar) - ตาม มยผ. 1103 ข้อ 4.2
            'DB10': 78.54,     # เหล็กข้ออ้อย 10mm (π × 5²)
            'DB12': 113.10,    # เหล็กข้ออ้อย 12mm (π × 6²)
            'DB20': 314.16,    # เหล็กข้ออ้อย 20mm (π × 10²)
            'DB25': 490.87,    # เหล็กข้ออ้อย 25mm (π × 12.5²)
            'DB32': 804.25,    # เหล็กข้ออ้อย 32mm (π × 16²)
            'DB36': 1017.88,   # เหล็กข้ออ้อย 36mm (π × 18²)
            'DB40': 1256.64,   # เหล็กข้ออ้อย 40mm (π × 20²)
            
            # เหล็กเส้นกลม (Round Bar) - ตาม มยผ. 1103 ข้อ 4.1
            'RB6': 28.27,      # เหล็กเส้นกลม 6mm (π × 3²)
            'RB9': 63.62,      # เหล็กเส้นกลม 9mm (π × 4.5²)
            
            # Combined arrangements (เหล็กข้ออ้อยผสม)
            'DB10+DB12': 191.64,  # DB10 + DB12
            'DB12+DB20': 427.26,  # DB12 + DB20
            'DB20+DB25': 805.03,  # DB20 + DB25
            'DB25+DB32': 1295.12  # DB25 + DB32
        }

    # === UNIT CONVERSION METHODS ===
    
    def ksc_to_mpa(self, ksc):
        """Convert ksc (kgf/cm²) to MPa"""
        return ksc * self.unit_conversions['ksc_to_mpa']
    
    def mpa_to_ksc(self, mpa):
        """Convert MPa to ksc (kgf/cm²)"""
        return mpa * self.unit_conversions['mpa_to_ksc']
    
    def kgf_to_n(self, kgf):
        """Convert kgf to N"""
        return kgf * self.unit_conversions['kgf_to_n']
    
    def tonf_to_kn(self, tonf):
        """Convert tonf to kN"""
        return tonf * self.unit_conversions['tonf_to_kn']
    
    def load_kgf_m2_to_kn_m2(self, load_kgf_m2):
        """Convert load from kgf/m² to kN/m²"""
        return load_kgf_m2 * self.unit_conversions['kgf_m2_to_kn_m2']
    
    def load_tonf_m2_to_kn_m2(self, load_tonf_m2):
        """Convert load from tonf/m² to kN/m²"""
        return load_tonf_m2 * self.unit_conversions['tonf_m2_to_kn_m2']
    
    # === UPDATED CALCULATION METHODS ===
    
    def Ec(self, fc, gamma=2400.0, input_units='ksc'):
        """
        Young's Modulus for concrete (Thai standards)
        Based on TIS 2525 (Thai concrete code)
        
        Formula: Ec = 4700 × √fc × (γ/2400)^1.5
        
        Args:
            fc: Compressive strength
            gamma: Concrete density (default 2400 kgf/m³ = 24.0 kN/m³)
            input_units: 'ksc' for Thai units or 'mpa' for SI units
            
        Returns:
            Ec: Young's modulus (same units as fc input)
        """
        if input_units == 'ksc':
            # Convert to SI for calculation
            fc_mpa = self.ksc_to_mpa(fc)
            gamma_kn_m3 = gamma / 100.0  # Convert kgf/m³ to kN/m³
        else:
            fc_mpa = fc
            gamma_kn_m3 = gamma
        
        # Weight factor for different concrete densities (standard = 24.0 kN/m³)
        weight_factor = (gamma_kn_m3 / 24.0) ** 1.5
        
        # Thai formula for modulus of elasticity
        ec_mpa = 4700 * (fc_mpa ** 0.5) * weight_factor
        
        if input_units == 'ksc':
            # Convert back to ksc for output
            return self.mpa_to_ksc(ec_mpa)
        else:
            return ec_mpa

    def get_steel_strength(self, grade, output_units='mpa'):
        """
        Get steel yield strength from grade
        
        Args:
            grade: Steel grade (SD40, SD50, SR24)
            output_units: 'ksc' for Thai units or 'mpa' for SI units
            
        Returns:
            Yield strength in requested units
        """
        if grade in self.steel_grades:
            steel_data = self.steel_grades[grade]
            if output_units == 'ksc':
                return steel_data['yield_ksc']
            else:
                return steel_data['yield_mpa']
        else:
            # Default to SD40
            if output_units == 'ksc':
                return 4000.0
            else:
                return 392.4

    def get_concrete_strength(self, grade, output_units='mpa'):
        """
        Get concrete compressive strength from grade
        
        Args:
            grade: Concrete grade (Fc180, Fc210, etc.)
            output_units: 'ksc' for Thai units or 'mpa' for SI units
            
        Returns:
            Compressive strength in requested units
        """
        if grade in self.concrete_grades:
            ksc_val, mpa_val, usage = self.concrete_grades[grade]
            if output_units == 'ksc':
                return ksc_val
            else:
                return mpa_val
        else:
            # Default to Fc210
            if output_units == 'ksc':
                return 210.0
            else:
                return 21.0

    def get_permissible_stress(self, steel_grade, safety_factor=1.15):
        """
        Get permissible stress for steel based on Thai standards
        
        Args:
            steel_grade: Steel grade (SD30, SD40, SD50, etc.)
            safety_factor: Safety factor for steel, default 1.15
            
        Returns:
            Permissible stress (N/mm²)
        """
        if steel_grade in self.steel_grades:
            yield_strength = self.steel_grades[steel_grade]
            return yield_strength / safety_factor
        else:
            # Default to SD40 if grade not found
            return self.steel_grades['SD40'] / safety_factor

    def Ra(self, bar_designation):
        """
        Rebar Area in mm²
        
        Args:
            bar_designation: Thai bar designation (DB6, DB9, DB12, etc.)
            
        Returns:
            Cross-sectional area in mm²
        """
        if bar_designation in self.bar_areas:
            return self.bar_areas[bar_designation]
        else:
            print(f"Warning: Bar designation '{bar_designation}' not found. Using DB12 default.")
            return self.bar_areas['DB12']  # Default to DB12

    def Ra_p(self, bar_designation, pitch):
        """
        Rebar Area per unit width (mm²/m)
        
        Args:
            bar_designation: Thai bar designation
            pitch: Bar spacing/pitch in mm
            
        Returns:
            Rebar area per meter width (mm²/m)
        """
        return self.Ra(bar_designation) * 1000.0 / pitch

    def get_concrete_strength(self, grade, output_units='mpa'):
        """
        Get concrete compressive strength from grade
        
        Args:
            grade: Concrete grade (Fc180, Fc210, etc.)
            output_units: 'ksc' for Thai units or 'mpa' for SI units
            
        Returns:
            Compressive strength in requested units
        """
        if grade in self.concrete_grades:
            ksc_val, mpa_val, usage = self.concrete_grades[grade]
            if output_units == 'ksc':
                return ksc_val
            else:
                return mpa_val
        else:
            # Default to Fc210
            if output_units == 'ksc':
                return 210.0
            else:
                return 21.0

    def get_steel_strength(self, grade, output_units='mpa'):
        """
        Get steel yield strength from grade based on มยผ. 1103
        
        Args:
            grade: Steel grade (SD40, SD50, SR24)
            output_units: 'ksc' for Thai units or 'mpa' for SI units
            
        Returns:
            Yield strength in requested units
        """
        if grade in self.steel_grades:
            steel_data = self.steel_grades[grade]
            if output_units == 'ksc':
                return steel_data['yield_ksc']
            else:
                return steel_data['yield_mpa']
        else:
            # Default to SD40
            if output_units == 'ksc':
                return 4000.0
            else:
                return 392.4

    def get_steel_grade_info(self, grade):
        """
        Get detailed information about Thai steel grades with both unit systems
        
        Args:
            grade: Steel grade
            
        Returns:
            Dictionary with detailed steel information in both ksc and MPa
        """
        steel_info = {
            'SD40': {
                'type': 'เหล็กข้ออ้อย (Deformed Bar)',
                'standard': 'มยผ. 1103 ข้อ 4.2',
                'yield_ksc': 4000,      # Traditional Thai units
                'yield_mpa': 392.4,     # SI units
                'tensile_ksc': 5600,    # Traditional Thai units
                'tensile_mpa': 549.4,   # SI units
                'elongation': 14.0,
                'usage': 'เหล็กเสริมโครงสร้างทั่วไป'
            },
            'SD50': {
                'type': 'เหล็กข้ออ้อย (Deformed Bar)',
                'standard': 'มยผ. 1103 ข้อ 4.2',
                'yield_ksc': 5000,      # Traditional Thai units
                'yield_mpa': 490.5,     # SI units
                'tensile_ksc': 6300,    # Traditional Thai units
                'tensile_mpa': 618.0,   # SI units
                'elongation': 12.0,
                'usage': 'เหล็กเสริมโครงสร้างแรงสูง'
            },
            'SR24': {
                'type': 'เหล็กเส้นกลม (Round Bar)',
                'standard': 'มยผ. 1103 ข้อ 4.1',
                'yield_ksc': 2400,      # Traditional Thai units (as you specified)
                'yield_mpa': 235.44,    # SI units (2400 × 0.0981)
                'tensile_ksc': 3800,    # Traditional Thai units
                'tensile_mpa': 372.8,   # SI units
                'elongation': 23.0,
                'usage': 'เหล็กเสริมทั่วไป, เหล็กปลอก'
            }
        }
        
        return steel_info.get(grade, {
            'type': 'Unknown',
            'standard': 'มยผ. 1103',
            'yield_ksc': 4000,
            'yield_mpa': 392.4,
            'tensile_ksc': 5600,
            'tensile_mpa': 549.4,
            'elongation': 14.0,
            'usage': 'ไม่ระบุ'
        })

    def get_concrete_grade_info(self, grade):
        """
        Get detailed information about Thai concrete grades with both unit systems
        
        Args:
            grade: Concrete grade (Fc180, Fc210, etc.)
            
        Returns:
            Dictionary with detailed concrete information in both ksc and MPa
        """
        concrete_info = {
            'Fc180': {
                'strength_ksc': 180,    # Traditional Thai units
                'strength_mpa': 18.0,   # SI units
                'standard': 'มยผ. 1101 ตารางที่ 3',
                'usage': 'คอนกรีตงานทั่วไป',
                'min_cement': 280,  # kg/m³
                'max_wc_ratio': 0.65
            },
            'Fc210': {
                'strength_ksc': 210,    # Traditional Thai units
                'strength_mpa': 21.0,   # SI units
                'standard': 'มยผ. 1101 ตารางที่ 3',
                'usage': 'คอนกรีตงานทั่วไป',
                'min_cement': 300,  # kg/m³
                'max_wc_ratio': 0.60
            },
            'Fc240': {
                'strength_ksc': 240,    # Traditional Thai units
                'strength_mpa': 24.0,   # SI units
                'standard': 'มยผ. 1101 ตารางที่ 3',
                'usage': 'คอนกรีตงานโครงสร้าง',
                'min_cement': 320,  # kg/m³
                'max_wc_ratio': 0.55
            },
            'Fc280': {
                'strength_ksc': 280,    # Traditional Thai units
                'strength_mpa': 28.0,   # SI units
                'standard': 'มยผ. 1101 ตารางที่ 3',
                'usage': 'คอนกรีตงานโครงสร้าง',
                'min_cement': 350,  # kg/m³
                'max_wc_ratio': 0.50
            },
            'Fc350': {
                'strength_ksc': 350,    # Traditional Thai units
                'strength_mpa': 35.0,   # SI units
                'standard': 'มยผ. 1101 ตารางที่ 3',
                'usage': 'คอนกรีตงานโครงสร้างแรงสูง',
                'min_cement': 380,  # kg/m³
                'max_wc_ratio': 0.45
            },
            'Fc420': {
                'strength_ksc': 420,    # Traditional Thai units
                'strength_mpa': 42.0,   # SI units
                'standard': 'มยผ. 1101 ตารางที่ 3',
                'usage': 'คอนกรีตงานโครงสร้างแรงสูง',
                'min_cement': 420,  # kg/m³
                'max_wc_ratio': 0.40
            },
            'Fc500': {
                'strength_ksc': 500,    # Traditional Thai units
                'strength_mpa': 50.0,   # SI units
                'standard': 'มยผ. 1101 ตารางที่ 3',
                'usage': 'คอนกรีตงานโครงสร้างแรงสูงพิเศษ',
                'min_cement': 450,  # kg/m³
                'max_wc_ratio': 0.35
            }
        }
        
        return concrete_info.get(grade, {
            'strength_ksc': 210,
            'strength_mpa': 21.0,
            'standard': 'มยผ. 1101 ตารางที่ 3',
            'usage': 'คอนกรีตงานทั่วไป',
            'min_cement': 300,
            'max_wc_ratio': 0.60
        })

    def get_available_rebar_sizes(self, bar_type='all'):
        """
        Get available rebar sizes based on type
        
        Args:
            bar_type: 'deformed', 'round', or 'all'
            
        Returns:
            List of available bar designations
        """
        deformed_bars = ['DB10', 'DB12', 'DB20', 'DB25', 'DB32', 'DB36', 'DB40']
        round_bars = ['RB6', 'RB9']
        
        if bar_type == 'deformed':
            return deformed_bars
        elif bar_type == 'round':
            return round_bars
        else:
            return deformed_bars + round_bars

    def validate_thai_standards(self, concrete_grade, steel_grade, bar_designation):
        """
        Validate if the combination follows Thai standards
        
        Args:
            concrete_grade: Concrete grade (Fc18, Fc21, etc.)
            steel_grade: Steel grade (SD40, SD50, SR24)
            bar_designation: Bar designation (DB10, DB12, etc.)
            
        Returns:
            Tuple (is_valid, warnings, recommendations)
        """
        warnings = []
        recommendations = []
        is_valid = True
        
        # Check if concrete grade is valid
        if concrete_grade not in self.concrete_grades:
            warnings.append(f"Concrete grade {concrete_grade} not in Thai standards")
            is_valid = False
        
        # Check if steel grade is valid
        if steel_grade not in self.steel_grades:
            warnings.append(f"Steel grade {steel_grade} not in Thai standards")
            is_valid = False
        
        # Check if bar designation is valid
        if bar_designation not in self.bar_areas:
            warnings.append(f"Bar designation {bar_designation} not in Thai standards")
            is_valid = False
        
        # Check compatibility between steel grade and bar type
        if bar_designation.startswith('DB') and steel_grade not in ['SD40', 'SD50']:
            warnings.append(f"Deformed bars (DB) should use SD40 or SD50 steel grade")
        
        if bar_designation.startswith('RB') and steel_grade not in ['SR24']:
            warnings.append(f"Round bars (RB) should use SR24 steel grade")
        
        # Recommendations for common usage
        if concrete_grade in ['Fc18', 'Fc21'] and steel_grade == 'SD50':
            recommendations.append("Consider using SD40 for normal strength concrete to optimize cost")
        
        if concrete_grade in ['Fc35', 'Fc42', 'Fc50'] and steel_grade == 'SR24':
            recommendations.append("Consider using SD40 or SD50 for high strength concrete")
        
        return is_valid, warnings, recommendations

    def get_concrete_density(self, concrete_type='normal'):
        """
        Get concrete density based on type
        
        Args:
            concrete_type: 'normal', 'lightweight', 'heavyweight'
            
        Returns:
            Density (kN/m³)
        """
        densities = {
            'normal': 24.0,
            'lightweight': 18.0,
            'heavyweight': 28.0
        }
        return densities.get(concrete_type, 24.0)

    def get_cover_requirement(self, environment='normal', bar_size=16):
        """
        Get concrete cover requirements based on Thai standards
        
        Args:
            environment: 'normal', 'aggressive', 'marine'
            bar_size: Bar diameter in mm
            
        Returns:
            Required cover (mm)
        """
        base_cover = {
            'normal': 20,
            'aggressive': 30,
            'marine': 40
        }
        
        # Minimum cover should not be less than bar diameter
        required_cover = max(base_cover.get(environment, 20), bar_size)
        
        return required_cover

    def get_ministry_regulation_2566(self):
        """
        Get Thai Ministry Regulation B.E. 2566 instance for additional structural requirements
        
        Returns:
            ThaiMinistryRegulation2566 instance or None if not available
        """
        if ThaiMinistryRegulation2566 is not None:
            return ThaiMinistryRegulation2566()
        else:
            print("Warning: Thai Ministry Regulation B.E. 2566 module not available")
            return None
    
    def validate_with_ministry_regulation(self, project_data: dict):
        """
        Validate design against Thai Ministry Regulation B.E. 2566
        
        Args:
            project_data: Dictionary containing project parameters
            
        Returns:
            Dictionary with validation results and compliance report
        """
        ministry_reg = self.get_ministry_regulation_2566()
        if ministry_reg is None:
            return {
                'available': False,
                'message': 'Ministry Regulation B.E. 2566 module not available'
            }
        
        result = {
            'available': True,
            'concrete_cover': {},
            'safety_factors': {},
            'load_combinations': {},
            'material_compliance': {},
            'compliance_report': ''
        }
        
        # Check concrete cover requirements
        if 'element_type' in project_data and 'environment' in project_data:
            cover, unit, desc = ministry_reg.get_concrete_cover(
                project_data['element_type'], 
                project_data.get('environment', 'normal')
            )
            result['concrete_cover'] = {
                'required_cover': cover,
                'unit': unit,
                'description': desc
            }
        
        # Get safety factors
        for factor_type in ['concrete', 'steel', 'dead_load', 'live_load']:
            result['safety_factors'][factor_type] = ministry_reg.get_safety_factor(factor_type)
        
        # Check load combinations if loads are provided
        if 'loads' in project_data:
            loads = project_data['loads']
            result['load_combinations']['ultimate'] = ministry_reg.check_load_combination(loads, 'ultimate')
            result['load_combinations']['serviceability'] = ministry_reg.check_load_combination(loads, 'serviceability')
        
        # Material compliance
        if 'concrete_grade' in project_data:
            grade = project_data['concrete_grade']
            result['material_compliance']['concrete'] = ministry_reg.get_material_properties('concrete', grade)
        
        if 'steel_grade' in project_data:
            grade = project_data['steel_grade']
            result['material_compliance']['steel'] = ministry_reg.get_material_properties('steel', grade)
        
        # Generate compliance report
        result['compliance_report'] = ministry_reg.generate_compliance_report(project_data)
        
        return result


class Aij_rc_set(ThaiRc_set):
    """
    Compatibility wrapper to maintain existing interface
    Maps Japanese designations to Thai equivalents where possible
    """
    
    def __init__(self):
        super().__init__()
        
        # Mapping from Japanese (D-series) to Thai (DB/RB-series) bars
        # Based on actual Thai standards มยผ. 1103
        self.compat_mapping = {
            # Japanese to Thai Deformed Bars
            'D10': 'DB10',   # Direct equivalent
            'D13': 'DB12',   # Map Japanese D13 to Thai DB12 (closest available)
            'D16': 'DB20',   # Map Japanese D16 to Thai DB20 (closest available) 
            'D19': 'DB20',   # Map Japanese D19 to Thai DB20
            'D22': 'DB25',   # Map Japanese D22 to Thai DB25 (closest available)
            'D25': 'DB25',   # Direct equivalent
            'D29': 'DB32',   # Map Japanese D29 to Thai DB32 (closest available)
            'D32': 'DB32',   # Direct equivalent
            'D35': 'DB36',   # Map Japanese D35 to Thai DB36 (closest available)
            'D38': 'DB40',   # Map Japanese D38 to Thai DB40 (closest available)
            'D41': 'DB40',   # Map Japanese D41 to Thai DB40 (closest available)
            
            # Combined bars - use Thai combinations
            'D10+D13': 'DB10+DB12',
            'D13+D16': 'DB12+DB20',
            'D16+D19': 'DB20+DB25'
        }

    def Ra(self, index):
        """
        Maintain compatibility with Japanese interface
        Maps Japanese bar designations to Thai equivalents
        
        Args:
            index: Japanese bar designation (D10, D13, etc.) or Thai designation (DB9, DB12, etc.)
            
        Returns:
            Cross-sectional area in mm²
        """
        # If it's already a Thai designation, use it directly
        if index in self.bar_areas:
            return self.bar_areas[index]
        
        # Try to map from Japanese to Thai designation
        thai_equiv = self.compat_mapping.get(index)
        if thai_equiv and thai_equiv in self.bar_areas:
            return self.bar_areas[thai_equiv]
        
        # If no mapping found, show warning and use default
        print(f"Warning: Bar designation '{index}' not found in Thai standards. Using DB12 default.")
        return self.bar_areas['DB12']

    def Ec(self, fc, gamma=24.0):
        """
        Young's Modulus calculation using Thai standards
        Overrides Japanese formula with Thai formula
        """
        return super().Ec(fc, gamma)


# Test functions
if __name__ == "__main__":
    # Test Thai RC implementation with traditional Thai units
    thai_rc = ThaiRc_set()
    
    print("=== Thai Building Code with Traditional Units (มยผ. 1103 & มยผ. 1101) ===")
    print(f"Available deformed bars: {thai_rc.get_available_rebar_sizes('deformed')}")
    print(f"Available round bars: {thai_rc.get_available_rebar_sizes('round')}")
    
    # Test unit conversions
    print("\n--- Unit Conversions (การแปลงหน่วย) ---")
    print(f"1000 ksc = {thai_rc.ksc_to_mpa(1000):.2f} MPa")
    print(f"100 MPa = {thai_rc.mpa_to_ksc(100):.0f} ksc")
    print(f"1000 kgf = {thai_rc.kgf_to_n(1000):.1f} N")
    print(f"10 tonf = {thai_rc.tonf_to_kn(10):.1f} kN")
    print(f"1000 kgf/m² = {thai_rc.load_kgf_m2_to_kn_m2(1000):.2f} kN/m²")
    print(f"5 tonf/m² = {thai_rc.load_tonf_m2_to_kn_m2(5):.1f} kN/m²")
    
    # Test steel grades in both unit systems
    print("\n--- Steel Grades in Both Units (ชั้นคุณภาพเหล็ก) ---")
    for grade in ['SD40', 'SD50', 'SR24']:
        strength_ksc = thai_rc.get_steel_strength(grade, 'ksc')
        strength_mpa = thai_rc.get_steel_strength(grade, 'mpa')
        info = thai_rc.get_steel_grade_info(grade)
        print(f"{grade}: {strength_ksc:.0f} ksc = {strength_mpa:.1f} MPa - {info['type']}")
        print(f"      Tensile: {info['yield_ksc']:.0f}/{info['tensile_ksc']:.0f} ksc, {info['yield_mpa']:.1f}/{info['tensile_mpa']:.1f} MPa")
    
    # Test concrete grades in both unit systems
    print("\n--- Concrete Grades in Both Units (เกรดคอนกรีต) ---")
    for grade in ['Fc180', 'Fc210', 'Fc240', 'Fc280', 'Fc350']:
        strength_ksc = thai_rc.get_concrete_strength(grade, 'ksc')
        strength_mpa = thai_rc.get_concrete_strength(grade, 'mpa')
        info = thai_rc.get_concrete_grade_info(grade)
        print(f"{grade}: {strength_ksc:.0f} ksc = {strength_mpa:.1f} MPa - {info['usage']}")
    
    # Test concrete modulus in both unit systems
    print("\n--- Concrete Modulus Calculation (การคำนวณ Ec) ---")
    
    # Using traditional Thai units
    fc_ksc = 210  # 210 ksc (Fc210)
    gamma_kgf_m3 = 2400  # 2400 kgf/m³ (standard concrete density)
    ec_ksc = thai_rc.Ec(fc_ksc, gamma_kgf_m3, 'ksc')
    print(f"Thai units: fc = {fc_ksc} ksc, γ = {gamma_kgf_m3} kgf/m³ ⇒ Ec = {ec_ksc:.0f} ksc")
    
    # Using SI units
    fc_mpa = 21.0  # 21 MPa
    gamma_kn_m3 = 24.0  # 24 kN/m³
    ec_mpa = thai_rc.Ec(fc_mpa, gamma_kn_m3, 'mpa')
    print(f"SI units: fc = {fc_mpa} MPa, γ = {gamma_kn_m3} kN/m³ ⇒ Ec = {ec_mpa:.0f} MPa")
    
    # Verify conversion consistency
    ec_ksc_converted = thai_rc.mpa_to_ksc(ec_mpa)
    print(f"Consistency check: {ec_mpa:.0f} MPa = {ec_ksc_converted:.0f} ksc (vs calculated {ec_ksc:.0f} ksc)")
    
    # Test deformed bars with realistic Thai loadings
    print("\n--- Practical Example: DB20 Reinforcement ---")
    db20_area = thai_rc.Ra('DB20')
    db20_per_m_200 = thai_rc.Ra_p('DB20', 200)
    sd40_ksc = thai_rc.get_steel_strength('SD40', 'ksc')
    
    print(f"DB20 area: {db20_area:.2f} mm²")
    print(f"DB20 @ 200mm: {db20_per_m_200:.0f} mm²/m")
    print(f"SD40 strength: {sd40_ksc:.0f} ksc")
    print(f"Allowable force per DB20 bar: {db20_area * sd40_ksc / 1000:.1f} tonf")
    
    # Test round bars
    print("\n--- Round Bars Example: RB9 for Stirrups ---")
    rb9_area = thai_rc.Ra('RB9')
    sr24_ksc = thai_rc.get_steel_strength('SR24', 'ksc')
    
    print(f"RB9 area: {rb9_area:.2f} mm²")
    print(f"SR24 strength: {sr24_ksc:.0f} ksc (target: 2400 ksc) ✓")
    print(f"Allowable force per RB9 bar: {rb9_area * sr24_ksc / 1000:.2f} tonf")
    
    # Test compatibility wrapper
    compat_rc = Aij_rc_set()
    
    print("\n=== Compatibility Test (Japanese → Thai with Units) ===")
    japanese_bars = ['D10', 'D13', 'D16', 'D19', 'D22']
    for jbar in japanese_bars:
        thai_area = compat_rc.Ra(jbar)
        mapping = compat_rc.compat_mapping.get(jbar, 'Not mapped')
        # Calculate capacity in traditional Thai units
        if mapping.startswith('DB'):
            steel_grade = 'SD40'
            capacity_tonf = thai_area * thai_rc.get_steel_strength(steel_grade, 'ksc') / 1000
        else:
            capacity_tonf = thai_area * 2400 / 1000  # Assume SR24 for round bars
        print(f"{jbar} → {mapping}: {thai_area:.2f} mm², capacity ≈ {capacity_tonf:.2f} tonf")
    
    # Traditional Thai engineering calculation example
    print("\n--- Traditional Thai Engineering Calculation Example ---")
    print("Slab design: 4m × 6m × 150mm thick")
    print("Live load: 300 kgf/m², Dead load: 200 kgf/m²")
    
    total_load_kgf_m2 = 300 + 200  # kgf/m²
    total_load_kn_m2 = thai_rc.load_kgf_m2_to_kn_m2(total_load_kgf_m2)
    print(f"Total load: {total_load_kgf_m2} kgf/m² = {total_load_kn_m2:.2f} kN/m²")
    
    # Use Fc210 concrete and DB20 @ 200mm reinforcement
    fc210_ksc = thai_rc.get_concrete_strength('Fc210', 'ksc')
    ec_thai = thai_rc.Ec(fc210_ksc, 2400, 'ksc')
    print(f"Concrete: Fc210 ({fc210_ksc} ksc), Ec = {ec_thai:.0f} ksc")
    print(f"Reinforcement: DB20 @ 200mm = {db20_per_m_200:.0f} mm²/m, SD40 ({sd40_ksc:.0f} ksc)")