# Resources Directory

This directory contains supporting resources for the structural design standards library.

## Directory Structure

```
resources/
├── __init__.py              # Package initialization
├── README.md               # This file
├── schemas/                # JSON validation schemas
│   ├── beam-design.json    # Beam design input/output validation
│   ├── column-design.json  # Column design validation
│   └── materials.json      # Material properties validation
├── templates/              # Document templates
│   ├── design_report.html  # HTML design report template
│   ├── calculation_sheet.html  # Calculation worksheet template
│   └── summary_report.html # Executive summary template
├── images/                 # Images and diagrams
│   ├── beam_diagrams/      # Beam loading and geometry diagrams
│   ├── column_diagrams/    # Column cross-sections and details
│   ├── material_charts/    # Material property charts
│   └── logos/              # Company and standard logos
└── diagrams/               # Technical drawings
    ├── reinforcement_details/  # Reinforcement detailing drawings
    ├── connection_details/     # Connection details
    └── section_properties/     # Cross-section property diagrams
```

## JSON Schemas

The `schemas/` directory contains JSON Schema files for validating input and output data:

### beam-design.json
Validates beam design input parameters and output results including:
- Geometry (width, height, effective depth, span length)
- Materials (concrete and steel properties)
- Loads (dead, live, wind, seismic)
- Design results (moments, reinforcement, deflection)

### column-design.json
Validates column design parameters including:
- Geometry (rectangular or circular sections)
- Axial loads and moments
- Slenderness analysis
- Interaction analysis results

### Example Usage
```python
import json
import jsonschema

# Load schema
with open('resources/schemas/beam-design.json') as f:
    schema = json.load(f)

# Validate input data
beam_input = {
    "type": "beam_design_input",
    "standard": "ACI318M25",
    "beam_type": "simply_supported",
    "geometry": {
        "width": 300,
        "height": 600,
        "effective_depth": 550,
        "span_length": 6000
    },
    "materials": {
        "concrete": {"fc_prime": 28.0},
        "steel": {"fy": 420, "grade": "GRADE420"}
    },
    "loads": {
        "dead_load": 5.0,
        "live_load": 8.0
    }
}

# Validate
jsonschema.validate(beam_input, schema)
```

## Templates

The `templates/` directory contains HTML templates for generating reports:

### design_report.html
Comprehensive design report template with:
- Project information header
- Design summary cards
- Member-by-member design results
- Material summaries
- Design verification tables
- Professional formatting for printing

### Template Usage
```python
from jinja2 import Template

# Load template
with open('resources/templates/design_report.html') as f:
    template = Template(f.read())

# Render with data
html_report = template.render(
    project_name="Office Building Design",
    client_name="ABC Construction",
    engineer_name="John Doe, P.E.",
    design_standard="ACI 318M-25",
    members=[
        {
            "type": "Beam",
            "name": "B1",
            "status": "PASS",
            "utilization": 85,
            "required_steel_area": 1200
        }
    ]
)
```

## Images and Diagrams

### Planned Content
- **Beam Diagrams**: Loading diagrams, shear and moment diagrams
- **Column Diagrams**: Cross-section details, reinforcement layouts
- **Material Charts**: Stress-strain curves, interaction diagrams
- **Standard Logos**: ACI, Thai Ministry, TIS logos

### Adding New Resources

To add new resources:

1. **Schemas**: Place JSON schema files in `schemas/` directory
2. **Templates**: Add HTML/CSS templates to `templates/` directory  
3. **Images**: Organize images by type in `images/` subdirectories
4. **Diagrams**: Add technical drawings to `diagrams/` subdirectories

### File Naming Conventions

- **Schemas**: Use kebab-case (e.g., `beam-design.json`)
- **Templates**: Use snake_case (e.g., `design_report.html`)
- **Images**: Use descriptive names with type prefix (e.g., `beam_simply_supported.svg`)
- **Diagrams**: Use standard abbreviations (e.g., `rc_section_detail.dwg`)

## Standards Compliance

Resources should comply with:
- **ACI 318M-25**: American Concrete Institute standards
- **Thai Ministry B.E. 2566**: Thai structural design regulations
- **TIS Standards**: Thai Industrial Standards
- **JSON Schema Draft 07**: For validation schemas
- **HTML5/CSS3**: For templates

## Quality Guidelines

1. **Schemas**: Must validate against JSON Schema meta-schema
2. **Templates**: Must render correctly in modern browsers
3. **Images**: Should be vector format (SVG) when possible
4. **Diagrams**: Must include dimension and scale information

## License and Usage

Resources in this directory are part of the structural design standards library and are subject to the same license terms. Templates and schemas may be customized for specific project needs.

## Contributing

When contributing new resources:

1. Follow established naming conventions
2. Include appropriate documentation
3. Test schemas with sample data
4. Verify template rendering
5. Update this README as needed

## Version History

- v1.0.0: Initial resource structure with basic schemas and templates
- Future: Additional schemas for slab, wall, and footing design
- Future: Interactive calculation templates
- Future: Multilingual template support