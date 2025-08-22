"""
Code Generators Module
======================

Automatic code generation utilities for structural design standards.
Generates boilerplate code for standards, materials, and design members.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class CodeType(Enum):
    """Type of code to generate"""
    STANDARD = "standard"
    MATERIAL = "material" 
    MEMBER_DESIGN = "member_design"
    TEST = "test"
    VALIDATION = "validation"

class LanguageStandard(Enum):
    """Structural design language standard"""
    ACI_318M_25 = "aci_318m_25"
    THAI_MINISTRY_2566 = "thai_ministry_2566"
    EUROCODE_2 = "eurocode_2"
    AS_3600 = "as_3600"

@dataclass
class GeneratorConfig:
    """Configuration for code generation"""
    output_dir: Path
    package_name: str
    author: str
    license_type: str = "MIT"
    include_tests: bool = True
    include_documentation: bool = True
    language_standard: LanguageStandard = LanguageStandard.ACI_318M_25

class StandardCodeGenerator:
    """
    Generates code templates for new structural design standards
    """
    
    def __init__(self, config: GeneratorConfig):
        """Initialize generator with configuration"""
        self.config = config
        self.templates_dir = Path(__file__).parent / "templates"
    
    def generate_standard_package(self, standard_name: str) -> Dict[str, str]:
        """
        Generate complete package structure for a new standard
        
        Parameters:
        -----------
        standard_name : str
            Name of the standard (e.g., 'eurocode_2', 'as_3600')
            
        Returns:
        --------
        dict
            Generated file paths and contents
        """
        files = {}
        
        # Package structure
        base_path = self.config.output_dir / standard_name
        
        # Generate __init__.py
        files[str(base_path / "__init__.py")] = self._generate_package_init(standard_name)
        
        # Generate materials module
        materials_path = base_path / "materials"
        files[str(materials_path / "__init__.py")] = self._generate_materials_init()
        files[str(materials_path / "concrete.py")] = self._generate_concrete_material(standard_name)
        files[str(materials_path / "steel.py")] = self._generate_steel_material(standard_name)
        
        # Generate members module
        members_path = base_path / "members"
        files[str(members_path / "__init__.py")] = self._generate_members_init()
        files[str(members_path / "beam_design.py")] = self._generate_beam_design(standard_name)
        files[str(members_path / "column_design.py")] = self._generate_column_design(standard_name)
        files[str(members_path / "slab_design.py")] = self._generate_slab_design(standard_name)
        
        # Generate load combinations
        files[str(base_path / "load_combinations.py")] = self._generate_load_combinations(standard_name)
        
        return files
    
    def _generate_package_init(self, standard_name: str) -> str:
        """Generate package __init__.py"""
        standard_title = standard_name.replace('_', ' ').title()
        
        return f'''"""
{standard_title} Design Standard Implementation
{'=' * (len(standard_title) + 30)}

Implementation of {standard_title} structural design standard.

Author: {self.config.author}
License: {self.config.license_type}
"""

from .materials import *
from .members import *
from .load_combinations import *

__version__ = "1.0.0"
__author__ = "{self.config.author}"
__standard__ = "{standard_title}"

__all__ = [
    # Materials
    "{standard_name.title()}Concrete",
    "{standard_name.title()}Steel",
    
    # Members
    "{standard_name.title()}BeamDesign",
    "{standard_name.title()}ColumnDesign", 
    "{standard_name.title()}SlabDesign",
    
    # Load combinations
    "{standard_name.title()}LoadCombinations"
]
'''
    
    def _generate_materials_init(self) -> str:
        """Generate materials package __init__.py"""
        return '''"""
Materials Module
================

Material property definitions and calculations.
"""

from .concrete import *
from .steel import *

__all__ = ["Concrete", "Steel"]
'''
    
    def _generate_concrete_material(self, standard_name: str) -> str:
        """Generate concrete material class"""
        class_name = f"{standard_name.title()}Concrete"
        
        return f'''"""
{standard_name.title()} Concrete Material
{'=' * (len(standard_name) + 20)}

Concrete material implementation according to {standard_name.title()} standard.
"""

from typing import Optional, Union
from structural_standards.base.material_base import ConcreteMaterial
from structural_standards.utils.validation import validate_positive, validate_range

class {class_name}(ConcreteMaterial):
    """
    {standard_name.title()} concrete material implementation
    """
    
    def __init__(self, 
                 fc_prime: float,
                 unit_weight: float = 24.0,
                 aggregate_type: str = "normal"):
        """
        Initialize concrete material
        
        Parameters:
        -----------
        fc_prime : float
            Compressive strength (MPa)
        unit_weight : float
            Unit weight (kN/m³)
        aggregate_type : str
            Type of aggregate ('normal', 'lightweight', 'heavyweight')
        """
        # Validation
        validate_positive(fc_prime, "concrete compressive strength")
        validate_range(unit_weight, 15.0, 30.0, "concrete unit weight")
        
        super().__init__(
            fc_prime=fc_prime,
            standard="{standard_name.title()}"
        )
        
        self.unit_weight = unit_weight
        self.aggregate_type = aggregate_type
    
    def elastic_modulus(self) -> float:
        """
        Calculate elastic modulus according to {standard_name.title()}
        
        Returns:
        --------
        float
            Elastic modulus (MPa)
        """
        # Implement standard-specific formula
        if self.aggregate_type == "normal":
            return 4700 * (self.fc_prime ** 0.5)  # Example formula
        elif self.aggregate_type == "lightweight":
            return 3300 * (self.fc_prime ** 0.5)
        else:
            return 4700 * (self.fc_prime ** 0.5)
    
    def tensile_strength(self) -> float:
        """
        Calculate tensile strength
        
        Returns:
        --------
        float
            Tensile strength (MPa)
        """
        return 0.6 * (self.fc_prime ** 0.5)
    
    def modulus_of_rupture(self) -> float:
        """
        Calculate modulus of rupture
        
        Returns:
        --------
        float
            Modulus of rupture (MPa)
        """
        return 0.7 * (self.fc_prime ** 0.5)
'''
    
    def _generate_steel_material(self, standard_name: str) -> str:
        """Generate steel material class"""
        class_name = f"{standard_name.title()}Steel"
        
        return f'''"""
{standard_name.title()} Steel Material
{'=' * (len(standard_name) + 17)}

Steel material implementation according to {standard_name.title()} standard.
"""

from typing import Optional, Dict
from structural_standards.base.material_base import SteelMaterial
from structural_standards.utils.validation import validate_positive

class {class_name}(SteelMaterial):
    """
    {standard_name.title()} steel material implementation
    """
    
    # Standard steel grades
    STANDARD_GRADES = {{
        "GRADE300": {{"fy": 300, "fu": 450}},
        "GRADE400": {{"fy": 400, "fu": 550}},
        "GRADE500": {{"fy": 500, "fu": 630}}
    }}
    
    def __init__(self, 
                 grade: str = "GRADE400",
                 bar_designation: str = "N20"):
        """
        Initialize steel material
        
        Parameters:
        -----------
        grade : str
            Steel grade designation
        bar_designation : str
            Reinforcement bar designation
        """
        if grade not in self.STANDARD_GRADES:
            raise ValueError(f"Unknown steel grade: {{grade}}")
        
        grade_props = self.STANDARD_GRADES[grade]
        
        super().__init__(
            fy=grade_props["fy"],
            standard="{standard_name.title()}"
        )
        
        self.grade = grade
        self.bar_designation = bar_designation
        self.fu = grade_props["fu"]
    
    def bar_area(self) -> float:
        """
        Get bar area from designation
        
        Returns:
        --------
        float
            Bar cross-sectional area (mm²)
        """
        # Standard bar areas (example)
        bar_areas = {{
            "N12": 113,
            "N16": 201,
            "N20": 314,
            "N25": 491,
            "N32": 804
        }}
        
        return bar_areas.get(self.bar_designation, 314)  # Default to N20
    
    def development_length(self, concrete_fc: float) -> float:
        """
        Calculate development length
        
        Parameters:
        -----------
        concrete_fc : float
            Concrete compressive strength (MPa)
            
        Returns:
        --------
        float
            Development length (mm)
        """
        db = self.bar_diameter()
        return max(0.019 * self.fy * db / (concrete_fc ** 0.5), 300)
    
    def bar_diameter(self) -> float:
        """
        Get bar diameter from designation
        
        Returns:
        --------
        float
            Bar diameter (mm)
        """
        # Extract diameter from designation
        import re
        match = re.search(r'\\d+', self.bar_designation)
        if match:
            return float(match.group())
        return 20.0  # Default
'''
    
    def _generate_beam_design(self, standard_name: str) -> str:
        """Generate beam design class"""
        class_name = f"{standard_name.title()}BeamDesign"
        
        return f'''"""
{standard_name.title()} Beam Design
{'=' * (len(standard_name) + 15)}

Beam design implementation according to {standard_name.title()} standard.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from structural_standards.base.design_base import StructuralMember, DesignResult
from .materials.concrete import {standard_name.title()}Concrete
from .materials.steel import {standard_name.title()}Steel

class BeamType(Enum):
    """Beam support types"""
    SIMPLY_SUPPORTED = "simply_supported"
    CONTINUOUS = "continuous"
    CANTILEVER = "cantilever"

@dataclass
class BeamGeometry:
    """Beam geometry parameters"""
    width: float  # mm
    height: float  # mm
    effective_depth: float  # mm
    span_length: float  # mm

@dataclass 
class BeamLoads:
    """Beam loading parameters"""
    dead_load: float  # kN/m
    live_load: float  # kN/m
    wind_load: float = 0.0  # kN/m
    seismic_load: float = 0.0  # kN/m

class {class_name}(StructuralMember):
    """
    {standard_name.title()} beam design implementation
    """
    
    def __init__(self, 
                 concrete: {standard_name.title()}Concrete,
                 steel: {standard_name.title()}Steel):
        """
        Initialize beam designer
        
        Parameters:
        -----------
        concrete : {standard_name.title()}Concrete
            Concrete material
        steel : {standard_name.title()}Steel
            Steel material
        """
        super().__init__("beam", "{standard_name.title()}")
        self.concrete = concrete
        self.steel = steel
    
    def design(self, 
               geometry: BeamGeometry,
               loads: BeamLoads,
               beam_type: BeamType = BeamType.SIMPLY_SUPPORTED) -> DesignResult:
        """
        Perform beam design
        
        Parameters:
        -----------
        geometry : BeamGeometry
            Beam geometry
        loads : BeamLoads
            Applied loads
        beam_type : BeamType
            Beam support type
            
        Returns:
        --------
        DesignResult
            Design result with status and calculations
        """
        try:
            # Calculate design moments
            moments = self._calculate_moments(geometry, loads, beam_type)
            
            # Design flexural reinforcement
            flexural_result = self._design_flexural(geometry, moments)
            
            # Design shear reinforcement
            shear_result = self._design_shear(geometry, loads)
            
            # Check deflection
            deflection_result = self._check_deflection(geometry, loads)
            
            # Combine results
            overall_status = self._get_overall_status([
                flexural_result["status"],
                shear_result["status"], 
                deflection_result["status"]
            ])
            
            return DesignResult(
                member_type="beam",
                overall_status=overall_status,
                design_moments=moments,
                required_reinforcement=flexural_result,
                shear_design=shear_result,
                deflection_check=deflection_result,
                utilization_ratio=max(
                    flexural_result.get("utilization", 0),
                    shear_result.get("utilization", 0)
                )
            )
            
        except Exception as e:
            return DesignResult(
                member_type="beam",
                overall_status="ERROR",
                error_message=str(e)
            )
    
    def _calculate_moments(self, 
                          geometry: BeamGeometry,
                          loads: BeamLoads,
                          beam_type: BeamType) -> Dict[str, float]:
        """Calculate design moments"""
        # Factored loads
        wu = 1.4 * loads.dead_load + 1.7 * loads.live_load
        
        # Moment calculations based on beam type
        if beam_type == BeamType.SIMPLY_SUPPORTED:
            Mu = wu * geometry.span_length**2 / 8
        elif beam_type == BeamType.CONTINUOUS:
            Mu = wu * geometry.span_length**2 / 10  # Simplified
        else:  # Cantilever
            Mu = wu * geometry.span_length**2 / 2
        
        return {{
            "factored_moment": Mu,
            "service_moment": (loads.dead_load + loads.live_load) * geometry.span_length**2 / 8
        }}
    
    def _design_flexural(self, 
                        geometry: BeamGeometry,
                        moments: Dict[str, float]) -> Dict[str, Any]:
        """Design flexural reinforcement"""
        # Simplified flexural design
        Mu = moments["factored_moment"] * 1e6  # N⋅mm
        
        # Required steel area (simplified)
        As_req = Mu / (0.9 * self.steel.fy * 0.8 * geometry.effective_depth)
        
        # Minimum steel
        As_min = max(
            1.4 * geometry.width * geometry.height / self.steel.fy,
            0.0025 * geometry.width * geometry.height
        )
        
        As_final = max(As_req, As_min)
        
        return {{
            "status": "PASS",
            "required_steel_area": As_final,
            "minimum_steel_area": As_min,
            "utilization": As_req / As_final if As_final > 0 else 0
        }}
    
    def _design_shear(self, 
                     geometry: BeamGeometry,
                     loads: BeamLoads) -> Dict[str, Any]:
        """Design shear reinforcement"""
        # Simplified shear design
        wu = 1.4 * loads.dead_load + 1.7 * loads.live_load
        Vu = wu * geometry.span_length / 2
        
        # Concrete shear capacity
        Vc = 0.17 * (self.concrete.fc_prime**0.5) * geometry.width * geometry.effective_depth / 1000
        
        status = "PASS" if Vu <= 0.75 * Vc else "FAIL"
        
        return {{
            "status": status,
            "applied_shear": Vu,
            "concrete_capacity": Vc,
            "utilization": Vu / (0.75 * Vc) if Vc > 0 else 1.0
        }}
    
    def _check_deflection(self, 
                         geometry: BeamGeometry,
                         loads: BeamLoads) -> Dict[str, Any]:
        """Check deflection limits"""
        # Simplified deflection check
        service_load = loads.dead_load + loads.live_load
        
        # Immediate deflection (simplified)
        Ig = geometry.width * geometry.height**3 / 12
        Ec = self.concrete.elastic_modulus()
        deflection = 5 * service_load * geometry.span_length**4 / (384 * Ec * Ig)
        
        # Allowable deflection
        allowable = geometry.span_length / 250  # L/250 limit
        
        status = "PASS" if deflection <= allowable else "FAIL"
        
        return {{
            "status": status,
            "calculated_deflection": deflection,
            "allowable_deflection": allowable,
            "utilization": deflection / allowable if allowable > 0 else 1.0
        }}
    
    def _get_overall_status(self, statuses: list) -> str:
        """Determine overall design status"""
        if "ERROR" in statuses:
            return "ERROR"
        elif "FAIL" in statuses:
            return "FAIL"
        else:
            return "PASS"
'''
    
    def _generate_column_design(self, standard_name: str) -> str:
        """Generate column design class (simplified version)"""
        return f'''"""
{standard_name.title()} Column Design
{'=' * (len(standard_name) + 17)}

Column design implementation according to {standard_name.title()} standard.
"""

# Placeholder for column design implementation
# Similar structure to beam design but for columns

from structural_standards.base.design_base import StructuralMember

class {standard_name.title()}ColumnDesign(StructuralMember):
    """Column design placeholder"""
    
    def __init__(self, concrete, steel):
        super().__init__("column", "{standard_name.title()}")
        self.concrete = concrete
        self.steel = steel
    
    def design(self, geometry, loads):
        """Column design placeholder"""
        # TODO: Implement column design
        pass
'''
    
    def _generate_slab_design(self, standard_name: str) -> str:
        """Generate slab design class (simplified version)"""
        return f'''"""
{standard_name.title()} Slab Design
{'=' * (len(standard_name) + 15)}

Slab design implementation according to {standard_name.title()} standard.
"""

# Placeholder for slab design implementation

from structural_standards.base.design_base import StructuralMember

class {standard_name.title()}SlabDesign(StructuralMember):
    """Slab design placeholder"""
    
    def __init__(self, concrete, steel):
        super().__init__("slab", "{standard_name.title()}")
        self.concrete = concrete
        self.steel = steel
    
    def design(self, geometry, loads):
        """Slab design placeholder"""
        # TODO: Implement slab design
        pass
'''
    
    def _generate_load_combinations(self, standard_name: str) -> str:
        """Generate load combinations module"""
        return f'''"""
{standard_name.title()} Load Combinations
{'=' * (len(standard_name) + 21)}

Load combination implementation according to {standard_name.title()} standard.
"""

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class LoadCombination:
    """Load combination definition"""
    name: str
    equation: str
    factors: Dict[str, float]

class {standard_name.title()}LoadCombinations:
    """
    {standard_name.title()} load combinations
    """
    
    def __init__(self):
        """Initialize load combinations"""
        self.ultimate_combinations = [
            LoadCombination(
                name="Basic",
                equation="1.4D + 1.7L",
                factors={{"dead": 1.4, "live": 1.7}}
            ),
            LoadCombination(
                name="Wind",
                equation="1.2D + 1.6W + 0.5L",
                factors={{"dead": 1.2, "wind": 1.6, "live": 0.5}}
            )
        ]
        
        self.service_combinations = [
            LoadCombination(
                name="Service",
                equation="D + L",
                factors={{"dead": 1.0, "live": 1.0}}
            )
        ]
    
    def get_ultimate_combinations(self) -> List[LoadCombination]:
        """Get ultimate limit state combinations"""
        return self.ultimate_combinations
    
    def get_service_combinations(self) -> List[LoadCombination]:
        """Get serviceability combinations"""
        return self.service_combinations
'''


class MaterialCodeGenerator:
    """
    Generates material property classes
    """
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
    
    def generate_concrete_class(self, 
                              standard_name: str,
                              grade_system: Dict[str, float]) -> str:
        """
        Generate concrete class with specific grade system
        
        Parameters:
        -----------
        standard_name : str
            Name of the standard
        grade_system : dict
            Grade system mapping (grade -> fc_prime)
            
        Returns:
        --------
        str
            Generated concrete class code
        """
        # Implementation for specific concrete class generation
        pass
    
    def generate_steel_class(self, 
                           standard_name: str,
                           grade_system: Dict[str, Dict[str, float]]) -> str:
        """
        Generate steel class with specific grade system
        
        Parameters:
        -----------
        standard_name : str
            Name of the standard
        grade_system : dict
            Grade system mapping (grade -> properties)
            
        Returns:
        --------
        str
            Generated steel class code
        """
        # Implementation for specific steel class generation
        pass


class TestCodeGenerator:
    """
    Generates test code for design standards
    """
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
    
    def generate_test_suite(self, standard_name: str) -> Dict[str, str]:
        """
        Generate complete test suite for a standard
        
        Parameters:
        -----------
        standard_name : str
            Name of the standard
            
        Returns:
        --------
        dict
            Generated test files and contents
        """
        files = {}
        
        # Test configuration
        test_dir = self.config.output_dir / "tests" / f"test_{standard_name}"
        
        # Generate test files
        files[str(test_dir / "test_materials.py")] = self._generate_material_tests(standard_name)
        files[str(test_dir / "test_beam_design.py")] = self._generate_beam_tests(standard_name)
        files[str(test_dir / "test_integration.py")] = self._generate_integration_tests(standard_name)
        
        return files
    
    def _generate_material_tests(self, standard_name: str) -> str:
        """Generate material tests"""
        return f'''"""
Material Tests for {standard_name.title()}
"""

import pytest
from {self.config.package_name}.{standard_name}.materials import (
    {standard_name.title()}Concrete, {standard_name.title()}Steel
)

class Test{standard_name.title()}Concrete:
    """Test concrete material"""
    
    def test_concrete_creation(self):
        """Test concrete creation"""
        concrete = {standard_name.title()}Concrete(fc_prime=25.0)
        assert concrete.fc_prime == 25.0
        assert concrete.standard == "{standard_name.title()}"
    
    def test_elastic_modulus(self):
        """Test elastic modulus calculation"""
        concrete = {standard_name.title()}Concrete(fc_prime=25.0)
        ec = concrete.elastic_modulus()
        assert ec > 0
        assert isinstance(ec, float)

class Test{standard_name.title()}Steel:
    """Test steel material"""
    
    def test_steel_creation(self):
        """Test steel creation"""
        steel = {standard_name.title()}Steel(grade="GRADE400")
        assert steel.fy == 400
        assert steel.standard == "{standard_name.title()}"
    
    def test_bar_area(self):
        """Test bar area calculation"""
        steel = {standard_name.title()}Steel(bar_designation="N20")
        area = steel.bar_area()
        assert area > 0
        assert isinstance(area, float)
'''
    
    def _generate_beam_tests(self, standard_name: str) -> str:
        """Generate beam design tests"""
        return f'''"""
Beam Design Tests for {standard_name.title()}
"""

import pytest
from {self.config.package_name}.{standard_name}.materials import (
    {standard_name.title()}Concrete, {standard_name.title()}Steel
)
from {self.config.package_name}.{standard_name}.members import (
    {standard_name.title()}BeamDesign, BeamGeometry, BeamLoads, BeamType
)

class Test{standard_name.title()}BeamDesign:
    """Test beam design"""
    
    @pytest.fixture
    def materials(self):
        """Create test materials"""
        concrete = {standard_name.title()}Concrete(fc_prime=25.0)
        steel = {standard_name.title()}Steel(grade="GRADE400")
        return concrete, steel
    
    @pytest.fixture
    def beam_designer(self, materials):
        """Create beam designer"""
        concrete, steel = materials
        return {standard_name.title()}BeamDesign(concrete, steel)
    
    def test_beam_design_simple(self, beam_designer):
        """Test simple beam design"""
        geometry = BeamGeometry(
            width=300, height=600, effective_depth=550, span_length=6000
        )
        loads = BeamLoads(dead_load=5.0, live_load=8.0)
        
        result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
        
        assert result.member_type == "beam"
        assert result.overall_status in ["PASS", "FAIL", "WARNING"]
        assert "required_steel_area" in result.required_reinforcement
'''
    
    def _generate_integration_tests(self, standard_name: str) -> str:
        """Generate integration tests"""
        return f'''"""
Integration Tests for {standard_name.title()}
"""

import pytest
from {self.config.package_name}.{standard_name} import *

class Test{standard_name.title()}Integration:
    """Test standard integration"""
    
    def test_complete_design_workflow(self):
        """Test complete design workflow"""
        # Create materials
        concrete = {standard_name.title()}Concrete(fc_prime=25.0)
        steel = {standard_name.title()}Steel(grade="GRADE400")
        
        # Create designers
        beam_designer = {standard_name.title()}BeamDesign(concrete, steel)
        
        # Test design
        geometry = BeamGeometry(
            width=300, height=600, effective_depth=550, span_length=6000
        )
        loads = BeamLoads(dead_load=5.0, live_load=8.0)
        
        result = beam_designer.design(geometry, loads)
        
        # Verify result structure
        assert hasattr(result, 'member_type')
        assert hasattr(result, 'overall_status')
        assert hasattr(result, 'required_reinforcement')
'''


# Convenience functions
def generate_new_standard(standard_name: str, 
                         output_dir: Path,
                         author: str = "Generated") -> Dict[str, str]:
    """
    Generate a complete new standard implementation
    
    Parameters:
    -----------
    standard_name : str
        Name of the standard
    output_dir : Path
        Output directory
    author : str
        Author name
        
    Returns:
    --------
    dict
        Generated files
    """
    config = GeneratorConfig(
        output_dir=output_dir,
        package_name="structural_standards",
        author=author
    )
    
    generator = StandardCodeGenerator(config)
    return generator.generate_standard_package(standard_name)