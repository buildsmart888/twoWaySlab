#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

"""
Enhanced Report Generation System
Multi-language PDF report generation with Thailand building code support

@author: Enhanced by AI Assistant
@date: 2024
"""

import os
import sys
import datetime

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

import linecache
import config
import i18n
import units

class EnhancedReport:
    """
    Enhanced report generator with multi-language and multi-building-code support
    """
    
    def __init__(self):
        # Initialize enhanced systems
        self.config = config.config
        self.i18n = i18n.i18n
        self.unit_converter = units.unit_converter
        
        # Font setup
        self.setup_fonts()
        
        # Page setup
        self.page_width, self.page_height = A4
        self.margin_left = 25 * mm
        self.margin_right = 25 * mm
        self.margin_top = 25 * mm
        self.margin_bottom = 25 * mm
        
        # Available width and height
        self.content_width = self.page_width - self.margin_left - self.margin_right
        self.content_height = self.page_height - self.margin_top - self.margin_bottom

    def setup_fonts(self):
        """Setup fonts for different languages"""
        try:
            # Japanese font (existing)
            self.japanese_font = "GenShinGothic"
            japanese_font_path = "./fonts/GenShinGothic-Monospace-Medium.ttf"
            if os.path.exists(japanese_font_path):
                pdfmetrics.registerFont(TTFont(self.japanese_font, japanese_font_path))
                self.has_japanese_font = True
            else:
                self.has_japanese_font = False
                print("Warning: Japanese font not found")
            
            # For Thai text, we'll try to use a Unicode font or fall back to built-in
            self.thai_font = "Helvetica"  # Fallback - should ideally use Thai font
            self.english_font = "Helvetica"
            
            # Default font based on current language
            current_lang = self.i18n.get_current_language()
            if current_lang == 'ja' and self.has_japanese_font:
                self.default_font = self.japanese_font
            elif current_lang == 'th':
                self.default_font = self.thai_font
            else:
                self.default_font = self.english_font
                
        except Exception as e:
            print(f"Font setup error: {e}")
            self.default_font = "Helvetica"
            self.has_japanese_font = False

    def get_font_for_language(self, language=None):
        """Get appropriate font for language"""
        if language is None:
            language = self.i18n.get_current_language()
        
        if language == 'ja' and self.has_japanese_font:
            return self.japanese_font
        elif language == 'th':
            return self.thai_font
        else:
            return self.english_font

    def create_enhanced_report(self, filename, data_list):
        """
        Create enhanced PDF report with current language and building code
        
        Args:
            filename: Output PDF filename
            data_list: List of calculation data
        """
        try:
            c = canvas.Canvas(filename, pagesize=A4)
            
            # Report header
            self.draw_report_header(c)
            
            # Process each data item
            for index, data in enumerate(data_list):
                if index > 0:
                    c.showPage()  # New page for each project
                    self.draw_report_header(c)
                
                self.draw_project_data(c, data, index)
            
            c.save()
            print(f"Enhanced report saved: {filename}")
            
        except Exception as e:
            print(f"Error creating enhanced report: {e}")
            raise

    def draw_report_header(self, c):
        """Draw report header with i18n support"""
        try:
            font = self.get_font_for_language()
            
            # Title
            c.setFont(font, 16)
            title = self.i18n.t('app_title')
            title_width = c.stringWidth(title, font, 16)
            x_center = (self.page_width - title_width) / 2
            c.drawString(x_center, self.page_height - 40*mm, title)
            
            # Building code info
            c.setFont(font, 10)
            building_code = self.config.get_building_code()
            code_info = self.config.get_building_code_info(building_code)
            code_text = f"{self.i18n.t('building_code', building_code=code_info['name'])}"
            c.drawString(self.margin_left, self.page_height - 55*mm, code_text)
            
            # Date
            date_text = f"{self.i18n.t('date')}: {datetime.datetime.now().strftime(self.i18n.get_date_format())}"
            c.drawString(self.margin_left, self.page_height - 65*mm, date_text)
            
            # Line separator
            c.line(self.margin_left, self.page_height - 70*mm, 
                  self.page_width - self.margin_right, self.page_height - 70*mm)
            
        except Exception as e:
            print(f"Error drawing report header: {e}")

    def draw_project_data(self, c, data, index):
        """Draw project data with enhanced formatting"""
        try:
            font = self.get_font_for_language()
            
            # Starting position
            y_start = self.page_height - 90*mm
            y_shift = -180 * index if index == 0 else 0
            
            # Project title
            c.setFont(font, 12)
            title = data[0] if len(data) > 0 else "Project"
            subtitle = data[1] if len(data) > 1 else ""
            
            c.drawString(self.margin_left, self.ypos(0, y_shift, y_start), 
                        f"{self.i18n.t('input_labels.title')}: {title}")
            c.drawString(self.margin_left, self.ypos(1, y_shift, y_start), 
                        f"{self.i18n.t('input_labels.subtitle')}: {subtitle}")
            
            # Slab conditions
            self.draw_slab_conditions(c, data, y_shift, y_start)
            
            # Results
            self.draw_calculation_results(c, data, y_shift, y_start)
            
            # Building code specific information
            self.draw_building_code_info(c, data, y_shift, y_start)
            
        except Exception as e:
            print(f"Error drawing project data: {e}")

    def draw_slab_conditions(self, c, data, y_shift, y_start):
        """Draw slab condition information"""
        try:
            font = self.get_font_for_language()
            c.setFont(font, 9)
            
            # Extract slab data
            lx = f"{float(data[2]):.2f}" if len(data) > 2 else "0"
            ly = f"{float(data[3]):.2f}" if len(data) > 3 else "0"
            t = data[4] if len(data) > 4 else "0"
            dt = data[5] if len(data) > 5 else "0"
            w = data[6] if len(data) > 6 else "0"
            fc = data[8] if len(data) > 8 else "0"
            gamma = data[9] if len(data) > 9 else "0"
            ft = data[39] if len(data) > 39 else "0"
            
            # Get units for current system
            length_unit = self.unit_converter.get_unit_for_quantity('length')
            stress_unit = self.unit_converter.get_unit_for_quantity('stress')
            load_unit = self.unit_converter.get_unit_for_quantity('load')
            density_unit = self.unit_converter.get_unit_for_quantity('density')
            
            # Design conditions section
            section_y = self.ypos(3, y_shift, y_start)
            c.setFont(font, 10)
            c.drawString(self.margin_left, section_y, 
                        self.i18n.t('sections.design_conditions'))
            
            c.setFont(font, 9)
            
            # Dimensions
            c.drawString(self.margin_left + 20*mm, self.ypos(4, y_shift, y_start),
                        f"{self.i18n.t('input_labels.lx')} = {lx} {length_unit}")
            c.drawString(self.margin_left + 60*mm, self.ypos(4, y_shift, y_start),
                        f"{self.i18n.t('input_labels.ly')} = {ly} {length_unit}")
            
            # Thickness
            c.drawString(self.margin_left + 20*mm, self.ypos(5, y_shift, y_start),
                        f"{self.i18n.t('input_labels.thickness')} = {t} mm")
            c.drawString(self.margin_left + 60*mm, self.ypos(5, y_shift, y_start),
                        f"{self.i18n.t('input_labels.effective_depth')} = {dt} mm")
            
            # Material properties
            c.drawString(self.margin_left + 20*mm, self.ypos(6, y_shift, y_start),
                        f"{self.i18n.t('input_labels.concrete_strength')} = {fc} {stress_unit}")
            c.drawString(self.margin_left + 60*mm, self.ypos(6, y_shift, y_start),
                        f"{self.i18n.t('input_labels.steel_strength')} = {ft} {stress_unit}")
            
            # Load and density
            c.drawString(self.margin_left + 20*mm, self.ypos(7, y_shift, y_start),
                        f"{self.i18n.t('input_labels.load')} = {w} {load_unit}")
            c.drawString(self.margin_left + 60*mm, self.ypos(7, y_shift, y_start),
                        f"{self.i18n.t('input_labels.unit_weight')} = {gamma} {density_unit}")
            
        except Exception as e:
            print(f"Error drawing slab conditions: {e}")

    def draw_calculation_results(self, c, data, y_shift, y_start):
        """Draw calculation results"""
        try:
            font = self.get_font_for_language()
            
            # Results section header
            section_y = self.ypos(9, y_shift, y_start)
            c.setFont(font, 10)
            c.drawString(self.margin_left, section_y, 
                        self.i18n.t('sections.calculation_results'))
            
            # Create results table
            self.draw_results_table(c, data, y_shift, y_start)
            
        except Exception as e:
            print(f"Error drawing calculation results: {e}")

    def draw_results_table(self, c, data, y_shift, y_start):
        """Draw results in table format"""
        try:
            font = self.get_font_for_language()
            c.setFont(font, 8)
            
            # Table headers
            headers = [
                "",
                self.i18n.t('rebar_positions.short_end'),
                self.i18n.t('rebar_positions.short_center'),
                self.i18n.t('rebar_positions.long_end'),
                self.i18n.t('rebar_positions.long_center')
            ]
            
            # Extract results data
            mx1 = data[23] if len(data) > 23 else "0"
            mx2 = data[24] if len(data) > 24 else "0"
            my1 = data[25] if len(data) > 25 else "0"
            my2 = data[26] if len(data) > 26 else "0"
            
            atx1 = data[27] if len(data) > 27 else "0"
            atx2 = data[28] if len(data) > 28 else "0"
            aty1 = data[29] if len(data) > 29 else "0"
            aty2 = data[30] if len(data) > 30 else "0"
            
            sfx1 = data[33] if len(data) > 33 else "0"
            sfx2 = data[34] if len(data) > 34 else "0"
            sfy1 = data[35] if len(data) > 35 else "0"
            sfy2 = data[36] if len(data) > 36 else "0"
            
            # Rebar info
            lx1_bar = data[19] if len(data) > 19 else ""
            lx1_pitch = data[10] if len(data) > 10 else ""
            lx2_bar = data[20] if len(data) > 20 else ""
            lx2_pitch = data[11] if len(data) > 11 else ""
            ly1_bar = data[21] if len(data) > 21 else ""
            ly1_pitch = data[12] if len(data) > 12 else ""
            ly2_bar = data[22] if len(data) > 22 else ""
            ly2_pitch = data[13] if len(data) > 13 else ""
            
            # Table data
            table_data = [
                headers,
                [f"{self.i18n.t('output_labels.moment')} (kN.m/m)", mx1, mx2, my1, my2],
                [f"{self.i18n.t('output_labels.required_area')} (mm²)", atx1, atx2, aty1, aty2],
                [self.i18n.t('output_labels.reinforcement_label'), 
                 f"{lx1_bar}@{lx1_pitch}", f"{lx2_bar}@{lx2_pitch}", 
                 f"{ly1_bar}@{ly1_pitch}", f"{ly2_bar}@{ly2_pitch}"],
                [self.i18n.t('output_labels.safety_factor'), sfx1, sfx2, sfy1, sfy2]
            ]
            
            # Draw table manually (simplified version)
            table_y = self.ypos(11, y_shift, y_start)
            row_height = 15
            col_widths = [40*mm, 30*mm, 30*mm, 30*mm, 30*mm]
            
            for row_idx, row in enumerate(table_data):
                y = table_y - row_idx * row_height
                x = self.margin_left
                
                for col_idx, cell in enumerate(row):
                    if row_idx == 0:  # Header
                        c.setFont(font, 9)
                    else:
                        c.setFont(font, 8)
                    
                    c.drawString(x, y, str(cell))
                    x += col_widths[col_idx]
            
            # Deflection results
            deflection_y = table_y - len(table_data) * row_height - 20
            c.setFont(font, 9)
            
            defl = data[37] if len(data) > 37 else "0"
            defl_ratio = data[38] if len(data) > 38 else "0"
            
            c.drawString(self.margin_left, deflection_y,
                        f"{self.i18n.t('output_labels.deflection')}: {defl} mm")
            c.drawString(self.margin_left + 60*mm, deflection_y,
                        f"{self.i18n.t('output_labels.deflection_ratio')}: {defl_ratio}")
            
        except Exception as e:
            print(f"Error drawing results table: {e}")

    def draw_building_code_info(self, c, data, y_shift, y_start):
        """Draw building code specific information"""
        try:
            font = self.get_font_for_language()
            c.setFont(font, 8)
            
            # Building code information
            info_y = self.ypos(20, y_shift, y_start)
            building_code = self.config.get_building_code()
            code_info = self.config.get_building_code_info(building_code)
            
            c.drawString(self.margin_left, info_y,
                        f"{self.i18n.t('building_code_info')}: {code_info['description']}")
            
            # Safety factors
            concrete_sf = self.config.get_safety_factor('concrete')
            steel_sf = self.config.get_safety_factor('steel')
            
            c.drawString(self.margin_left, info_y - 10,
                        f"{self.i18n.t('safety_factors')}: "
                        f"{self.i18n.t('concrete')} = {concrete_sf}, "
                        f"{self.i18n.t('steel')} = {steel_sf}")
            
        except Exception as e:
            print(f"Error drawing building code info: {e}")

    def ypos(self, line_number, y_shift=0, y_start=None):
        """Calculate Y position for line"""
        if y_start is None:
            y_start = self.page_height - 90*mm
        
        line_height = 12  # mm
        return y_start + y_shift - line_number * line_height

    def create_multilingual_report(self, filename, data_list, languages=None):
        """Create report in multiple languages"""
        if languages is None:
            languages = [self.i18n.get_current_language()]
        
        for lang in languages:
            # Set language
            original_lang = self.i18n.get_current_language()
            self.i18n.set_language(lang)
            
            # Update font
            self.default_font = self.get_font_for_language(lang)
            
            # Create report
            lang_filename = f"{filename.replace('.pdf', '')}_{lang}.pdf"
            self.create_enhanced_report(lang_filename, data_list)
            
            # Restore original language
            self.i18n.set_language(original_lang)

# Global enhanced report instance
enhanced_report = EnhancedReport()

# Convenience functions
def create_enhanced_report(filename, data_list):
    """Create enhanced report"""
    return enhanced_report.create_enhanced_report(filename, data_list)

def create_multilingual_report(filename, data_list, languages=None):
    """Create multilingual report"""
    return enhanced_report.create_multilingual_report(filename, data_list, languages)

# Test the enhanced report system
if __name__ == "__main__":
    print("=== Enhanced Report System Test ===")
    
    # Test data
    test_data = [
        "Test Project", "Sample Slab", "4.0", "6.0", "150", "40", "10.0", "2.0",
        "21", "24", "200", "200", "200", "200", "1", "", "", "", "", "",
        "DB16", "DB16", "DB16", "DB16", "50.5", "50.5", "45.2", "45.2",
        "1256", "1256", "1130", "1130", "127", "25.4", "1.2", "1.2", "1.1", "1.1",
        "8.5", "1/470", "390"
    ]
    
    try:
        # Test single language report
        enhanced_report.create_enhanced_report("test_enhanced_report.pdf", [test_data])
        print("✓ Enhanced report created successfully")
        
        # Test multilingual report
        enhanced_report.create_multilingual_report("test_multilingual", [test_data], ['en', 'th'])
        print("✓ Multilingual reports created successfully")
        
    except Exception as e:
        print(f"✗ Report test failed: {e}")