#!/usr/bin/env python3
"""
Documentation Build Script
===========================

Automated documentation building and validation script.
Builds Sphinx documentation, validates content, and generates reports.

Usage:
    python scripts/build_docs.py [options]

Options:
    --clean         Clean build directory before building
    --check-links   Check external links in documentation
    --format        Check documentation formatting
    --output DIR    Output directory for documentation
    --verbose       Verbose output
    --serve         Serve documentation locally after build
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path
import webbrowser
import http.server
import socketserver
from threading import Thread
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def clean_build_directory(docs_dir: Path, build_dir: Path):
    """Clean the documentation build directory"""
    if build_dir.exists():
        print(f"🧹 Cleaning build directory: {build_dir}")
        shutil.rmtree(build_dir)
    
    # Also clean any cached files
    cache_dirs = [
        docs_dir / "_build",
        docs_dir / ".doctrees",
        project_root / ".pytest_cache",
        project_root / "__pycache__"
    ]
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            print(f"🧹 Cleaning cache: {cache_dir}")
            shutil.rmtree(cache_dir)

def check_sphinx_installation():
    """Check if Sphinx is installed"""
    try:
        import sphinx
        print(f"✅ Sphinx {sphinx.__version__} is installed")
        return True
    except ImportError:
        print("❌ Sphinx is not installed. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "sphinx", "sphinx-rtd-theme"], 
                         check=True, capture_output=True)
            print("✅ Sphinx installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Sphinx: {e}")
            return False

def create_sphinx_config(docs_dir: Path):
    """Create or update Sphinx configuration"""
    conf_py = docs_dir / "source" / "conf.py"
    
    if not conf_py.exists():
        print("📝 Creating Sphinx configuration...")
        
        # Ensure source directory exists
        (docs_dir / "source").mkdir(parents=True, exist_ok=True)
        
        # Create basic conf.py
        conf_content = '''"""
Sphinx configuration for Structural Design Standards
"""

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# Project information
project = 'Structural Design Standards'
copyright = '2024, Development Team'
author = 'Development Team'
version = '1.0.0'
release = '1.0.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
]

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'special-members': '__init__',
}

# Napoleon settings (for Google/NumPy style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Theme
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False
}

# Output file settings
html_static_path = ['_static']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Internationalization
language = 'en'

# Math
mathjax_path = 'https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}

# TODO extension
todo_include_todos = True
'''
        
        with open(conf_py, 'w', encoding='utf-8') as f:
            f.write(conf_content)
        
        print(f"✅ Created Sphinx configuration: {conf_py}")
    
    return conf_py.exists()

def create_index_rst(docs_dir: Path):
    """Create main index.rst file if it doesn't exist"""
    index_rst = docs_dir / "source" / "index.rst"
    
    if not index_rst.exists():
        print("📝 Creating main index.rst...")
        
        index_content = '''Structural Design Standards Documentation
========================================

Welcome to the Structural Design Standards library documentation.

This library provides implementations for various international structural design standards
including ACI 318M-25, Thai Ministry Regulation B.E. 2566, and utilities for multi-standard projects.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/index
   examples/index
   tutorials/index

Quick Start
-----------

.. code-block:: python

   from structural_standards.aci.aci318m25.materials import ACI318M25Concrete, ACI318M25ReinforcementSteel
   from structural_standards.aci.aci318m25.members import ACI318M25BeamDesign

   # Create materials
   concrete = ACI318M25Concrete(fc_prime=28.0)
   steel = ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')

   # Design beam
   beam_designer = ACI318M25BeamDesign(concrete, steel)

Features
--------

* **ACI 318M-25 Implementation**: Complete beam, column, slab, wall, footing, and diaphragm design
* **Thai Standards Support**: Ministry Regulation B.E. 2566, TIS standards, provincial load data
* **Multi-language Support**: English, Thai with automatic language detection
* **Comprehensive Testing**: Unit tests, integration tests, performance benchmarks
* **Development Tools**: Code generators, validators, quality checks

API Reference
=============

.. toctree::
   :maxdepth: 2

   api/aci
   api/thai  
   api/utils

Examples
========

.. toctree::
   :maxdepth: 2

   examples/basic_usage
   examples/advanced_usage
   examples/validation_examples

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
'''
        
        with open(index_rst, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"✅ Created main index.rst: {index_rst}")

def create_api_index(docs_dir: Path):
    """Create API index file"""
    api_index = docs_dir / "source" / "api" / "index.rst"
    api_index.parent.mkdir(exist_ok=True)
    
    if not api_index.exists():
        print("📝 Creating API index...")
        
        api_content = '''API Reference
=============

Complete API reference for all modules and classes.

.. toctree::
   :maxdepth: 3

   aci
   thai
   utils

Core Standards
--------------

.. toctree::
   :maxdepth: 2

   aci

Thai Standards
--------------

.. toctree::
   :maxdepth: 2

   thai

Utilities
---------

.. toctree::
   :maxdepth: 2

   utils
'''
        
        with open(api_index, 'w', encoding='utf-8') as f:
            f.write(api_content)

def create_examples_index(docs_dir: Path):
    """Create examples index file"""
    examples_index = docs_dir / "source" / "examples" / "index.rst"
    examples_index.parent.mkdir(exist_ok=True)
    
    if not examples_index.exists():
        print("📝 Creating examples index...")
        
        examples_content = '''Examples
========

Comprehensive examples demonstrating library usage.

.. toctree::
   :maxdepth: 2

   basic_usage/index
   advanced_usage/index
   validation_examples/index

Basic Usage
-----------

.. toctree::
   :maxdepth: 2

   basic_usage/aci_beam_example
   basic_usage/thai_slab_example
   basic_usage/comparison_example

Advanced Usage
--------------

.. toctree::
   :maxdepth: 2

   advanced_usage/custom_materials
   advanced_usage/optimization
   advanced_usage/integration

Validation Examples
-------------------

.. toctree::
   :maxdepth: 2

   validation_examples/benchmark_tests
   validation_examples/known_solutions
   validation_examples/standards_compliance
'''
        
        with open(examples_index, 'w', encoding='utf-8') as f:
            f.write(examples_content)

def build_documentation(docs_dir: Path, build_dir: Path, verbose: bool = False):
    """Build Sphinx documentation"""
    print(f"🏗️  Building documentation...")
    print(f"   Source: {docs_dir / 'source'}")
    print(f"   Output: {build_dir}")
    
    # Prepare build command
    cmd = [
        "sphinx-build",
        "-b", "html",  # Build HTML
        "-E",          # Don't use saved environment
        str(docs_dir / "source"),
        str(build_dir)
    ]
    
    if verbose:
        cmd.insert(1, "-v")
    
    # Run Sphinx build
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Documentation built successfully!")
            
            # Count built files
            html_files = list(build_dir.rglob("*.html"))
            print(f"   Generated {len(html_files)} HTML files")
            
            # Show main index location
            index_file = build_dir / "index.html"
            if index_file.exists():
                print(f"   Main page: {index_file}")
            
            return True
        else:
            print(f"❌ Documentation build failed!")
            print(f"   Error: {result.stderr}")
            if verbose:
                print(f"   Output: {result.stdout}")
            return False
            
    except FileNotFoundError:
        print("❌ sphinx-build command not found. Make sure Sphinx is installed.")
        return False
    except Exception as e:
        print(f"❌ Build failed with exception: {e}")
        return False

def check_documentation_links(build_dir: Path):
    """Check for broken links in documentation"""
    print("🔗 Checking documentation links...")
    
    # This is a placeholder for link checking
    # In a real implementation, you might use tools like:
    # - sphinx-build -b linkcheck
    # - Custom HTML parsing to check links
    
    try:
        cmd = [
            "sphinx-build",
            "-b", "linkcheck",
            str(project_root / "docs" / "source"),
            str(build_dir / "_linkcheck")
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Link check passed")
            return True
        else:
            print("⚠️  Some links may be broken")
            print(result.stdout)
            return False
            
    except FileNotFoundError:
        print("⚠️  Link checking skipped (sphinx not available)")
        return True

def validate_documentation_format(docs_dir: Path):
    """Validate documentation formatting and structure"""
    print("📋 Validating documentation format...")
    
    issues = []
    
    # Check for required files
    required_files = [
        docs_dir / "source" / "conf.py",
        docs_dir / "source" / "index.rst"
    ]
    
    for file_path in required_files:
        if not file_path.exists():
            issues.append(f"Missing required file: {file_path}")
    
    # Check RST files for basic formatting
    rst_files = list((docs_dir / "source").rglob("*.rst"))
    
    for rst_file in rst_files:
        try:
            with open(rst_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Basic checks
                if not content.strip():
                    issues.append(f"Empty RST file: {rst_file}")
                
                # Check for title underlines
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if i > 0 and line.strip() and all(c in '=-~^"' for c in line.strip()):
                        prev_line = lines[i-1].strip()
                        if len(line.strip()) < len(prev_line):
                            issues.append(f"Title underline too short in {rst_file}:{i+1}")
                            
        except Exception as e:
            issues.append(f"Error reading {rst_file}: {e}")
    
    if issues:
        print(f"⚠️  Found {len(issues)} formatting issues:")
        for issue in issues[:10]:  # Show first 10 issues
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues) - 10} more")
        return False
    else:
        print("✅ Documentation format validation passed")
        return True

def serve_documentation(build_dir: Path, port: int = 8000):
    """Serve documentation locally"""
    if not build_dir.exists():
        print("❌ Build directory not found. Build documentation first.")
        return
    
    index_file = build_dir / "index.html"
    if not index_file.exists():
        print("❌ Documentation index not found. Build documentation first.")
        return
    
    print(f"🌐 Starting documentation server on port {port}...")
    
    # Change to build directory
    os.chdir(build_dir)
    
    # Create server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"   Server running at: http://localhost:{port}")
            print(f"   Press Ctrl+C to stop")
            
            # Open browser
            def open_browser():
                time.sleep(1)
                webbrowser.open(f"http://localhost:{port}")
            
            Thread(target=open_browser, daemon=True).start()
            
            # Serve
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main script function"""
    parser = argparse.ArgumentParser(description="Build and validate documentation")
    parser.add_argument("--clean", action="store_true", help="Clean build directory")
    parser.add_argument("--check-links", action="store_true", help="Check external links")
    parser.add_argument("--format", action="store_true", help="Check formatting")
    parser.add_argument("--output", type=Path, help="Output directory", 
                       default=project_root / "docs" / "_build" / "html")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--serve", action="store_true", help="Serve documentation after build")
    parser.add_argument("--port", type=int, default=8000, help="Server port for --serve")
    
    args = parser.parse_args()
    
    # Setup paths
    docs_dir = project_root / "docs"
    build_dir = args.output
    
    print("📚 Structural Design Standards - Documentation Builder")
    print("=" * 60)
    
    # Check Sphinx installation
    if not check_sphinx_installation():
        sys.exit(1)
    
    # Clean if requested
    if args.clean:
        clean_build_directory(docs_dir, build_dir)
    
    # Ensure documentation structure exists
    (docs_dir / "source").mkdir(parents=True, exist_ok=True)
    
    # Create configuration and index files if needed
    if not create_sphinx_config(docs_dir):
        print("❌ Failed to create Sphinx configuration")
        sys.exit(1)
    
    create_index_rst(docs_dir)
    create_api_index(docs_dir)
    create_examples_index(docs_dir)
    
    # Validate format if requested
    if args.format:
        if not validate_documentation_format(docs_dir):
            print("⚠️  Format validation failed, but continuing...")
    
    # Build documentation
    if not build_documentation(docs_dir, build_dir, args.verbose):
        sys.exit(1)
    
    # Check links if requested
    if args.check_links:
        check_documentation_links(build_dir)
    
    # Serve if requested
    if args.serve:
        serve_documentation(build_dir, args.port)
    
    print("\n✅ Documentation build completed successfully!")
    print(f"   Open: {build_dir / 'index.html'}")

if __name__ == "__main__":
    main()