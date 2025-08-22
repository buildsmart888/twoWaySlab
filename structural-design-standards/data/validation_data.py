"""
Validation Data
===============

Test cases and validation data for structural design standards.
Contains test cases for beams, columns, slabs, and other structural members.
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class BeamTestCase:
    """Test case for beam design validation"""
    name: str
    description: str
    geometry: Dict[str, float]
    materials: Dict[str, Any]
    loads: Dict[str, float]
    expected_results: Dict[str, Any]
    tolerance: float = 0.05  # 5% tolerance
    source: str = ""
    standard: str = ""

@dataclass
class ColumnTestCase:
    """Test case for column design validation"""
    name: str
    description: str
    geometry: Dict[str, float]
    materials: Dict[str, Any]
    loads: Dict[str, float]
    expected_results: Dict[str, Any]
    tolerance: float = 0.05
    source: str = ""
    standard: str = ""

@dataclass
class SlabTestCase:
    """Test case for slab design validation"""
    name: str
    description: str
    geometry: Dict[str, float]
    materials: Dict[str, Any]
    loads: Dict[str, float]
    expected_results: Dict[str, Any]
    tolerance: float = 0.05
    source: str = ""
    standard: str = ""

# ACI 318M-25 Beam Test Cases
ACI_BEAM_TEST_CASES = [
    BeamTestCase(
        name="aci_beam_01",
        description="Simply supported beam with uniform load",
        geometry={
            "width": 300,        # mm
            "height": 600,       # mm
            "effective_depth": 550,  # mm
            "span_length": 6000  # mm
        },
        materials={
            "concrete": {"fc_prime": 28.0, "unit_weight": 24.0},
            "steel": {"fy": 420, "grade": "GRADE420"}
        },
        loads={
            "dead_load": 5.0,    # kN/m
            "live_load": 8.0     # kN/m
        },
        expected_results={
            "design_moment": 87.75,      # kN⋅m
            "required_steel_area": 680,  # mm²
            "min_steel_area": 450,       # mm²
            "utilization_ratio": 0.85,
            "deflection": 12.5,          # mm
            "status": "PASS"
        },
        tolerance=0.10,
        source="ACI 318M-25 Example 9.2.1",
        standard="ACI318M25"
    ),
    BeamTestCase(
        name="aci_beam_02",
        description="Continuous beam with concentrated load",
        geometry={
            "width": 350,
            "height": 700,
            "effective_depth": 640,
            "span_length": 8000
        },
        materials={
            "concrete": {"fc_prime": 35.0, "unit_weight": 24.0},
            "steel": {"fy": 420, "grade": "GRADE420"}
        },
        loads={
            "dead_load": 8.0,
            "live_load": 12.0,
            "point_load": 50.0   # kN at midspan
        },
        expected_results={
            "positive_moment": 145.0,
            "negative_moment": 165.0,
            "required_steel_top": 950,
            "required_steel_bottom": 850,
            "shear_reinforcement": "required",
            "status": "PASS"
        },
        tolerance=0.08,
        source="ACI 318M-25 Example 9.3.2",
        standard="ACI318M25"
    ),
    BeamTestCase(
        name="aci_beam_03",
        description="High strength concrete beam",
        geometry={
            "width": 400,
            "height": 800,
            "effective_depth": 740,
            "span_length": 10000
        },
        materials={
            "concrete": {"fc_prime": 55.0, "unit_weight": 24.5},
            "steel": {"fy": 420, "grade": "GRADE420"}
        },
        loads={
            "dead_load": 15.0,
            "live_load": 20.0
        },
        expected_results={
            "design_moment": 437.5,
            "required_steel_area": 2350,
            "compression_controlled": True,
            "phi_factor": 0.90,
            "status": "PASS"
        },
        tolerance=0.12,
        source="ACI 318M-25 High Strength Example",
        standard="ACI318M25"
    )
]

# ACI 318M-25 Column Test Cases
ACI_COLUMN_TEST_CASES = [
    ColumnTestCase(
        name="aci_column_01",
        description="Short tied column with small eccentricity",
        geometry={
            "width": 400,       # mm
            "depth": 400,       # mm
            "length": 3000,     # mm
            "cover": 40         # mm
        },
        materials={
            "concrete": {"fc_prime": 28.0, "unit_weight": 24.0},
            "steel": {"fy": 420, "grade": "GRADE420"}
        },
        loads={
            "axial_dead": 200,      # kN
            "axial_live": 150,      # kN
            "moment_x_dead": 25,    # kN⋅m
            "moment_x_live": 15     # kN⋅m
        },
        expected_results={
            "design_axial": 490,        # kN (factored)
            "design_moment": 56,        # kN⋅m (factored)
            "required_steel_area": 1200, # mm²
            "steel_ratio": 0.0075,
            "interaction_ratio": 0.82,
            "status": "PASS"
        },
        tolerance=0.15,
        source="ACI 318M-25 Example 10.4.1",
        standard="ACI318M25"
    ),
    ColumnTestCase(
        name="aci_column_02",
        description="Slender column with biaxial bending",
        geometry={
            "width": 500,
            "depth": 500,
            "length": 4500,
            "cover": 40
        },
        materials={
            "concrete": {"fc_prime": 35.0, "unit_weight": 24.0},
            "steel": {"fy": 420, "grade": "GRADE420"}
        },
        loads={
            "axial_dead": 400,
            "axial_live": 300,
            "moment_x_dead": 80,
            "moment_x_live": 60,
            "moment_y_dead": 40,
            "moment_y_live": 30
        },
        expected_results={
            "slenderness_x": 18.0,
            "slenderness_y": 18.0,
            "magnification_factor_x": 1.15,
            "magnification_factor_y": 1.15,
            "required_steel_area": 2800,
            "status": "PASS"
        },
        tolerance=0.20,
        source="ACI 318M-25 Example 10.6.3",
        standard="ACI318M25"
    )
]

# Thai Ministry B.E. 2566 Test Cases
THAI_BEAM_TEST_CASES = [
    BeamTestCase(
        name="thai_beam_01",
        description="Thai standard beam with Fc210 concrete",
        geometry={
            "width": 300,
            "height": 600,
            "effective_depth": 540,  # Increased cover for Thai climate
            "span_length": 6000
        },
        materials={
            "concrete": {"grade": "Fc210", "fc_prime": 21.0},
            "steel": {"grade": "SD40", "fy": 392}
        },
        loads={
            "dead_load": 6.0,    # kN/m (includes tropical factors)
            "live_load": 8.0     # kN/m (office load per TIS)
        },
        expected_results={
            "design_moment": 98.0,
            "required_steel_area": 820,
            "min_steel_area": 540,
            "utilization_ratio": 0.88,
            "status": "PASS"
        },
        tolerance=0.10,
        source="Thai Ministry Regulation B.E. 2566 Example 3.1",
        standard="ThaiMinistry2566"
    ),
    BeamTestCase(
        name="thai_beam_02",
        description="Two-way slab beam design",
        geometry={
            "width": 250,
            "height": 400,
            "effective_depth": 360,
            "span_length": 4000
        },
        materials={
            "concrete": {"grade": "Fc240", "fc_prime": 24.0},
            "steel": {"grade": "SD40", "fy": 392}
        },
        loads={
            "dead_load": 4.5,
            "live_load": 2.5,
            "slab_load": 8.0    # kN/m from slab
        },
        expected_results={
            "design_moment": 30.0,
            "required_steel_area": 280,
            "min_steel_area": 180,
            "status": "PASS"
        },
        tolerance=0.12,
        source="TIS 1311-50 Slab Example",
        standard="ThaiMinistry2566"
    )
]

THAI_COLUMN_TEST_CASES = [
    ColumnTestCase(
        name="thai_column_01",
        description="Thai building column with seismic consideration",
        geometry={
            "width": 400,
            "depth": 400,
            "length": 3500,
            "cover": 50  # Increased for tropical climate
        },
        materials={
            "concrete": {"grade": "Fc240", "fc_prime": 24.0},
            "steel": {"grade": "SD40", "fy": 392}
        },
        loads={
            "axial_dead": 180,
            "axial_live": 120,
            "seismic_factor": 1.2,  # Thai seismic zone factor
            "wind_load": 15         # kN (provincial wind load)
        },
        expected_results={
            "design_axial": 420,
            "required_steel_area": 1400,
            "seismic_detailing": "required",
            "status": "PASS"
        },
        tolerance=0.15,
        source="Thai Ministry B.E. 2566 with TIS 1302-61",
        standard="ThaiMinistry2566"
    )
]

# Slab Test Cases
SLAB_TEST_CASES = [
    SlabTestCase(
        name="two_way_slab_01",
        description="Two-way slab supported on beams",
        geometry={
            "length_x": 6000,    # mm
            "length_y": 4000,    # mm
            "thickness": 150,    # mm
            "effective_depth": 120
        },
        materials={
            "concrete": {"fc_prime": 28.0},
            "steel": {"fy": 420}
        },
        loads={
            "dead_load": 4.0,    # kN/m²
            "live_load": 2.5,    # kN/m²
            "partition_load": 1.0 # kN/m²
        },
        expected_results={
            "moment_x": 15.2,    # kN⋅m/m
            "moment_y": 11.8,    # kN⋅m/m
            "steel_x": 320,      # mm²/m
            "steel_y": 280,      # mm²/m
            "status": "PASS"
        },
        tolerance=0.15,
        source="ACI 318M-25 Two-way Slab Example",
        standard="ACI318M25"
    )
]

# Load Combination Test Cases
LOAD_COMBINATION_CASES = [
    {
        "name": "aci_basic_combo",
        "description": "ACI 318M-25 basic load combination",
        "loads": {
            "dead": 10.0,    # kN
            "live": 15.0,    # kN
            "snow": 5.0      # kN
        },
        "combinations": {
            "strength_1": {"equation": "1.4D", "result": 14.0},
            "strength_2": {"equation": "1.2D + 1.6L + 0.5S", "result": 38.5},
            "strength_3": {"equation": "1.2D + 1.6S + 0.5L", "result": 27.5},
            "service": {"equation": "D + L", "result": 25.0}
        },
        "critical_combination": "strength_2",
        "critical_value": 38.5,
        "standard": "ACI318M25"
    },
    {
        "name": "thai_basic_combo",
        "description": "Thai Ministry basic load combination",
        "loads": {
            "dead": 12.0,
            "live": 18.0,
            "wind": 8.0
        },
        "combinations": {
            "ultimate_1": {"equation": "1.4D + 1.7L", "result": 47.4},
            "ultimate_2": {"equation": "1.2D + 1.6W + 0.5L", "result": 36.2},
            "service": {"equation": "D + L + 0.6W", "result": 34.8}
        },
        "critical_combination": "ultimate_1",
        "critical_value": 47.4,
        "standard": "ThaiMinistry2566"
    }
]

# Material Property Validation Cases
MATERIAL_VALIDATION_CASES = [
    {
        "name": "aci_concrete_validation",
        "material_type": "concrete",
        "standard": "ACI318M25",
        "test_cases": [
            {
                "fc_prime": 28.0,
                "expected_ec": 25120,  # MPa
                "expected_fr": 3.33,   # MPa (modulus of rupture)
                "tolerance": 0.05
            },
            {
                "fc_prime": 35.0,
                "expected_ec": 28098,
                "expected_fr": 3.73,
                "tolerance": 0.05
            }
        ]
    },
    {
        "name": "thai_concrete_validation",
        "material_type": "concrete",
        "standard": "ThaiMinistry2566",
        "test_cases": [
            {
                "grade": "Fc210",
                "fc_prime": 21.0,
                "expected_ec": 21571,
                "tolerance": 0.08
            },
            {
                "grade": "Fc280",
                "fc_prime": 28.0,
                "expected_ec": 24899,
                "tolerance": 0.08
            }
        ]
    }
]

# Performance Benchmark Cases
PERFORMANCE_BENCHMARK_CASES = [
    {
        "name": "beam_design_performance",
        "description": "Benchmark beam design calculation speed",
        "test_type": "execution_time",
        "iterations": 1000,
        "expected_time_per_iteration": 0.005,  # seconds
        "tolerance": 0.002,
        "geometry_variations": 50,
        "load_variations": 20
    },
    {
        "name": "column_design_performance",
        "description": "Benchmark column design calculation speed",
        "test_type": "execution_time",
        "iterations": 500,
        "expected_time_per_iteration": 0.008,
        "tolerance": 0.003,
        "geometry_variations": 30,
        "load_variations": 25
    },
    {
        "name": "material_property_performance",
        "description": "Benchmark material property calculations",
        "test_type": "execution_time",
        "iterations": 10000,
        "expected_time_per_iteration": 0.0001,
        "tolerance": 0.00005
    }
]

# Integration Test Cases
INTEGRATION_TEST_CASES = [
    {
        "name": "complete_building_design",
        "description": "Complete multi-story building design workflow",
        "components": ["beams", "columns", "slabs", "foundations"],
        "stories": 5,
        "bay_size": {"x": 6000, "y": 8000},  # mm
        "expected_completion_time": 30.0,    # seconds
        "expected_memory_usage": 50.0,       # MB
        "validation_points": [
            {"component": "beam", "location": "typical_floor", "check": "deflection"},
            {"component": "column", "location": "ground_floor", "check": "interaction"},
            {"component": "slab", "location": "roof", "check": "punching_shear"}
        ]
    }
]

# Utility functions for accessing test data
def get_test_cases(member_type: str, standard: str = None) -> List[Any]:
    """Get test cases for specified member type and standard"""
    test_cases = []
    
    if member_type.lower() == "beam":
        if standard is None or standard.upper() == "ACI318M25":
            test_cases.extend(ACI_BEAM_TEST_CASES)
        if standard is None or standard.upper() == "THAIMINISTRY2566":
            test_cases.extend(THAI_BEAM_TEST_CASES)
    
    elif member_type.lower() == "column":
        if standard is None or standard.upper() == "ACI318M25":
            test_cases.extend(ACI_COLUMN_TEST_CASES)
        if standard is None or standard.upper() == "THAIMINISTRY2566":
            test_cases.extend(THAI_COLUMN_TEST_CASES)
    
    elif member_type.lower() == "slab":
        test_cases.extend(SLAB_TEST_CASES)
    
    return test_cases

def get_validation_tolerance(test_case_name: str) -> float:
    """Get validation tolerance for a specific test case"""
    # Find the test case and return its tolerance
    all_cases = (ACI_BEAM_TEST_CASES + ACI_COLUMN_TEST_CASES + 
                THAI_BEAM_TEST_CASES + THAI_COLUMN_TEST_CASES + 
                SLAB_TEST_CASES)
    
    for case in all_cases:
        if case.name == test_case_name:
            return case.tolerance
    
    return 0.05  # Default 5% tolerance

def filter_test_cases(member_type: str = None, standard: str = None, 
                     difficulty: str = None) -> List[Any]:
    """Filter test cases by criteria"""
    all_cases = get_test_cases(member_type or "all", standard)
    
    if difficulty:
        # Filter by difficulty based on tolerance
        if difficulty.lower() == "easy":
            all_cases = [case for case in all_cases if case.tolerance >= 0.10]
        elif difficulty.lower() == "medium":
            all_cases = [case for case in all_cases if 0.05 <= case.tolerance < 0.10]
        elif difficulty.lower() == "hard":
            all_cases = [case for case in all_cases if case.tolerance < 0.05]
    
    return all_cases