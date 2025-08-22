"""
Resources Package
=================

Contains supporting resources for the structural design standards library:
- images/: Diagrams, charts, and visual aids
- diagrams/: Technical drawings and design diagrams  
- templates/: Document and report templates
- schemas/: JSON validation schemas
"""

from pathlib import Path

# Resource directory paths
RESOURCES_DIR = Path(__file__).parent
IMAGES_DIR = RESOURCES_DIR / "images"
DIAGRAMS_DIR = RESOURCES_DIR / "diagrams"
TEMPLATES_DIR = RESOURCES_DIR / "templates"
SCHEMAS_DIR = RESOURCES_DIR / "schemas"

# Create directories if they don't exist
for directory in [IMAGES_DIR, DIAGRAMS_DIR, TEMPLATES_DIR, SCHEMAS_DIR]:
    directory.mkdir(exist_ok=True)

__all__ = [
    'RESOURCES_DIR',
    'IMAGES_DIR', 
    'DIAGRAMS_DIR',
    'TEMPLATES_DIR',
    'SCHEMAS_DIR'
]