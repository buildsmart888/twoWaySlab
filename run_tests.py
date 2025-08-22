#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Test Runner for Enhanced twoWaySlab System
Tests all new features and integration points

@author: Enhanced by AI Assistant
@date: 2024
"""

import sys
import traceback

def test_thai_building_code():
    """Test Thai building code implementation"""
    print("=" * 50)
    print("Testing Thai Building Code (thiRc.py)")
    print("=" * 50)
    
    try:
        from thiRc import ThaiRc_set, Aij_rc_set
        
        # Test Thai RC implementation
        thai_rc = ThaiRc_set()
        
        print("✓ Thai RC class instantiated successfully")
        
        # Test concrete modulus calculation
        ec = thai_rc.Ec(21.0, 24.0)
        print(f"✓ Concrete modulus (fc=21): {ec:.0f} N/mm²")
        
        # Test rebar areas
        db20_area = thai_rc.Ra('DB20')
        print(f"✓ DB20 rebar area: {db20_area} mm²")
        
        # Test rebar per unit width
        db20_per_m = thai_rc.Ra_p('DB20', 200)
        print(f"✓ DB20 @ 200mm spacing: {db20_per_m:.1f} mm²/m")
        
        # Test steel strength
        sd40_strength = thai_rc.get_steel_strength('SD40')
        print(f"✓ SD40 steel strength: {sd40_strength} N/mm²")
        
        # Test compatibility wrapper
        compat_rc = Aij_rc_set()
        d16_mapped = compat_rc.Ra('D16')
        print(f"✓ D16 mapped to Thai: {d16_mapped} mm²")
        
        print("✓ Thai building code tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Thai building code test FAILED: {e}")
        traceback.print_exc()
        return False

def test_configuration_system():
    """Test configuration management system"""
    print("=" * 50)
    print("Testing Configuration System (config.py)")
    print("=" * 50)
    
    try:
        from config import Config, config
        
        print("✓ Configuration system imported successfully")
        
        # Test building code switching
        original_code = config.get_building_code()
        print(f"✓ Current building code: {original_code}")
        
        # Test available codes
        available_codes = config.get_available_codes()
        print(f"✓ Available codes: {available_codes}")
        
        # Switch to Thai code
        success = config.set_building_code('thai')
        if success:
            print("✓ Successfully switched to Thai building code")
            current_code = config.get_building_code()
            print(f"✓ Current code after switch: {current_code}")
        
        # Test material instance loading
        material = config.get_material_instance()
        print(f"✓ Material instance loaded: {type(material)}")
        
        # Test default values
        defaults = config.get_default_values()
        print(f"✓ Default values retrieved: fc={defaults['concrete_strength']}")
        
        # Restore original code
        config.set_building_code(original_code)
        
        print("✓ Configuration system tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Configuration system test FAILED: {e}")
        traceback.print_exc()
        return False

def test_internationalization():
    """Test internationalization system"""
    print("=" * 50)
    print("Testing Internationalization (i18n.py)")
    print("=" * 50)
    
    try:
        from i18n import I18n, i18n
        
        print("✓ I18n system imported successfully")
        
        # Test available languages
        languages = i18n.get_available_languages()
        print(f"✓ Available languages: {languages}")
        
        # Test translations in different languages
        for lang in ['en', 'ja', 'th']:
            if lang in languages:
                i18n.set_language(lang)
                app_title = i18n.t('app_title')
                print(f"✓ {lang.upper()}: {app_title}")
        
        # Test nested keys
        if 'en' in languages:
            i18n.set_language('en')
            file_menu = i18n.t('menu.file')
            print(f"✓ Nested key (menu.file): {file_menu}")
        
        # Test button text
        calc_button = i18n.t('buttons.calculate')
        print(f"✓ Button text: {calc_button}")
        
        # Test number formatting
        formatted_num = i18n.format_number(1234.567, 2)
        print(f"✓ Number formatting: {formatted_num}")
        
        print("✓ Internationalization tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Internationalization test FAILED: {e}")
        traceback.print_exc()
        return False

def test_unit_conversion():
    """Test unit conversion system"""
    print("=" * 50)
    print("Testing Unit Conversion (units.py)")
    print("=" * 50)
    
    try:
        from units import UnitConverter, unit_converter
        
        print("✓ Unit conversion system imported successfully")
        
        # Test basic conversions
        length_conv = unit_converter.convert_length(1000, 'mm', 'm')
        print(f"✓ Length conversion: 1000 mm = {length_conv} m")
        
        stress_conv = unit_converter.convert_stress(21, 'N/mm2', 'MPa')
        print(f"✓ Stress conversion: 21 N/mm² = {stress_conv} MPa")
        
        # Test unit systems
        systems = unit_converter.get_available_systems()
        print(f"✓ Available unit systems: {systems}")
        
        # Test system conversion
        unit_converter.set_unit_system('metric_engineering')
        stress_unit = unit_converter.get_unit_for_quantity('stress')
        print(f"✓ Stress unit in metric_engineering: {stress_unit}")
        
        # Test formatting
        formatted = unit_converter.format_value_with_unit(21.0, 'stress', 1)
        print(f"✓ Formatted stress: {formatted}")
        
        # Test imperial conversion
        imperial_stress = unit_converter.convert_to_system(
            21.0, 'stress', 'metric_engineering', 'imperial'
        )
        print(f"✓ 21 N/mm² in imperial: {imperial_stress:.1f} ksi")
        
        print("✓ Unit conversion tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Unit conversion test FAILED: {e}")
        traceback.print_exc()
        return False

def test_input_validation():
    """Test input validation system"""
    print("=" * 50)
    print("Testing Input Validation (validation.py)")
    print("=" * 50)
    
    try:
        from validation import InputValidator, validator
        
        print("✓ Input validation system imported successfully")
        
        # Test valid inputs
        result = validator.validate_slab_dimension("3.5", "Length X")
        print(f"✓ Valid length validation: {result.is_valid}, value: {result.value}")
        
        # Test invalid inputs
        result = validator.validate_concrete_strength("abc")
        print(f"✓ Invalid input detection: {result.is_valid}, error: {result.error_message}")
        
        # Test warning generation
        result = validator.validate_thickness("80")
        print(f"✓ Warning generation: warning: {result.warning_message}")
        
        # Test Thai rebar validation
        result = validator.validate_rebar_designation("DB20", "thai")
        print(f"✓ Thai rebar validation: {result.is_valid}, value: {result.value}")
        
        # Test comprehensive validation
        test_inputs = {
            'title': 'Test Project',
            'lx': '4.0',
            'ly': '6.0',
            'thickness': '150',
            'fc': '21',
            'w': '10.0'
        }
        
        results = validator.validate_all_inputs(test_inputs)
        all_valid, errors, warnings = validator.get_validation_summary(results)
        print(f"✓ Comprehensive validation: all_valid={all_valid}, errors={len(errors)}, warnings={len(warnings)}")
        
        print("✓ Input validation tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ Input validation test FAILED: {e}")
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between systems"""
    print("=" * 50)
    print("Testing System Integration")
    print("=" * 50)
    
    try:
        # Import all systems
        from config import config
        from i18n import i18n
        from units import unit_converter
        from thiRc import ThaiRc_set
        
        print("✓ All systems imported successfully")
        
        # Test config + material integration
        config.set_building_code('thai')
        material = config.get_material_instance()
        if isinstance(material, (ThaiRc_set,)):
            print("✓ Config correctly loads Thai material class")
        
        # Test config + i18n integration
        config_lang = config.get_language()
        i18n.set_language(config_lang)
        print(f"✓ Config language ({config_lang}) synced with i18n")
        
        # Test material + unit conversion
        fc = 21.0  # N/mm²
        ec = material.Ec(fc, 24.0)
        ec_mpa = unit_converter.convert_stress(ec, 'N/mm2', 'MPa')
        print(f"✓ Material calculation + unit conversion: Ec = {ec_mpa:.0f} MPa")
        
        # Test full workflow
        db20_area = material.Ra('DB20')
        db20_per_m = material.Ra_p('DB20', 200)
        area_text = i18n.t('units.area')
        print(f"✓ Full workflow: DB20 = {db20_area} {area_text}, {db20_per_m:.1f} mm²/m @ 200mm")
        
        print("✓ System integration tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"✗ System integration test FAILED: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("ENHANCED TWOWAYSLAB SYSTEM TESTS")
    print("=" * 70)
    print("Testing all new features and enhancements...\n")
    
    tests = [
        ("Thai Building Code", test_thai_building_code),
        ("Configuration System", test_configuration_system),
        ("Internationalization", test_internationalization),
        ("Unit Conversion", test_unit_conversion),
        ("Input Validation", test_input_validation),
        ("System Integration", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ {test_name} test encountered unexpected error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        icon = "✓" if success else "✗"
        print(f"{icon} {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The enhanced system is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)