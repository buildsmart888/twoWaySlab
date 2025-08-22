#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Input Validation System
Provides comprehensive validation for structural design inputs

@author: Enhanced by AI Assistant
@date: 2024
"""

import re
import math
from typing import Tuple, Union, List, Optional

class ValidationResult:
    """Result of a validation operation"""
    
    def __init__(self, is_valid: bool, value: Union[float, str, None] = None, 
                 error_message: str = "", warning_message: str = ""):
        self.is_valid = is_valid
        self.value = value
        self.error_message = error_message
        self.warning_message = warning_message

    def __bool__(self):
        return self.is_valid

    def __str__(self):
        if self.is_valid:
            return f"Valid: {self.value}"
        else:
            return f"Invalid: {self.error_message}"


class InputValidator:
    """
    Input validation system for structural engineering parameters
    """
    
    def __init__(self):
        # Practical ranges for structural parameters
        self.ranges = {
            'slab_length': (0.5, 50.0),      # meters
            'slab_thickness': (50, 1000),     # mm
            'concrete_strength': (10, 100),   # N/mm²
            'steel_strength': (200, 700),     # N/mm²
            'unit_weight': (15, 35),          # kN/m³
            'load': (0.1, 100.0),             # kN/m²
            'creep_factor': (1.0, 5.0),       # dimensionless
            'effective_depth': (20, 800),     # mm
            'bar_spacing': (50, 500),         # mm
            'cover': (10, 100),               # mm
            'deflection_limit': (150, 500)    # L/x ratio
        }
        
        # Thai rebar designations - Updated per มยผ. 1103
        self.thai_rebars = [
            # เหล็กข้ออ้อย (Deformed Bar) - ตาม มยผ. 1103 ข้อ 4.2
            'DB10', 'DB12', 'DB20', 'DB25', 'DB32', 'DB36', 'DB40',
            # เหล็กเส้นกลม (Round Bar) - ตาม มยผ. 1103 ข้อ 4.1  
            'RB6', 'RB9',
            # เหล็กข้ออ้อยผสม (Combined deformed bars)
            'DB10+DB12', 'DB12+DB20', 'DB20+DB25', 'DB25+DB32'
        ]
        
        # Japanese rebar designations  
        self.japanese_rebars = [
            'D10', 'D13', 'D16', 'D19', 'D22', 'D25', 'D29', 'D32', 'D35', 'D38', 'D41',
            'D10+D13', 'D13+D16', 'D16+D19'
        ]
        
        # Boundary condition IDs
        self.boundary_conditions = list(range(1, 12))  # 1-11 based on original code

    def validate_float(self, value: str, param_name: str, 
                      min_val: float = None, max_val: float = None) -> ValidationResult:
        """
        Validate float input with optional range checking
        
        Args:
            value: String input to validate
            param_name: Parameter name for error messages
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            ValidationResult object
        """
        # Check if empty
        if not value or value.strip() == "":
            return ValidationResult(False, None, f"{param_name} cannot be empty")
        
        # Try to convert to float
        try:
            float_val = float(value.strip())
        except ValueError:
            return ValidationResult(False, None, f"{param_name} must be a valid number")
        
        # Check for special float values
        if math.isnan(float_val):
            return ValidationResult(False, None, f"{param_name} cannot be NaN")
        
        if math.isinf(float_val):
            return ValidationResult(False, None, f"{param_name} cannot be infinite")
        
        # Check range if specified
        if min_val is not None and float_val < min_val:
            return ValidationResult(False, None, 
                                  f"{param_name} must be at least {min_val}")
        
        if max_val is not None and float_val > max_val:
            return ValidationResult(False, None, 
                                  f"{param_name} must be at most {max_val}")
        
        return ValidationResult(True, float_val)

    def validate_slab_dimension(self, value: str, dimension_name: str) -> ValidationResult:
        """Validate slab dimensions (length, width)"""
        min_val, max_val = self.ranges['slab_length']
        result = self.validate_float(value, dimension_name, min_val, max_val)
        
        if result.is_valid:
            # Additional checks for slab dimensions
            if result.value < 1.0:
                result.warning_message = f"Small {dimension_name} ({result.value}m) - check if realistic"
            elif result.value > 15.0:
                result.warning_message = f"Large {dimension_name} ({result.value}m) - may need special analysis"
        
        return result

    def validate_thickness(self, value: str) -> ValidationResult:
        """Validate slab thickness"""
        min_val, max_val = self.ranges['slab_thickness']
        result = self.validate_float(value, "Thickness", min_val, max_val)
        
        if result.is_valid:
            if result.value < 100:
                result.warning_message = f"Thin slab ({result.value}mm) - check deflection requirements"
            elif result.value > 500:
                result.warning_message = f"Thick slab ({result.value}mm) - check if economical"
        
        return result

    def validate_effective_depth(self, thickness: float, effective_depth: str) -> ValidationResult:
        """Validate effective depth considering thickness"""
        min_val, max_val = self.ranges['effective_depth']
        result = self.validate_float(effective_depth, "Effective depth", min_val, max_val)
        
        if result.is_valid:
            dt = result.value
            
            # Check if effective depth is reasonable compared to thickness
            if dt >= thickness:
                return ValidationResult(False, None, 
                                      "Effective depth cannot be greater than or equal to total thickness")
            
            cover = thickness - dt
            if cover < 15:
                result.warning_message = f"Very small cover ({cover:.1f}mm) - check durability requirements"
            elif cover > 80:
                result.warning_message = f"Large cover ({cover:.1f}mm) - check if necessary"
        
        return result

    def validate_concrete_strength(self, value: str) -> ValidationResult:
        """Validate concrete compressive strength"""
        min_val, max_val = self.ranges['concrete_strength']
        result = self.validate_float(value, "Concrete strength", min_val, max_val)
        
        if result.is_valid:
            fc = result.value
            
            # Common concrete grades check
            common_grades = [15, 18, 21, 24, 28, 35, 42, 50]
            if fc not in common_grades:
                closest = min(common_grades, key=lambda x: abs(x - fc))
                result.warning_message = f"Unusual concrete strength. Closest standard grade: {closest} N/mm²"
        
        return result

    def validate_steel_strength(self, value: str) -> ValidationResult:
        """Validate steel yield strength"""
        min_val, max_val = self.ranges['steel_strength']
        result = self.validate_float(value, "Steel strength", min_val, max_val)
        
        if result.is_valid:
            fy = result.value
            
            # Common steel grades
            if abs(fy - 295) < 5:
                pass  # SD30
            elif abs(fy - 390) < 5:
                pass  # SD40
            elif abs(fy - 490) < 5:
                pass  # SD50
            else:
                result.warning_message = f"Unusual steel strength ({fy} N/mm²). Common grades: 295, 390, 490"
        
        return result

    def validate_load(self, value: str) -> ValidationResult:
        """Validate applied load"""
        min_val, max_val = self.ranges['load']
        result = self.validate_float(value, "Load", min_val, max_val)
        
        if result.is_valid:
            load = result.value
            
            if load < 2.0:
                result.warning_message = "Low load - check if live load is included"
            elif load > 30.0:
                result.warning_message = "High load - verify load calculations"
        
        return result

    def validate_unit_weight(self, value: str) -> ValidationResult:
        """Validate concrete unit weight"""
        min_val, max_val = self.ranges['unit_weight']
        result = self.validate_float(value, "Unit weight", min_val, max_val)
        
        if result.is_valid:
            gamma = result.value
            
            if abs(gamma - 24.0) > 2.0:
                result.warning_message = f"Non-standard concrete density ({gamma} kN/m³). Normal: 24 kN/m³"
        
        return result

    def validate_creep_factor(self, value: str) -> ValidationResult:
        """Validate creep factor"""
        min_val, max_val = self.ranges['creep_factor']
        result = self.validate_float(value, "Creep factor", min_val, max_val)
        
        if result.is_valid:
            creep = result.value
            
            if creep < 1.5:
                result.warning_message = "Low creep factor - check if appropriate for loading conditions"
            elif creep > 3.0:
                result.warning_message = "High creep factor - check if appropriate for concrete age/loading"
        
        return result

    def validate_rebar_designation(self, value: str, building_code: str = 'thai') -> ValidationResult:
        """Validate rebar designation based on building code"""
        if not value or value.strip() == "":
            return ValidationResult(False, None, "Rebar designation cannot be empty")
        
        designation = value.strip().upper()
        
        if building_code.lower() == 'thai':
            valid_rebars = self.thai_rebars
        elif building_code.lower() in ['japanese', 'japan']:
            valid_rebars = self.japanese_rebars
        else:
            # Accept both
            valid_rebars = self.thai_rebars + self.japanese_rebars
        
        if designation in valid_rebars:
            return ValidationResult(True, designation)
        else:
            return ValidationResult(False, None, 
                                  f"Invalid rebar designation '{designation}'. Valid options: {', '.join(valid_rebars[:10])}...")

    def validate_bar_spacing(self, value: str, bar_size: int = 16) -> ValidationResult:
        """Validate bar spacing/pitch"""
        min_val, max_val = self.ranges['bar_spacing']
        result = self.validate_float(value, "Bar spacing", min_val, max_val)
        
        if result.is_valid:
            spacing = result.value
            
            # Check minimum spacing (typically 3 times bar diameter)
            min_spacing = max(50, 3 * bar_size)
            if spacing < min_spacing:
                return ValidationResult(False, None, 
                                      f"Bar spacing ({spacing}mm) too small. Minimum: {min_spacing}mm")
            
            # Check maximum spacing for crack control
            max_spacing_crack = min(300, 2 * 150)  # 2 times slab thickness (assumed 150mm average)
            if spacing > max_spacing_crack:
                result.warning_message = f"Large spacing ({spacing}mm) - check crack control requirements"
        
        return result

    def validate_boundary_condition(self, value: str) -> ValidationResult:
        """Validate boundary condition selection"""
        try:
            bc_id = int(value)
            if bc_id in self.boundary_conditions:
                return ValidationResult(True, bc_id)
            else:
                return ValidationResult(False, None, 
                                      f"Invalid boundary condition ID. Valid range: 1-{len(self.boundary_conditions)}")
        except (ValueError, TypeError):
            return ValidationResult(False, None, "Boundary condition must be a valid integer")

    def validate_title(self, value: str) -> ValidationResult:
        """Validate project title"""
        if not value or value.strip() == "":
            return ValidationResult(False, None, "Title cannot be empty")
        
        title = value.strip()
        
        # Check for forbidden characters
        if ',' in title:
            return ValidationResult(False, None, "Title cannot contain commas")
        
        # Check length
        if len(title) > 100:
            return ValidationResult(False, None, "Title too long (max 100 characters)")
        
        return ValidationResult(True, title)

    def validate_aspect_ratio(self, lx: float, ly: float) -> ValidationResult:
        """Validate slab aspect ratio"""
        if lx <= 0 or ly <= 0:
            return ValidationResult(False, None, "Dimensions must be positive")
        
        ratio = max(lx, ly) / min(lx, ly)
        
        if ratio > 4.0:
            return ValidationResult(False, None, 
                                  f"Aspect ratio ({ratio:.1f}) too high. Consider one-way slab analysis")
        elif ratio > 2.5:
            result = ValidationResult(True, ratio)
            result.warning_message = f"High aspect ratio ({ratio:.1f}) - check if two-way action is significant"
            return result
        
        return ValidationResult(True, ratio)

    def validate_deflection_requirement(self, span: float, thickness: float) -> ValidationResult:
        """Validate deflection requirements (span/depth ratio)"""
        if span <= 0 or thickness <= 0:
            return ValidationResult(False, None, "Span and thickness must be positive")
        
        span_mm = span * 1000  # Convert to mm
        ratio = span_mm / thickness
        
        # Typical limits: L/250 for live load, L/350 for total load
        # For span/depth: typically 20-35 for slabs
        if ratio > 40:
            return ValidationResult(False, None, 
                                  f"Span/depth ratio ({ratio:.1f}) too high - deflection problems likely")
        elif ratio > 30:
            result = ValidationResult(True, ratio)
            result.warning_message = f"High span/depth ratio ({ratio:.1f}) - check deflection carefully"
            return result
        elif ratio < 15:
            result = ValidationResult(True, ratio)
            result.warning_message = f"Low span/depth ratio ({ratio:.1f}) - may be over-conservative"
            return result
        
        return ValidationResult(True, ratio)

    def validate_all_inputs(self, inputs: dict, building_code: str = 'thai') -> dict:
        """
        Validate all inputs at once
        
        Args:
            inputs: Dictionary of input values
            building_code: Building code for validation context
            
        Returns:
            Dictionary of validation results
        """
        results = {}
        
        # Validate individual inputs
        if 'title' in inputs:
            results['title'] = self.validate_title(inputs['title'])
        
        if 'lx' in inputs:
            results['lx'] = self.validate_slab_dimension(inputs['lx'], 'Length X')
        
        if 'ly' in inputs:
            results['ly'] = self.validate_slab_dimension(inputs['ly'], 'Length Y')
        
        if 't' in inputs:
            results['thickness'] = self.validate_thickness(inputs['t'])
        
        if 'fc' in inputs:
            results['concrete_strength'] = self.validate_concrete_strength(inputs['fc'])
        
        if 'fy' in inputs:
            results['steel_strength'] = self.validate_steel_strength(inputs['fy'])
        
        if 'w' in inputs:
            results['load'] = self.validate_load(inputs['w'])
        
        if 'gamma' in inputs:
            results['unit_weight'] = self.validate_unit_weight(inputs['gamma'])
        
        if 'creep' in inputs:
            results['creep'] = self.validate_creep_factor(inputs['creep'])
        
        if 'boundary_condition' in inputs:
            results['boundary_condition'] = self.validate_boundary_condition(inputs['boundary_condition'])
        
        # Cross-validation checks
        if all(key in results and results[key].is_valid for key in ['lx', 'ly']):
            lx_val = results['lx'].value
            ly_val = results['ly'].value
            results['aspect_ratio'] = self.validate_aspect_ratio(lx_val, ly_val)
        
        if all(key in results and results[key].is_valid for key in ['lx', 'thickness']):
            span = max(results['lx'].value, results.get('ly', results['lx']).value)
            thickness = results['thickness'].value
            results['deflection_ratio'] = self.validate_deflection_requirement(span, thickness)
        
        return results

    def get_validation_summary(self, results: dict) -> Tuple[bool, List[str], List[str]]:
        """
        Get summary of validation results
        
        Returns:
            Tuple of (all_valid, errors, warnings)
        """
        errors = []
        warnings = []
        all_valid = True
        
        for name, result in results.items():
            if not result.is_valid:
                all_valid = False
                errors.append(f"{name}: {result.error_message}")
            elif result.warning_message:
                warnings.append(f"{name}: {result.warning_message}")
        
        return all_valid, errors, warnings


# Global validator instance
validator = InputValidator()

# Convenience functions
def validate_float_input(value: str, param_name: str, min_val: float = None, max_val: float = None) -> ValidationResult:
    """Validate float input"""
    return validator.validate_float(value, param_name, min_val, max_val)

def validate_all_inputs(inputs: dict, building_code: str = 'thai') -> dict:
    """Validate all inputs"""
    return validator.validate_all_inputs(inputs, building_code)

def get_validation_summary(results: dict) -> Tuple[bool, List[str], List[str]]:
    """Get validation summary"""
    return validator.get_validation_summary(results)


# Test the validation system
if __name__ == "__main__":
    print("=== Input Validation System Test ===")
    
    # Test individual validations
    print("Testing individual validations:")
    
    # Valid inputs
    result = validator.validate_slab_dimension("3.5", "Length")
    print(f"Valid length: {result}")
    
    # Invalid inputs
    result = validator.validate_concrete_strength("abc")
    print(f"Invalid concrete strength: {result}")
    
    # Warning case
    result = validator.validate_thickness("80")
    print(f"Thin slab warning: {result}")
    if result.warning_message:
        print(f"Warning: {result.warning_message}")
    
    # Test comprehensive validation
    print(f"\nTesting comprehensive validation:")
    
    test_inputs = {
        'title': 'Test Project',
        'lx': '4.0',
        'ly': '6.0', 
        'thickness': '150',
        'fc': '21',
        'fy': '390',
        'w': '10.0',
        'gamma': '24',
        'creep': '2.0',
        'boundary_condition': '1'
    }
    
    results = validator.validate_all_inputs(test_inputs, 'thai')
    all_valid, errors, warnings = validator.get_validation_summary(results)
    
    print(f"All valid: {all_valid}")
    if errors:
        print(f"Errors: {errors}")
    if warnings:
        print(f"Warnings: {warnings}")
    
    print(f"\nValidation results summary:")
    for name, result in results.items():
        status = "✓" if result.is_valid else "✗"
        print(f"{status} {name}: {result.value if result.is_valid else result.error_message}")