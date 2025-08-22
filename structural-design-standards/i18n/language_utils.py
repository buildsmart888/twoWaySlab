"""
Language Utilities Module
=========================

Provides utility functions for language detection, validation, and management
in the structural design standards library.

ยูทิลิตี้สำหรับการจัดการภาษาในไลบรารี่มาตรฐานการออกแบบโครงสร้าง
"""

import re
import locale
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

from .translator import SupportedLanguage, TranslationDomain, get_translator


class LanguageDirection(Enum):
    """Text direction enumeration"""
    LEFT_TO_RIGHT = "ltr"
    RIGHT_TO_LEFT = "rtl"


@dataclass
class LanguageMetadata:
    """Language metadata information"""
    code: str
    name: str
    native_name: str
    direction: LanguageDirection
    locale_codes: List[str]
    decimal_separator: str
    thousands_separator: str
    currency_symbol: str
    date_format: str
    time_format: str


class LanguageDetector:
    """
    Automatic language detection for text content
    """
    
    def __init__(self):
        """Initialize language detector with patterns"""
        self.language_patterns = {
            SupportedLanguage.THAI: [
                r'[\u0E00-\u0E7F]+',  # Thai Unicode range
                r'(?:การ|ที่|ใน|และ|หรือ|เป็น|มี|ของ|จาก)',  # Common Thai words
                r'(?:คอนกรีต|เหล็ก|โครงสร้าง|ออกแบบ|คาน|เสา)',  # Technical Thai terms
            ],
            SupportedLanguage.ENGLISH: [
                r'\b(?:the|and|or|is|are|has|have|from|with|for)\b',  # Common English words
                r'\b(?:concrete|steel|beam|column|design|structure)\b',  # Technical English terms
            ],
            SupportedLanguage.JAPANESE: [
                r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+',  # Japanese Unicode ranges
                r'(?:コンクリート|鋼|梁|柱|設計|構造)',  # Technical Japanese terms
            ]
        }
    
    def detect_language(self, text: str, threshold: float = 0.3) -> Optional[SupportedLanguage]:
        """
        Detect language from text content
        
        Parameters:
        -----------
        text : str
            Text to analyze
        threshold : float
            Minimum confidence threshold (0.0 to 1.0)
            
        Returns:
        --------
        SupportedLanguage or None
            Detected language or None if confidence below threshold
        """
        if not text or not text.strip():
            return None
        
        text = text.lower().strip()
        scores = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0
            total_matches = 0
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                total_matches += len(matches)
                score += len(matches) * len(''.join(matches))
            
            # Normalize score by text length
            if len(text) > 0:
                scores[language] = score / len(text)
            else:
                scores[language] = 0
        
        # Find language with highest score
        if scores:
            best_language = max(scores, key=scores.get)
            if scores[best_language] >= threshold:
                return best_language
        
        return None
    
    def get_confidence_scores(self, text: str) -> Dict[SupportedLanguage, float]:
        """
        Get confidence scores for all languages
        
        Parameters:
        -----------
        text : str
            Text to analyze
            
        Returns:
        --------
        dict
            Confidence scores for each supported language
        """
        if not text or not text.strip():
            return {lang: 0.0 for lang in SupportedLanguage}
        
        text = text.lower().strip()
        scores = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches) * len(''.join(matches))
            
            # Normalize score by text length
            scores[language] = score / len(text) if len(text) > 0 else 0.0
        
        return scores


class LanguageManager:
    """
    Comprehensive language management system
    """
    
    def __init__(self):
        """Initialize language manager"""
        self.detector = LanguageDetector()
        self.translator = get_translator()
        
        # Language metadata
        self.language_metadata = {
            SupportedLanguage.ENGLISH: LanguageMetadata(
                code="en",
                name="English",
                native_name="English",
                direction=LanguageDirection.LEFT_TO_RIGHT,
                locale_codes=["en_US", "en_GB", "en_CA", "en_AU"],
                decimal_separator=".",
                thousands_separator=",",
                currency_symbol="$",
                date_format="%Y-%m-%d",
                time_format="%H:%M:%S"
            ),
            SupportedLanguage.THAI: LanguageMetadata(
                code="th",
                name="Thai",
                native_name="ไทย",
                direction=LanguageDirection.LEFT_TO_RIGHT,
                locale_codes=["th_TH"],
                decimal_separator=".",
                thousands_separator=",",
                currency_symbol="฿",
                date_format="%d/%m/%Y",
                time_format="%H:%M:%S"
            ),
            SupportedLanguage.JAPANESE: LanguageMetadata(
                code="ja",
                name="Japanese",
                native_name="日本語",
                direction=LanguageDirection.LEFT_TO_RIGHT,
                locale_codes=["ja_JP"],
                decimal_separator=".",
                thousands_separator=",",
                currency_symbol="¥",
                date_format="%Y/%m/%d",
                time_format="%H:%M:%S"
            )
        }
    
    def get_system_language(self) -> SupportedLanguage:
        """
        Get system default language
        
        Returns:
        --------
        SupportedLanguage
            System language or English as fallback
        """
        try:
            # Get system locale
            system_locale = locale.getdefaultlocale()[0]
            
            if system_locale:
                # Extract language code
                lang_code = system_locale.split('_')[0].lower()
                
                # Map to supported languages
                for language in SupportedLanguage:
                    if language.value == lang_code:
                        return language
        
        except Exception:
            pass
        
        # Default to English
        return SupportedLanguage.ENGLISH
    
    def get_language_from_env(self) -> Optional[SupportedLanguage]:
        """
        Get language from environment variables
        
        Returns:
        --------
        SupportedLanguage or None
            Language from environment or None if not found
        """
        # Check common environment variables
        env_vars = ['LANG', 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES']
        
        for var in env_vars:
            value = os.environ.get(var)
            if value:
                # Extract language code
                lang_code = value.split('_')[0].split('.')[0].lower()
                
                # Map to supported languages
                for language in SupportedLanguage:
                    if language.value == lang_code:
                        return language
        
        return None
    
    def get_metadata(self, language: SupportedLanguage) -> LanguageMetadata:
        """
        Get language metadata
        
        Parameters:
        -----------
        language : SupportedLanguage
            Language to get metadata for
            
        Returns:
        --------
        LanguageMetadata
            Language metadata
        """
        return self.language_metadata.get(language, self.language_metadata[SupportedLanguage.ENGLISH])
    
    def format_number(self, number: Union[int, float], language: SupportedLanguage) -> str:
        """
        Format number according to language conventions
        
        Parameters:
        -----------
        number : int or float
            Number to format
        language : SupportedLanguage
            Language for formatting
            
        Returns:
        --------
        str
            Formatted number string
        """
        metadata = self.get_metadata(language)
        
        # Convert to string with appropriate decimal places
        if isinstance(number, float):
            number_str = f"{number:.2f}"
        else:
            number_str = str(number)
        
        # Split into integer and decimal parts
        if '.' in number_str:
            integer_part, decimal_part = number_str.split('.')
        else:
            integer_part, decimal_part = number_str, ""
        
        # Add thousands separators
        if len(integer_part) > 3:
            # Reverse, group by 3, reverse back
            reversed_int = integer_part[::-1]
            grouped = [reversed_int[i:i+3] for i in range(0, len(reversed_int), 3)]
            integer_part = metadata.thousands_separator.join(grouped)[::-1]
        
        # Combine with decimal separator
        if decimal_part:
            return f"{integer_part}{metadata.decimal_separator}{decimal_part}"
        else:
            return integer_part
    
    def validate_language_support(self, language: Union[str, SupportedLanguage]) -> bool:
        """
        Validate if language is supported
        
        Parameters:
        -----------
        language : str or SupportedLanguage
            Language to validate
            
        Returns:
        --------
        bool
            True if language is supported
        """
        try:
            if isinstance(language, str):
                SupportedLanguage(language)
            return True
        except ValueError:
            return False
    
    def get_available_locales(self, language: SupportedLanguage) -> List[str]:
        """
        Get available locale codes for language
        
        Parameters:
        -----------
        language : SupportedLanguage
            Language to get locales for
            
        Returns:
        --------
        list
            Available locale codes
        """
        metadata = self.get_metadata(language)
        return metadata.locale_codes.copy()
    
    def auto_detect_and_set(self, text: str, threshold: float = 0.3) -> SupportedLanguage:
        """
        Auto-detect language from text and set as current
        
        Parameters:
        -----------
        text : str
            Text to analyze for language detection
        threshold : float
            Confidence threshold for detection
            
        Returns:
        --------
        SupportedLanguage
            Detected and set language
        """
        detected_language = self.detector.detect_language(text, threshold)
        
        if detected_language:
            self.translator.set_language(detected_language)
            return detected_language
        else:
            # Fall back to system language
            system_lang = self.get_system_language()
            self.translator.set_language(system_lang)
            return system_lang
    
    def get_translation_status(self) -> Dict[str, Dict[str, float]]:
        """
        Get translation completeness status for all languages
        
        Returns:
        --------
        dict
            Translation status with completion percentages
        """
        validation_report = self.translator.validate_translations()
        
        status = {}
        for lang_code, lang_data in validation_report["languages"].items():
            status[lang_code] = {
                "overall_completion": (
                    lang_data["translated_messages"] / lang_data["total_messages"] * 100
                    if lang_data["total_messages"] > 0 else 0
                ),
                "domains": {}
            }
            
            for domain, domain_data in lang_data["domains"].items():
                completion = (
                    domain_data["translated_count"] / domain_data["message_count"] * 100
                    if domain_data["message_count"] > 0 else 0
                )
                status[lang_code]["domains"][domain] = completion
        
        return status


# Global language manager instance
_language_manager_instance: Optional[LanguageManager] = None

def get_language_manager() -> LanguageManager:
    """Get global language manager instance"""
    global _language_manager_instance
    if _language_manager_instance is None:
        _language_manager_instance = LanguageManager()
    return _language_manager_instance

def detect_language(text: str, threshold: float = 0.3) -> Optional[SupportedLanguage]:
    """Detect language from text using global detector"""
    manager = get_language_manager()
    return manager.detector.detect_language(text, threshold)

def get_system_language() -> SupportedLanguage:
    """Get system language using global manager"""
    manager = get_language_manager()
    return manager.get_system_language()

def format_number(number: Union[int, float], language: Optional[SupportedLanguage] = None) -> str:
    """Format number according to language conventions"""
    manager = get_language_manager()
    if language is None:
        language = manager.translator.get_current_language()
    return manager.format_number(number, language)

def auto_detect_and_set_language(text: str, threshold: float = 0.3) -> SupportedLanguage:
    """Auto-detect and set language from text"""
    manager = get_language_manager()
    return manager.auto_detect_and_set(text, threshold)