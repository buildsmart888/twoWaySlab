Utilities API
=============

This section documents the utility modules and helper functions available in the structural design standards library.

Base Classes
------------

.. automodule:: structural_standards.base
   :members:
   :undoc-members:
   :show-inheritance:

Design Base
^^^^^^^^^^

.. automodule:: structural_standards.base.design_base
   :members:
   :undoc-members:
   :show-inheritance:

Material Base
^^^^^^^^^^^^

.. automodule:: structural_standards.base.material_base
   :members:
   :undoc-members:
   :show-inheritance:

Standard Base
^^^^^^^^^^^^

.. automodule:: structural_standards.base.standard_base
   :members:
   :undoc-members:
   :show-inheritance:

Utilities
---------

.. automodule:: structural_standards.utils
   :members:
   :undoc-members:
   :show-inheritance:

Validation Utilities
^^^^^^^^^^^^^^^^^^^

.. automodule:: structural_standards.utils.validation
   :members:
   :undoc-members:
   :show-inheritance:

Unit Conversion
^^^^^^^^^^^^^^

.. automodule:: structural_standards.utils.units
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
^^^^^^^^^^^^

.. automodule:: structural_standards.utils.config
   :members:
   :undoc-members:
   :show-inheritance:

Internationalization
^^^^^^^^^^^^^^^^^^^

.. automodule:: structural_standards.utils.i18n
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Validation Utilities
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.utils.validation import (
       StructuralValidator, validate_positive, validate_range
   )

   # Basic validation functions
   validate_positive(28.0, "concrete strength")  # Passes
   validate_range(0.85, 0.0, 1.0, "reduction factor")  # Passes
   
   # Advanced structural validator
   validator = StructuralValidator()
   
   # Validate material properties
   concrete_props = {
       'fc_prime': 28.0,
       'unit_weight': 24.0,
       'elastic_modulus': 24847.0
   }
   
   is_valid = validator.validate_concrete_properties(concrete_props)
   print(f"Concrete properties valid: {is_valid}")
   
   # Validate design result
   design_result = {
       'member_type': 'beam',
       'overall_status': 'PASS',
       'utilization_ratio': 0.85,
       'required_reinforcement': {'required_steel_area': 1200}
   }
   
   is_valid = validator.validate_design_result(design_result)
   print(f"Design result valid: {is_valid}")

Unit Conversion
^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.utils.units import UnitConverter

   converter = UnitConverter()

   # Length conversions
   mm_to_m = converter.convert_length(1000, 'mm', 'm')
   print(f"1000 mm = {mm_to_m} m")  # 1.0 m
   
   in_to_mm = converter.convert_length(12, 'in', 'mm')
   print(f"12 in = {in_to_mm:.1f} mm")  # 304.8 mm

   # Force conversions
   kn_to_n = converter.convert_force(10, 'kN', 'N')
   print(f"10 kN = {kn_to_n:.0f} N")  # 10000 N
   
   kip_to_kn = converter.convert_force(1, 'kip', 'kN')
   print(f"1 kip = {kip_to_kn:.2f} kN")  # 4.45 kN

   # Stress conversions
   mpa_to_psi = converter.convert_stress(28, 'MPa', 'psi')
   print(f"28 MPa = {mpa_to_psi:.0f} psi")  # 4061 psi
   
   ksi_to_mpa = converter.convert_stress(60, 'ksi', 'MPa')
   print(f"60 ksi = {ksi_to_mpa:.1f} MPa")  # 413.7 MPa

Configuration Management
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.utils.config import ConfigManager

   config = ConfigManager()

   # Set default design standard
   config.set_default_standard('ACI 318M-25')
   
   # Configure material defaults
   config.set_material_defaults({
       'concrete_grade': 'fc28',
       'steel_grade': 'GRADE420',
       'unit_system': 'metric'
   })
   
   # Get configuration
   default_standard = config.get_default_standard()
   material_defaults = config.get_material_defaults()
   
   print(f"Default standard: {default_standard}")
   print(f"Default concrete: {material_defaults['concrete_grade']}")

Internationalization
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.utils.i18n import Translator

   # Initialize translator
   translator = Translator()
   
   # Set language
   translator.set_language('th')  # Thai
   
   # Translate messages
   msg_en = translator.get_message('beam_design_complete', lang='en')
   msg_th = translator.get_message('beam_design_complete', lang='th')
   
   print(f"English: {msg_en}")  # "Beam design completed successfully"
   print(f"Thai: {msg_th}")     # "การออกแบบคานเสร็จสมบูรณ์"
   
   # Format messages with parameters
   error_msg = translator.format_message(
       'validation_error', 
       parameter='concrete strength',
       value='-5.0',
       lang='th'
   )
   print(f"Error: {error_msg}")

Base Class Usage
^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.base.design_base import StructuralMember
   from structural_standards.base.material_base import ConcreteMaterial
   from structural_standards.base.standard_base import StructuralStandard

   # Using base classes for custom implementations
   class CustomConcrete(ConcreteMaterial):
       def __init__(self, fc_prime):
           super().__init__(fc_prime=fc_prime, standard="Custom Standard")
       
       def elastic_modulus(self):
           return 4700 * (self.fc_prime ** 0.5)  # Custom formula
   
   # Create custom concrete
   concrete = CustomConcrete(fc_prime=30.0)
   print(f"Custom concrete Ec: {concrete.elastic_modulus():.0f} MPa")

   # Check if object follows standard interface
   print(f"Is concrete material: {isinstance(concrete, ConcreteMaterial)}")

Advanced Validation
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.utils.validation import (
       ValidationLevel, ValidationResult, ValidationContext
   )

   # Create validation context
   context = ValidationContext(
       standard='ACI 318M-25',
       member_type='beam',
       validation_level=ValidationLevel.STRICT
   )

   validator = StructuralValidator()

   # Validate with context
   geometry = {
       'width': 300,
       'height': 600,
       'effective_depth': 550,
       'span_length': 6000
   }

   result = validator.validate_geometry(geometry, context)
   
   if result.is_valid:
       print("Geometry validation passed")
   else:
       print(f"Validation errors: {result.errors}")
       print(f"Warnings: {result.warnings}")

Error Handling
^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.utils.validation import (
       ValidationError, DesignError, MaterialError
   )

   try:
       # This will raise a validation error
       validate_positive(-5.0, "concrete strength")
   except ValidationError as e:
       print(f"Validation error: {e}")
       print(f"Parameter: {e.parameter}")
       print(f"Value: {e.value}")

   try:
       # Design calculation that might fail
       result = beam_designer.design(invalid_geometry, loads, BeamType.SIMPLY_SUPPORTED)
   except DesignError as e:
       print(f"Design error: {e}")
       print(f"Member type: {e.member_type}")
       print(f"Failure reason: {e.reason}")

Performance Utilities
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.utils.performance import PerformanceMonitor

   # Monitor design performance
   monitor = PerformanceMonitor()
   
   monitor.start()
   
   # Perform design calculations
   result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
   
   performance = monitor.stop()
   
   print(f"Execution time: {performance.execution_time:.3f} seconds")
   print(f"Memory usage: {performance.memory_usage:.1f} MB")
   print(f"Peak memory: {performance.peak_memory:.1f} MB")