#!/usr/bin/env python3
"""
Standards Compliance Checker
=============================

Automated compliance checking for structural design standards.
Validates code against design standards, checks implementation completeness,
and ensures compliance with international codes.

Usage:
    python scripts/check_standards.py [options]

Options:
    --standard STANDARD  Check specific standard (aci, thai, all)
    --level LEVEL        Validation level (basic, standard, strict, comprehensive)
    --output DIR         Output directory for reports
    --fix                Attempt to fix issues automatically
    --verbose            Verbose output
    --report-format      Report format (json, html, markdown)
"""

import os
import sys
import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import importlib.util

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import our validation tools
try:
    from tools.validators import (
        StandardsValidator, CodeQualityValidator, ComplianceValidator,
        ValidationLevel, ComplianceStandard, ValidationResult
    )
except ImportError:
    print("❌ Unable to import validation tools. Make sure the tools package is available.")
    sys.exit(1)

@dataclass
class ComplianceReport:
    """Complete compliance report"""
    timestamp: float
    standard: str
    validation_level: str
    overall_score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    warnings: int
    categories: Dict[str, ValidationResult]
    recommendations: List[str]
    summary: str

class StandardsChecker:
    """Main standards compliance checker"""
    
    def __init__(self, standard: str, level: ValidationLevel, output_dir: Path):
        """Initialize checker"""
        self.standard = self._parse_standard(standard)
        self.level = level
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize validators
        self.standards_validator = StandardsValidator(self.standard, level)
        self.code_validator = CodeQualityValidator(level)
        self.compliance_validator = ComplianceValidator(self.standard, level)
    
    def _parse_standard(self, standard: str) -> ComplianceStandard:
        """Parse standard string to enum"""
        standard_map = {
            "aci": ComplianceStandard.ACI_318M_25,
            "thai": ComplianceStandard.THAI_MINISTRY_2566,
            "eurocode": ComplianceStandard.EUROCODE_2,
            "as3600": ComplianceStandard.AS_3600
        }
        
        if standard.lower() in standard_map:
            return standard_map[standard.lower()]
        else:
            print(f"⚠️  Unknown standard '{standard}', defaulting to ACI 318M-25")
            return ComplianceStandard.ACI_318M_25
    
    def check_package_structure(self) -> ValidationResult:
        """Check package structure compliance"""
        print("🏗️  Checking package structure...")
        
        # Find the main package
        structural_standards_dir = project_root / "structural_standards"
        
        if not structural_standards_dir.exists():
            return ValidationResult(
                is_valid=False,
                score=0.0,
                errors=["Main package 'structural_standards' not found"],
                warnings=[],
                suggestions=["Create the main package directory"],
                details={}
            )
        
        return self.code_validator.validate_package_structure(structural_standards_dir)
    
    def check_standard_implementation(self) -> ValidationResult:
        """Check if standard is properly implemented"""
        print(f"📋 Checking {self.standard.value} implementation...")
        
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        # Check for standard-specific package
        if self.standard == ComplianceStandard.ACI_318M_25:
            standard_dir = project_root / "structural_standards" / "aci" / "aci318m25"
            required_modules = ["materials", "members", "load_combinations"]
        elif self.standard == ComplianceStandard.THAI_MINISTRY_2566:
            standard_dir = project_root / "structural_standards" / "thai"
            required_modules = ["materials", "ministry_2566", "unit_systems"]
        else:
            standard_dir = project_root / "structural_standards" / self.standard.value
            required_modules = ["materials", "members"]
        
        if not standard_dir.exists():
            errors.append(f"Standard implementation directory not found: {standard_dir}")
            score -= 50
        else:
            # Check required modules
            for module in required_modules:
                module_path = standard_dir / module
                if not module_path.exists():
                    errors.append(f"Required module missing: {module}")
                    score -= 15
                elif not (module_path / "__init__.py").exists():
                    warnings.append(f"Module {module} missing __init__.py")
                    score -= 5
        
        # Check for test coverage
        test_dir = project_root / "tests" / f"test_{self.standard.value.split('_')[0]}"
        if not test_dir.exists():
            warnings.append(f"Test directory missing for {self.standard.value}")
            score -= 10
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"standard": self.standard.value, "checked_modules": required_modules}
        )
    
    def check_material_implementations(self) -> ValidationResult:
        """Check material property implementations"""
        print("🧱 Checking material implementations...")
        
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        try:
            # Try to import and validate materials
            if self.standard == ComplianceStandard.ACI_318M_25:
                from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
                from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
                
                # Test concrete creation
                try:
                    concrete = ACI318M25Concrete(fc_prime=28.0)
                    concrete_props = {
                        "fc_prime": concrete.fc_prime,
                        "unit_weight": getattr(concrete, 'unit_weight', 24.0)
                    }
                    material_result = self.standards_validator.validate_material_properties(concrete_props)
                    
                    if not material_result.is_valid:
                        errors.extend(material_result.errors)
                        score -= 20
                    
                    warnings.extend(material_result.warnings)
                    
                except Exception as e:
                    errors.append(f"Failed to create ACI concrete: {e}")
                    score -= 25
                
                # Test steel creation
                try:
                    steel = ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')
                    steel_props = {
                        "fy": steel.fy
                    }
                    steel_result = self.standards_validator.validate_material_properties(steel_props)
                    
                    if not steel_result.is_valid:
                        errors.extend(steel_result.errors)
                        score -= 20
                    
                    warnings.extend(steel_result.warnings)
                    
                except Exception as e:
                    errors.append(f"Failed to create ACI steel: {e}")
                    score -= 25
            
            elif self.standard == ComplianceStandard.THAI_MINISTRY_2566:
                from structural_standards.thai.materials.concrete import ThaiConcrete
                from structural_standards.thai.materials.steel import ThaiSteel
                
                # Test Thai materials
                try:
                    concrete = ThaiConcrete(grade='Fc210')
                    steel = ThaiSteel(grade='SD40', bar_designation='DB20')
                    
                    # Validate properties
                    concrete_props = {"fc_prime": concrete.fc_prime}
                    steel_props = {"fy": steel.fy}
                    
                    concrete_result = self.standards_validator.validate_material_properties(concrete_props)
                    steel_result = self.standards_validator.validate_material_properties(steel_props)
                    
                    if not concrete_result.is_valid:
                        errors.extend(concrete_result.errors)
                        score -= 20
                    
                    if not steel_result.is_valid:
                        errors.extend(steel_result.errors)
                        score -= 20
                    
                except Exception as e:
                    errors.append(f"Failed to create Thai materials: {e}")
                    score -= 25
        
        except ImportError as e:
            errors.append(f"Failed to import materials: {e}")
            score -= 50
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"materials_checked": True}
        )
    
    def check_design_implementations(self) -> ValidationResult:
        """Check design member implementations"""
        print("🏗️  Checking design implementations...")
        
        errors = []
        warnings = []
        suggestions = []
        score = 100.0
        
        try:
            if self.standard == ComplianceStandard.ACI_318M_25:
                # Test beam design
                try:
                    from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
                    from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
                    from structural_standards.aci.aci318m25.members.beam_design import (
                        ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
                    )
                    
                    # Create materials
                    concrete = ACI318M25Concrete(fc_prime=28.0)
                    steel = ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')
                    
                    # Create beam designer
                    beam_designer = ACI318M25BeamDesign(concrete, steel)
                    
                    # Test geometry validation
                    geometry = BeamGeometry(
                        width=300,
                        height=600,
                        effective_depth=550,
                        span_length=6000
                    )
                    
                    geometry_dict = {
                        "width": geometry.width,
                        "height": geometry.height,
                        "effective_depth": geometry.effective_depth,
                        "span_length": geometry.span_length
                    }
                    
                    geom_result = self.standards_validator.validate_geometry(geometry_dict, "beam")
                    
                    if not geom_result.is_valid:
                        errors.extend(geom_result.errors)
                        score -= 15
                    
                    warnings.extend(geom_result.warnings)
                    
                    # Test basic design functionality
                    loads = BeamLoads(dead_load=5.0, live_load=8.0)
                    
                    try:
                        result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
                        
                        # Validate design result
                        if hasattr(result, '__dict__'):
                            result_dict = result.__dict__
                        else:
                            result_dict = {"member_type": "beam", "overall_status": "UNKNOWN"}
                        
                        design_result = self.standards_validator.validate_design_result(result_dict)
                        
                        if not design_result.is_valid:
                            errors.extend(design_result.errors)
                            score -= 20
                        
                        warnings.extend(design_result.warnings)
                        
                    except Exception as e:
                        errors.append(f"Beam design execution failed: {e}")
                        score -= 30
                
                except ImportError as e:
                    errors.append(f"Failed to import beam design modules: {e}")
                    score -= 40
                
                # Test column design
                try:
                    from structural_standards.aci.aci318m25.members.column_design import (
                        ACI318M25ColumnDesign, ColumnGeometry, ColumnLoads, ColumnType
                    )
                    
                    column_designer = ACI318M25ColumnDesign(concrete, steel)
                    
                    column_geometry = ColumnGeometry(
                        width=400,
                        depth=400,
                        length=3000
                    )
                    
                    column_loads = ColumnLoads(
                        axial_dead=200,
                        axial_live=150,
                        moment_x_dead=25,
                        moment_x_live=15
                    )
                    
                    # Test column design
                    try:
                        column_result = column_designer.design(column_geometry, column_loads, ColumnType.TIED)
                        suggestions.append("Column design implementation validated")
                    except Exception as e:
                        warnings.append(f"Column design execution warning: {e}")
                        score -= 10
                
                except ImportError as e:
                    warnings.append(f"Column design modules not available: {e}")
                    score -= 15
        
        except Exception as e:
            errors.append(f"Design implementation check failed: {e}")
            score -= 50
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            score=max(0.0, score),
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={"design_modules_checked": True}
        )
    
    def check_code_quality(self) -> ValidationResult:
        """Check overall code quality"""
        print("📝 Checking code quality...")
        
        # Get all Python files in the project
        python_files = []
        
        # Check main package
        structural_standards_dir = project_root / "structural_standards"
        if structural_standards_dir.exists():
            python_files.extend(structural_standards_dir.rglob("*.py"))
        
        # Check tools
        tools_dir = project_root / "tools"
        if tools_dir.exists():
            python_files.extend(tools_dir.rglob("*.py"))
        
        if not python_files:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                errors=["No Python files found to check"],
                warnings=[],
                suggestions=[],
                details={}
            )
        
        # Analyze code quality for a sample of files
        total_score = 0.0
        file_count = 0
        all_errors = []
        all_warnings = []
        all_suggestions = []
        
        # Check up to 10 files to avoid overwhelming output
        for py_file in python_files[:10]:
            if py_file.name.startswith("__"):
                continue
            
            try:
                result = self.code_validator.validate_module(py_file)
                total_score += result.score
                file_count += 1
                
                all_errors.extend([f"{py_file.name}: {err}" for err in result.errors])
                all_warnings.extend([f"{py_file.name}: {warn}" for warn in result.warnings])
                all_suggestions.extend([f"{py_file.name}: {sugg}" for sugg in result.suggestions])
                
            except Exception as e:
                all_warnings.append(f"Failed to check {py_file.name}: {e}")
        
        avg_score = total_score / file_count if file_count > 0 else 0.0
        
        return ValidationResult(
            is_valid=avg_score >= 70.0,
            score=avg_score,
            errors=all_errors[:5],  # Limit to first 5 errors
            warnings=all_warnings[:10],  # Limit to first 10 warnings
            suggestions=all_suggestions[:5],  # Limit to first 5 suggestions
            details={"files_checked": file_count, "total_files": len(python_files)}
        )
    
    def generate_compliance_report(self, results: Dict[str, ValidationResult]) -> ComplianceReport:
        """Generate comprehensive compliance report"""
        
        # Calculate overall metrics
        total_checks = len(results)
        passed_checks = sum(1 for r in results.values() if r.is_valid)
        failed_checks = total_checks - passed_checks
        total_warnings = sum(len(r.warnings) for r in results.values())
        
        # Calculate overall score (weighted average)
        weights = {
            "package_structure": 0.15,
            "standard_implementation": 0.25,
            "material_implementations": 0.25,
            "design_implementations": 0.25,
            "code_quality": 0.10
        }
        
        overall_score = 0.0
        for category, result in results.items():
            weight = weights.get(category, 1.0 / total_checks)
            overall_score += result.score * weight
        
        # Generate recommendations
        recommendations = []
        
        for category, result in results.items():
            if not result.is_valid:
                recommendations.append(f"Fix critical issues in {category}")
            elif result.score < 80.0:
                recommendations.append(f"Improve {category} (current score: {result.score:.1f})")
            
            # Add specific suggestions
            recommendations.extend(result.suggestions[:2])  # Limit suggestions
        
        # Generate summary
        if overall_score >= 90:
            summary = "Excellent compliance - ready for production"
        elif overall_score >= 80:
            summary = "Good compliance - minor improvements needed"
        elif overall_score >= 70:
            summary = "Acceptable compliance - some issues to address"
        elif overall_score >= 60:
            summary = "Poor compliance - significant improvements required"
        else:
            summary = "Critical compliance issues - major fixes needed"
        
        return ComplianceReport(
            timestamp=time.time(),
            standard=self.standard.value,
            validation_level=self.level.value,
            overall_score=overall_score,
            total_checks=total_checks,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warnings=total_warnings,
            categories=results,
            recommendations=recommendations[:10],  # Limit recommendations
            summary=summary
        )
    
    def save_report(self, report: ComplianceReport, format_type: str = "json"):
        """Save compliance report to file"""
        
        if format_type.lower() == "json":
            report_file = self.output_dir / "compliance_report.json"
            
            # Convert ValidationResult objects to dicts for JSON serialization
            report_dict = asdict(report)
            report_dict["categories"] = {
                k: {
                    "is_valid": v.is_valid,
                    "score": v.score,
                    "errors": v.errors,
                    "warnings": v.warnings,
                    "suggestions": v.suggestions,
                    "details": v.details
                }
                for k, v in report.categories.items()
            }
            
            with open(report_file, 'w') as f:
                json.dump(report_dict, f, indent=2)
        
        elif format_type.lower() == "markdown":
            report_file = self.output_dir / "compliance_report.md"
            
            with open(report_file, 'w') as f:
                f.write(f"# Standards Compliance Report\n\n")
                f.write(f"**Standard:** {report.standard}\n")
                f.write(f"**Validation Level:** {report.validation_level}\n")
                f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report.timestamp))}\n\n")
                
                f.write(f"## Overall Results\n\n")
                f.write(f"- **Score:** {report.overall_score:.1f}/100\n")
                f.write(f"- **Status:** {'✅ PASS' if report.overall_score >= 70 else '❌ FAIL'}\n")
                f.write(f"- **Summary:** {report.summary}\n\n")
                
                f.write(f"## Detailed Results\n\n")
                f.write(f"- **Total Checks:** {report.total_checks}\n")
                f.write(f"- **Passed:** {report.passed_checks}\n")
                f.write(f"- **Failed:** {report.failed_checks}\n")
                f.write(f"- **Warnings:** {report.warnings}\n\n")
                
                f.write(f"## Category Results\n\n")
                for category, result in report.categories.items():
                    status = "✅ PASS" if result.is_valid else "❌ FAIL"
                    f.write(f"### {category.replace('_', ' ').title()}\n")
                    f.write(f"**Status:** {status} (Score: {result.score:.1f})\n\n")
                    
                    if result.errors:
                        f.write("**Errors:**\n")
                        for error in result.errors:
                            f.write(f"- {error}\n")
                        f.write("\n")
                    
                    if result.warnings:
                        f.write("**Warnings:**\n")
                        for warning in result.warnings:
                            f.write(f"- {warning}\n")
                        f.write("\n")
                
                if report.recommendations:
                    f.write(f"## Recommendations\n\n")
                    for i, rec in enumerate(report.recommendations, 1):
                        f.write(f"{i}. {rec}\n")
        
        print(f"📊 Compliance report saved: {report_file}")
        return report_file

def main():
    """Main script function"""
    parser = argparse.ArgumentParser(description="Check standards compliance")
    parser.add_argument("--standard", choices=["aci", "thai", "all"], default="all",
                       help="Standard to check")
    parser.add_argument("--level", choices=["basic", "standard", "strict", "comprehensive"],
                       default="standard", help="Validation level")
    parser.add_argument("--output", type=Path, default=project_root / "compliance_results",
                       help="Output directory")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--report-format", choices=["json", "markdown", "both"],
                       default="both", help="Report format")
    
    args = parser.parse_args()
    
    print("📋 Structural Design Standards - Compliance Checker")
    print("=" * 60)
    
    # Parse validation level
    level_map = {
        "basic": ValidationLevel.BASIC,
        "standard": ValidationLevel.STANDARD,
        "strict": ValidationLevel.STRICT,
        "comprehensive": ValidationLevel.COMPREHENSIVE
    }
    validation_level = level_map[args.level]
    
    # Determine standards to check
    standards_to_check = []
    if args.standard == "all":
        standards_to_check = ["aci", "thai"]
    else:
        standards_to_check = [args.standard]
    
    all_reports = []
    
    for standard in standards_to_check:
        print(f"\n🔍 Checking {standard.upper()} compliance...")
        
        # Create checker
        checker = StandardsChecker(standard, validation_level, args.output)
        
        # Run checks
        results = {}
        
        results["package_structure"] = checker.check_package_structure()
        results["standard_implementation"] = checker.check_standard_implementation()
        results["material_implementations"] = checker.check_material_implementations()
        results["design_implementations"] = checker.check_design_implementations()
        results["code_quality"] = checker.check_code_quality()
        
        # Generate report
        report = checker.generate_compliance_report(results)
        all_reports.append(report)
        
        # Display results
        print(f"\n📊 {standard.upper()} Results:")
        print(f"   Overall Score: {report.overall_score:.1f}/100")
        print(f"   Status: {'✅ PASS' if report.overall_score >= 70 else '❌ FAIL'}")
        print(f"   Passed Checks: {report.passed_checks}/{report.total_checks}")
        print(f"   Warnings: {report.warnings}")
        
        if args.verbose:
            print(f"   Summary: {report.summary}")
            if report.recommendations:
                print("   Top Recommendations:")
                for i, rec in enumerate(report.recommendations[:3], 1):
                    print(f"     {i}. {rec}")
        
        # Save report
        if args.report_format in ["json", "both"]:
            checker.save_report(report, "json")
        
        if args.report_format in ["markdown", "both"]:
            checker.save_report(report, "markdown")
    
    # Overall summary
    if len(all_reports) > 1:
        avg_score = sum(r.overall_score for r in all_reports) / len(all_reports)
        print(f"\n🎯 Overall Compliance Summary:")
        print(f"   Average Score: {avg_score:.1f}/100")
        print(f"   Standards Checked: {len(all_reports)}")
        
        if avg_score >= 70:
            print("   Status: ✅ COMPLIANT")
            sys.exit(0)
        else:
            print("   Status: ❌ NON-COMPLIANT")
            sys.exit(1)
    else:
        report = all_reports[0]
        if report.overall_score >= 70:
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()