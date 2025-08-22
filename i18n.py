#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Internationalization (i18n) System
Provides multi-language support for the twoWaySlab application

@author: Enhanced by AI Assistant
@date: 2024
"""

import json
import os
from config import config

class I18n:
    """
    Internationalization manager
    Handles loading and retrieving translations
    """
    
    def __init__(self):
        self.translations = {}
        self.current_language = 'ja'  # Default to Japanese
        self.translation_dir = 'translations'
        self.fallback_language = 'en'  # English as fallback
        
        # Load initial translations
        self.load_translations()

    def load_translations(self):
        """Load all available translation files"""
        if not os.path.exists(self.translation_dir):
            print(f"Warning: Translation directory '{self.translation_dir}' not found")
            return
        
        # Get all JSON files in translations directory
        for filename in os.listdir(self.translation_dir):
            if filename.endswith('.json'):
                language_code = filename[:-5]  # Remove .json extension
                file_path = os.path.join(self.translation_dir, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[language_code] = json.load(f)
                    print(f"Loaded translations for: {language_code}")
                except Exception as e:
                    print(f"Error loading translation file {filename}: {e}")

    def set_language(self, language_code):
        """Set current language"""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        else:
            print(f"Warning: Language '{language_code}' not available")
            return False

    def get_current_language(self):
        """Get current language code"""
        return self.current_language

    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())

    def t(self, key, language=None, **kwargs):
        """
        Translate a key to current language
        
        Args:
            key: Translation key (can be nested with dots, e.g., 'menu.file')
            language: Override language (optional)
            **kwargs: Variables for string formatting
            
        Returns:
            Translated string or key if not found
        """
        lang = language or self.current_language
        
        # Try to get translation in requested language
        translation = self._get_nested_value(self.translations.get(lang, {}), key)
        
        # Fallback to fallback language if not found
        if translation is None and lang != self.fallback_language:
            translation = self._get_nested_value(
                self.translations.get(self.fallback_language, {}), key
            )
        
        # If still not found, return the key itself
        if translation is None:
            translation = key
        
        # Format with provided variables
        if kwargs and isinstance(translation, str):
            try:
                translation = translation.format(**kwargs)
            except KeyError as e:
                print(f"Warning: Missing variable {e} in translation for key '{key}'")
        
        return translation

    def _get_nested_value(self, dictionary, key):
        """Get value from nested dictionary using dot notation"""
        keys = key.split('.')
        value = dictionary
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return value

    def get_boundary_conditions(self, language=None):
        """Get boundary condition names in specified language"""
        return self.t('boundary_types', language)

    def get_units(self, unit_type, language=None):
        """Get unit labels in specified language"""
        return self.t(f'units.{unit_type}', language)

    def get_error_message(self, error_key, language=None, **kwargs):
        """Get error message in specified language"""
        return self.t(f'messages.{error_key}', language, **kwargs)

    def get_button_text(self, button_key, language=None):
        """Get button text in specified language"""
        return self.t(f'buttons.{button_key}', language)

    def get_label_text(self, label_key, language=None):
        """Get label text in specified language"""
        return self.t(f'input_labels.{label_key}', language)

    def get_output_label(self, output_key, language=None):
        """Get output label text in specified language"""
        return self.t(f'output_labels.{output_key}', language)

    def update_from_config(self):
        """Update language from config system"""
        config_language = config.get_language()
        if config_language != self.current_language:
            self.set_language(config_language)

    def get_building_code_name(self, code_key, language=None):
        """Get building code name in specified language"""
        # This would need to be added to translation files
        return self.t(f'building_codes.{code_key}', language)

    def format_number(self, number, precision=2, language=None):
        """Format number according to language conventions"""
        lang = language or self.current_language
        
        # Different number formatting for different languages
        if lang == 'th':
            # Thai uses comma as thousand separator, period as decimal
            return f"{number:,.{precision}f}"
        elif lang == 'ja':
            # Japanese typically uses comma as thousand separator
            return f"{number:,.{precision}f}"
        else:
            # Default English formatting
            return f"{number:,.{precision}f}"

    def get_date_format(self, language=None):
        """Get date format for language"""
        lang = language or self.current_language
        formats = {
            'en': '%Y-%m-%d',
            'ja': '%Y年%m月%d日',
            'th': '%d/%m/%Y'
        }
        return formats.get(lang, '%Y-%m-%d')

    def reload_translations(self):
        """Reload all translation files"""
        self.translations.clear()
        self.load_translations()


# Global i18n instance
i18n = I18n()

# Convenience functions
def t(key, **kwargs):
    """Global translation function"""
    return i18n.t(key, **kwargs)

def set_language(language_code):
    """Set global language"""
    return i18n.set_language(language_code)

def get_language():
    """Get current language"""
    return i18n.get_current_language()

def get_available_languages():
    """Get available languages"""
    return i18n.get_available_languages()

def update_language_from_config():
    """Update language from config"""
    i18n.update_from_config()


# Test the i18n system
if __name__ == "__main__":
    print("=== Internationalization System Test ===")
    
    # Test available languages
    print(f"Available languages: {i18n.get_available_languages()}")
    
    # Test translations in different languages
    languages = ['en', 'ja', 'th']
    
    for lang in languages:
        if lang in i18n.get_available_languages():
            print(f"\n--- {lang.upper()} ---")
            i18n.set_language(lang)
            print(f"App title: {i18n.t('app_title')}")
            print(f"Calculate button: {i18n.t('buttons.calculate')}")
            print(f"Length unit: {i18n.t('units.length_m')}")
    
    # Test nested keys
    print(f"\nTesting nested keys:")
    print(f"File menu: {i18n.t('menu.file')}")
    print(f"Input error: {i18n.t('messages.input_error')}")
    
    # Test missing key fallback
    print(f"\nTesting missing key: {i18n.t('non.existent.key')}")
    
    # Test number formatting
    print(f"\nNumber formatting tests:")
    test_number = 1234.567
    for lang in ['en', 'ja', 'th']:
        if lang in i18n.get_available_languages():
            formatted = i18n.format_number(test_number, 2, lang)
            print(f"{lang}: {formatted}")