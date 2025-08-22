# Thai Earthquake Load Library
# ไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย

## 📋 Overview / ภาพรวม

The **Thai Earthquake Load Library** is a standalone, reusable library for calculating seismic loads on buildings according to Thai standards. It can be used across multiple projects and integrates seamlessly with existing structural engineering software.

**ไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย** เป็นไลบรารีแยกต่างหาก สามารถนำไปใช้ซ้ำได้ สำหรับการคำนวณแรงแผ่นดินไหวที่กระทำต่ออาคารตามมาตรฐานไทย สามารถนำไปใช้งานโปรเจคต่างๆ และบูรณาการเข้ากับซอฟต์แวร์วิศวกรรมโครงสร้างที่มีอยู่

## 🎯 Key Standards / มาตรฐานหลัก

### ✨ **Based on Thai Standards**
- **มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1)** - TIS 1301/1302-61 (Revised Edition 1)
- **มาตรฐานการออกแบบอาคารต้านทานการสั่นสะเทือนของแผ่นดินไหว** - Standard for Earthquake Resistant Building Design

## 🌍 **Seismic Zones in Thailand / โซนแผ่นดินไหวในประเทศไทย**

| Zone | Region | Peak Ground Acceleration | Risk Level | Example Provinces |
|------|--------|-------------------------|------------|-------------------|
| **Zone A** | พื้นที่เสี่ยงต่ำ (Low Risk) | 0.15g | ต่ำ / Low | กรุงเทพฯ, ขอนแก่น, ภูเก็ต |
| **Zone B** | พื้นที่เสี่ยงปานกลาง (Moderate Risk) | 0.25g | ปานกลาง / Moderate | ลำปาง, กาญจนบุรี |
| **Zone C** | พื้นที่เสี่ยงสูง (High Risk) | 0.40g | สูง / High | เชียงใหม่, เชียงราย, แม่ฮ่องสอน |

## 🏗️ **Core Features / คุณสมบัติหลัก**

### ✨ **Seismic Load Calculations**
- **Peak Ground Acceleration** - ความเร่งพื้นดินสูงสุดตามโซน
- **Site Coefficients** - ค่าประกอบดิน Fa และ Fv (6 soil types)
- **Building Importance** - ค่าประกอบความสำคัญอาคาร (3 levels)
- **Structural System Factors** - ค่าปรับลดแรง R และ Cd (4 systems)
- **Fundamental Period** - การคำนวณคาบธรรมชาติ
- **Base Shear Calculation** - การคำนวณแรงเฉือนฐาน
- **Lateral Force Distribution** - การกระจายแรงด้านข้าง
- **Drift Analysis** - การวิเคราะห์การเอียง

### 🔧 **Library Features**
- **Standalone Library** - ใช้งานแยกต่างหากได้
- **Reusable Across Projects** - นำไปใช้โปรเจคอื่นได้
- **Thai Province Support** - รองรับจังหวัดไทยครบถ้วน
- **Multiple Structural Systems** - รองรับระบบโครงสร้างหลากหลาย
- **Comprehensive Reports** - สร้างรายงานครบถ้วน
- **Bilingual Interface** - อินเตอร์เฟซภาษาไทย-อังกฤษ

## 📚 **Usage Examples / ตัวอย่างการใช้งาน**

### Basic Usage:

```python
from thaiEarthquakeLoad import ThaiEarthquakeLoad, SoilType

# Initialize earthquake calculator
earthquake_calc = ThaiEarthquakeLoad()

# Quick seismic load summary
summary = earthquake_calc.get_seismic_load_summary('เชียงใหม่', 25.0, SoilType.TYPE_C)
print(f"Base shear coefficient: {summary['seismic_coefficient']:.4f}")
print(f"Estimated base shear: {summary['estimated_base_shear_kn']:.1f} kN")
```

### Complete Analysis:

```python
from thaiEarthquakeLoad import (
    ThaiEarthquakeLoad, BuildingGeometrySeismic, SoilType, 
    BuildingImportance, StructuralSystem
)

# Define building geometry
building = BuildingGeometrySeismic(
    total_height=28.0,          # 28m height
    story_heights=[4.0] + [3.5] * 7,  # Ground + 7 floors
    story_weights=[1000.0] + [800.0] * 7,  # kN per floor
    plan_dimensions=(30.0, 25.0),  # 30m x 25m
    structural_system=StructuralSystem.MOMENT_FRAME,
    building_type="office",
    irregularity_factors={}
)

# Perform complete seismic analysis
result = earthquake_calc.calculate_complete_seismic_analysis(
    location='เชียงใหม่',
    building_geometry=building,
    soil_type=SoilType.TYPE_C,
    building_importance=BuildingImportance.STANDARD
)

print(f"Design Base Shear: {result.design_base_shear:.1f} kN")
print(f"Fundamental Period: {result.fundamental_period:.3f} seconds")
```

### Generate Report:

```python
# Building information
building_info = {
    'project_name': 'อาคารสำนักงาน 8 ชั้น เชียงใหม่',
    'location': 'เชียงใหม่',
    'date': '2024-01-15',
    'engineer': 'วิศวกรตัวอย่าง'
}

# Generate detailed report
report = earthquake_calc.generate_seismic_load_report(result, building_info)
print(report)

# Save to file
with open('earthquake_load_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
```

## 🏛️ **Building Importance Levels / ระดับความสำคัญอาคาร**

| Level | Factor | Description | Examples |
|-------|--------|-------------|----------|
| **Standard** | 1.00 | อาคารทั่วไป | Residential, office buildings, factories |
| **Important** | 1.25 | อาคารสำคัญ | Schools, hospitals, assembly buildings |
| **Essential** | 1.50 | อาคารจำเป็น | Police stations, fire stations, emergency hospitals |

## 🏗️ **Structural Systems / ระบบโครงสร้าง**

| System | R Factor | Cd Factor | Description | Material Support |
|--------|----------|-----------|-------------|-----------------|
| **Moment Frame** | 8 | 5.5 | โครงข้อแข็ง | Steel, Concrete |
| **Shear Wall** | 2-5 | 2.5-5.0 | กำแพงรับแรงเฉือน | Concrete, Masonry |
| **Dual System** | 7-8 | 5.5-6.5 | ระบบผสม | Steel, Concrete |
| **Braced Frame** | 6 | 5.0 | โครงค้ำยัน | Steel, Concrete |

## 🌄 **Soil Types / ประเภทชั้นดิน**

| Type | Description | Fa Range | Fv Range | Examples |
|------|-------------|----------|----------|----------|
| **A** | หินแข็ง / Hard Rock | 0.8 | 0.8 | Hard rock, granite |
| **B** | หินอ่อน / Rock | 1.0 | 1.0 | Rock, soft rock |
| **C** | ดินแน่นมาก / Very Dense Soil | 1.1-1.2 | 1.5-1.8 | Very dense sand, gravel |
| **D** | ดินแน่นปานกลาง / Stiff Soil | 1.2-1.6 | 1.8-2.4 | Stiff clay, dense sand |
| **E** | ดินอ่อน / Soft Soil | 1.2-2.5 | 3.0-3.5 | Soft clay, loose sand |
| **F** | ดินพิเศษ / Special Soil | - | - | Site-specific analysis required |

## 📊 **Practical Examples / ตัวอย่างเชิงปฏิบัติ**

### Example Results from Test:

| Building Type | Location | Zone | PGA | Base Shear/Height |
|---------------|----------|------|-----|-------------------|
| **Bangkok Office** | กรุงเทพมหานคร | A | 0.15g | 12.5 kN/m |
| **Chiang Mai Hospital** | เชียงใหม่ | C | 0.40g | 45.2 kN/m |
| **Chiang Rai School** | เชียงราย | C | 0.40g | 56.5 kN/m (Important) |

### Seismic Load by Province:

| Province | Zone | PGA | Seismic Coefficient* | Base Shear/Height* |
|----------|------|-----|---------------------|-------------------|
| กรุงเทพมหานคร | A | 0.15g | 0.0125 | 12.5 kN/m |
| ขอนแก่น | A | 0.15g | 0.0125 | 12.5 kN/m |
| ลำปาง | B | 0.25g | 0.0208 | 20.8 kN/m |
| เชียงใหม่ | C | 0.40g | 0.0333 | 33.3 kN/m |
| เชียงราย | C | 0.40g | 0.0333 | 33.3 kN/m |

*For standard building, moment frame, soil type C

## 🔄 **Integration with Other Systems**

### Integration with Ministry Regulation B.E. 2566:

```python
from thaiMinistryReg import ThaiMinistryRegulation2566

# Load combinations with earthquake load
ministry_reg = ThaiMinistryRegulation2566()

loads = {
    'D': 8.0,   # Dead load (kN/m²)
    'L': 4.0,   # Live load (kN/m²)
    'W': 2.0,   # Wind load (kN/m²)
    'E': result.design_base_shear / total_area  # Earthquake load (kN/m²)
}

# Ultimate limit state combinations
combinations = ministry_reg.check_load_combination(loads, 'ultimate')
for combo in combinations:
    if 'E' in combo['formula']:
        print(f"{combo['name']}: {combo['result']:.2f} kN/m²")
```

### Integration with Structural Analysis:

```python
# Export earthquake loads for structural analysis software
def export_earthquake_loads_to_etabs(result, building_geometry):
    """Export earthquake loads in ETABS format"""
    earthquake_loads = {
        'load_case': 'EARTHQUAKE_X',
        'base_shear': result.design_base_shear,
        'period': result.fundamental_period,
        'building_height': building_geometry.total_height,
        'story_forces': result.story_forces
    }
    return earthquake_loads

# Export to SAP2000/ETABS
etabs_loads = export_earthquake_loads_to_etabs(result, building)
```

## ⚙️ **API Reference / คู่มือ API**

### Core Classes:

#### `ThaiEarthquakeLoad`
Main calculation class for earthquake load analysis.

**Key Methods:**
- `get_seismic_zone_info(location)` - Get seismic zone information
- `get_site_coefficients(pga, soil_type)` - Calculate site coefficients
- `calculate_fundamental_period(building_geometry, material)` - Calculate fundamental period
- `calculate_complete_seismic_analysis(...)` - Complete analysis
- `generate_seismic_load_report(...)` - Generate report

#### `BuildingGeometrySeismic`
```python
@dataclass
class BuildingGeometrySeismic:
    total_height: float              # Total height (m)
    story_heights: List[float]       # Story heights (m)
    story_weights: List[float]       # Story weights (kN)
    plan_dimensions: Tuple[float, float]  # Plan dimensions (m)
    structural_system: StructuralSystem   # Structural system
    building_type: str               # Building type description
    irregularity_factors: Dict[str, float]  # Irregularity factors
```

#### `SeismicLoadResult`
```python
@dataclass
class SeismicLoadResult:
    design_base_shear: float         # Design base shear (kN)
    seismic_coefficient: float       # Seismic coefficient
    peak_ground_acceleration: float  # Peak ground acceleration (g)
    site_coefficient_fa: float       # Site coefficient Fa
    site_coefficient_fv: float       # Site coefficient Fv
    importance_factor: float         # Importance factor
    response_modification: float     # Response modification factor
    fundamental_period: float        # Fundamental period (sec)
    story_forces: Dict[int, float]   # Story forces by floor (kN)
    lateral_displacement: Dict[int, float]  # Lateral displacement (mm)
    drift_ratio: Dict[int, float]    # Drift ratio by floor
    description: str                 # Analysis description
    calculation_method: str          # Method used
```

### Enums:

- **`SeismicZone`**: ZONE_A, ZONE_B, ZONE_C
- **`SoilType`**: TYPE_A, TYPE_B, TYPE_C, TYPE_D, TYPE_E, TYPE_F
- **`BuildingImportance`**: STANDARD, IMPORTANT, ESSENTIAL
- **`StructuralSystem`**: MOMENT_FRAME, SHEAR_WALL, DUAL_SYSTEM, BRACED_FRAME

## 🧪 **Testing / การทดสอบ**

### Run Tests:

```bash
# Run comprehensive tests
python test_thai_earthquake_load.py
```

**Test Coverage:**
- ✅ Seismic zone and PGA lookup
- ✅ Site coefficient calculations
- ✅ Building importance factors
- ✅ Structural system factors
- ✅ Complete earthquake analysis
- ✅ Report generation
- ✅ Integration with Ministry Regulation
- ✅ Practical examples

### Expected Output:
```
🎉 ALL TESTS PASSED! Thai Earthquake Load Library is ready to use.
📚 The library can now be used in other projects.
```

## 📦 **Installation & Setup**

### Requirements:
```python
# Required packages
python>=3.7
typing  # For type hints
dataclasses  # For data structures
enum  # For enumerations
math  # For calculations
```

### Installation:
1. Copy `thaiEarthquakeLoad.py` to your project
2. Import and use:

```python
from thaiEarthquakeLoad import ThaiEarthquakeLoad
earthquake_calc = ThaiEarthquakeLoad()
```

## 🌟 **Use Cases / กรณีการใช้งาน**

### 1. **Structural Design Software Integration**
- Import earthquake loads into ETABS, SAP2000, STAAD
- Automated seismic load generation
- Code compliance checking

### 2. **Building Design Automation**
- Parametric building design
- Preliminary design tools
- Code compliance verification

### 3. **Educational Tools**
- Teaching earthquake engineering concepts
- Demonstrating Thai standards
- Student calculation tools

### 4. **Consulting Engineering**
- Quick seismic load estimates
- Client presentations
- Detailed analysis reports

## 🔗 **Project Integration Examples**

### Example 1: Integration with Existing twoWaySlab:

```python
# In your main structural analysis
from thaiEarthquakeLoad import ThaiEarthquakeLoad
from thiRc import ThaiRc_set

# Initialize systems
earthquake_calc = ThaiEarthquakeLoad()
thai_rc = ThaiRc_set()

# Calculate earthquake loads
earthquake_result = earthquake_calc.calculate_complete_seismic_analysis(...)

# Convert to load for slab analysis
earthquake_load_kn_m2 = earthquake_result.design_base_shear / total_area

# Use in load combinations
total_load = dead_load + live_load + earthquake_load_kn_m2
```

### Example 2: Custom Project Integration:

```python
# Create custom wrapper for your project
class ProjectSeismicAnalysis:
    def __init__(self):
        self.earthquake_calc = ThaiEarthquakeLoad()
    
    def analyze_building(self, project_data):
        """Custom analysis for your project needs"""
        result = self.earthquake_calc.calculate_complete_seismic_analysis(
            location=project_data['location'],
            building_geometry=project_data['geometry'],
            soil_type=project_data['soil_type'],
            building_importance=project_data['importance']
        )
        
        # Custom post-processing for your project
        return self.process_results(result)
```

## 📈 **Comparison with International Standards**

| Parameter | TIS 1301/1302-61 | ASCE 7 | Eurocode 8 |
|-----------|------------------|---------|------------|
| **Seismic Zones** | 3 zones (A, B, C) | Ss, S1 maps | ag maps |
| **Max PGA** | 0.40g | Varies | Varies |
| **Site Classes** | 6 types (A-F) | 6 types (A-F) | 5 types (A-E) |
| **R Factors** | 2-8 | 1.5-8 | 1.5-6.5 |
| **Drift Limits** | 2.0-2.5% | 2.0-2.5% | 1.0-2.5% |

## 📄 **License / ใบอนุญาต**

This library follows the same license terms as the original twoWaySlab project while providing standalone functionality for earthquake load calculations according to Thai standards.

---

**Thai Earthquake Load Library v1.0** - Standalone library for Thai earthquake load calculations supporting TIS 1301/1302-61 (Revised Edition 1) standards.

**ไลบรารีการคำนวณแรงแผ่นดินไหวประเทศไทย v1.0** - ไลบรารีแยกต่างหากสำหรับการคำนวณแรงแผ่นดินไหวตามมาตรฐานไทย รองรับ มยผ. 1301/1302-61 (ฉบับปรับปรุงครั้งที่ 1)