#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-
#
# Enhanced twoWaySlab Application with Thailand Building Code Support
# Integrates all new features: i18n, config management, unit conversion, validation
#

import numpy, matplotlib
if matplotlib.__version__ < '2.2':
    raise ValueError("Minimum Matplotlib version required: 2.2")

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

# Enhanced imports
import config
import i18n
import units
import validation
import thiRc
import aijRc
import higashi
import report

import wx
import os
import csv
import linecache

# Read from glade
import gui

class EnhancedMyFrame2(gui.MyFrame2):
    """
    Enhanced version of MyFrame2 with multi-language support,
    building code selection, and improved validation
    """

    def __init__(self, *args, **kwds):
        # Initialize enhanced systems first
        self.setup_enhanced_systems()
        
        # Call parent constructor
        super().__init__(*args, **kwds)
        
        # Setup enhanced UI
        self.setup_enhanced_ui()
        
    def setup_enhanced_systems(self):
        """Initialize all enhanced systems"""
        # Load configuration
        self.config = config.config
        
        # Setup internationalization
        self.i18n = i18n.i18n
        self.i18n.update_from_config()
        
        # Setup unit converter
        self.unit_converter = units.unit_converter
        
        # Setup validator
        self.validator = validation.validator
        
        # Load current material based on config
        self.material = self.config.get_material_instance()
        
        print(f"Enhanced systems initialized:")
        print(f"  Building code: {self.config.get_building_code()}")
        print(f"  Language: {self.config.get_language()}")
        print(f"  Material class: {type(self.material)}")

    def setup_enhanced_ui(self):
        """Setup enhanced UI elements"""
        try:
            # Update window title with i18n
            app_title = self.i18n.t('app_title')
            self.SetTitle(app_title)
            
            # Add building code selection
            self.add_building_code_selector()
            
            # Add language selector
            self.add_language_selector()
            
            # Update labels with i18n
            self.update_ui_labels()
            
            # Update boundary condition choices
            self.update_boundary_conditions()
            
            # Update rebar choices based on building code
            self.update_rebar_choices()
            
        except Exception as e:
            print(f"Warning: Enhanced UI setup failed: {e}")

    def add_building_code_selector(self):
        """Add building code selection to UI"""
        try:
            # Create building code selection panel
            if hasattr(self, 'panel_10'):  # Main input panel
                # Add building code choice
                building_codes = self.config.get_available_codes()
                code_names = [self.config.get_building_code_info(code)['name'] for code in building_codes]
                
                self.choice_building_code = wx.Choice(self.panel_10, choices=code_names)
                current_code = self.config.get_building_code()
                current_index = building_codes.index(current_code)
                self.choice_building_code.SetSelection(current_index)
                
                # Bind event
                self.Bind(wx.EVT_CHOICE, self.OnBuildingCodeChange, self.choice_building_code)
                
                print("Building code selector added successfully")
        except Exception as e:
            print(f"Failed to add building code selector: {e}")

    def add_language_selector(self):
        """Add language selection to UI"""
        try:
            if hasattr(self, 'panel_10'):
                # Language selection
                languages = self.i18n.get_available_languages()
                lang_names = {'en': 'English', 'ja': '日本語', 'th': 'ไทย'}
                lang_display = [lang_names.get(lang, lang) for lang in languages]
                
                self.choice_language = wx.Choice(self.panel_10, choices=lang_display)
                current_lang = self.i18n.get_current_language()
                if current_lang in languages:
                    current_index = languages.index(current_lang)
                    self.choice_language.SetSelection(current_index)
                
                # Bind event
                self.Bind(wx.EVT_CHOICE, self.OnLanguageChange, self.choice_language)
                
                print("Language selector added successfully")
        except Exception as e:
            print(f"Failed to add language selector: {e}")

    def update_ui_labels(self):
        """Update all UI labels with i18n"""
        try:
            # Update button labels
            if hasattr(self, 'button_7'):  # Calculate button
                self.button_7.SetLabel(self.i18n.t('buttons.calculate'))
            
            if hasattr(self, 'button_6'):  # Store button
                self.button_6.SetLabel(self.i18n.t('buttons.store'))
            
            # Update other buttons as needed
            print("UI labels updated with i18n")
        except Exception as e:
            print(f"Failed to update UI labels: {e}")

    def update_boundary_conditions(self):
        """Update boundary condition choices with i18n"""
        try:
            if hasattr(self, 'combo_box_bound'):
                boundary_types = self.i18n.t('boundary_types')
                if isinstance(boundary_types, list):
                    self.combo_box_bound.Clear()
                    for boundary_type in boundary_types:
                        self.combo_box_bound.Append(boundary_type)
                    print("Boundary conditions updated with i18n")
        except Exception as e:
            print(f"Failed to update boundary conditions: {e}")

    def update_rebar_choices(self):
        """Update rebar choices based on current building code"""
        try:
            current_code = self.config.get_building_code()
            
            if current_code == 'thai':
                # Thai rebar choices per มยผ. 1103
                rebar_choices = ['DB10', 'DB12', 'DB20', 'DB25', 'DB32', 'DB36', 'DB40', 'RB6', 'RB9']
            else:  # Japanese or others
                rebar_choices = ['D10', 'D13', 'D16', 'D19', 'D22', 'D25', 'D29', 'D32']
            
            # Update all rebar combo boxes
            rebar_combos = [
                'combo_box_lx1bar', 'combo_box_lx2bar', 
                'combo_box_ly1bar', 'combo_box_ly2bar'
            ]
            
            for combo_name in rebar_combos:
                if hasattr(self, combo_name):
                    combo = getattr(self, combo_name)
                    combo.Clear()
                    for choice in rebar_choices:
                        combo.Append(choice)
                    combo.SetSelection(2)  # Default to middle choice
            
            print(f"Rebar choices updated for {current_code} building code")
        except Exception as e:
            print(f"Failed to update rebar choices: {e}")

    def OnBuildingCodeChange(self, event):
        """Handle building code change"""
        try:
            selection = event.GetSelection()
            building_codes = self.config.get_available_codes()
            
            if 0 <= selection < len(building_codes):
                new_code = building_codes[selection]
                
                # Update configuration
                self.config.set_building_code(new_code)
                
                # Update material instance
                self.material = self.config.get_material_instance()
                
                # Update language to match building code
                self.i18n.update_from_config()
                
                # Update UI elements
                self.update_ui_labels()
                self.update_boundary_conditions()
                self.update_rebar_choices()
                
                # Clear previous calculations
                self.Clear_R()
                
                # Show message
                code_info = self.config.get_building_code_info(new_code)
                message = f"Building code changed to: {code_info['name']}"
                wx.MessageBox(message, "Building Code Changed", wx.OK | wx.ICON_INFORMATION)
                
                print(f"Building code changed to: {new_code}")
                
        except Exception as e:
            wx.MessageBox(f"Error changing building code: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def OnLanguageChange(self, event):
        """Handle language change"""
        try:
            selection = event.GetSelection()
            languages = self.i18n.get_available_languages()
            
            if 0 <= selection < len(languages):
                new_language = languages[selection]
                
                # Update i18n
                self.i18n.set_language(new_language)
                
                # Update config
                self.config.set_language(new_language)
                
                # Update UI
                self.update_ui_labels()
                self.update_boundary_conditions()
                
                print(f"Language changed to: {new_language}")
                
        except Exception as e:
            wx.MessageBox(f"Error changing language: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def OnChangeBound(self, event):
        """Enhanced boundary condition change with validation"""
        try:
            IdBound = self.combo_box_bound.GetSelection()
            
            # Validate boundary condition
            validation_result = self.validator.validate_boundary_condition(str(IdBound + 1))
            if not validation_result.is_valid:
                wx.MessageBox(validation_result.error_message, 
                            self.i18n.t('messages.boundary_error'), 
                            wx.OK | wx.ICON_ERROR)
                return
            
            # Original boundary condition logic
            image_paths = {
                0: "./images/4sideFix.jpg", 1: "./images/4sideFix.jpg",
                2: "./images/m3_1.jpg", 3: "./images/m3_2.jpg",
                4: "./images/m2.jpg", 5: "./images/m4pin.jpg",
                6: "./images/m3_1pin.jpg", 7: "./images/m3-1pin2.jpg",
                8: "./images/m2_2pin.jpg", 9: "./images/m2_2pin2.jpg",
                10: "./images/m2_2pin3.jpg", 11: "./images/m1-3pin1.jpg",
                12: "./images/m1-3pin2.jpg"
            }
            
            image_data = image_paths.get(IdBound, "./images/4sideFix.jpg")
            
            if os.path.exists(image_data):
                image = wx.Image(image_data)
                image = image.Scale(150, 150, wx.IMAGE_QUALITY_BICUBIC)
                bitmap = image.ConvertToBitmap()
                wx.StaticBitmap(self.panel_bound, -1, bitmap, pos=(0, 0))
            else:
                print(f"Warning: Image file not found: {image_data}")
            
            # Clear results
            self.Clear_R()
            
        except Exception as e:
            wx.MessageBox(f"Error changing boundary condition: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def OnCal(self, event):
        """Enhanced calculation with comprehensive validation and error handling"""
        try:
            # Collect all inputs
            inputs = self.collect_inputs()
            
            # Validate all inputs
            current_code = self.config.get_building_code()
            validation_results = self.validator.validate_all_inputs(inputs, current_code)
            
            # Check validation results
            all_valid, errors, warnings = self.validator.get_validation_summary(validation_results)
            
            # Show errors if any
            if not all_valid:
                error_message = "\\n".join(errors)
                wx.MessageBox(error_message, 
                            self.i18n.t('messages.input_error'), 
                            wx.OK | wx.ICON_ERROR)
                return
            
            # Show warnings if any
            if warnings:
                warning_message = "\\n".join(warnings)
                result = wx.MessageBox(warning_message + "\\n\\nContinue with calculation?",
                                     "Warnings", 
                                     wx.YES_NO | wx.ICON_WARNING)
                if result != wx.YES:
                    return
            
            # Perform calculation with validated inputs
            self.perform_enhanced_calculation(validation_results)
            
        except Exception as e:
            wx.MessageBox(f"Calculation error: {e}", "Calculation Error", wx.OK | wx.ICON_ERROR)
            print(f"Calculation error: {e}")

    def collect_inputs(self):
        """Collect all input values for validation"""
        inputs = {}
        
        try:
            inputs['title'] = self.text_ctrl_title.GetValue()
            inputs['subtitle'] = self.text_ctrl_subtitle.GetValue()
            inputs['lx'] = self.text_ctrl_lx.GetValue()
            inputs['ly'] = self.text_ctrl_ly.GetValue()
            inputs['thickness'] = self.text_ctrl_t.GetValue()
            inputs['effective_depth'] = self.text_ctrl_dt.GetValue()
            inputs['load'] = self.text_ctrl_w.GetValue()
            inputs['concrete_strength'] = self.text_ctrl_fc.GetValue()
            inputs['steel_strength'] = self.text_ctrl_ft.GetValue()
            inputs['unit_weight'] = self.text_ctrl_gamma.GetValue()
            inputs['creep'] = self.text_ctrl_creep.GetValue()
            inputs['boundary_condition'] = str(self.combo_box_bound.GetSelection() + 1)
            
            # Rebar information
            inputs['lx1_bar'] = self.combo_box_lx1bar.GetStringSelection()
            inputs['lx1_pitch'] = self.text_ctrl_lx1Pitch.GetValue()
            inputs['lx2_bar'] = self.combo_box_lx2bar.GetStringSelection()
            inputs['lx2_pitch'] = self.text_ctrl_lx2Pitch.GetValue()
            inputs['ly1_bar'] = self.combo_box_ly1bar.GetStringSelection()
            inputs['ly1_pitch'] = self.text_ctrl_ly1Pitch.GetValue()
            inputs['ly2_bar'] = self.combo_box_ly2bar.GetStringSelection()
            inputs['ly2_pitch'] = self.text_ctrl_ly2Pitch.GetValue()
            
        except Exception as e:
            print(f"Error collecting inputs: {e}")
        
        return inputs

    def perform_enhanced_calculation(self, validation_results):
        """Perform calculation using validated inputs"""
        try:
            # Extract validated values
            lx = validation_results['lx'].value
            ly = validation_results['ly'].value
            t = validation_results['thickness'].value
            dt = float(self.text_ctrl_dt.GetValue())
            w = validation_results['load'].value
            fc = validation_results['concrete_strength'].value
            gamma = validation_results['unit_weight'].value
            creep = validation_results['creep'].value
            bound_id = validation_results['boundary_condition'].value
            
            # Get material properties using current building code
            ec = self.material.Ec(fc, gamma)
            nu = 0.2  # Poisson's ratio
            
            # Perform calculation using Higashi method
            higashi_calc = higashi.Higashi()
            
            # Calculate moments and deflection
            mx1, mx2, my1, my2, deflection = higashi_calc.solve(
                bound_id, lx, ly, t, w, creep, ec, nu, 5, 5
            )
            
            # Calculate required reinforcement
            self.calculate_reinforcement(mx1, mx2, my1, my2, dt, fc)
            
            # Display results with proper units and formatting
            self.display_enhanced_results(mx1, mx2, my1, my2, deflection, lx)
            
            # Success message
            wx.MessageBox(self.i18n.t('messages.calculation_complete'), 
                         "Success", wx.OK | wx.ICON_INFORMATION)
            
        except Exception as e:
            raise Exception(f"Calculation failed: {e}")

    def calculate_reinforcement(self, mx1, mx2, my1, my2, dt, fc):
        """Calculate required reinforcement areas"""
        try:
            # Simplified reinforcement calculation
            # This is a basic implementation - should be enhanced with proper design equations
            
            k = 0.85  # Concrete stress block factor
            fy = float(self.text_ctrl_ft.GetValue())
            
            # Calculate required areas (simplified)
            atx1 = abs(mx1 * 1000000) / (0.9 * fy * (dt - 0.4 * dt))  # mm²
            atx2 = abs(mx2 * 1000000) / (0.9 * fy * (dt - 0.4 * dt))
            aty1 = abs(my1 * 1000000) / (0.9 * fy * (dt - 0.4 * dt))
            aty2 = abs(my2 * 1000000) / (0.9 * fy * (dt - 0.4 * dt))
            
            # Get actual reinforcement areas
            lx1_bar = self.combo_box_lx1bar.GetStringSelection()
            lx1_pitch = float(self.text_ctrl_lx1Pitch.GetValue())
            asx1 = self.material.Ra_p(lx1_bar, lx1_pitch)
            
            lx2_bar = self.combo_box_lx2bar.GetStringSelection()
            lx2_pitch = float(self.text_ctrl_lx2Pitch.GetValue())
            asx2 = self.material.Ra_p(lx2_bar, lx2_pitch)
            
            ly1_bar = self.combo_box_ly1bar.GetStringSelection()
            ly1_pitch = float(self.text_ctrl_ly1Pitch.GetValue())
            asy1 = self.material.Ra_p(ly1_bar, ly1_pitch)
            
            ly2_bar = self.combo_box_ly2bar.GetStringSelection()
            ly2_pitch = float(self.text_ctrl_ly2Pitch.GetValue())
            asy2 = self.material.Ra_p(ly2_bar, ly2_pitch)
            
            # Calculate safety factors
            sfx1 = asx1 / atx1 if atx1 > 0 else 999
            sfx2 = asx2 / atx2 if atx2 > 0 else 999
            sfy1 = asy1 / aty1 if aty1 > 0 else 999
            sfy2 = asy2 / aty2 if aty2 > 0 else 999
            
            # Store results for display
            self.reinforcement_results = {
                'atx1': atx1, 'atx2': atx2, 'aty1': aty1, 'aty2': aty2,
                'sfx1': sfx1, 'sfx2': sfx2, 'sfy1': sfy1, 'sfy2': sfy2
            }
            
        except Exception as e:
            print(f"Reinforcement calculation error: {e}")
            self.reinforcement_results = {}

    def display_enhanced_results(self, mx1, mx2, my1, my2, deflection, span):
        """Display results with proper formatting and units"""
        try:
            precision = self.config.get_precision('moment')
            
            # Format moments with units
            current_system = self.unit_converter.get_current_system()
            moment_unit = self.unit_converter.get_unit_for_quantity('moment')
            
            # Display moments
            self.text_ctrl_mx1.SetValue(f"{abs(mx1):.{precision}f}")
            self.text_ctrl_mx2.SetValue(f"{mx2:.{precision}f}")
            self.text_ctrl_my1.SetValue(f"{abs(my1):.{precision}f}")
            self.text_ctrl_my2.SetValue(f"{my2:.{precision}f}")
            
            # Display reinforcement if calculated
            if hasattr(self, 'reinforcement_results'):
                results = self.reinforcement_results
                self.text_ctrl_atx1.SetValue(f"{results.get('atx1', 0):.0f}")
                self.text_ctrl_atx2.SetValue(f"{results.get('atx2', 0):.0f}")
                self.text_ctrl_aty1.SetValue(f"{results.get('aty1', 0):.0f}")
                self.text_ctrl_aty2.SetValue(f"{results.get('aty2', 0):.0f}")
                
                self.text_ctrl_sfx1.SetValue(f"{results.get('sfx1', 0):.2f}")
                self.text_ctrl_sfx2.SetValue(f"{results.get('sfx2', 0):.2f}")
                self.text_ctrl_sfy1.SetValue(f"{results.get('sfy1', 0):.2f}")
                self.text_ctrl_sfy2.SetValue(f"{results.get('sfy2', 0):.2f}")
            
            # Display deflection
            deflection_precision = self.config.get_precision('deflection')
            self.text_ctrl_def.SetValue(f"{deflection:.{deflection_precision}f}")
            
            # Calculate deflection ratio
            span_mm = span * 1000
            if deflection > 0:
                deflection_ratio = span_mm / deflection
                self.text_ctrl_dBySpan.SetValue(f"1/{deflection_ratio:.0f}")
            
        except Exception as e:
            print(f"Error displaying results: {e}")

    def Clear_R(self):
        """Enhanced clear function with validation"""
        try:
            # Validate title for commas (original logic)
            title = self.text_ctrl_title.GetValue()
            subtitle = self.text_ctrl_subtitle.GetValue()
            
            title_result = self.validator.validate_title(title)
            subtitle_result = self.validator.validate_title(subtitle)
            
            if not title_result.is_valid:
                wx.MessageBox(title_result.error_message, 
                            self.i18n.t('messages.input_error'), 
                            wx.OK | wx.ICON_ERROR)
                return
            
            if not subtitle_result.is_valid:
                wx.MessageBox(subtitle_result.error_message, 
                            self.i18n.t('messages.input_error'), 
                            wx.OK | wx.ICON_ERROR)
                return
            
            # Clear all result fields
            result_fields = [
                'text_ctrl_mx1', 'text_ctrl_mx2', 'text_ctrl_my1', 'text_ctrl_my2',
                'text_ctrl_atx1', 'text_ctrl_atx2', 'text_ctrl_aty1', 'text_ctrl_aty2',
                'text_ctrl_rebarx1', 'text_ctrl_rebarx2', 'text_ctrl_rebary1', 'text_ctrl_rebary2',
                'text_ctrl_reqt', 'text_ctrl_tbyl', 'text_ctrl_sfx1', 'text_ctrl_sfx2',
                'text_ctrl_sfy1', 'text_ctrl_sfy2', 'text_ctrl_def', 'text_ctrl_dBySpan',
                'text_ctrl_lx1PitchOut', 'text_ctrl_lx2PitchOut', 
                'text_ctrl_ly1PitchOut', 'text_ctrl_ly2PitchOut'
            ]
            
            for field_name in result_fields:
                if hasattr(self, field_name):
                    field = getattr(self, field_name)
                    field.SetValue('')
            
        except Exception as e:
            print(f"Error in Clear_R: {e}")

    # Preserve other original methods with enhancements
    def OnStore(self, event):
        """Enhanced store function with validation"""
        try:
            # Validate inputs before storing
            inputs = self.collect_inputs()
            validation_results = self.validator.validate_all_inputs(inputs)
            all_valid, errors, warnings = self.validator.get_validation_summary(validation_results)
            
            if not all_valid:
                error_message = "\\n".join(errors)
                wx.MessageBox(error_message, 
                            self.i18n.t('messages.input_error'), 
                            wx.OK | wx.ICON_ERROR)
                return
            
            # Call original store logic
            super().OnStore(event)
            
        except Exception as e:
            wx.MessageBox(f"Store error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def OnReport(self, event):
        """Enhanced report generation with i18n support"""
        try:
            # Generate report with current language and building code info
            # This would need enhancement to report.py for full i18n support
            super().OnReport(event)
            
        except Exception as e:
            wx.MessageBox(f"Report error: {e}", "Error", wx.OK | wx.ICON_ERROR)


class EnhancedMyFrame(gui.MyFrame):
    """Enhanced main frame with building code selection"""
    
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        
        # Update title with i18n
        try:
            app_title = i18n.i18n.t('app_title')
            self.SetTitle(app_title)
        except:
            self.SetTitle("Enhanced RC Slab Design")

    def OnRcslab(self, event):
        """Launch enhanced RC slab design window"""
        frame = EnhancedMyFrame2(None, wx.ID_ANY, "")
        frame.Show()


class EnhancedApp(wx.App):
    """Enhanced application class"""
    
    def OnInit(self):
        # Initialize enhanced systems
        print("Initializing Enhanced twoWaySlab Application...")
        print(f"Building code: {config.config.get_building_code()}")
        print(f"Language: {i18n.i18n.get_current_language()}")
        
        # Create main window
        frame = EnhancedMyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame)
        frame.Show()
        
        return True


if __name__ == '__main__':
    # Create and run enhanced application
    app = EnhancedApp(0)
    app.MainLoop()