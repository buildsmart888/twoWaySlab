# Thai Ministry Regulation B.E. 2566 Implementation
# กฎกระทรวง กำหนดการออกแบบโครงสร้างอาคาร และลักษณะและคุณสมบัติของวัสดุที่ใช้ในงานโครงสร้างอาคาร พ.ศ. 2566

## 📋 Overview / ภาพรวม

This implementation provides comprehensive support for the **Thai Ministry Regulation for Building Structural Design B.E. 2566 (2023)** as a separate function within the twoWaySlab structural engineering software.

การดำเนินการนี้ให้การสนับสนุนอย่างครอบคลุมสำหรับ **กฎกระทรวง กำหนดการออกแบบโครงสร้างอาคาร และลักษณะและคุณสมบัติของวัสดุที่ใช้ในงานโครงสร้างอาคาร พ.ศ. 2566** เป็นฟังก์ชันแยกต่างหากภายในซอฟต์แวร์วิศวกรรมโครงสร้าง twoWaySlab

## 🎯 Key Features / คุณสมบัติหลัก

### ✨ **Ministry Regulation Compliance**
- **Concrete Cover Requirements** - ความหนาคอนกรีตปิดตามสภาพแวดล้อม
- **Safety Factors** - ค่าความปลอดภัยตามกฎกระทรวง
- **Load Combinations** - การผสมน้ำหนักตามมาตรฐาน
- **Material Properties** - คุณสมบัติวัสดุตาม TIS
- **Quality Control** - การควบคุมคุณภาพ
- **Construction Tolerances** - ความคลาดเคลื่อนในการก่อสร้าง

### 🔧 **Integration Features**
- **Seamless Integration** - บูรณาการเข้ากับระบบ Thai RC ที่มีอยู่
- **Configuration Support** - รองรับในระบบการกำหนดค่า
- **Multi-language** - รองรับภาษาไทยและอังกฤษ
- **Unit Conversion** - การแปลงหน่วยระหว่าง Traditional Thai (ksc, kgf, tonf) และ SI (MPa, kN)

## 🏗️ **Implementation Structure / โครงสร้างการทำงาน**

```
thaiMinistryReg.py          - Main Ministry Regulation module
├── ThaiMinistryRegulation2566  - Core regulation class
├── Concrete Cover Requirements  - ความหนาคอนกรีตปิด
├── Safety Factors              - ค่าความปลอดภัย
├── Load Combinations           - การผสมน้ำหนัก
├── Material Specifications     - ข้อกำหนดวัสดุ
├── Quality Control            - การควบคุมคุณภาพ
└── Compliance Reporting       - รายงานการตรวจสอบ

thiRc.py (Enhanced)         - Enhanced Thai RC module with Ministry Regulation integration
config.py (Enhanced)        - Configuration system with Ministry Regulation support
translations/th.json        - Thai language translations for Ministry Regulation
test_ministry_regulation.py - Comprehensive test suite
```

## 📚 **Core Components / องค์ประกอบหลัก**

### 1. **Concrete Cover Requirements / ความหนาคอนกรีตปิด**

```python
from thaiMinistryReg import ThaiMinistryRegulation2566

reg = ThaiMinistryRegulation2566()

# Get cover requirements based on environment and element type
cover, unit, desc = reg.get_concrete_cover('slab', 'normal')
# Result: (20, 'mm', 'พื้นธรรมดา')
```

**Available Environments / สภาพแวดล้อม:**
- `normal` - สภาพแวดล้อมปกติ
- `aggressive` - สภาพแวดล้อมรุนแรง  
- `marine` - สภาพแวดล้อมทางทะเล

**Available Elements / องค์ประกอบ:**
- `slab` - พื้น
- `beam` - คาน
- `column` - เสา
- `foundation` - ฐานราก

### 2. **Safety Factors / ค่าความปลอดภัย**

```python
# Get safety factors per Ministry Regulation B.E. 2566
sf_concrete = reg.get_safety_factor('concrete')      # 1.5
sf_steel = reg.get_safety_factor('steel')           # 1.15
sf_dead = reg.get_safety_factor('dead_load')        # 1.4
sf_live = reg.get_safety_factor('live_load')        # 1.6
sf_wind = reg.get_safety_factor('wind_load')        # 1.6
sf_seismic = reg.get_safety_factor('seismic_load')  # 1.0
```

### 3. **Load Combinations / การผสมน้ำหนัก**

```python
# Define loads (kN/m² or kN)
loads = {
    'D': 10.0,  # Dead load / น้ำหนักตาย
    'L': 5.0,   # Live load / น้ำหนักใช้สอย
    'W': 8.0,   # Wind load / น้ำหนักลม
    'E': 6.0    # Earthquake load / น้ำหนักแผ่นดินไหว
}

# Check ultimate limit state combinations
uls_results = reg.check_load_combination(loads, 'ultimate')

# Check serviceability limit state combinations  
sls_results = reg.check_load_combination(loads, 'serviceability')
```

**Ultimate Limit State Combinations:**
- ULS-1: `1.4D + 1.6L`
- ULS-2: `1.2D + 1.6L + 1.6W`
- ULS-3: `1.2D + 1.0L + 1.0E`
- ULS-4: `0.9D + 1.6W`
- ULS-5: `0.9D + 1.0E`

**Serviceability Limit State Combinations:**
- SLS-1: `1.0D + 1.0L`
- SLS-2: `1.0D + 0.7L`
- SLS-3: `1.0D + 0.5L + 1.0W`

### 4. **Material Properties / คุณสมบัติวัสดุ**

```python
# Get concrete properties
concrete_props = reg.get_material_properties('concrete', 'Fc210')
# Returns: {
#   'fc_ksc': 210, 'fc_mpa': 21.0,
#   'w_c_ratio': 0.60, 'min_cement': 300,
#   'usage': 'งานโครงสร้าง'
# }

# Get steel properties
steel_props = reg.get_material_properties('steel', 'SD40')
# Returns: {
#   'fy_ksc': 4000, 'fy_mpa': 392.4,
#   'fu_ksc': 5600, 'fu_mpa': 549.4,
#   'type': 'เหล็กข้ออ้อย'
# }
```

**Available Concrete Grades:**
- `Fc180` - 180 ksc (18.0 MPa) - งานทั่วไป
- `Fc210` - 210 ksc (21.0 MPa) - งานโครงสร้าง
- `Fc240` - 240 ksc (24.0 MPa) - งานโครงสร้าง
- `Fc280` - 280 ksc (28.0 MPa) - งานโครงสร้างแรงสูง
- `Fc350` - 350 ksc (35.0 MPa) - งานโครงสร้างพิเศษ

**Available Steel Grades:**
- `SD40` - 4000 ksc (392.4 MPa) - เหล็กข้ออ้อย
- `SD50` - 5000 ksc (490.5 MPa) - เหล็กข้ออ้อย  
- `SR24` - 2400 ksc (235.4 MPa) - เหล็กเส้นกลม

### 5. **Design Strength Calculation / การคำนวณกำลังรับแรงออกแบบ**

```python
# Calculate design strength including safety factors
fc_nominal = 21.0  # MPa
fc_design, desc = reg.calculate_design_strength('concrete', 'Fc210', fc_nominal)
# Result: (14.0, "Design strength = 21.0/1.5 = 14.0")

fy_nominal = 392.4  # MPa  
fy_design, desc = reg.calculate_design_strength('steel', 'SD40', fy_nominal)
# Result: (341.2, "Design strength = 392.4/1.15 = 341.2")
```

### 6. **Concrete Mix Validation / การตรวจสอบส่วนผสมคอนกรีต**

```python
# Validate concrete mix design
validation = reg.validate_concrete_mix(
    grade='Fc210',
    w_c_ratio=0.55,
    cement_content=320,  # kg/m³
    aggregate_size=25    # mm
)

print(f"Valid: {validation['is_valid']}")
if validation['errors']:
    print(f"Errors: {validation['errors']}")
if validation['warnings']:
    print(f"Warnings: {validation['warnings']}")
```

### 7. **Construction Tolerances / ความคลาดเคลื่อนในการก่อสร้าง**

```python
# Get construction tolerances
tolerances = reg.get_construction_tolerances()

# Access specific tolerances
column_tolerance = tolerances['dimensional_tolerances']['column_position']
# Result: {'horizontal': '±12 mm', 'vertical': '±6 mm'}

cover_tolerance = tolerances['dimensional_tolerances']['concrete_cover']
# Result: '+10mm/-5mm'
```

## 🔄 **Integration with Existing Thai RC System**

### Using Ministry Regulation through Thai RC:

```python
from thiRc import ThaiRc_set

# Initialize Thai RC with Ministry Regulation support
thai_rc = ThaiRc_set()

# Get Ministry Regulation instance
ministry_reg = thai_rc.get_ministry_regulation_2566()

# Validate project against Ministry Regulation
project_data = {
    'project_name': 'ตัวอย่างโครงการพื้น 2 ทิศทาง',
    'concrete_grade': 'Fc210',
    'steel_grade': 'SD40',
    'element_type': 'slab',
    'environment': 'normal',
    'loads': {
        'D': 12.0,  # kN/m²
        'L': 6.0,   # kN/m²
        'W': 4.0,   # kN/m²
        'E': 3.0    # kN/m²
    }
}

# Comprehensive validation
validation_result = thai_rc.validate_with_ministry_regulation(project_data)

# Generate compliance report
compliance_report = validation_result['compliance_report']
print(compliance_report)
```

## ⚙️ **Configuration System Integration**

### Using through Configuration System:

```python
from config import Config

config = Config()

# Switch to Ministry Regulation mode
config.set_building_code('thai_ministry_2566')

# Get Ministry Regulation instance through config
ministry_reg = config.get_ministry_regulation_instance()

# Check if available
is_available = config.is_ministry_regulation_available()
```

## 🌐 **Multi-language Support / การรองรับหลายภาษา**

### Thai Language Support:

```python
from i18n import i18n

# Set Thai language
i18n.set_language('th')

# Get translated terms
ministry_title = i18n.t('ministry_regulation.title')
# Result: "กฎกระทรวง พ.ศ. 2566"

concrete_cover = i18n.t('ministry_regulation.concrete_cover')
# Result: "ความหนาคอนกรีตปิด"

safety_factors = i18n.t('ministry_regulation.safety_factors')  
# Result: "ค่าความปลอดภัย"
```

## 📊 **Practical Usage Examples / ตัวอย่างการใช้งานจริง**

### Example 1: Two-Way Slab Design

```python
from thiRc import ThaiRc_set
from thaiMinistryReg import ThaiMinistryRegulation2566

# Initialize systems
thai_rc = ThaiRc_set()
ministry_reg = ThaiMinistryRegulation2566()

# Project parameters
slab_dimensions = (4.0, 6.0)  # 4m × 6m
thickness = 150  # mm
concrete_grade = 'Fc210'
steel_grade = 'SD40'

# Material properties in traditional Thai units
fc_ksc = 210  # ksc
fy_ksc = thai_rc.get_steel_strength('SD40', 'ksc')  # 4000 ksc

# Convert to SI for Ministry Regulation
fc_mpa = thai_rc.ksc_to_mpa(fc_ksc)  # 20.6 MPa
fy_mpa = thai_rc.get_steel_strength('SD40', 'mpa')  # 392.4 MPa

# Get Ministry Regulation requirements
cover_req, unit, desc = ministry_reg.get_concrete_cover('slab', 'normal')
print(f"Required cover: {cover_req} {unit} ({desc})")

# Safety factors per Ministry Regulation
sf_concrete = ministry_reg.get_safety_factor('concrete')  # 1.5
sf_steel = ministry_reg.get_safety_factor('steel')      # 1.15

# Design strengths
fcd_ksc = fc_ksc / sf_concrete  # 140.0 ksc
fyd_ksc = fy_ksc / sf_steel     # 3478.3 ksc

print(f"Design strengths: fcd = {fcd_ksc:.1f} ksc, fyd = {fyd_ksc:.1f} ksc")

# Load analysis in traditional Thai units
self_weight = 0.15 * 2400  # 360 kgf/m² (150mm × 2400 kgf/m³)
floor_finish = 100         # 100 kgf/m²
live_load = 300           # 300 kgf/m²

dead_load_kgf = self_weight + floor_finish  # 460 kgf/m²
live_load_kgf = live_load                   # 300 kgf/m²

# Convert to SI for Ministry Regulation load combinations
dead_load_kn = thai_rc.load_kgf_m2_to_kn_m2(dead_load_kgf)  # 4.51 kN/m²
live_load_kn = thai_rc.load_kgf_m2_to_kn_m2(live_load_kgf)  # 2.94 kN/m²

print(f"Loads: Dead = {dead_load_kgf:.0f} kgf/m² ({dead_load_kn:.2f} kN/m²)")
print(f"       Live = {live_load_kgf:.0f} kgf/m² ({live_load_kn:.2f} kN/m²)")

# Load combinations per Ministry Regulation
loads = {'D': dead_load_kn, 'L': live_load_kn, 'W': 0.0, 'E': 0.0}
uls_combinations = ministry_reg.check_load_combination(loads, 'ultimate')

for combo in uls_combinations[:2]:  # Show first 2 combinations
    print(f"{combo['name']}: {combo['formula']} = {combo['result']:.2f} kN/m²")

# Reinforcement using Thai bar designations
bar_designation = 'DB20'
spacing = 200  # mm

bar_area = thai_rc.Ra(bar_designation)      # 314.2 mm²
area_per_m = thai_rc.Ra_p(bar_designation, spacing)  # 1571 mm²/m

print(f"Reinforcement: {bar_designation} @ {spacing}mm")
print(f"Area provided: {area_per_m:.0f} mm²/m")

# Capacity in traditional Thai units
capacity_tonf = bar_area * fy_ksc / 1000000  # Convert to tonf
print(f"Capacity per bar: {capacity_tonf:.3f} tonf")
```

### Example 2: Compliance Report Generation

```python
# Generate comprehensive compliance report
project_info = {
    'project_name': 'Two-Way Slab Design Example',
    'date': '2024-01-15',
    'concrete_grade': 'Fc210',
    'steel_grade': 'SD40',
    'environment': 'normal',
    'element_type': 'slab'
}

compliance_report = ministry_reg.generate_compliance_report(project_info)
print(compliance_report)

# Save report to file
with open('ministry_regulation_compliance_report.txt', 'w', encoding='utf-8') as f:
    f.write(compliance_report)
```

## 🧪 **Testing / การทดสอบ**

### Run Comprehensive Tests:

```bash
# Run the test suite
python test_ministry_regulation.py
```

**Test Coverage:**
1. ✅ **Ministry Regulation Standalone** - การทำงานของโมดูลแยกเดี่ยว
2. ✅ **Integration with Thai RC** - การบูรณาการกับระบบ Thai RC
3. ✅ **Configuration System** - ระบบการกำหนดค่า
4. ✅ **Practical Examples** - ตัวอย่างการใช้งานจริง

### Expected Test Output:

```
🎉 ALL TESTS PASSED! Ministry Regulation B.E. 2566 is ready to use.
```

## 📋 **Reference Standards / มาตรฐานอ้างอิง**

- **กฎกระทรวง พ.ศ. 2566** - Ministry Regulation B.E. 2566 (2023)
- **มยผ. 1103** - Thai Industrial Standard for Reinforcement Steel
- **มยผ. 1101** - Thai Industrial Standard for Concrete and Reinforced Concrete
- **ASA Guidelines** - Association of Siamese Architects Guidelines

## 🛠️ **Installation Requirements / ความต้องการในการติดตั้ง**

```python
# Required Python packages
numpy>=1.19.0
sympy>=1.8.0
pandas>=1.3.0
```

## 🤝 **Contributing / การมีส่วนร่วม**

To contribute to the Ministry Regulation implementation:

1. Follow existing code structure and patterns
2. Add comprehensive tests for new features
3. Update documentation and translations
4. Maintain compatibility with existing Thai RC system
5. Use proper Thai technical terminology

## 📄 **License / ใบอนุญาต**

This implementation follows the same license terms as the original twoWaySlab project while adding compliance with Thai Ministry Regulation B.E. 2566.

---

**Enhanced twoWaySlab with Thai Ministry Regulation B.E. 2566** - Supporting Thai structural engineering standards with comprehensive regulatory compliance and traditional unit system support.

**โปรแกรม twoWaySlab ปรับปรุงพร้อมกฎกระทรวง พ.ศ. 2566** - รองรับมาตรฐานวิศวกรรมโครงสร้างไทยพร้อมการตรวจสอบตามกฎระเบียบและระบบหน่วยแบบดั้งเดิม