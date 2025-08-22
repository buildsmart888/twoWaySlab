# Thai Wind Load Library
# ไลบรารีการคำนวณแรงลมประเทศไทย

## 📋 Overview / ภาพรวม

The **Thai Wind Load Library** is a standalone, reusable library for calculating wind loads on buildings according to Thai standards. It can be used across multiple projects and integrates seamlessly with existing structural engineering software.

**ไลบรารีการคำนวณแรงลมประเทศไทย** เป็นไลบรารีแยกต่างหาก สามารถนำไปใช้ซ้ำได้ สำหรับการคำนวณแรงลมที่กระทำต่ออาคารตามมาตรฐานไทย สามารถนำไปใช้งานโปรเจคต่างๆ และบูรณาการเข้ากับซอฟต์แวร์วิศวกรรมโครงสร้างที่มีอยู่

## 🎯 Key Standards / มาตรฐานหลัก

### ✨ **Based on Thai Standards**
- **กฎกระทรวง พ.ศ. 2566 หมวด 4** - Ministry Regulation B.E. 2566 Chapter 4
- **มยผ. 1311-50** - Thai Industrial Standard for Wind Load Calculation and Building Response

## 🌬️ **Wind Zones in Thailand / โซนลมในประเทศไทย**

| Zone | Region | Basic Wind Speed | Example Provinces |
|------|--------|------------------|-------------------|
| **Zone 1** | ภาคเหนือ (Northern) | 30 m/s (108 km/h) | เชียงใหม่, เชียงราย, ลำปาง |
| **Zone 2** | ภาคกลาง/อีสาน (Central/Northeast) | 25 m/s (90 km/h) | กรุงเทพฯ, นครราชสีมา, ขอนแก่น |
| **Zone 3** | ภาคใต้ (Southern Inland) | 35 m/s (126 km/h) | สุราษฎร์ธานี, นครศรีธรรมราช |
| **Zone 4** | ชายฝั่ง (Coastal Areas) | 40 m/s (144 km/h) | ภูเก็ต, สงขลา, ระยอง, ชลบุรี |

## 🏗️ **Core Features / คุณสมบัติหลัก**

### ✨ **Wind Load Calculations**
- **Basic Wind Speed** - ความเร็วลมพื้นฐานตามโซน
- **Terrain Factors** - ค่าประกอบภูมิประเทศ (4 categories)
- **Building Importance** - ค่าประกอบความสำคัญอาคาร (4 types)
- **Topographic Effects** - ผลกระทบจากภูมิทัศน์
- **Pressure Coefficients** - ค่าสัมประสิทธิ์แรงดัน
- **Complete Force Calculation** - การคำนวณแรงลมครบถ้วน

### 🔧 **Library Features**
- **Standalone Library** - ใช้งานแยกต่างหากได้
- **Reusable Across Projects** - นำไปใช้โปรเจคอื่นได้
- **Thai Province Support** - รองรับจังหวัดไทยครบถ้วน
- **Multiple Building Types** - รองรับประเภทอาคารหลากหลาย
- **Comprehensive Reports** - สร้างรายงานครบถ้วน
- **Unit Conversions** - แปลงหน่วยต่างๆ

## 📚 **Usage Examples / ตัวอย่างการใช้งาน**

### Basic Usage:

```python
from thaiWindLoad import ThaiWindLoad, BuildingType, TerrainCategory

# Initialize wind calculator
wind_calc = ThaiWindLoad()

# Quick wind load summary
summary = wind_calc.get_wind_load_summary('กรุงเทพมหานคร', 30.0)
print(f"Design pressure: {summary['design_pressure_kpa']:.2f} kPa")
print(f"Force per m²: {summary['force_per_sqm_kgf']:.1f} kgf/m²")
```

### Complete Analysis:

```python
from thaiWindLoad import (
    ThaiWindLoad, BuildingGeometry, TerrainCategory, BuildingType
)

# Define building geometry
building = BuildingGeometry(
    height=30.0,          # 30m height
    width=25.0,           # 25m width  
    depth=20.0,           # 20m depth
    roof_angle=0,         # Flat roof
    building_type="office",
    exposure_category=TerrainCategory.CATEGORY_III  # Urban terrain
)

# Perform complete wind analysis
result = wind_calc.calculate_complete_wind_analysis(
    location='กรุงเทพมหานคร',
    building_geometry=building,
    building_type=BuildingType.STANDARD
)

print(f"Design Wind Pressure: {result.design_wind_pressure:.1f} Pa")
print(f"Total Wind Force: {result.total_wind_force/1000:.1f} kN")
```

### Generate Report:

```python
# Building information
building_info = {
    'project_name': 'อาคารสำนักงาน 8 ชั้น',
    'location': 'กรุงเทพมหานคร',
    'date': '2024-01-15'
}

# Generate detailed report
report = wind_calc.generate_wind_load_report(result, building_info)
print(report)

# Save to file
with open('wind_load_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
```

## 🏛️ **Building Types / ประเภทอาคาร**

| Type | Factor | Description | Examples |
|------|--------|-------------|----------|
| **Standard** | 1.00 | อาคารทั่วไป | Residential, office buildings |
| **Important** | 1.15 | อาคารสำคัญ | Schools, hospitals, assembly |
| **Essential** | 1.25 | อาคารจำเป็น | Emergency facilities, power plants |
| **Hazardous** | 1.25 | อาคารอันตราย | Chemical plants, toxic storage |

## 🌄 **Terrain Categories / ประเภทภูมิประเทศ**

| Category | Description | Examples | Roughness |
|----------|-------------|----------|-----------|
| **I** | ภูมิประเทศเปิด | Large water bodies, flat open country | z₀ = 0.03m |
| **II** | ภูมิประเทศขรุขระ | Open terrain with scattered obstacles | z₀ = 0.3m |
| **III** | ภูมิประเทศเมือง | Suburban areas, towns | z₀ = 1.0m |
| **IV** | ภูมิประเทศเมืองหนาแน่น | Dense urban areas, city centers | z₀ = 2.5m |

## 📊 **Practical Examples / ตัวอย่างเชิงปฏิบัติ**

### Example Results from Test:

| Building Type | Location | Wind Speed | Pressure | Force |
|---------------|----------|------------|----------|-------|
| **Bangkok Office** | กรุงเทพมหานคร | 27.1 m/s | 0.45 kPa | 269 kN |
| **Chiang Mai Hospital** | เชียงใหม่ | 33.2 m/s | 0.68 kPa | 676 kN |
| **Phuket Hotel** | ภูเก็ต | 47.9 m/s | 1.41 kPa | 4049 kN |

### Wind Load by Province:

| Province | Zone | Basic Speed | Design Pressure* | Force per m²* |
|----------|------|-------------|------------------|---------------|
| กรุงเทพมหานคร | 2 | 25.0 m/s | 0.41 kPa | 33.8 kgf/m² |
| เชียงใหม่ | 1 | 30.0 m/s | 0.60 kPa | 48.6 kgf/m² |
| ภูเก็ต | 4 | 40.0 m/s | 1.06 kPa | 86.4 kgf/m² |
| สงขลา | 4 | 40.0 m/s | 1.06 kPa | 86.4 kgf/m² |

*For 25m building in urban terrain

## 🔄 **Integration with Other Systems**

### Integration with Ministry Regulation B.E. 2566:

```python
from thaiMinistryReg import ThaiMinistryRegulation2566

# Load combinations with wind load
ministry_reg = ThaiMinistryRegulation2566()

loads = {
    'D': 5.0,   # Dead load (kN/m²)
    'L': 3.0,   # Live load (kN/m²)
    'W': result.design_wind_pressure / 1000,  # Wind load (kN/m²)
    'E': 0.0    # Earthquake load (kN/m²)
}

# Ultimate limit state combinations
combinations = ministry_reg.check_load_combination(loads, 'ultimate')
for combo in combinations:
    if 'W' in combo['formula']:
        print(f"{combo['name']}: {combo['result']:.2f} kN/m²")
```

### Integration with Structural Analysis:

```python
# Export wind loads for structural analysis software
def export_wind_loads_to_etabs(result, building_geometry):
    """Export wind loads in ETABS format"""
    wind_loads = {
        'load_case': 'WIND_X',
        'pressure': result.design_wind_pressure,
        'direction': 'X',
        'building_height': building_geometry.height,
        'pressure_coefficients': result.pressure_coefficients
    }
    return wind_loads

# Export to SAP2000/ETABS
etabs_loads = export_wind_loads_to_etabs(result, building)
```

## ⚙️ **API Reference / คู่มือ API**

### Core Classes:

#### `ThaiWindLoad`
Main calculation class for wind load analysis.

**Key Methods:**
- `get_basic_wind_speed(location)` - Get basic wind speed
- `calculate_terrain_factor(height, terrain)` - Calculate terrain factor
- `calculate_design_wind_pressure(...)` - Calculate design pressure
- `calculate_complete_wind_analysis(...)` - Complete analysis
- `generate_wind_load_report(...)` - Generate report

#### `BuildingGeometry`
```python
@dataclass
class BuildingGeometry:
    height: float           # Building height (m)
    width: float           # Building width (m)
    depth: float           # Building depth (m)
    roof_angle: float      # Roof angle (degrees)
    building_type: str     # Building type description
    exposure_category: TerrainCategory  # Terrain exposure
```

#### `WindLoadResult`
```python
@dataclass
class WindLoadResult:
    design_wind_pressure: float    # Design pressure (Pa)
    design_wind_speed: float       # Design speed (m/s)
    basic_wind_speed: float        # Basic speed (m/s)
    terrain_factor: float          # Terrain factor
    topographic_factor: float      # Topographic factor
    importance_factor: float       # Importance factor
    pressure_coefficients: Dict    # Pressure coefficients
    total_wind_force: float        # Total force (N)
    description: str               # Analysis description
    calculation_method: str        # Method used
```

### Enums:

- **`WindZone`**: ZONE_1, ZONE_2, ZONE_3, ZONE_4
- **`TerrainCategory`**: CATEGORY_I, CATEGORY_II, CATEGORY_III, CATEGORY_IV  
- **`BuildingType`**: STANDARD, IMPORTANT, ESSENTIAL, HAZARDOUS

## 🧪 **Testing / การทดสอบ**

### Run Tests:

```bash
# Run comprehensive tests
python test_thai_wind_load.py
```

**Test Coverage:**
- ✅ Wind zone and basic speed lookup
- ✅ Terrain factor calculations  
- ✅ Building importance factors
- ✅ Complete wind analysis
- ✅ Report generation
- ✅ Integration with Ministry Regulation
- ✅ Practical examples

### Expected Output:
```
🎉 ALL TESTS PASSED! Thai Wind Load Library is ready to use.
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
1. Copy `thaiWindLoad.py` to your project
2. Import and use:

```python
from thaiWindLoad import ThaiWindLoad
wind_calc = ThaiWindLoad()
```

## 🌟 **Use Cases / กรณีการใช้งาน**

### 1. **Structural Design Software Integration**
- Import wind loads into ETABS, SAP2000, STAAD
- Automated wind load generation
- Code compliance checking

### 2. **Building Design Automation**
- Parametric building design
- Preliminary design tools
- Code compliance verification

### 3. **Educational Tools**
- Teaching wind load concepts
- Demonstrating Thai standards
- Student calculation tools

### 4. **Consulting Engineering**
- Quick wind load estimates
- Client presentations
- Detailed analysis reports

## 🔗 **Project Integration Examples**

### Example 1: Integration with Existing twoWaySlab:

```python
# In your main structural analysis
from thaiWindLoad import ThaiWindLoad
from thiRc import ThaiRc_set

# Initialize systems
wind_calc = ThaiWindLoad()
thai_rc = ThaiRc_set()

# Calculate wind loads
wind_result = wind_calc.calculate_complete_wind_analysis(...)

# Convert to load for slab analysis
wind_load_kn_m2 = wind_result.design_wind_pressure / 1000

# Use in load combinations
total_load = dead_load + live_load + wind_load_kn_m2
```

### Example 2: Custom Project Integration:

```python
# Create custom wrapper for your project
class ProjectWindAnalysis:
    def __init__(self):
        self.wind_calc = ThaiWindLoad()
    
    def analyze_building(self, project_data):
        """Custom analysis for your project needs"""
        result = self.wind_calc.calculate_complete_wind_analysis(
            location=project_data['location'],
            building_geometry=project_data['geometry'],
            building_type=project_data['building_type']
        )
        
        # Custom post-processing for your project
        return self.process_results(result)
```

## 📄 **License / ใบอนุญาต**

This library follows the same license terms as the original twoWaySlab project while providing standalone functionality for wind load calculations according to Thai standards.

---

**Thai Wind Load Library v1.0** - Standalone library for Thai wind load calculations supporting Ministry Regulation B.E. 2566 and TIS 1311-50 standards.

**ไลบรารีการคำนวณแรงลมประเทศไทย v1.0** - ไลบรารีแยกต่างหากสำหรับการคำนวณแรงลมตามมาตรฐานไทย รองรับกฎกระทรวง พ.ศ. 2566 และ มยผ. 1311-50