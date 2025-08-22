"""
Base Interface for Structural Design Standards
==============================================

Abstract base class defining the common interface for all structural design standards.
This ensures consistency across different national and international standards.

คลาสฐานนามธรรมสำหรับมาตรฐานการออกแบบโครงสร้างทุกประเภท
เพื่อให้แน่ใจว่ามีความสอดคล้องกันระหว่างมาตรฐานต่างประเทศ
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass
from enum import Enum

class LoadType(Enum):
    """Load types for structural design"""
    DEAD = "dead"
    LIVE = "live"
    WIND = "wind"
    SEISMIC = "seismic"
    SNOW = "snow"
    THERMAL = "thermal"

class MemberType(Enum):
    """Structural member types"""
    BEAM = "beam"
    COLUMN = "column"
    SLAB = "slab"
    WALL = "wall"
    FOOTING = "footing"
    DIAPHRAGM = "diaphragm"

class DesignMethod(Enum):
    """Design methodology"""
    ALLOWABLE_STRESS = "allowable_stress"
    LOAD_RESISTANCE_FACTOR = "lrfd"
    LIMIT_STATE = "limit_state"

@dataclass
class StandardInfo:
    """Information about a design standard"""
    name: str
    version: str
    country: str
    language: str
    organization: str
    year_published: int
    design_method: DesignMethod
    units_system: str  # 'SI', 'Imperial', 'Mixed'

@dataclass
class MaterialProperties:
    """Standard material properties"""
    name: str
    grade: str
    strength: float
    elastic_modulus: float
    unit_weight: float
    poisson_ratio: float
    thermal_expansion: float
    properties: Dict[str, Any]

@dataclass
class SafetyFactors:
    """Safety factors for different load types and materials"""
    concrete: float
    steel: float
    dead_load: float
    live_load: float
    wind_load: float
    seismic_load: float
    additional_factors: Dict[str, float]

class StructuralStandard(ABC):
    """
    Abstract base class for all structural design standards
    
    This class defines the minimum interface that all structural design
    standards must implement, ensuring consistency and interoperability
    between different national and international standards.
    
    คลาสฐานนามธรรมสำหรับมาตรฐานการออกแบบโครงสร้างทุกประเภท
    
    กำหนด interface ขั้นต่ำที่มาตรฐานการออกแบบโครงสร้างทุกประเภทต้องมี
    เพื่อให้แน่ใจว่ามีความสอดคล้องและสามารถทำงานร่วมกันได้
    ระหว่างมาตรฐานต่างประเทศและนานาชาติ
    """
    
    def __init__(self, info: StandardInfo):
        """
        Initialize structural standard
        
        Parameters:
        -----------
        info : StandardInfo
            Information about the standard
        """
        self.info = info
        self._material_database: Dict[str, MaterialProperties] = {}
        self._safety_factors: Optional[SafetyFactors] = None
    
    @property
    def name(self) -> str:
        """Standard name"""
        return self.info.name
    
    @property
    def version(self) -> str:
        """Standard version"""
        return self.info.version
    
    @property
    def country(self) -> str:
        """Country of origin"""
        return self.info.country
    
    @property
    def language(self) -> str:
        """Primary language"""
        return self.info.language
    
    # Abstract methods that must be implemented by all standards
    
    @abstractmethod
    def get_material_properties(self, material_type: str, grade: str) -> MaterialProperties:
        """
        Get material properties for specified type and grade
        
        Parameters:
        -----------
        material_type : str
            Type of material ('concrete', 'steel', etc.)
        grade : str
            Material grade designation
            
        Returns:
        --------
        MaterialProperties
            Complete material properties
        """
        pass
    
    @abstractmethod
    def get_safety_factors(self) -> SafetyFactors:
        """
        Get safety factors for the standard
        
        Returns:
        --------
        SafetyFactors
            Safety factors for materials and loads
        """
        pass
    
    @abstractmethod
    def get_load_combinations(self, loads: Dict[LoadType, float]) -> Dict[str, float]:
        """
        Calculate load combinations per the standard
        
        Parameters:
        -----------
        loads : Dict[LoadType, float]
            Applied loads by type
            
        Returns:
        --------
        Dict[str, float]
            Load combination results
        """
        pass
    
    @abstractmethod
    def calculate_design_strength(self, 
                                nominal_strength: float,
                                member_type: MemberType,
                                failure_mode: str) -> float:
        """
        Calculate design strength with appropriate reduction factors
        
        Parameters:
        -----------
        nominal_strength : float
            Nominal strength
        member_type : MemberType
            Type of structural member
        failure_mode : str
            Mode of failure ('flexure', 'shear', 'compression', etc.)
            
        Returns:
        --------
        float
            Design strength
        """
        pass
    
    @abstractmethod
    def check_serviceability(self, 
                           deflection: float,
                           span: float,
                           member_type: MemberType) -> Dict[str, bool]:
        """
        Check serviceability requirements
        
        Parameters:
        -----------
        deflection : float
            Calculated deflection
        span : float
            Member span
        member_type : MemberType
            Type of structural member
            
        Returns:
        --------
        Dict[str, bool]
            Serviceability check results
        """
        pass
    
    # Common utility methods
    
    def get_concrete_grades(self) -> List[str]:
        """Get available concrete grades"""
        return [grade for grade, props in self._material_database.items() 
                if 'concrete' in props.name.lower()]
    
    def get_steel_grades(self) -> List[str]:
        """Get available steel grades"""
        return [grade for grade, props in self._material_database.items() 
                if 'steel' in props.name.lower()]
    
    def compare_with_standard(self, other: 'StructuralStandard') -> Dict[str, Any]:
        """
        Compare this standard with another standard
        
        Parameters:
        -----------
        other : StructuralStandard
            Another standard to compare with
            
        Returns:
        --------
        Dict[str, Any]
            Comparison results
        """
        comparison = {
            'standards': {
                'this': f"{self.name} {self.version}",
                'other': f"{other.name} {other.version}"
            },
            'countries': {
                'this': self.country,
                'other': other.country
            },
            'design_methods': {
                'this': self.info.design_method.value,
                'other': other.info.design_method.value
            },
            'units_systems': {
                'this': self.info.units_system,
                'other': other.info.units_system
            }
        }
        
        # Compare safety factors if both available
        try:
            this_sf = self.get_safety_factors()
            other_sf = other.get_safety_factors()
            
            comparison['safety_factors'] = {
                'concrete': {'this': this_sf.concrete, 'other': other_sf.concrete},
                'steel': {'this': this_sf.steel, 'other': other_sf.steel},
                'dead_load': {'this': this_sf.dead_load, 'other': other_sf.dead_load},
                'live_load': {'this': this_sf.live_load, 'other': other_sf.live_load},
            }
        except Exception:
            comparison['safety_factors'] = "Comparison not available"
        
        return comparison
    
    def validate_input(self, parameter: str, value: Any, 
                      min_val: Optional[float] = None,
                      max_val: Optional[float] = None,
                      allowed_values: Optional[List[Any]] = None) -> bool:
        """
        Validate input parameters
        
        Parameters:
        -----------
        parameter : str
            Parameter name
        value : Any
            Value to validate
        min_val : float, optional
            Minimum allowed value
        max_val : float, optional
            Maximum allowed value
        allowed_values : List[Any], optional
            List of allowed values
            
        Returns:
        --------
        bool
            True if valid
            
        Raises:
        -------
        ValueError
            If validation fails
        """
        if allowed_values is not None and value not in allowed_values:
            raise ValueError(f"{parameter} must be one of {allowed_values}, got {value}")
        
        if isinstance(value, (int, float)):
            if min_val is not None and value < min_val:
                raise ValueError(f"{parameter} must be >= {min_val}, got {value}")
            if max_val is not None and value > max_val:
                raise ValueError(f"{parameter} must be <= {max_val}, got {value}")
        
        return True
    
    def __str__(self) -> str:
        """String representation of the standard"""
        return f"{self.name} {self.version} ({self.country})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"StructuralStandard(name='{self.name}', version='{self.version}', "
                f"country='{self.country}', language='{self.language}')")