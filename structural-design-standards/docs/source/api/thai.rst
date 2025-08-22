Thai Standards API
==================

This section documents the Thai building code standards implementation according to Ministry Regulation B.E. 2566.

การใช้งาน API มาตรฐานการออกแบบโครงสร้างไทย
========================================

Thai Ministry Regulation B.E. 2566
-----------------------------------

.. automodule:: structural_standards.thai.ministry_2566
   :members:
   :undoc-members:
   :show-inheritance:

Ministry Regulation
^^^^^^^^^^^^^^^^^^

.. automodule:: structural_standards.thai.ministry_2566.ministry_regulation
   :members:
   :undoc-members:
   :show-inheritance:

Load Combinations
^^^^^^^^^^^^^^^^

.. automodule:: structural_standards.thai.ministry_2566.load_combinations
   :members:
   :undoc-members:
   :show-inheritance:

Wind Loads (TIS 1311-50)
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: structural_standards.thai.ministry_2566.wind_loads
   :members:
   :undoc-members:
   :show-inheritance:

Seismic Loads (TIS 1301/1302-61)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: structural_standards.thai.ministry_2566.seismic_loads
   :members:
   :undoc-members:
   :show-inheritance:

Thai Materials
--------------

.. automodule:: structural_standards.thai.materials
   :members:
   :undoc-members:
   :show-inheritance:

Thai Concrete
^^^^^^^^^^^^

.. automodule:: structural_standards.thai.materials.concrete
   :members:
   :undoc-members:
   :show-inheritance:

Thai Steel
^^^^^^^^^

.. automodule:: structural_standards.thai.materials.steel
   :members:
   :undoc-members:
   :show-inheritance:

Thai Unit Systems
-----------------

.. automodule:: structural_standards.thai.unit_systems
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Thai Load Combinations
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.thai.ministry_2566.load_combinations import ThaiMinistryLoadCombinations

   # Create load combinations manager
   thai_loads = ThaiMinistryLoadCombinations()

   # Get Ultimate Limit State combinations
   uls_combinations = thai_loads.get_ultimate_combinations()
   
   for combo in uls_combinations[:5]:  # First 5 combinations
       print(f"{combo.name}: {combo.get_equation()}")

   # Example output:
   # 1000: 1.4×DL
   # 1001: 1.4×DL + 1.7×LL
   # 1002: 1.05×DL + 1.275×LL + 1.6×W+x
   # 1003: 1.05×DL + 1.275×LL + 1.6×W-x
   # 1004: 1.05×DL + 1.275×LL + 1.6×W+y

Thai Wind Loads
^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.thai.ministry_2566.wind_loads import ThaiWindLoads
   from structural_standards.thai.unit_systems import ThaiUnitConverter

   # Create wind load calculator
   wind_calc = ThaiWindLoads()
   
   # Calculate wind load for building in Bangkok (Zone 2)
   wind_load = wind_calc.calculate_wind_load(
       building_height=30.0,        # meters
       building_width=20.0,         # meters
       terrain_category='II',       # Rough terrain
       importance_factor='standard', # Standard building
       province='กรุงเทพมหานคร'       # Bangkok
   )
   
   print(f"Design wind pressure: {wind_load.design_pressure:.2f} kN/m²")
   print(f"Wind zone: {wind_load.wind_zone}")
   print(f"Basic wind speed: {wind_load.basic_speed:.1f} m/s")

Thai Seismic Loads
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.thai.ministry_2566.seismic_loads import ThaiSeismicLoads

   # Create seismic load calculator
   seismic_calc = ThaiSeismicLoads()
   
   # Calculate seismic load for building in Chiang Mai (Zone C)
   seismic_load = seismic_calc.calculate_seismic_load(
       building_height=25.0,          # meters
       building_weight=5000.0,        # kN
       soil_type='D',                 # Stiff soil
       structural_system='moment_frame', # Moment resisting frame
       importance_factor='standard',   # Standard building
       province='เชียงใหม่'             # Chiang Mai
   )
   
   print(f"Design base shear: {seismic_load.base_shear:.1f} kN")
   print(f"Seismic zone: {seismic_load.seismic_zone}")
   print(f"Peak ground acceleration: {seismic_load.pga:.2f}g")

Thai Unit Conversions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.thai.unit_systems import ThaiUnitConverter

   converter = ThaiUnitConverter()

   # Convert traditional Thai units to SI
   stress_mpa = converter.ksc_to_mpa(1000)  # 1000 ksc to MPa
   print(f"1000 ksc = {stress_mpa:.1f} MPa")  # ~98.1 MPa

   force_kn = converter.tonf_to_kn(10)  # 10 tonf to kN
   print(f"10 tonf = {force_kn:.1f} kN")  # ~98.1 kN

   pressure_kn_m2 = converter.kgf_m2_to_kn_m2(1000)  # 1000 kgf/m² to kN/m²
   print(f"1000 kgf/m² = {pressure_kn_m2:.1f} kN/m²")  # ~9.81 kN/m²

Thai Material Properties
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.thai.materials.concrete import ThaiConcrete
   from structural_standards.thai.materials.steel import ThaiSteel

   # Create Thai concrete (traditional grades)
   concrete_fc210 = ThaiConcrete(grade='Fc210')  # 21 MPa concrete
   print(f"Fc210: {concrete_fc210.fc_prime} MPa")
   print(f"Fc210: {concrete_fc210.fc_ksc:.1f} ksc")

   # Create Thai steel
   steel_sd40 = ThaiSteel(grade='SD40')  # SD40 deformed bar
   print(f"SD40: {steel_sd40.fy} MPa")
   print(f"SD40: {steel_sd40.fy_ksc:.0f} ksc")

Thai Provincial Information
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.thai.ministry_2566.provincial_data import ThaiProvincialData

   provincial = ThaiProvincialData()

   # Get wind zone for a province
   wind_info = provincial.get_wind_zone_info('ภูเก็ต')
   print(f"Phuket Wind Zone: {wind_info['zone']} ({wind_info['basic_speed']} m/s)")

   # Get seismic zone for a province  
   seismic_info = provincial.get_seismic_zone_info('เชียงใหม่')
   print(f"Chiang Mai Seismic Zone: {seismic_info['zone']} ({seismic_info['pga']}g PGA)")

   # List all provinces in a specific zone
   zone_c_provinces = provincial.get_provinces_by_seismic_zone('C')
   print(f"High seismic risk provinces: {', '.join(zone_c_provinces)}")