ACI 318M-25 Standards API
=========================

This section documents the ACI 318M-25 Building Code Requirements for Structural Concrete implementation.

ACI 318M-25 Materials
---------------------

.. automodule:: structural_standards.aci.aci318m25.materials
   :members:
   :undoc-members:
   :show-inheritance:

Concrete Materials
^^^^^^^^^^^^^^^^^

.. automodule:: structural_standards.aci.aci318m25.materials.concrete
   :members:
   :undoc-members:
   :show-inheritance:

Steel Materials
^^^^^^^^^^^^^^

.. automodule:: structural_standards.aci.aci318m25.materials.steel
   :members:
   :undoc-members:
   :show-inheritance:

ACI 318M-25 Structural Members
------------------------------

.. automodule:: structural_standards.aci.aci318m25.members
   :members:
   :undoc-members:
   :show-inheritance:

Beam Design
^^^^^^^^^^

.. automodule:: structural_standards.aci.aci318m25.members.beam_design
   :members:
   :undoc-members:
   :show-inheritance:

Column Design
^^^^^^^^^^^^

.. automodule:: structural_standards.aci.aci318m25.members.column_design
   :members:
   :undoc-members:
   :show-inheritance:

Slab Design
^^^^^^^^^^

.. automodule:: structural_standards.aci.aci318m25.members.slab_design
   :members:
   :undoc-members:
   :show-inheritance:

Wall Design
^^^^^^^^^^

.. automodule:: structural_standards.aci.aci318m25.members.wall_design
   :members:
   :undoc-members:
   :show-inheritance:

Footing Design
^^^^^^^^^^^^^

.. automodule:: structural_standards.aci.aci318m25.members.footing_design
   :members:
   :undoc-members:
   :show-inheritance:

Diaphragm Design
^^^^^^^^^^^^^^^

.. automodule:: structural_standards.aci.aci318m25.members.diaphragm_design
   :members:
   :undoc-members:
   :show-inheritance:

ACI 318M-25 Load Combinations
-----------------------------

.. automodule:: structural_standards.aci.aci318m25.load_combinations
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Beam Design
^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
   from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
   from structural_standards.aci.aci318m25.members.beam_design import (
       ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
   )

   # Create materials
   concrete = ACI318M25Concrete(fc_prime=28.0)  # 28 MPa concrete
   steel = ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')

   # Create beam designer
   beam_designer = ACI318M25BeamDesign(concrete, steel)

   # Define geometry
   geometry = BeamGeometry(
       width=300,           # mm
       height=600,          # mm
       effective_depth=550, # mm
       span_length=6000     # mm
   )

   # Define loads
   loads = BeamLoads(
       dead_load=5.0,       # kN/m
       live_load=8.0        # kN/m
   )

   # Perform design
   result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
   
   print(f"Design Status: {result.overall_status}")
   print(f"Required Steel Area: {result.required_reinforcement['required_steel_area']:.0f} mm²")

Basic Column Design
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from structural_standards.aci.aci318m25.members.column_design import (
       ACI318M25ColumnDesign, ColumnGeometry, ColumnLoads, ColumnType
   )

   # Create column designer
   column_designer = ACI318M25ColumnDesign(concrete, steel)

   # Define geometry
   geometry = ColumnGeometry(
       width=400,      # mm
       depth=400,      # mm
       length=3000     # mm
   )

   # Define loads
   loads = ColumnLoads(
       axial_dead=200,    # kN
       axial_live=150,    # kN
       moment_x_dead=25,  # kN⋅m
       moment_x_live=15   # kN⋅m
   )

   # Perform design
   result = column_designer.design(geometry, loads, ColumnType.TIED)
   
   print(f"Design Status: {result.overall_status}")
   print(f"Required Steel Area: {result.required_reinforcement['required_steel_area']:.0f} mm²")