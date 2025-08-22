#!/usr/bin/env python3
"""
Code Generation Script
======================

Automated code generation for new structural design standards.
Creates boilerplate code, tests, documentation, and validation.

Usage:
    python scripts/generate_code.py [command] [options]

Commands:
    new-standard    Generate complete new standard implementation
    new-material    Generate material class
    new-member      Generate member design class
    new-test        Generate test suite
    
Options:
    --name NAME         Name of the item to generate
    --output DIR        Output directory
    --author AUTHOR     Author name
    --template TEMPLATE Template to use
    --interactive       Interactive mode
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import code generation tools
try:
    from tools.code_generators import (
        StandardCodeGenerator, MaterialCodeGenerator, TestCodeGenerator,
        GeneratorConfig, CodeType, LanguageStandard
    )
except ImportError:
    print("❌ Unable to import code generation tools. Make sure the tools package is available.")
    sys.exit(1)

def interactive_new_standard():
    """Interactive mode for creating new standard"""
    print("🎯 Creating New Structural Design Standard")
    print("=" * 50)
    
    # Get standard information
    standard_name = input("Standard name (e.g., 'eurocode_2', 'as_3600'): ").strip()
    if not standard_name:
        print("❌ Standard name is required")
        return None
    
    # Validate name format
    if not standard_name.replace('_', '').replace('-', '').isalnum():
        print("❌ Standard name should contain only letters, numbers, underscores, and hyphens")
        return None
    
    # Get additional information
    author = input("Author name [Generated]: ").strip() or "Generated"
    description = input("Standard description: ").strip()
    
    # Get output directory
    default_output = project_root / "structural_standards" / standard_name
    output_str = input(f"Output directory [{default_output}]: ").strip()
    output_dir = Path(output_str) if output_str else default_output
    
    # Confirm generation
    print(f"\n📋 Generation Summary:")
    print(f"   Standard: {standard_name}")
    print(f"   Author: {author}")
    print(f"   Output: {output_dir}")
    print(f"   Description: {description}")
    
    confirm = input("\nProceed with generation? [y/N]: ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Generation cancelled")
        return None
    
    return {
        "name": standard_name,
        "author": author,
        "description": description,
        "output_dir": output_dir
    }

def generate_new_standard(name: str, output_dir: Path, author: str = "Generated") -> bool:
    """Generate complete new standard implementation"""
    print(f"🏗️  Generating new standard: {name}")
    
    # Create generator config
    config = GeneratorConfig(
        output_dir=output_dir.parent,
        package_name="structural_standards",
        author=author,
        include_tests=True,
        include_documentation=True
    )
    
    # Create generator
    generator = StandardCodeGenerator(config)
    
    try:
        # Generate standard package
        files = generator.generate_standard_package(name)
        
        # Write files
        created_files = []
        for file_path, content in files.items():
            file_path_obj = Path(file_path)
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path_obj, 'w', encoding='utf-8') as f:
                f.write(content)
            
            created_files.append(file_path_obj)
            print(f"   ✅ Created: {file_path_obj.relative_to(project_root)}")
        
        # Generate corresponding tests
        print(f"🧪 Generating tests for {name}...")
        test_generator = TestCodeGenerator(config)
        test_files = test_generator.generate_test_suite(name)
        
        for file_path, content in test_files.items():
            file_path_obj = Path(file_path)
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path_obj, 'w', encoding='utf-8') as f:
                f.write(content)
            
            created_files.append(file_path_obj)
            print(f"   ✅ Created: {file_path_obj.relative_to(project_root)}")
        
        # Generate documentation template
        docs_dir = project_root / "docs" / "source" / "api"
        docs_file = docs_dir / f"{name}.rst"
        
        if not docs_file.exists():
            docs_dir.mkdir(parents=True, exist_ok=True)
            
            docs_content = f'''
{name.title()} Standards API
{'=' * (len(name) + 15)}

This section documents the {name.title()} structural design standard implementation.

{name.title()} Materials
{'-' * (len(name) + 10)}

.. automodule:: structural_standards.{name}.materials
   :members:
   :undoc-members:
   :show-inheritance:

Concrete Materials
^^^^^^^^^^^^^^^^^

.. automodule:: structural_standards.{name}.materials.concrete
   :members:
   :undoc-members:
   :show-inheritance:

Steel Materials
^^^^^^^^^^^^^^

.. automodule:: structural_standards.{name}.materials.steel
   :members:
   :undoc-members:
   :show-inheritance:

{name.title()} Structural Members
{'-' * (len(name) + 20)}

.. automodule:: structural_standards.{name}.members
   :members:
   :undoc-members:
   :show-inheritance:

Beam Design
^^^^^^^^^^

.. automodule:: structural_standards.{name}.members.beam_design
   :members:
   :undoc-members:
   :show-inheritance:

Column Design
^^^^^^^^^^^^

.. automodule:: structural_standards.{name}.members.column_design
   :members:
   :undoc-members:
   :show-inheritance:

{name.title()} Load Combinations
{'-' * (len(name) + 17)}

.. automodule:: structural_standards.{name}.load_combinations
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Usage
^^^^^^^^^^

.. code-block:: python

   from structural_standards.{name}.materials import {name.title()}Concrete, {name.title()}Steel
   from structural_standards.{name}.members import {name.title()}BeamDesign

   # Create materials
   concrete = {name.title()}Concrete(fc_prime=25.0)
   steel = {name.title()}Steel(grade="GRADE400")

   # Create beam designer
   beam_designer = {name.title()}BeamDesign(concrete, steel)

   # Perform design
   # ... design code here ...
'''
            
            with open(docs_file, 'w', encoding='utf-8') as f:
                f.write(docs_content)
            
            created_files.append(docs_file)
            print(f"   ✅ Created: {docs_file.relative_to(project_root)}")
        
        print(f"\n✅ Standard '{name}' generated successfully!")
        print(f"   Files created: {len(created_files)}")
        print(f"   Location: {output_dir}")
        print(f"\n📋 Next Steps:")
        print(f"   1. Review generated code in {output_dir}")
        print(f"   2. Implement specific design formulas")
        print(f"   3. Run tests: python -m pytest tests/test_{name}/")
        print(f"   4. Update documentation")
        
        return True
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False

def generate_material_class(name: str, material_type: str, output_dir: Path, author: str = "Generated") -> bool:
    """Generate individual material class"""
    print(f"🧱 Generating {material_type} material: {name}")
    
    # Determine template based on material type
    if material_type.lower() == "concrete":
        template = f'''"""
{name} Concrete Material
{'=' * (len(name) + 17)}

Concrete material implementation for {name} standard.
"""

from typing import Optional
from structural_standards.base.material_base import ConcreteMaterial
from structural_standards.utils.validation import validate_positive

class {name}Concrete(ConcreteMaterial):
    """
    {name} concrete material implementation
    """
    
    def __init__(self, fc_prime: float, unit_weight: float = 24.0):
        """
        Initialize concrete material
        
        Parameters:
        -----------
        fc_prime : float
            Compressive strength (MPa)
        unit_weight : float
            Unit weight (kN/m³)
        """
        validate_positive(fc_prime, "concrete compressive strength")
        
        super().__init__(fc_prime=fc_prime, standard="{name}")
        self.unit_weight = unit_weight
    
    def elastic_modulus(self) -> float:
        """
        Calculate elastic modulus
        
        Returns:
        --------
        float
            Elastic modulus (MPa)
        """
        # TODO: Implement standard-specific formula
        return 4700 * (self.fc_prime ** 0.5)
    
    def tensile_strength(self) -> float:
        """
        Calculate tensile strength
        
        Returns:
        --------
        float
            Tensile strength (MPa)
        """
        # TODO: Implement standard-specific formula
        return 0.6 * (self.fc_prime ** 0.5)
'''
    
    elif material_type.lower() == "steel":
        template = f'''"""
{name} Steel Material
{'=' * (len(name) + 14)}

Steel material implementation for {name} standard.
"""

from typing import Dict
from structural_standards.base.material_base import SteelMaterial
from structural_standards.utils.validation import validate_positive

class {name}Steel(SteelMaterial):
    """
    {name} steel material implementation
    """
    
    # Standard steel grades - customize for your standard
    STANDARD_GRADES = {{
        "GRADE300": {{"fy": 300, "fu": 450}},
        "GRADE400": {{"fy": 400, "fu": 550}},
        "GRADE500": {{"fy": 500, "fu": 630}}
    }}
    
    def __init__(self, grade: str = "GRADE400", bar_designation: str = "R20"):
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
        
        super().__init__(fy=grade_props["fy"], standard="{name}")
        
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
        # TODO: Implement standard-specific bar areas
        bar_areas = {{
            "R12": 113,
            "R16": 201,
            "R20": 314,
            "R25": 491,
            "R32": 804
        }}
        
        return bar_areas.get(self.bar_designation, 314)
'''
    
    else:
        print(f"❌ Unknown material type: {material_type}")
        return False
    
    # Write file
    output_file = output_dir / f"{material_type.lower()}.py"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"   ✅ Created: {output_file.relative_to(project_root)}")
    return True

def list_templates():
    """List available templates"""
    print("📋 Available Templates:")
    print("   Standards:")
    print("     - aci_318m_25 (ACI 318M-25 template)")
    print("     - thai_ministry (Thai Ministry template)")
    print("     - eurocode_2 (Eurocode 2 template)")
    print("     - generic (Generic standard template)")
    print()
    print("   Materials:")
    print("     - concrete (Concrete material class)")
    print("     - steel (Steel material class)")
    print()
    print("   Members:")
    print("     - beam (Beam design class)")
    print("     - column (Column design class)")
    print("     - slab (Slab design class)")

def main():
    """Main script function"""
    parser = argparse.ArgumentParser(description="Generate code for structural standards")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # New standard command
    new_std_parser = subparsers.add_parser("new-standard", help="Generate new standard")
    new_std_parser.add_argument("--name", required=True, help="Standard name")
    new_std_parser.add_argument("--output", type=Path, help="Output directory")
    new_std_parser.add_argument("--author", default="Generated", help="Author name")
    new_std_parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    # New material command
    new_mat_parser = subparsers.add_parser("new-material", help="Generate material class")
    new_mat_parser.add_argument("--name", required=True, help="Material name")
    new_mat_parser.add_argument("--type", choices=["concrete", "steel"], required=True, help="Material type")
    new_mat_parser.add_argument("--output", type=Path, help="Output directory")
    new_mat_parser.add_argument("--author", default="Generated", help="Author name")
    
    # List templates command
    list_parser = subparsers.add_parser("list-templates", help="List available templates")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Interactive mode")
    
    args = parser.parse_args()
    
    print("🏗️  Structural Design Standards - Code Generator")
    print("=" * 60)
    
    if args.command == "new-standard":
        if args.interactive:
            config = interactive_new_standard()
            if config:
                success = generate_new_standard(
                    config["name"], 
                    config["output_dir"], 
                    config["author"]
                )
                sys.exit(0 if success else 1)
        else:
            output_dir = args.output or (project_root / "structural_standards" / args.name)
            success = generate_new_standard(args.name, output_dir, args.author)
            sys.exit(0 if success else 1)
    
    elif args.command == "new-material":
        output_dir = args.output or (project_root / "structural_standards" / args.name.lower() / "materials")
        success = generate_material_class(args.name, args.type, output_dir, args.author)
        sys.exit(0 if success else 1)
    
    elif args.command == "list-templates":
        list_templates()
    
    elif args.command == "interactive":
        config = interactive_new_standard()
        if config:
            success = generate_new_standard(
                config["name"], 
                config["output_dir"], 
                config["author"]
            )
            sys.exit(0 if success else 1)
    
    else:
        print("❌ No command specified. Use --help for available commands.")
        print("\n🎯 Quick Start:")
        print("   Generate new standard:    python scripts/generate_code.py new-standard --name eurocode_2")
        print("   Interactive mode:         python scripts/generate_code.py interactive")
        print("   List templates:           python scripts/generate_code.py list-templates")
        sys.exit(1)

if __name__ == "__main__":
    main()