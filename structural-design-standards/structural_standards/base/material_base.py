"""
Base Material Classes
=====================

Abstract base classes for material modeling in structural design.
Provides common interface for concrete, steel, and other materials.

คลาสฐานสำหรับการจำลองวัสดุในการออกแบบโครงสร้าง
มี interface ร่วมสำหรับคอนกรีต เหล็ก และวัสดุอื่นๆ
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from enum import Enum
import math

class MaterialType(Enum):
    """Material type enumeration"""
    CONCRETE = "concrete"
    STEEL = "steel" 
    REINFORCEMENT = "reinforcement"
    MASONRY = "masonry"
    TIMBER = "timber"
    COMPOSITE = "composite"

class ConcreteType(Enum):
    """Concrete type enumeration"""
    NORMAL_WEIGHT = "normal_weight"
    LIGHTWEIGHT = "lightweight"
    HIGH_STRENGTH = "high_strength"
    PRECAST = "precast"
    PRESTRESSED = "prestressed"

class SteelType(Enum):
    """Steel type enumeration"""
    MILD_STEEL = "mild_steel"
    HIGH_STRENGTH = "high_strength"
    STAINLESS = "stainless"
    WEATHERING = "weathering"

@dataclass
class StressStrainPoint:
    """Stress-strain point for material behavior"""
    strain: float
    stress: float

@dataclass
class MaterialBehavior:
    """Material behavior characteristics"""
    elastic_modulus: float
    poisson_ratio: float
    thermal_expansion: float
    stress_strain_curve: List[StressStrainPoint] = field(default_factory=list)
    ultimate_strain: Optional[float] = None
    fracture_energy: Optional[float] = None

class Material(ABC):
    """
    Abstract base class for all materials
    
    คลาสฐานนามธรรมสำหรับวัสดุทุกประเภท
    """
    
    def __init__(self, 
                 name: str,
                 grade: str,
                 unit_weight: float,
                 standard: str):
        """
        Initialize material
        
        Parameters:
        -----------
        name : str
            Material name
        grade : str
            Material grade designation
        unit_weight : float
            Unit weight (kN/m³ for SI, pcf for Imperial)
        standard : str
            Design standard reference
        """
        self.name = name
        self.grade = grade
        self.unit_weight = unit_weight
        self.standard = standard
        self.material_type: Optional[MaterialType] = None
        self.behavior: Optional[MaterialBehavior] = None
        
    @abstractmethod
    def get_design_properties(self) -> Dict[str, float]:
        """Get design properties for the material"""
        pass
    
    @abstractmethod
    def validate_grade(self, grade: str) -> bool:
        """Validate if the grade is acceptable for this material"""
        pass
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.name} {self.grade}"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return (f"{self.__class__.__name__}(name='{self.name}', "
                f"grade='{self.grade}', unit_weight={self.unit_weight})")

class ConcreteMaterial(Material):
    """
    Base class for concrete materials
    
    คลาสฐานสำหรับวัสดุคอนกรีต
    """
    
    def __init__(self,
                 fc_prime: float,
                 unit_weight: float = 24.0,
                 concrete_type: ConcreteType = ConcreteType.NORMAL_WEIGHT,
                 aggregate_size: float = 25.0,
                 standard: str = "Generic"):
        """
        Initialize concrete material
        
        Parameters:
        -----------
        fc_prime : float
            Specified compressive strength (MPa or psi)
        unit_weight : float
            Unit weight (kN/m³ or pcf)
        concrete_type : ConcreteType
            Type of concrete
        aggregate_size : float
            Maximum aggregate size (mm or inches)
        standard : str
            Design standard
        """
        super().__init__(
            name=f"Concrete fc'={fc_prime}",
            grade=f"fc{int(fc_prime)}",
            unit_weight=unit_weight,
            standard=standard
        )
        
        self.fc_prime = fc_prime
        self.concrete_type = concrete_type
        self.aggregate_size = aggregate_size
        self.material_type = MaterialType.CONCRETE
        
        # Validate inputs
        self._validate_inputs()
        
    def _validate_inputs(self) -> None:
        """Validate input parameters"""
        if self.fc_prime <= 0:
            raise ValueError("Compressive strength must be positive")
        if self.unit_weight <= 0:
            raise ValueError("Unit weight must be positive")
        if self.aggregate_size <= 0:
            raise ValueError("Aggregate size must be positive")
    
    @abstractmethod
    def elastic_modulus(self) -> float:
        """Calculate elastic modulus"""
        pass
    
    @abstractmethod
    def modulus_of_rupture(self) -> float:
        """Calculate modulus of rupture (tensile strength)"""
        pass
    
    def get_design_properties(self) -> Dict[str, float]:
        """Get concrete design properties"""
        return {
            'fc_prime': self.fc_prime,
            'elastic_modulus': self.elastic_modulus(),
            'modulus_of_rupture': self.modulus_of_rupture(),
            'unit_weight': self.unit_weight,
            'aggregate_size': self.aggregate_size,
        }
    
    def validate_grade(self, grade: str) -> bool:
        """Validate concrete grade"""
        # Basic validation - can be overridden by subclasses
        try:
            # Extract numeric part from grade
            numeric_part = ''.join(filter(str.isdigit, grade))
            if numeric_part:
                strength = float(numeric_part)
                return 10 <= strength <= 150  # Reasonable range for concrete
        except ValueError:
            pass
        return False
    
    def density(self) -> float:
        """Get concrete density in kg/m³"""
        # Convert from kN/m³ to kg/m³ assuming g = 9.81 m/s²
        return self.unit_weight * 1000 / 9.81
    
    def is_lightweight(self) -> bool:
        """Check if concrete is lightweight"""
        return (self.concrete_type == ConcreteType.LIGHTWEIGHT or 
                self.unit_weight < 20.0)  # kN/m³
    
    def is_high_strength(self) -> bool:
        """Check if concrete is high strength"""
        # Typically fc' > 55 MPa (8000 psi) is considered high strength
        return self.fc_prime > 55.0

class SteelMaterial(Material):
    """
    Base class for steel materials
    
    คลาสฐานสำหรับวัสดุเหล็ก
    """
    
    def __init__(self,
                 fy: float,
                 fu: Optional[float] = None,
                 steel_type: SteelType = SteelType.MILD_STEEL,
                 unit_weight: float = 77.0,
                 standard: str = "Generic"):
        """
        Initialize steel material
        
        Parameters:
        -----------
        fy : float
            Yield strength (MPa or psi)
        fu : float, optional
            Ultimate tensile strength (MPa or psi)
        steel_type : SteelType
            Type of steel
        unit_weight : float
            Unit weight (kN/m³ or pcf), default 77.0 kN/m³
        standard : str
            Design standard
        """
        super().__init__(
            name=f"Steel fy={fy}",
            grade=f"fy{int(fy)}",
            unit_weight=unit_weight,
            standard=standard
        )
        
        self.fy = fy
        self.fu = fu if fu is not None else fy * 1.5  # Typical assumption
        self.steel_type = steel_type
        self.material_type = MaterialType.STEEL
        
        # Standard elastic modulus for steel
        self.Es = 200000.0  # MPa (SI) or 29000000 psi (Imperial)
        
        # Validate inputs
        self._validate_inputs()
        
    def _validate_inputs(self) -> None:
        """Validate input parameters"""
        if self.fy <= 0:
            raise ValueError("Yield strength must be positive")
        if self.fu <= 0:
            raise ValueError("Ultimate strength must be positive")
        if self.fu < self.fy:
            raise ValueError("Ultimate strength must be >= yield strength")
        if self.unit_weight <= 0:
            raise ValueError("Unit weight must be positive")
    
    def elastic_modulus(self) -> float:
        """Get elastic modulus"""
        return self.Es
    
    def get_design_properties(self) -> Dict[str, float]:
        """Get steel design properties"""
        return {
            'fy': self.fy,
            'fu': self.fu,
            'elastic_modulus': self.elastic_modulus(),
            'unit_weight': self.unit_weight,
            'yield_ratio': self.fy / self.fu,
        }
    
    def validate_grade(self, grade: str) -> bool:
        """Validate steel grade"""
        # Basic validation - can be overridden by subclasses
        try:
            # Extract numeric part from grade  
            numeric_part = ''.join(filter(str.isdigit, grade))
            if numeric_part:
                strength = float(numeric_part)
                return 200 <= strength <= 800  # Reasonable range for steel (MPa)
        except ValueError:
            pass
        return False
    
    def ductility_ratio(self) -> float:
        """Calculate ductility ratio"""
        return self.fu / self.fy
    
    def is_high_strength(self) -> bool:
        """Check if steel is high strength"""
        # Typically fy > 420 MPa (60 ksi) is considered high strength
        return self.fy > 420.0

class ReinforcementSteel(SteelMaterial):
    """
    Reinforcement steel (rebar) material
    
    เหล็กเสริม (เหล็กข้ออ้อย)
    """
    
    def __init__(self,
                 fy: float,
                 bar_designation: str,
                 surface_condition: str = "deformed",
                 standard: str = "Generic"):
        """
        Initialize reinforcement steel
        
        Parameters:
        -----------
        fy : float
            Yield strength
        bar_designation : str
            Bar designation (e.g., "DB20", "#8", "20M")
        surface_condition : str
            "plain" or "deformed"
        standard : str
            Design standard
        """
        super().__init__(fy=fy, standard=standard)
        
        self.bar_designation = bar_designation
        self.surface_condition = surface_condition
        self.material_type = MaterialType.REINFORCEMENT
        
        # Update name to include bar designation
        self.name = f"Rebar {bar_designation} fy={fy}"
        self.grade = bar_designation
    
    @abstractmethod
    def bar_area(self) -> float:
        """Get cross-sectional area of the bar (mm² or in²)"""
        pass
    
    @abstractmethod
    def bar_diameter(self) -> float:
        """Get nominal diameter of the bar (mm or inches)"""
        pass
    
    def bar_perimeter(self) -> float:
        """Get perimeter of the bar"""
        return math.pi * self.bar_diameter()
    
    def development_length_factor(self) -> float:
        """Get development length factor based on surface condition"""
        if self.surface_condition == "deformed":
            return 1.0
        else:  # plain bars
            return 1.5  # Typically require longer development length

class MaterialDatabase:
    """
    Database for storing and retrieving material properties
    
    ฐานข้อมูลสำหรับเก็บและเรียกใช้คุณสมบัติของวัสดุ
    """
    
    def __init__(self, standard_name: str):
        """
        Initialize material database
        
        Parameters:
        -----------
        standard_name : str
            Name of the design standard
        """
        self.standard_name = standard_name
        self._concrete_materials: Dict[str, ConcreteMaterial] = {}
        self._steel_materials: Dict[str, SteelMaterial] = {}
        self._reinforcement_materials: Dict[str, ReinforcementSteel] = {}
    
    def add_concrete(self, grade: str, material: ConcreteMaterial) -> None:
        """Add concrete material to database"""
        self._concrete_materials[grade] = material
    
    def add_steel(self, grade: str, material: SteelMaterial) -> None:
        """Add steel material to database"""
        self._steel_materials[grade] = material
    
    def add_reinforcement(self, designation: str, material: ReinforcementSteel) -> None:
        """Add reinforcement material to database"""
        self._reinforcement_materials[designation] = material
    
    def get_concrete(self, grade: str) -> ConcreteMaterial:
        """Get concrete material by grade"""
        if grade not in self._concrete_materials:
            raise ValueError(f"Concrete grade '{grade}' not found in {self.standard_name} database")
        return self._concrete_materials[grade]
    
    def get_steel(self, grade: str) -> SteelMaterial:
        """Get steel material by grade"""
        if grade not in self._steel_materials:
            raise ValueError(f"Steel grade '{grade}' not found in {self.standard_name} database")
        return self._steel_materials[grade]
    
    def get_reinforcement(self, designation: str) -> ReinforcementSteel:
        """Get reinforcement material by designation"""
        if designation not in self._reinforcement_materials:
            raise ValueError(f"Reinforcement '{designation}' not found in {self.standard_name} database")
        return self._reinforcement_materials[designation]
    
    def list_concrete_grades(self) -> List[str]:
        """List available concrete grades"""
        return list(self._concrete_materials.keys())
    
    def list_steel_grades(self) -> List[str]:
        """List available steel grades"""
        return list(self._steel_materials.keys())
    
    def list_reinforcement_designations(self) -> List[str]:
        """List available reinforcement designations"""
        return list(self._reinforcement_materials.keys())
    
    def get_all_materials(self) -> Dict[str, Dict[str, Material]]:
        """Get all materials in the database"""
        return {
            'concrete': dict(self._concrete_materials),
            'steel': dict(self._steel_materials),
            'reinforcement': dict(self._reinforcement_materials)
        }