#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Configuration Management System
Handles building code selection, language settings, and application preferences

@author: Enhanced by AI Assistant
@date: 2024
"""

import json
import os

class Config:
    """
    Configuration manager for twoWaySlab application
    Supports multiple building codes and internationalization
    """
    
    def __init__(self):
        self.config_file = "config.json"
        self.building_codes = {
            'japanese': {
                'name': 'AIJ/JSCE (Japan)',
                'module': 'aijRc',
                'class': 'Aij_rc_set',
                'language': 'ja',
                'description': 'Architectural Institute of Japan standards',
                'default_concrete_strength': 21.0,
                'default_steel_strength': 295.0,
                'default_unit_weight': 24.0,
                'cover_requirements': {
                    'normal': 20,
                    'aggressive': 30,
                    'marine': 40
                }
            },
            'thai': {
                'name': 'TIS (Thailand)', 
                'module': 'thiRc',
                'class': 'ThaiRc_set',
                'language': 'th',
                'description': 'Thai Industrial Standards',
                'default_concrete_strength': 21.0,
                'default_steel_strength': 390.0,
                'default_unit_weight': 24.0,
                'cover_requirements': {
                    'normal': 20,
                    'aggressive': 30,
                    'marine': 40
                }
            },
            'thai_ministry_2566': {
                'name': 'กฎกระทรวง พ.ศ. 2566 (Thailand)', 
                'module': 'thaiMinistryReg',
                'class': 'ThaiMinistryRegulation2566',
                'language': 'th',
                'description': 'Thai Ministry Regulation for Building Structural Design B.E. 2566',
                'default_concrete_strength': 21.0,
                'default_steel_strength': 392.4,
                'default_unit_weight': 24.0,
                'cover_requirements': {
                    'normal': 20,
                    'aggressive': 30,
                    'marine': 40
                },
                'safety_factors': {
                    'concrete': 1.5,
                    'steel': 1.15,
                    'dead_load': 1.4,
                    'live_load': 1.6,
                    'wind_load': 1.6,
                    'seismic_load': 1.0
                },
                'deflection_limits': {
                    'simply_supported': 300,
                    'continuous': 350,
                    'cantilever': 250
                }
            },
            'aci': {
                'name': 'ACI 318-19 (USA)',
                'module': 'aciRc', 
                'class': 'AciRc_set',
                'language': 'en',
                'description': 'American Concrete Institute standards (US Customary)',
                'default_concrete_strength': 3000,  # psi
                'default_steel_strength': 60000,    # psi
                'default_unit_weight': 150,         # pcf
                'cover_requirements': {
                    'normal': 0.75,  # inches
                    'aggressive': 1.5,
                    'marine': 2.0
                }
            },
            'aci318m25': {
                'name': 'ACI 318M-25 (International SI)',
                'module': 'aci318m25',
                'class': 'ACI318M25',
                'language': 'en',
                'description': 'ACI 318M-25 Building Code for Structural Concrete (International System of Units)',
                'default_concrete_strength': 28.0,  # MPa
                'default_steel_strength': 420.0,    # MPa
                'default_unit_weight': 24.0,        # kN/m³
                'cover_requirements': {
                    'normal': 20,    # mm
                    'corrosive': 40, # mm
                    'severe': 65     # mm
                },
                'strength_reduction_factors': {
                    'tension_controlled': 0.90,
                    'compression_controlled_tied': 0.65,
                    'compression_controlled_spiral': 0.75,
                    'shear': 0.75,
                    'torsion': 0.75
                },
                'concrete_classes': ['FC14', 'FC17', 'FC21', 'FC28', 'FC35', 'FC42', 'FC50', 'FC70', 'FC100'],
                'steel_grades': ['GRADE280', 'GRADE420', 'GRADE520'],
                'bar_designations': ['10M', '15M', '20M', '25M', '30M', '35M', '45M', '55M'],
                'member_libraries': {
                    'beam': {
                        'module': 'aci318m25_beam',
                        'class': 'ACI318M25BeamDesign',
                        'description': 'Beam flexural and shear design'
                    },
                    'column': {
                        'module': 'aci318m25_column',
                        'class': 'ACI318M25ColumnDesign',
                        'description': 'Column axial and P-M interaction design'
                    },
                    'slab': {
                        'module': 'aci318m25_slab',
                        'class': 'ACI318M25SlabDesign',
                        'description': 'One-way and two-way slab design'
                    },
                    'footing': {
                        'module': 'aci318m25_footing',
                        'class': 'ACI318M25FootingDesign',
                        'description': 'Foundation design and analysis'
                    },
                    'wall': {
                        'module': 'aci318m25_wall',
                        'class': 'ACI318M25WallDesign',
                        'description': 'Bearing and shear wall design'
                    },
                    'diaphragm': {
                        'module': 'aci318m25_diaphragm',
                        'class': 'ACI318M25DiaphragmDesign',
                        'description': 'In-plane diaphragm design and collector elements'
                    },
                    'complete': {
                        'module': 'aci318m25_complete',
                        'class': 'ACI318M25MemberLibrary',
                        'description': 'Complete member library manager'
                    }
                }
            },
            'eurocode': {
                'name': 'Eurocode (EU)',
                'module': 'euRc',
                'class': 'EuRc_set', 
                'language': 'en',
                'description': 'European standards for concrete design',
                'default_concrete_strength': 25.0,
                'default_steel_strength': 500.0,
                'default_unit_weight': 25.0,
                'cover_requirements': {
                    'normal': 25,
                    'aggressive': 35,
                    'marine': 45
                }
            }
        }
        
        # Default settings
        self.default_config = {
            'building_code': 'japanese',
            'language': 'ja',
            'units': 'metric',
            'precision': {
                'stress': 1,
                'moment': 2,
                'deflection': 3,
                'area': 1
            },
            'calculation_settings': {
                'creep_factor': 2.0,
                'safety_factors': {
                    'concrete': 1.5,
                    'steel': 1.15
                },
                'fourier_terms': 5
            },
            'gui_settings': {
                'window_size': [1200, 800],
                'font_size': 9,
                'show_tooltips': True,
                'auto_save': True
            }
        }
        
        self.current_config = self.load_config()

    def load_config(self):
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_config(self.default_config, config)
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def _merge_config(self, default, loaded):
        """Merge loaded config with defaults to ensure all keys exist"""
        merged = default.copy()
        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_config(merged[key], value)
            else:
                merged[key] = value
        return merged

    def get_building_code(self):
        """Get current building code"""
        return self.current_config['building_code']

    def set_building_code(self, code):
        """Set building code and update related settings"""
        if code in self.building_codes:
            self.current_config['building_code'] = code
            # Update language to match building code default
            self.current_config['language'] = self.building_codes[code]['language']
            self.save_config()
            return True
        return False

    def get_building_code_info(self, code=None):
        """Get information about a building code"""
        if code is None:
            code = self.current_config['building_code']
        return self.building_codes.get(code, {})

    def get_available_codes(self):
        """Get list of available building codes"""
        return list(self.building_codes.keys())

    def get_language(self):
        """Get current language setting"""
        return self.current_config['language']

    def set_language(self, language):
        """Set language"""
        self.current_config['language'] = language
        self.save_config()

    def get_material_module(self):
        """Get the material module for current building code"""
        code_info = self.get_building_code_info()
        return code_info.get('module', 'aijRc')

    def get_material_class(self):
        """Get the material class for current building code"""
        code_info = self.get_building_code_info()
        return code_info.get('class', 'Aij_rc_set')

    def get_default_values(self):
        """Get default material values for current building code"""
        code_info = self.get_building_code_info()
        return {
            'concrete_strength': code_info.get('default_concrete_strength', 21.0),
            'steel_strength': code_info.get('default_steel_strength', 295.0),
            'unit_weight': code_info.get('default_unit_weight', 24.0),
            'cover_requirements': code_info.get('cover_requirements', {})
        }

    def get_precision(self, value_type):
        """Get precision setting for different value types"""
        return self.current_config['precision'].get(value_type, 2)

    def get_safety_factor(self, material):
        """Get safety factor for material"""
        return self.current_config['calculation_settings']['safety_factors'].get(material, 1.0)

    def get_creep_factor(self):
        """Get creep factor setting"""
        return self.current_config['calculation_settings']['creep_factor']

    def get_fourier_terms(self):
        """Get number of Fourier terms for calculation"""
        return self.current_config['calculation_settings']['fourier_terms']

    def update_setting(self, section, key, value):
        """Update a specific setting"""
        if section in self.current_config:
            if isinstance(self.current_config[section], dict):
                self.current_config[section][key] = value
            else:
                self.current_config[section] = value
        else:
            self.current_config[section] = {key: value}
        self.save_config()

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.current_config = self.default_config.copy()
        self.save_config()

    def get_material_instance(self):
        """
        Dynamically load and return material class instance
        based on current building code selection
        """
        try:
            module_name = self.get_material_module()
            class_name = self.get_material_class()
            
            # Import the module dynamically
            if module_name == 'aijRc':
                import aijRc
                return getattr(aijRc, class_name)()
            elif module_name == 'thiRc':
                import thiRc
                return getattr(thiRc, class_name)()
            elif module_name == 'thaiMinistryReg':
                import thaiMinistryReg
                return getattr(thaiMinistryReg, class_name)()
            else:
                # Fallback to Japanese standard
                import aijRc
                return aijRc.Aij_rc_set()
                
        except Exception as e:
            print(f"Error loading material module: {e}")
            # Fallback to Japanese standard
            import aijRc
            return aijRc.Aij_rc_set()
    
    def get_ministry_regulation_instance(self):
        """
        Get Thai Ministry Regulation B.E. 2566 instance regardless of current building code
        
        Returns:
            ThaiMinistryRegulation2566 instance or None if not available
        """
        try:
            import thaiMinistryReg
            return thaiMinistryReg.ThaiMinistryRegulation2566()
        except ImportError:
            print("Warning: Thai Ministry Regulation B.E. 2566 module not available")
            return None
    
    def is_ministry_regulation_available(self):
        """
        Check if Thai Ministry Regulation B.E. 2566 is available
        
        Returns:
            Boolean indicating availability
        """
        try:
            import thaiMinistryReg
            return True
        except ImportError:
            return False


# Global configuration instance
config = Config()

# Convenience functions
def get_current_building_code():
    """Get current building code"""
    return config.get_building_code()

def set_building_code(code):
    """Set building code"""
    return config.set_building_code(code)

def get_material_instance():
    """Get material class instance for current building code"""
    return config.get_material_instance()

def get_language():
    """Get current language"""
    return config.get_language()

def set_language(language):
    """Set language"""
    return config.set_language(language)


# Test the configuration system
if __name__ == "__main__":
    print("=== Configuration System Test ===")
    
    # Test building code switching
    print(f"Current building code: {config.get_building_code()}")
    print(f"Available codes: {config.get_available_codes()}")
    
    # Switch to Thai code
    print(f"\nSwitching to Thai building code...")
    config.set_building_code('thai')
    print(f"Current building code: {config.get_building_code()}")
    print(f"Language: {config.get_language()}")
    
    # Test material instance loading
    print(f"\nTesting material instance loading...")
    material = config.get_material_instance()
    print(f"Material class: {type(material)}")
    
    # Test default values
    defaults = config.get_default_values()
    print(f"Default values: {defaults}")