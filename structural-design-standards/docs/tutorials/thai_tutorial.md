# Thai Ministry Regulation B.E. 2566 Tutorial

This comprehensive tutorial demonstrates how to use the Thai Ministry of Interior Regulation B.E. 2566 implementation for structural design calculations in Thailand.

## Overview

The Thai standards implementation includes:
- **Thai Ministry Regulation B.E. 2566**: Building structure design standards
- **TIS Standards**: Thai Industrial Standards for materials and loads
- **Thai Materials**: Local concrete and steel grades
- **Thai Units**: Traditional Thai units with metric conversions
- **Localization**: Thai language support for documentation

## Table of Contents

1. [Setting Up Thai Standards](#setting-up-thai-standards)
2. [Thai Materials](#thai-materials)
3. [Thai Load Combinations](#thai-load-combinations)
4. [Concrete Beam Design](#concrete-beam-design)
5. [Steel Column Design](#steel-column-design)
6. [Wind Load Calculations](#wind-load-calculations)
7. [Seismic Load Calculations](#seismic-load-calculations)
8. [Multi-Language Reports](#multi-language-reports)

## Setting Up Thai Standards

### Basic Import and Configuration

```python
from structural_standards.thai.ministry_2566 import (
    ThaiLoadCombinations,
    ThaiWindLoads,
    ThaiSeismicLoads
)
from structural_standards.thai.materials import (
    ThaiConcrete,
    ThaiSteel
)
from structural_standards.thai.units import ThaiUnitConverter
from structural_standards.i18n.translator import get_translator

# Set up Thai language support
translator = get_translator()
translator.set_language('th')

# Initialize unit converter
unit_converter = ThaiUnitConverter()
```

### Project Configuration

```python
# Define project parameters for Thai building design
project_config = {
    "location": "Bangkok",
    "building_type": "office",
    "importance_factor": 1.0,
    "design_standard": "Thai Ministry B.E. 2566",
    "language": "thai"
}

print("โครงการ: อาคารสำนักงาน กรุงเทพมหานคร")
print("มาตรฐานการออกแบบ: กฎกระทรวงมหาดไทย พ.ศ. 2566")
```

## Thai Materials

### Thai Concrete Grades

Thailand uses different concrete grade classifications based on local standards:

```python
# Create Thai concrete materials
# Fc180 = 18 MPa (18 kg/cm²)
concrete_fc180 = ThaiConcrete(
    grade="Fc180",
    fc_prime=18.0,  # MPa
    density=2400,   # kg/m³
    ec_modulus=None  # Auto-calculated per Thai standards
)

# Fc210 = 21 MPa (common for general construction)
concrete_fc210 = ThaiConcrete(
    grade="Fc210", 
    fc_prime=21.0,
    density=2400
)

# Fc280 = 28 MPa (high-strength for major structures)
concrete_fc280 = ThaiConcrete(
    grade="Fc280",
    fc_prime=28.0,
    density=2400
)

# Display material properties in Thai
print(f"คอนกรีต {concrete_fc210.grade}")
print(f"กำลังรับแรงอัด fc' = {concrete_fc210.fc_prime} MPa")
print(f"โมดูลัสยืดหยุ่น Ec = {concrete_fc210.get_elastic_modulus():.0f} MPa")
```

### Thai Steel Grades

```python
# Thai steel grades per TIS standards
# SR24 = 240 MPa yield strength (mild steel)
steel_sr24 = ThaiSteel(
    grade="SR24",
    fy=240,  # MPa
    fu=370,  # MPa
    density=7850  # kg/m³
)

# SD40 = 400 MPa (deformed bars, common for reinforcement)
steel_sd40 = ThaiSteel(
    grade="SD40",
    fy=400,
    fu=560,
    density=7850
)

# SD50 = 500 MPa (high-strength deformed bars)
steel_sd50 = ThaiSteel(
    grade="SD50", 
    fy=500,
    fu=665,
    density=7850
)

print(f"เหล็กเส้น {steel_sd40.grade}")
print(f"จุดครากแรง fy = {steel_sd40.fy} MPa")
print(f"จุดขาดแรง fu = {steel_sd40.fu} MPa")
```

## Thai Load Combinations

### Load Combination Factors

```python
# Initialize Thai load combinations per Ministry Regulation B.E. 2566
load_combos = ThaiLoadCombinations()

# Basic loads (in kN/m²)
dead_load = 5.0      # น้ำหนักคงที่
live_load = 3.0      # น้ำหนักบรรทุกใช้สอย
wind_load = 1.2      # น้ำหนักลม
earthquake_load = 2.0 # น้ำหนักแผ่นดินไหว

# Get design load combinations
strength_combinations = load_combos.get_strength_combinations(
    dead_load=dead_load,
    live_load=live_load, 
    wind_load=wind_load,
    earthquake_load=earthquake_load
)

print("ชุดค่าผสมแรงกระทำ (Strength Design):")
for i, combo in enumerate(strength_combinations):
    print(f"LC{i+1}: {combo['name']}")
    print(f"  Wu = {combo['total_load']:.2f} kN/m²")
    print(f"  สูตร: {combo['formula']}")
```

### Service Load Combinations

```python
# Service load combinations for deflection and crack control
service_combinations = load_combos.get_service_combinations(
    dead_load=dead_load,
    live_load=live_load,
    wind_load=wind_load
)

print("\nชุดค่าผสมแรงกระทำ (Service Load):")
for combo in service_combinations:
    print(f"{combo['name']}: {combo['total_load']:.2f} kN/m²")
```

## Concrete Beam Design

### Thai RC Beam Design Example

```python
from structural_standards.thai.members import ThaiBeam

# Define beam geometry (typical Thai building dimensions)
beam = ThaiBeam(
    width=300,      # mm (30 cm)
    height=600,     # mm (60 cm) 
    span_length=6000,  # mm (6 m)
    concrete=concrete_fc210,
    steel=steel_sd40,
    clear_cover=25  # mm
)

# Apply Thai building loads
# Dead load: self-weight + finishes + utilities
beam_dead_load = 8.0  # kN/m
# Live load: office building per Thai building code
beam_live_load = 5.0  # kN/m

# Calculate design moments using Thai load combinations
design_moments = load_combos.calculate_beam_moments(
    span=6.0,  # m
    dead_load=beam_dead_load,
    live_load=beam_live_load
)

critical_moment = max(design_moments.values())  # kN⋅m

print(f"คาน RC ขนาด {beam.width}×{beam.height} mm")
print(f"คอนกรีต: {beam.concrete.grade}")
print(f"เหล็กเส้น: {beam.steel.grade}")
print(f"โมเมนต์ออกแบบ: {critical_moment:.1f} kN⋅m")

# Design reinforcement per Thai standards
beam_design = beam.design_flexural_reinforcement(critical_moment)

print(f"\nผลการออกแบบ:")
print(f"เหล็กเส้นที่ต้องการ: {beam_design['required_steel_area']:.0f} mm²")
print(f"เหล็กเส้นที่ใส่: {beam_design['provided_steel_area']:.0f} mm²")
print(f"อัตราส่วนเหล็ก: {beam_design['steel_ratio']:.4f}")
print(f"สถานะ: {'ผ่าน' if beam_design['status'] == 'PASS' else 'ไม่ผ่าน'}")
```

## Steel Column Design

### Thai Steel Column with Thai Units

```python
from structural_standards.thai.members import ThaiSteelColumn

# Steel column using Thai structural steel
steel_column = ThaiSteelColumn(
    section="H-400×400×13×21",  # Thai standard H-section
    steel_grade="SS400",        # Thai structural steel grade
    length=4000,                # mm (4 m floor height)
    end_conditions="pinned"
)

# Convert loads from traditional Thai units
axial_load_ton = 50  # metric tons (common in Thai practice)
axial_load_kn = unit_converter.tons_to_kn(axial_load_ton)

moment_load = 80  # kN⋅m

print(f"เสาเหล็ก {steel_column.section}")
print(f"แรงอัด: {axial_load_ton} ตัน = {axial_load_kn:.0f} kN")
print(f"โมเมนต์: {moment_load} kN⋅m")

# Check column capacity per Thai steel design code
column_check = steel_column.check_capacity(
    axial_load=axial_load_kn,
    moment_load=moment_load
)

print(f"\nการตรวจสอบกำลังรับแรง:")
print(f"อัตราส่วนการใช้งาน: {column_check['utilization']:.1f}%")
print(f"สถานะ: {'ปลอดภัย' if column_check['status'] == 'PASS' else 'ไม่ปลอดภัย'}")
```

## Wind Load Calculations

### Thai Wind Load per TIS 1311-50

```python
# Initialize Thai wind load calculations
wind_calculator = ThaiWindLoads()

# Building parameters for Bangkok high-rise
building_data = {
    "location": "Bangkok",           # จังหวัดกรุงเทพมหานคร
    "terrain_category": "B",         # Urban area
    "building_height": 50,           # m
    "building_width": 20,            # m
    "building_length": 40,           # m
    "importance_factor": 1.0         # Standard occupancy
}

# Calculate wind loads per TIS 1311-50
wind_loads = wind_calculator.calculate_wind_loads(building_data)

print("การคำนวณแรงลมตาม TIS 1311-50:")
print(f"ความเร็วลมออกแบบ: {wind_loads['design_wind_speed']:.1f} m/s")
print(f"ความดันลมพื้นฐาน: {wind_loads['basic_wind_pressure']:.2f} kN/m²")
print(f"แรงลมด้านหน้า: {wind_loads['windward_pressure']:.2f} kN/m²")
print(f"แรงลมด้านหลัง: {wind_loads['leeward_pressure']:.2f} kN/m²")

# Wind force on structure
total_wind_force = wind_loads['total_wind_force']  # kN
print(f"แรงลมรวม: {total_wind_force:.0f} kN")
```

### Provincial Wind Zone Analysis

```python
# Different wind zones in Thailand
provinces = ["กรุงเทพมหานคร", "ภูเก็ต", "สงขลา", "เชียงใหม่"]

print("\nแรงลมในจังหวัดต่างๆ:")
for province in provinces:
    wind_data = wind_calculator.get_provincial_wind_data(province)
    print(f"{province}: {wind_data['basic_wind_speed']} m/s, "
          f"Zone {wind_data['wind_zone']}")
```

## Seismic Load Calculations

### Thai Earthquake Load per TIS 1301/1302-61

```python
# Initialize Thai seismic load calculations
seismic_calculator = ThaiSeismicLoads()

# Building seismic parameters
seismic_data = {
    "location": "Bangkok",
    "soil_type": "SC",              # Soft clay (common in Bangkok)
    "building_height": 50,          # m
    "structural_system": "moment_frame",
    "importance_factor": 1.0,
    "building_weight": 50000        # kN (total building weight)
}

# Calculate seismic loads per TIS standards
seismic_loads = seismic_calculator.calculate_seismic_loads(seismic_data)

print("การคำนวณแรงแผ่นดินไหวตาม TIS 1301/1302-61:")
print(f"ค่าสัมประสิทธิ์ตอบสนองแผ่นดินไหว: {seismic_loads['response_coefficient']:.3f}")
print(f"แรงแผ่นดินไหวพื้นฐาน: {seismic_loads['base_shear']:.0f} kN")
print(f"คาบการสั่นพื้นฐาน: {seismic_loads['fundamental_period']:.2f} วินาที")

# Vertical distribution of seismic forces
floor_forces = seismic_loads['floor_forces']
print(f"\nการกระจายแรงแผ่นดินไหวตามความสูง:")
for floor, force in floor_forces.items():
    print(f"ชั้นที่ {floor}: {force:.0f} kN")
```

## Multi-Language Reports

### Generating Thai Language Reports

```python
from structural_standards.reports import DesignReport
import datetime

# Create comprehensive design report in Thai
report = DesignReport(language='th')

# Project information in Thai
project_info = {
    "project_name": "อาคารสำนักงาน ABC",
    "client_name": "บริษัท เอบีซี จำกัด",
    "engineer_name": "นาย สมชาย วิศวกร, วศ.บ.",
    "design_date": datetime.date.today().strftime("%d/%m/%Y"),
    "design_standard": "กฎกระทรวงมหาดไทย พ.ศ. 2566",
    "location": "กรุงเทพมหานคร"
}

# Add beam design results
report.add_member_design(
    member_type="คาน",
    member_id="B1",
    design_results={
        "moment_capacity": "120 kN⋅m",
        "steel_reinforcement": "6-DB20 (1,884 mm²)",
        "concrete_grade": "Fc210",
        "steel_grade": "SD40",
        "status": "ผ่านเกณฑ์"
    }
)

# Generate Thai language report
thai_report = report.generate_html_report(project_info)

# Save report
with open("รายงานการออกแบบโครงสร้าง.html", "w", encoding="utf-8") as f:
    f.write(thai_report)

print("สร้างรายงานการออกแบบโครงสร้างเป็นภาษาไทยเสร็จสิ้น")
print("ไฟล์: รายงานการออกแบบโครงสร้าง.html")
```

### Bilingual Documentation

```python
# Create bilingual report (Thai-English)
from structural_standards.i18n import BillingualReport

bilingual_report = BillingualReport(
    primary_language='th',
    secondary_language='en'
)

# Technical terms in both languages
technical_terms = {
    'concrete_strength': {
        'th': 'กำลังรับแรงอัดของคอนกรีต',
        'en': 'Concrete Compressive Strength'
    },
    'steel_yield': {
        'th': 'จุดคราก ของเหล็กเส้น',
        'en': 'Steel Yield Strength'
    },
    'moment_capacity': {
        'th': 'กำลังรับโมเมนต์',
        'en': 'Moment Capacity'
    }
}

# Generate bilingual technical specifications
specifications = bilingual_report.create_technical_specifications(
    concrete=concrete_fc210,
    steel=steel_sd40,
    terms=technical_terms
)

print("รายละเอียดทางเทคนิค / Technical Specifications:")
for key, value in specifications.items():
    print(f"{value['th']} / {value['en']}")
```

## Advanced Features

### Thai Unit Conversions

```python
# Traditional Thai units commonly used in construction
converter = ThaiUnitConverter()

# Length conversions
wah = 4.0  # วา (traditional Thai length unit)
meters = converter.wah_to_meters(wah)
print(f"{wah} วา = {meters} เมตร")

# Area conversions  
rai = 1.0  # ไร่ (traditional Thai area unit)
square_meters = converter.rai_to_square_meters(rai)
print(f"{rai} ไร่ = {square_meters} ตารางเมตร")

# Pressure conversions (old Thai practice)
ksc = 210  # กิโลกรัมแรงต่อตารางเซนติเมตร
mpa = converter.ksc_to_mpa(ksc)
print(f"{ksc} กก./ซม.² = {mpa:.1f} MPa")
```

### Integration with Building Information Modeling (BIM)

```python
# Export Thai design results for BIM integration
from structural_standards.integration import BIMExporter

bim_exporter = BIMExporter(language='th')

# Prepare structural elements for BIM
elements = [
    {
        'type': 'beam',
        'id': 'B1', 
        'dimensions': '300×600',
        'concrete': 'Fc210',
        'reinforcement': '6-DB20',
        'location': 'ชั้น 2'
    },
    {
        'type': 'column',
        'id': 'C1',
        'dimensions': '400×400', 
        'concrete': 'Fc280',
        'reinforcement': '8-DB25',
        'location': 'แกน A-1'
    }
]

# Export to industry standard formats
ifc_file = bim_exporter.export_to_ifc(elements, "thai_building_model.ifc")
tekla_file = bim_exporter.export_to_tekla(elements, "thai_structures.xml")

print("ส่งออกข้อมูลโครงสร้างสำหรับ BIM สำเร็จ")
print(f"IFC File: {ifc_file}")
print(f"Tekla File: {tekla_file}")
```

## Best Practices

### 1. Thai Building Code Compliance

- Always use appropriate Thai material grades (Fc180-Fc350 for concrete)
- Apply correct load factors per Ministry Regulation B.E. 2566
- Consider local environmental conditions (high humidity, monsoon)
- Follow Thai construction practices and dimensional standards

### 2. Language and Documentation

- Use Thai language for client communications and official reports
- Include both Thai and international units in technical drawings
- Reference appropriate Thai industrial standards (TIS)
- Maintain consistent terminology throughout project documentation

### 3. Regional Considerations

- Account for Bangkok's soft soil conditions in foundation design
- Apply appropriate wind loads for coastal vs. inland locations
- Consider seismic requirements for different regions of Thailand
- Use local material availability and construction methods

### 4. Quality Assurance

- Validate calculations against hand calculations and established precedents
- Cross-check with international standards for benchmarking
- Review designs with local engineering consultants
- Ensure compliance with local building permits and approvals

## Troubleshooting

### Common Issues

1. **Unit Conversion Errors**
   ```python
   # Always specify units clearly
   force_kn = 100  # kN
   force_ton = unit_converter.kn_to_tons(force_kn)  # 10.2 tons
   ```

2. **Material Grade Confusion**
   ```python
   # Use standard Thai material naming
   concrete = ThaiConcrete(grade="Fc210")  # Not "fc21" or "C21"
   steel = ThaiSteel(grade="SD40")         # Not "Grade40" or "Fy400"
   ```

3. **Load Combination Application**
   ```python
   # Apply correct Thai load factors
   combinations = load_combos.get_strength_combinations(
       dead_load=dead_load,
       live_load=live_load,
       wind_load=wind_load,
       earthquake_load=earthquake_load,
       include_earthquake=True  # Always consider seismic for Thailand
   )
   ```

## Summary

This tutorial covered the comprehensive use of Thai structural design standards including:

- ✅ Thai Ministry Regulation B.E. 2566 implementation  
- ✅ Thai material specifications and grades
- ✅ Thai load combinations and environmental loads
- ✅ Practical design examples for beams and columns
- ✅ Wind and seismic load calculations per TIS standards
- ✅ Multi-language documentation and reporting
- ✅ Integration with BIM and modern design workflows

The Thai standards module provides full localization support while maintaining compatibility with international engineering practices, making it ideal for infrastructure projects in Thailand.

For additional support or advanced features, refer to the [API Documentation](../source/thai.rst) or contact the development team.

---
*บันทึก: คู่มือนี้ใช้สำหรับการออกแบบโครงสร้างตามมาตรฐานไทย กรุณาตรวจสอบการเปลี่ยนแปลงของกฎระเบียบล่าสุดก่อนการใช้งานจริง*

*Note: This tutorial is for structural design according to Thai standards. Please verify the latest regulatory changes before actual implementation.*