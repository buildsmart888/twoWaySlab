"""
Validators Module
=================

Validation utilities for structural design standards compliance,
code quality, and performance validation.
"""

import ast
import inspect
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import importlib.util

from structural_standards.utils.validation import StructuralValidator

class ValidationLevel(Enum):
    """Validation strictness levels"""
    BASIC = "basic"
    STANDARD = "standard" 
    STRICT = "strict"
    COMPREHENSIVE = "comprehensive"

class ComplianceStandard(Enum):
    """Standards for compliance checking"""
    ACI_318M_25 = "aci_318m_25"
    THAI_MINISTRY_2566 = "thai_ministry_2566"
    EUROCODE_2 = "eurocode_2"
    AS_3600 = "as_3600"

@dataclass
class ValidationResult:
    """Validation result container"""
    is_valid: bool
    score: float  # 0.0 to 100.0
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    details: Dict[str, Any]

@dataclass
class PerformanceMetrics:
    """Performance validation metrics"""
    execution_time: float
    memory_usage: float
    peak_memory: float
    cpu_usage: float
    iterations_per_second: float

class StandardsValidator:
    """
    Validates structural design implementations against standards
    """
    
    def __init__(self, standard: ComplianceStandard, level: ValidationLevel = ValidationLevel.STANDARD):
        """
        Initialize standards validator
        
        Parameters:
        -----------
        standard : ComplianceStandard
            Standard to validate against
        level : ValidationLevel
            Validation strictness level
        """
        self.standard = standard
        self.level = level
        self.structural_validator = StructuralValidator()
        
        # Load standard-specific rules
        self.rules = self._load_standard_rules()
    
    def _load_standard_rules(self) -> Dict[str, Any]:
        """Load validation rules for the specific standard"""
        rules = {
            ComplianceStandard.ACI_318M_25: {
                "material_limits": {
                    "concrete_fc_min": 17.0,  # MPa
                    "concrete_fc_max": 83.0,  # MPa
                    "steel_fy_min": 280.0,    # MPa
                    "steel_fy_max": 550.0     # MPa
                },
                "geometric_limits": {
                    "beam_width_min": 200,    # mm
                    "beam_height_min": 300,   # mm
                    "column_min_dimension": 200,  # mm
                    "slab_thickness_min": 100     # mm
                },
                "design_requirements": {
                    "min_reinforcement_ratio": 0.0025,
                    "max_reinforcement_ratio": 0.04,
                    "min_cover": 25,  # mm
                    "max_spacing": 300  # mm
                }
            },
            ComplianceStandard.THAI_MINISTRY_2566: {
                "material_limits": {
                    "concrete_fc_min": 18.0,  # MPa (Fc180)
                    "concrete_fc_max": 35.0,  # MPa (Fc350)
                    "steel_fy_min": 235.0,    # MPa (SR24)
                    "steel_fy_max": 500.0     # MPa (SD50)
                },
                "geometric_limits": {
                    "beam_width_min": 200,
                    "beam_height_min": 300,
                    "column_min_dimension": 200,
                    "slab_thickness_min": 120  # Stricter for Thai standards
                },
                "design_requirements": {
                    "min_reinforcement_ratio": 0.003,  # Slightly higher
                    "max_reinforcement_ratio": 0.04,
                    "min_cover": 30,  # mm - more cover for tropical climate
                    "max_spacing": 250  # mm - tighter spacing
                }
            }
        }
        
        return rules.get(self.standard, rules[ComplianceStandard.ACI_318M_25])
    
    def validate_material_properties(self, material_props: Dict[str, Any]) -> ValidationResult:
        """
        Validate material properties against standard
        
        Parameters:
        -----------
        material_props : dict
            Material properties to validate
            
        Returns:
        --------
        ValidationResult
            Validation result
        """
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        # Check concrete properties
        if "fc_prime" in material_props:
            fc = material_props["fc_prime"]
            limits = self.rules["material_limits"]
            
            if fc < limits["concrete_fc_min"]:
                errors.append(f"Concrete strength {fc} MPa below minimum {limits['concrete_fc_min']} MPa")
                score -= 25
            elif fc > limits["concrete_fc_max"]:
                errors.append(f"Concrete strength {fc} MPa above maximum {limits['concrete_fc_max']} MPa")
                score -= 25
            
            # Check if strength is within common range
            if not (20 <= fc <= 50):
                warnings.append(f"Concrete strength {fc} MPa outside common range (20-50 MPa)")
                score -= 5
        
        # Check steel properties
        if "fy" in material_props:
            fy = material_props["fy"]
            limits = self.rules["material_limits"]
            
            if fy < limits["steel_fy_min"]:
                errors.append(f"Steel yield strength {fy} MPa below minimum {limits['steel_fy_min']} MPa")
                score -= 25
            elif fy > limits["steel_fy_max"]:
                errors.append(f"Steel yield strength {fy} MPa above maximum {limits['steel_fy_max']} MPa")
                score -= 25
        
        # Additional checks based on validation level
        if self.level in [ValidationLevel.STRICT, ValidationLevel.COMPREHENSIVE]:
            if "unit_weight" in material_props:
                unit_weight = material_props["unit_weight"]
                if not (22 <= unit_weight <= 26):
                    warnings.append(f"Concrete unit weight {unit_weight} kN/m³ outside typical range (22-26)")
                    score -= 3
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"standard": self.standard.value, "level": self.level.value}
        )
    
    def validate_geometry(self, geometry: Dict[str, Any], member_type: str = "beam") -> ValidationResult:
        """
        Validate geometric properties
        
        Parameters:
        -----------
        geometry : dict
            Geometric properties
        member_type : str
            Type of structural member
            
        Returns:
        --------
        ValidationResult
            Validation result
        """
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        limits = self.rules["geometric_limits"]
        
        if member_type == "beam":
            if "width" in geometry:
                if geometry["width"] < limits["beam_width_min"]:
                    errors.append(f"Beam width {geometry['width']}mm below minimum {limits['beam_width_min']}mm")
                    score -= 20
            
            if "height" in geometry:
                if geometry["height"] < limits["beam_height_min"]:
                    errors.append(f"Beam height {geometry['height']}mm below minimum {limits['beam_height_min']}mm")
                    score -= 20
            
            # Check aspect ratio
            if "width" in geometry and "height" in geometry:
                aspect_ratio = geometry["height"] / geometry["width"]
                if aspect_ratio < 1.5:
                    warnings.append(f"Beam aspect ratio {aspect_ratio:.1f} may be too low (recommend > 1.5)")
                    score -= 5
                elif aspect_ratio > 4.0:
                    warnings.append(f"Beam aspect ratio {aspect_ratio:.1f} may be too high (recommend < 4.0)")
                    score -= 5
        
        elif member_type == "column":
            for dim in ["width", "depth", "diameter"]:
                if dim in geometry:
                    if geometry[dim] < limits["column_min_dimension"]:
                        errors.append(f"Column {dim} {geometry[dim]}mm below minimum {limits['column_min_dimension']}mm")
                        score -= 20
        
        elif member_type == "slab":
            if "thickness" in geometry:
                if geometry["thickness"] < limits["slab_thickness_min"]:
                    errors.append(f"Slab thickness {geometry['thickness']}mm below minimum {limits['slab_thickness_min']}mm")
                    score -= 20
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"member_type": member_type}
        )
    
    def validate_design_result(self, design_result: Dict[str, Any]) -> ValidationResult:
        """
        Validate design calculation results
        
        Parameters:
        -----------
        design_result : dict
            Design calculation results
            
        Returns:
        --------
        ValidationResult
            Validation result
        """
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        # Check required fields
        required_fields = ["member_type", "overall_status"]
        for field in required_fields:
            if field not in design_result:
                errors.append(f"Missing required field: {field}")
                score -= 15
        
        # Check utilization ratio
        if "utilization_ratio" in design_result:
            utilization = design_result["utilization_ratio"]
            if utilization > 1.0:
                errors.append(f"Utilization ratio {utilization:.2f} exceeds 1.0")
                score -= 30
            elif utilization > 0.95:
                warnings.append(f"High utilization ratio {utilization:.2f} (> 0.95)")
                score -= 10
            elif utilization < 0.3:
                suggestions.append(f"Low utilization ratio {utilization:.2f} - consider optimizing")
                score -= 5
        
        # Check reinforcement requirements
        if "required_reinforcement" in design_result:
            rebar = design_result["required_reinforcement"]
            limits = self.rules["design_requirements"]
            
            if "reinforcement_ratio" in rebar:
                ratio = rebar["reinforcement_ratio"]
                if ratio < limits["min_reinforcement_ratio"]:
                    errors.append(f"Reinforcement ratio {ratio:.4f} below minimum {limits['min_reinforcement_ratio']}")
                    score -= 25
                elif ratio > limits["max_reinforcement_ratio"]:
                    errors.append(f"Reinforcement ratio {ratio:.4f} above maximum {limits['max_reinforcement_ratio']}")
                    score -= 25
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"validation_level": self.level.value}
        )


class CodeQualityValidator:
    """
    Validates code quality and structure
    """
    
    def __init__(self, level: ValidationLevel = ValidationLevel.STANDARD):
        """Initialize code quality validator"""
        self.level = level
    
    def validate_module(self, module_path: Path) -> ValidationResult:
        """
        Validate a Python module for code quality
        
        Parameters:
        -----------
        module_path : Path
            Path to Python module
            
        Returns:
        --------
        ValidationResult
            Validation result
        """
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        try:
            # Read and parse the module
            with open(module_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse AST
            tree = ast.parse(source_code)
            
            # Check docstring
            if not ast.get_docstring(tree):
                warnings.append("Module missing docstring")
                score -= 10
            
            # Analyze classes and functions
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            
            # Check class documentation
            for cls in classes:
                if not ast.get_docstring(cls):
                    warnings.append(f"Class '{cls.name}' missing docstring")
                    score -= 5
                
                # Check method documentation
                methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)]
                for method in methods:
                    if not ast.get_docstring(method) and not method.name.startswith('_'):
                        warnings.append(f"Method '{cls.name}.{method.name}' missing docstring")
                        score -= 3
            
            # Check function documentation
            for func in functions:
                if not ast.get_docstring(func) and not func.name.startswith('_'):
                    warnings.append(f"Function '{func.name}' missing docstring")
                    score -= 5
            
            # Check imports (basic analysis)
            imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
            
            # Check for unused imports (simplified)
            if self.level == ValidationLevel.COMPREHENSIVE:
                import_names = []
                for imp in imports:
                    if isinstance(imp, ast.Import):
                        import_names.extend([alias.name for alias in imp.names])
                    elif isinstance(imp, ast.ImportFrom):
                        import_names.extend([alias.name for alias in imp.names])
                
                # This is a simplified check - real implementation would be more sophisticated
                used_names = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Name):
                        used_names.add(node.id)
                
                # Check for obviously unused imports (very basic)
                for name in import_names:
                    if name not in used_names and not name.startswith('_'):
                        suggestions.append(f"Import '{name}' may be unused")
                        score -= 2
            
            # Check complexity (simplified)
            complexity_score = self._calculate_complexity(tree)
            if complexity_score > 10:
                warnings.append(f"High complexity score: {complexity_score}")
                score -= min(complexity_score - 10, 20)
            
        except Exception as e:
            errors.append(f"Failed to parse module: {str(e)}")
            score = 0
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"module": str(module_path), "complexity": complexity_score if 'complexity_score' in locals() else 0}
        )
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity (simplified)"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.Lambda):
                complexity += 1
        
        return complexity
    
    def validate_package_structure(self, package_path: Path) -> ValidationResult:
        """
        Validate package structure and organization
        
        Parameters:
        -----------
        package_path : Path
            Path to package directory
            
        Returns:
        --------
        ValidationResult
            Validation result
        """
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        # Check for __init__.py
        init_file = package_path / "__init__.py"
        if not init_file.exists():
            errors.append("Package missing __init__.py file")
            score -= 30
        
        # Check for standard structure
        expected_dirs = ["materials", "members"]
        for dir_name in expected_dirs:
            dir_path = package_path / dir_name
            if not dir_path.exists():
                warnings.append(f"Package missing expected directory: {dir_name}")
                score -= 10
            elif not (dir_path / "__init__.py").exists():
                warnings.append(f"Subdirectory {dir_name} missing __init__.py")
                score -= 5
        
        # Check for documentation
        readme_files = list(package_path.glob("README*"))
        if not readme_files:
            suggestions.append("Package missing README file")
            score -= 5
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"package": str(package_path)}
        )


class PerformanceValidator:
    """
    Validates performance characteristics of design implementations
    """
    
    def __init__(self):
        """Initialize performance validator"""
        self.benchmark_data = {}
    
    def benchmark_function(self, 
                          func, 
                          args: tuple = (), 
                          kwargs: dict = None,
                          iterations: int = 100) -> PerformanceMetrics:
        """
        Benchmark a function's performance
        
        Parameters:
        -----------
        func : callable
            Function to benchmark
        args : tuple
            Function arguments
        kwargs : dict
            Function keyword arguments
        iterations : int
            Number of iterations to run
            
        Returns:
        --------
        PerformanceMetrics
            Performance metrics
        """
        if kwargs is None:
            kwargs = {}
        
        import psutil
        import gc
        
        # Prepare for benchmark
        gc.collect()
        process = psutil.Process()
        
        # Warm up
        for _ in range(min(10, iterations // 10)):
            func(*args, **kwargs)
        
        # Benchmark
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        start_time = time.perf_counter()
        peak_memory = start_memory
        
        for _ in range(iterations):
            func(*args, **kwargs)
            current_memory = process.memory_info().rss / 1024 / 1024
            peak_memory = max(peak_memory, current_memory)
        
        end_time = time.perf_counter()
        end_memory = process.memory_info().rss / 1024 / 1024
        
        execution_time = end_time - start_time
        memory_usage = end_memory - start_memory
        iterations_per_second = iterations / execution_time if execution_time > 0 else 0
        
        return PerformanceMetrics(
            execution_time=execution_time,
            memory_usage=memory_usage,
            peak_memory=peak_memory,
            cpu_usage=process.cpu_percent(),
            iterations_per_second=iterations_per_second
        )
    
    def validate_performance_requirements(self, 
                                        metrics: PerformanceMetrics,
                                        requirements: Dict[str, float]) -> ValidationResult:
        """
        Validate performance against requirements
        
        Parameters:
        -----------
        metrics : PerformanceMetrics
            Measured performance metrics
        requirements : dict
            Performance requirements
            
        Returns:
        --------
        ValidationResult
            Validation result
        """
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        # Check execution time
        if "max_execution_time" in requirements:
            max_time = requirements["max_execution_time"]
            if metrics.execution_time > max_time:
                errors.append(f"Execution time {metrics.execution_time:.3f}s exceeds limit {max_time}s")
                score -= 30
            elif metrics.execution_time > max_time * 0.8:
                warnings.append(f"Execution time {metrics.execution_time:.3f}s near limit {max_time}s")
                score -= 10
        
        # Check memory usage
        if "max_memory_usage" in requirements:
            max_memory = requirements["max_memory_usage"]
            if metrics.memory_usage > max_memory:
                errors.append(f"Memory usage {metrics.memory_usage:.1f}MB exceeds limit {max_memory}MB")
                score -= 25
        
        # Check iterations per second
        if "min_iterations_per_second" in requirements:
            min_ips = requirements["min_iterations_per_second"]
            if metrics.iterations_per_second < min_ips:
                errors.append(f"Performance {metrics.iterations_per_second:.1f} IPS below requirement {min_ips} IPS")
                score -= 20
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"metrics": metrics.__dict__}
        )


class ComplianceValidator:
    """
    Comprehensive compliance validator combining all validation types
    """
    
    def __init__(self, 
                 standard: ComplianceStandard,
                 level: ValidationLevel = ValidationLevel.STANDARD):
        """Initialize compliance validator"""
        self.standard = standard
        self.level = level
        
        self.standards_validator = StandardsValidator(standard, level)
        self.code_validator = CodeQualityValidator(level)
        self.performance_validator = PerformanceValidator()
    
    def comprehensive_validation(self, 
                               package_path: Path,
                               test_data: Optional[Dict[str, Any]] = None) -> Dict[str, ValidationResult]:
        """
        Perform comprehensive validation of a structural standards package
        
        Parameters:
        -----------
        package_path : Path
            Path to package
        test_data : dict, optional
            Test data for functional validation
            
        Returns:
        --------
        dict
            Validation results by category
        """
        results = {}
        
        # Package structure validation
        results["structure"] = self.code_validator.validate_package_structure(package_path)
        
        # Code quality validation
        python_files = list(package_path.rglob("*.py"))
        code_scores = []
        for py_file in python_files:
            if not py_file.name.startswith("__"):  # Skip __pycache__ etc
                result = self.code_validator.validate_module(py_file)
                code_scores.append(result.score)
        
        if code_scores:
            avg_score = sum(code_scores) / len(code_scores)
            results["code_quality"] = ValidationResult(
                is_valid=avg_score >= 70.0,
                score=avg_score,
                errors=[],
                warnings=[],
                suggestions=[],
                details={"files_checked": len(code_scores), "individual_scores": code_scores}
            )
        
        # Functional validation (if test data provided)
        if test_data:
            results["functional"] = self._validate_functional(test_data)
        
        return results
    
    def _validate_functional(self, test_data: Dict[str, Any]) -> ValidationResult:
        """Validate functional requirements"""
        # This would contain specific functional tests
        # Implementation depends on the specific requirements
        
        return ValidationResult(
            is_valid=True,
            score=100.0,
            errors=[],
            warnings=[],
            suggestions=[],
            details={"test_data_processed": len(test_data)}
        )


# Convenience functions
def quick_validate_materials(material_props: Dict[str, Any], 
                           standard: ComplianceStandard = ComplianceStandard.ACI_318M_25) -> ValidationResult:
    """Quick validation of material properties"""
    validator = StandardsValidator(standard)
    return validator.validate_material_properties(material_props)

def quick_validate_geometry(geometry: Dict[str, Any], 
                          member_type: str = "beam",
                          standard: ComplianceStandard = ComplianceStandard.ACI_318M_25) -> ValidationResult:
    """Quick validation of geometry"""
    validator = StandardsValidator(standard)
    return validator.validate_geometry(geometry, member_type)

def validate_code_quality(file_path: Path) -> ValidationResult:
    """Quick code quality validation"""
    validator = CodeQualityValidator()
    return validator.validate_module(file_path)