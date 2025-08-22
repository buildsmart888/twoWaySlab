#!/usr/bin/env python3
"""
Test Execution Script
=====================

Automated test execution, reporting, and coverage analysis script.
Runs pytest with various configurations and generates comprehensive reports.

Usage:
    python scripts/run_tests.py [options]

Options:
    --coverage          Run with coverage analysis
    --benchmark         Include benchmark tests
    --integration       Run integration tests only
    --unit              Run unit tests only
    --fast              Skip slow tests
    --parallel          Run tests in parallel
    --output DIR        Output directory for reports
    --verbose           Verbose test output
    --html              Generate HTML test report
    --xml               Generate XML test report (JUnit format)
    --markers MARKERS   Run tests with specific markers
"""

import os
import sys
import subprocess
import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_pytest_installation():
    """Check if pytest and related tools are installed"""
    required_packages = [
        ("pytest", "pytest"),
        ("pytest-cov", "pytest-cov"),
        ("pytest-html", "pytest-html"),
        ("pytest-xdist", "pytest-xdist"),
        ("pytest-benchmark", "pytest-benchmark")
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name.replace('-', '_'))
            print(f"✅ {package_name} is available")
        except ImportError:
            missing_packages.append(package_name)
            print(f"⚠️  {package_name} not found")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages, check=True, capture_output=True)
            print("✅ All required packages installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            return False
    
    return True

def discover_tests(test_dir: Path) -> Dict[str, List[Path]]:
    """Discover and categorize test files"""
    test_categories = {
        "unit": [],
        "integration": [],
        "benchmark": [],
        "validation": [],
        "other": []
    }
    
    if not test_dir.exists():
        print(f"⚠️  Test directory not found: {test_dir}")
        return test_categories
    
    # Find all test files
    test_files = list(test_dir.rglob("test_*.py"))
    
    for test_file in test_files:
        # Categorize based on directory structure and file name
        path_parts = test_file.parts
        
        if "integration" in path_parts:
            test_categories["integration"].append(test_file)
        elif "benchmark" in path_parts or "benchmark" in test_file.name:
            test_categories["benchmark"].append(test_file)
        elif "validation" in path_parts:
            test_categories["validation"].append(test_file)
        elif any(unit_dir in path_parts for unit_dir in ["test_aci", "test_thai", "test_base", "test_utils"]):
            test_categories["unit"].append(test_file)
        else:
            test_categories["other"].append(test_file)
    
    # Print discovery summary
    print("🔍 Test Discovery Summary:")
    for category, files in test_categories.items():
        if files:
            print(f"   {category.title()}: {len(files)} files")
    
    return test_categories

def build_pytest_command(args: argparse.Namespace, test_paths: List[Path]) -> List[str]:
    """Build pytest command with options"""
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test paths
    cmd.extend([str(path) for path in test_paths])
    
    # Verbose output
    if args.verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Coverage
    if args.coverage:
        cmd.extend([
            "--cov=structural_standards",
            "--cov-branch",
            f"--cov-report=html:{args.output}/coverage_html",
            f"--cov-report=xml:{args.output}/coverage.xml",
            "--cov-report=term-missing"
        ])
    
    # HTML report
    if args.html:
        cmd.extend([
            "--html", str(args.output / "test_report.html"),
            "--self-contained-html"
        ])
    
    # XML report (JUnit format)
    if args.xml:
        cmd.extend([
            "--junitxml", str(args.output / "test_results.xml")
        ])
    
    # Parallel execution
    if args.parallel:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        cmd.extend(["-n", str(min(cpu_count, 4))])  # Limit to 4 workers
    
    # Benchmark tests
    if args.benchmark:
        cmd.append("--benchmark-only")
    else:
        cmd.append("--benchmark-skip")
    
    # Fast mode (skip slow tests)
    if args.fast:
        cmd.extend(["-m", "not slow"])
    
    # Custom markers
    if args.markers:
        cmd.extend(["-m", args.markers])
    
    # Additional pytest options
    cmd.extend([
        "--tb=short",  # Shorter traceback format
        "--strict-markers",  # Require markers to be defined
        "--disable-warnings"  # Disable warnings for cleaner output
    ])
    
    return cmd

def run_tests(cmd: List[str], timeout: int = 300) -> subprocess.CompletedProcess:
    """Run pytest with the given command"""
    print(f"🧪 Running tests...")
    print(f"   Command: {' '.join(cmd[:3])} ... ({len(cmd)-3} more args)")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"   Execution time: {execution_time:.1f} seconds")
        
        return result
        
    except subprocess.TimeoutExpired:
        print(f"❌ Tests timed out after {timeout} seconds")
        return subprocess.CompletedProcess(cmd, 1, "", "Test execution timed out")
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return subprocess.CompletedProcess(cmd, 1, "", str(e))

def parse_test_results(output: str, xml_file: Optional[Path] = None) -> Dict:
    """Parse test results from pytest output"""
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
        "execution_time": 0.0,
        "success_rate": 0.0
    }
    
    # Parse from XML if available (more reliable)
    if xml_file and xml_file.exists():
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Get test counts from XML
            results["total"] = int(root.get("tests", 0))
            results["failed"] = int(root.get("failures", 0))
            results["errors"] = int(root.get("errors", 0))
            results["skipped"] = int(root.get("skipped", 0))
            results["passed"] = results["total"] - results["failed"] - results["errors"] - results["skipped"]
            results["execution_time"] = float(root.get("time", 0))
            
            if results["total"] > 0:
                results["success_rate"] = results["passed"] / results["total"]
            
            return results
            
        except Exception as e:
            print(f"⚠️  Failed to parse XML results: {e}")
    
    # Parse from text output (fallback)
    lines = output.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Look for summary line like "4 passed, 1 failed in 2.3s"
        if " passed" in line or " failed" in line:
            parts = line.split()
            
            for i, part in enumerate(parts):
                if part == "passed" and i > 0:
                    results["passed"] = int(parts[i-1])
                elif part == "failed" and i > 0:
                    results["failed"] = int(parts[i-1])
                elif part == "skipped" and i > 0:
                    results["skipped"] = int(parts[i-1])
                elif part == "error" and i > 0:
                    results["errors"] = int(parts[i-1])
            
            # Extract execution time
            if "in" in parts:
                time_idx = parts.index("in") + 1
                if time_idx < len(parts):
                    time_str = parts[time_idx].rstrip('s')
                    try:
                        results["execution_time"] = float(time_str)
                    except ValueError:
                        pass
    
    # Calculate totals
    results["total"] = results["passed"] + results["failed"] + results["skipped"] + results["errors"]
    
    if results["total"] > 0:
        results["success_rate"] = results["passed"] / results["total"]
    
    return results

def generate_test_summary(results: Dict, output_dir: Path):
    """Generate a comprehensive test summary"""
    summary = {
        "timestamp": time.time(),
        "results": results,
        "status": "PASS" if results["failed"] == 0 and results["errors"] == 0 else "FAIL"
    }
    
    # Save JSON summary
    summary_file = output_dir / "test_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Generate markdown report
    md_report = output_dir / "test_summary.md"
    with open(md_report, 'w') as f:
        f.write("# Test Execution Summary\n\n")
        f.write(f"**Status:** {'✅ PASS' if summary['status'] == 'PASS' else '❌ FAIL'}\n\n")
        f.write(f"**Execution Time:** {results['execution_time']:.1f} seconds\n\n")
        f.write("## Results\n\n")
        f.write(f"- **Total Tests:** {results['total']}\n")
        f.write(f"- **Passed:** {results['passed']} ({results['success_rate']:.1%})\n")
        f.write(f"- **Failed:** {results['failed']}\n")
        f.write(f"- **Skipped:** {results['skipped']}\n")
        f.write(f"- **Errors:** {results['errors']}\n\n")
        
        if results['total'] > 0:
            f.write("## Performance\n\n")
            f.write(f"- **Success Rate:** {results['success_rate']:.1%}\n")
            f.write(f"- **Tests per Second:** {results['total'] / results['execution_time']:.1f}\n\n")
    
    print(f"📊 Test summary saved:")
    print(f"   JSON: {summary_file}")
    print(f"   Markdown: {md_report}")

def check_test_quality(test_dir: Path) -> Dict[str, int]:
    """Analyze test quality metrics"""
    metrics = {
        "total_test_files": 0,
        "total_test_functions": 0,
        "files_with_fixtures": 0,
        "files_with_parametrize": 0,
        "files_with_docstrings": 0
    }
    
    test_files = list(test_dir.rglob("test_*.py"))
    metrics["total_test_files"] = len(test_files)
    
    for test_file in test_files:
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Count test functions
                test_functions = content.count("def test_")
                metrics["total_test_functions"] += test_functions
                
                # Check for fixtures
                if "@pytest.fixture" in content:
                    metrics["files_with_fixtures"] += 1
                
                # Check for parametrize
                if "@pytest.mark.parametrize" in content:
                    metrics["files_with_parametrize"] += 1
                
                # Check for docstrings
                if '"""' in content or "'''" in content:
                    metrics["files_with_docstrings"] += 1
                    
        except Exception:
            pass  # Skip files that can't be read
    
    return metrics

def main():
    """Main script function"""
    parser = argparse.ArgumentParser(description="Run tests with comprehensive reporting")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage analysis")
    parser.add_argument("--benchmark", action="store_true", help="Include benchmark tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--fast", action="store_true", help="Skip slow tests")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--output", type=Path, help="Output directory", 
                       default=project_root / "test_results")
    parser.add_argument("--verbose", action="store_true", help="Verbose test output")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--xml", action="store_true", help="Generate XML report")
    parser.add_argument("--markers", help="Run tests with specific markers")
    parser.add_argument("--timeout", type=int, default=300, help="Test timeout in seconds")
    
    args = parser.parse_args()
    
    print("🧪 Structural Design Standards - Test Runner")
    print("=" * 60)
    
    # Check dependencies
    if not check_pytest_installation():
        sys.exit(1)
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Discover tests
    test_dir = project_root / "tests"
    test_categories = discover_tests(test_dir)
    
    # Determine which tests to run
    test_paths = []
    
    if args.unit:
        test_paths.extend(test_categories["unit"])
        print("🎯 Running unit tests only")
    elif args.integration:
        test_paths.extend(test_categories["integration"])
        print("🎯 Running integration tests only")
    elif args.benchmark:
        test_paths.extend(test_categories["benchmark"])
        print("🎯 Running benchmark tests only")
    else:
        # Run all tests except benchmarks (unless specifically requested)
        for category, files in test_categories.items():
            if category != "benchmark" or args.benchmark:
                test_paths.extend(files)
        print("🎯 Running all available tests")
    
    if not test_paths:
        print("⚠️  No test files found to execute")
        sys.exit(1)
    
    print(f"   Test files: {len(test_paths)}")
    
    # Build pytest command
    cmd = build_pytest_command(args, test_paths)
    
    # Run tests
    result = run_tests(cmd, args.timeout)
    
    # Parse results
    xml_file = args.output / "test_results.xml" if args.xml else None
    test_results = parse_test_results(result.stdout, xml_file)
    
    # Display results
    print("\n📊 Test Results:")
    print(f"   Total: {test_results['total']}")
    print(f"   Passed: {test_results['passed']} ({test_results['success_rate']:.1%})")
    print(f"   Failed: {test_results['failed']}")
    print(f"   Skipped: {test_results['skipped']}")
    print(f"   Errors: {test_results['errors']}")
    print(f"   Time: {test_results['execution_time']:.1f}s")
    
    # Generate summary
    generate_test_summary(test_results, args.output)
    
    # Test quality analysis
    quality_metrics = check_test_quality(test_dir)
    print(f"\n📋 Test Quality Metrics:")
    print(f"   Test files: {quality_metrics['total_test_files']}")
    print(f"   Test functions: {quality_metrics['total_test_functions']}")
    print(f"   Files with fixtures: {quality_metrics['files_with_fixtures']}")
    print(f"   Files with parametrize: {quality_metrics['files_with_parametrize']}")
    
    # Show output files
    print(f"\n📁 Output files in {args.output}:")
    output_files = list(args.output.iterdir())
    for file_path in sorted(output_files):
        if file_path.is_file():
            size_kb = file_path.stat().st_size / 1024
            print(f"   {file_path.name} ({size_kb:.1f} KB)")
    
    # Exit with appropriate code
    if result.returncode == 0 and test_results["failed"] == 0 and test_results["errors"] == 0:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ Tests failed (exit code: {result.returncode})")
        if result.stderr:
            print("Error output:")
            print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()