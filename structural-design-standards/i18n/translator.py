"""
Internationalization Translator Module
======================================

Provides translation utilities for multi-language support in the 
structural design standards library.

ระบบแปลภาษาสำหรับไลบรารี่มาตรฐานการออกแบบโครงสร้าง
"""

import os
import gettext
import json
from pathlib import Path
from typing import Dict, Optional, Union, Any
from enum import Enum

class SupportedLanguage(Enum):
    """Supported languages enumeration"""
    ENGLISH = "en"
    THAI = "th"
    JAPANESE = "ja"  # Future support

class TranslationDomain(Enum):
    """Translation domain categories"""
    ACI = "aci"
    THAI = "thai"
    COMMON = "common"

class Translator:
    """
    Multi-language translator for structural design standards
    
    Provides translation services for:
    - ACI 318M-25 terminology
    - Thai standards terminology
    - Common engineering terms
    - User interface elements
    """
    
    def __init__(self, default_language: Union[str, SupportedLanguage] = SupportedLanguage.ENGLISH):
        """
        Initialize translator
        
        Parameters:
        -----------
        default_language : str or SupportedLanguage
            Default language for translations
        """
        self.default_language = self._validate_language(default_language)
        self.current_language = self.default_language
        
        # Find locales directory
        self.locales_dir = self._find_locales_directory()
        
        # Initialize translation catalogs
        self._translations: Dict[str, Dict[str, gettext.GNUTranslations]] = {}
        self._load_translations()
        
        # Message cache for performance
        self._message_cache: Dict[str, str] = {}
    
    def _validate_language(self, language: Union[str, SupportedLanguage]) -> SupportedLanguage:
        """Validate and convert language parameter"""
        if isinstance(language, str):
            try:
                return SupportedLanguage(language)
            except ValueError:
                raise ValueError(f"Unsupported language: {language}")
        return language
    
    def _find_locales_directory(self) -> Path:
        """Find the locales directory relative to this module"""
        current_dir = Path(__file__).parent
        
        # Try different possible locations
        possible_paths = [
            current_dir.parent / "locales",  # ../locales
            current_dir / "locales",         # ./locales
            current_dir.parent.parent / "locales",  # ../../locales
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_dir():
                return path
        
        # Create default locales directory if not found
        default_path = current_dir.parent / "locales"
        default_path.mkdir(exist_ok=True)
        return default_path
    
    def _load_translations(self) -> None:
        """Load all available translation catalogs"""
        for language in SupportedLanguage:
            self._translations[language.value] = {}
            
            for domain in TranslationDomain:
                try:
                    translation = gettext.translation(
                        domain.value,
                        localedir=self.locales_dir,
                        languages=[language.value],
                        fallback=True
                    )
                    self._translations[language.value][domain.value] = translation
                except Exception as e:
                    # Create null translation for missing catalogs
                    self._translations[language.value][domain.value] = gettext.NullTranslations()
    
    def set_language(self, language: Union[str, SupportedLanguage]) -> None:
        """
        Set the current language for translations
        
        Parameters:
        -----------
        language : str or SupportedLanguage
            Language to set as current
        """
        self.current_language = self._validate_language(language)
        self._message_cache.clear()  # Clear cache when language changes
    
    def get_current_language(self) -> SupportedLanguage:
        """Get the current language setting"""
        return self.current_language
    
    def get_supported_languages(self) -> list[SupportedLanguage]:
        """Get list of supported languages"""
        return list(SupportedLanguage)
    
    def get_message(self, 
                   message_id: str, 
                   domain: Union[str, TranslationDomain] = TranslationDomain.COMMON,
                   lang: Optional[Union[str, SupportedLanguage]] = None) -> str:
        """
        Get translated message for given message ID
        
        Parameters:
        -----------
        message_id : str
            Message identifier to translate
        domain : str or TranslationDomain
            Translation domain (aci, thai, common)
        lang : str or SupportedLanguage, optional
            Language for translation (uses current if not specified)
            
        Returns:
        --------
        str
            Translated message or original message_id if not found
        """
        # Use current language if not specified
        if lang is None:
            lang = self.current_language
        else:
            lang = self._validate_language(lang)
        
        # Validate domain
        if isinstance(domain, str):
            try:
                domain = TranslationDomain(domain)
            except ValueError:
                domain = TranslationDomain.COMMON
        
        # Create cache key
        cache_key = f"{lang.value}:{domain.value}:{message_id}"
        
        # Check cache first
        if cache_key in self._message_cache:
            return self._message_cache[cache_key]
        
        # Get translation
        try:
            translation = self._translations[lang.value][domain.value]
            translated_message = translation.gettext(message_id)
            
            # If translation returns the same as input, try fallback
            if translated_message == message_id and lang != SupportedLanguage.ENGLISH:
                translation = self._translations[SupportedLanguage.ENGLISH.value][domain.value]
                translated_message = translation.gettext(message_id)
            
            # Cache the result
            self._message_cache[cache_key] = translated_message
            return translated_message
            
        except KeyError:
            # Return original message if translation not available
            return message_id
    
    def format_message(self, 
                      message_id: str, 
                      domain: Union[str, TranslationDomain] = TranslationDomain.COMMON,
                      lang: Optional[Union[str, SupportedLanguage]] = None,
                      **kwargs) -> str:
        """
        Get formatted translated message with parameters
        
        Parameters:
        -----------
        message_id : str
            Message identifier to translate
        domain : str or TranslationDomain
            Translation domain
        lang : str or SupportedLanguage, optional
            Language for translation
        **kwargs : dict
            Parameters for message formatting
            
        Returns:
        --------
        str
            Formatted translated message
        """
        message_template = self.get_message(message_id, domain, lang)
        
        try:
            return message_template.format(**kwargs)
        except (KeyError, ValueError) as e:
            # Return template with error info if formatting fails
            return f"{message_template} [Format Error: {e}]"
    
    def translate_dict(self, 
                      data: Dict[str, Any], 
                      domain: Union[str, TranslationDomain] = TranslationDomain.COMMON,
                      lang: Optional[Union[str, SupportedLanguage]] = None) -> Dict[str, Any]:
        """
        Translate all string values in a dictionary
        
        Parameters:
        -----------
        data : dict
            Dictionary with string values to translate
        domain : str or TranslationDomain
            Translation domain
        lang : str or SupportedLanguage, optional
            Language for translation
            
        Returns:
        --------
        dict
            Dictionary with translated values
        """
        if lang is None:
            lang = self.current_language
        
        translated_data = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                translated_data[key] = self.get_message(value, domain, lang)
            elif isinstance(value, dict):
                translated_data[key] = self.translate_dict(value, domain, lang)
            elif isinstance(value, list):
                translated_data[key] = [
                    self.get_message(item, domain, lang) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                translated_data[key] = value
        
        return translated_data
    
    def get_language_info(self, lang: Optional[Union[str, SupportedLanguage]] = None) -> Dict[str, str]:
        """
        Get language information
        
        Parameters:
        -----------
        lang : str or SupportedLanguage, optional
            Language to get info for (current if not specified)
            
        Returns:
        --------
        dict
            Language information
        """
        if lang is None:
            lang = self.current_language
        else:
            lang = self._validate_language(lang)
        
        language_info = {
            SupportedLanguage.ENGLISH: {
                "code": "en",
                "name": "English",
                "native_name": "English",
                "direction": "ltr"
            },
            SupportedLanguage.THAI: {
                "code": "th", 
                "name": "Thai",
                "native_name": "ไทย",
                "direction": "ltr"
            },
            SupportedLanguage.JAPANESE: {
                "code": "ja",
                "name": "Japanese", 
                "native_name": "日本語",
                "direction": "ltr"
            }
        }
        
        return language_info.get(lang, language_info[SupportedLanguage.ENGLISH])
    
    def export_translations_json(self, 
                                domain: Union[str, TranslationDomain],
                                lang: Union[str, SupportedLanguage],
                                output_file: Optional[Path] = None) -> Dict[str, str]:
        """
        Export translations to JSON format
        
        Parameters:
        -----------
        domain : str or TranslationDomain
            Translation domain to export
        lang : str or SupportedLanguage
            Language to export
        output_file : Path, optional
            Output file path (if provided, saves to file)
            
        Returns:
        --------
        dict
            Translation dictionary
        """
        lang = self._validate_language(lang)
        
        if isinstance(domain, str):
            domain = TranslationDomain(domain)
        
        translation = self._translations[lang.value][domain.value]
        
        # Extract all messages from catalog
        translations_dict = {}
        if hasattr(translation, '_catalog'):
            for msgid, msgstr in translation._catalog.items():
                if msgid and msgstr and msgid != msgstr:  # Skip empty and untranslated
                    translations_dict[msgid] = msgstr
        
        # Save to file if specified
        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(translations_dict, f, ensure_ascii=False, indent=2)
        
        return translations_dict
    
    def validate_translations(self) -> Dict[str, Any]:
        """
        Validate translation completeness and consistency
        
        Returns:
        --------
        dict
            Validation report
        """
        report = {
            "languages": {},
            "domains": {},
            "missing_translations": [],
            "statistics": {}
        }
        
        for lang in SupportedLanguage:
            lang_stats = {
                "total_messages": 0,
                "translated_messages": 0,
                "missing_messages": 0,
                "domains": {}
            }
            
            for domain in TranslationDomain:
                translation = self._translations[lang.value][domain.value]
                
                domain_stats = {
                    "available": False,
                    "message_count": 0,
                    "translated_count": 0
                }
                
                if hasattr(translation, '_catalog'):
                    domain_stats["available"] = True
                    domain_stats["message_count"] = len(translation._catalog)
                    
                    # Count translated messages
                    for msgid, msgstr in translation._catalog.items():
                        if msgid and msgstr and msgid != msgstr:
                            domain_stats["translated_count"] += 1
                
                lang_stats["domains"][domain.value] = domain_stats
                lang_stats["total_messages"] += domain_stats["message_count"]
                lang_stats["translated_messages"] += domain_stats["translated_count"]
            
            lang_stats["missing_messages"] = (
                lang_stats["total_messages"] - lang_stats["translated_messages"]
            )
            
            report["languages"][lang.value] = lang_stats
        
        # Overall statistics
        total_msgs = sum(lang["total_messages"] for lang in report["languages"].values())
        translated_msgs = sum(lang["translated_messages"] for lang in report["languages"].values())
        
        report["statistics"] = {
            "total_messages": total_msgs,
            "translated_messages": translated_msgs,
            "translation_coverage": translated_msgs / total_msgs * 100 if total_msgs > 0 else 0
        }
        
        return report


# Global translator instance
_translator_instance: Optional[Translator] = None

def get_translator() -> Translator:
    """Get global translator instance"""
    global _translator_instance
    if _translator_instance is None:
        _translator_instance = Translator()
    return _translator_instance

def set_language(language: Union[str, SupportedLanguage]) -> None:
    """Set global language"""
    translator = get_translator()
    translator.set_language(language)

def get_message(message_id: str, 
               domain: Union[str, TranslationDomain] = TranslationDomain.COMMON,
               lang: Optional[Union[str, SupportedLanguage]] = None) -> str:
    """Get translated message using global translator"""
    translator = get_translator()
    return translator.get_message(message_id, domain, lang)

def format_message(message_id: str, 
                  domain: Union[str, TranslationDomain] = TranslationDomain.COMMON,
                  lang: Optional[Union[str, SupportedLanguage]] = None,
                  **kwargs) -> str:
    """Format translated message using global translator"""
    translator = get_translator()
    return translator.format_message(message_id, domain, lang, **kwargs)

# Convenience functions for specific domains
def get_aci_message(message_id: str, lang: Optional[Union[str, SupportedLanguage]] = None) -> str:
    """Get ACI domain message"""
    return get_message(message_id, TranslationDomain.ACI, lang)

def get_thai_message(message_id: str, lang: Optional[Union[str, SupportedLanguage]] = None) -> str:
    """Get Thai domain message"""
    return get_message(message_id, TranslationDomain.THAI, lang)

def get_common_message(message_id: str, lang: Optional[Union[str, SupportedLanguage]] = None) -> str:
    """Get common domain message"""
    return get_message(message_id, TranslationDomain.COMMON, lang)