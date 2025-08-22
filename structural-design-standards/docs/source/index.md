# Structural Design Standards Library Documentation

**ไลบรารี Python สำหรับมาตรฐานการออกแบบโครงสร้างระดับนานาชาติ**  
*Python Library for International Structural Design Standards*

Welcome to the documentation for the Structural Design Standards Library, a comprehensive Python package implementing international structural design standards including ACI 318M-25 (USA) and Thai Ministry Regulation B.E. 2566.

ยินดีต้อนรับสู่เอกสารของไลบรารีมาตรฐานการออกแบบโครงสร้าง แพ็คเกจ Python ที่ครอบคลุมสำหรับมาตรฐานการออกแบบโครงสร้างระดับนานาชาติ รวมถึง ACI 318M-25 (สหรัฐอเมริกา) และกฎกระทรวง พ.ศ. 2566 (ไทย)

```{toctree}
:maxdepth: 2
:caption: Contents / สารบัญ:

installation
quickstart
examples/index
api/index
theory/index
standards/index
contributing
changelog
```

## 🎯 Key Features / ฟีเจอร์หลัก

### 🇺🇸 ACI 318M-25 (International SI Units)
- Complete concrete and steel material models / โมเดลวัสดุคอนกรีตและเหล็กที่สมบูรณ์
- Comprehensive member design capabilities / ความสามารถการออกแบบสมาชิกที่ครอบคลุม
- Load combinations and strength reduction factors / การรวมน้ำหนักและตัวประกอบลดกำลัง
- Serviceability checks and deflection limits / การตรวจสอบการใช้งานและขีดจำกัดการโก่งตัว

### 🇹🇭 Thai Standards (มาตรฐานไทย)
- Thai concrete grades (Fc180-Fc350) / เกรดคอนกรีตไทย
- Steel grades (SD40, SD50, SR24) / เกรดเหล็ก
- Wind loads per TIS 1311-50 / น้ำหนักลมตาม มอก. 1311-50
- Seismic loads per TIS 1301/1302-61 / น้ำหนักแผ่นดินไหวตาม มอก. 1301/1302-61
- Thai unit conversions / การแปลงหน่วยไทย
- Bilingual documentation / เอกสารสองภาษา

### 🔧 Core Framework / กรอบงานหลัก
- Modular plugin-based architecture / สถาปัตยกรรมแบบโมดูลาร์
- Cross-standard comparisons / การเปรียบเทียบข้ามมาตรฐาน
- Comprehensive validation / การตรวจสอบที่ครอบคลุม
- Professional testing suite / ชุดทดสอบระดับมืออาชีพ

## 🚀 Quick Start / เริ่มต้นใช้งาน

### Installation / การติดตั้ง
```bash
pip install structural-design-standards
```

### Basic Usage / การใช้งานพื้นฐาน

#### ACI 318M-25 Example
```python
from structural_standards.aci.aci318m25 import ACI318M25Concrete, ACI318M25BeamDesign

# Create materials / สร้างวัสดุ
concrete = ACI318M25Concrete(fc_prime=28.0)  # 28 MPa concrete
steel = ACI318M25Steel(grade='GRADE420')     # 420 MPa steel

# Design beam / ออกแบบคาน
beam_designer = ACI318M25BeamDesign(concrete, steel)
result = beam_designer.design_flexural_reinforcement(
    moment_ultimate=150.0,  # kN⋅m
    beam_width=300.0,       # mm
    beam_depth=500.0        # mm
)

print(f"Required reinforcement: {result['As_required_mm2']:.0f} mm²")
```

#### Thai Standards Example / ตัวอย่างมาตรฐานไทย
```python
from structural_standards.thai.ministry_2566 import ThaiConcrete, ThaiWindLoads

# Thai concrete / คอนกรีตไทย
concrete = ThaiConcrete(grade='Fc210')  # 210 ksc ≈ 21 MPa

# Wind load calculation / การคำนวณน้ำหนักลม
wind_calc = ThaiWindLoads()
wind_pressure = wind_calc.calculate_wind_pressure(
    province='กรุงเทพมหานคร',    # Bangkok
    building_height=30.0,        # meters
    terrain_category='urban'     # Urban terrain
)
```

## 📖 Documentation Structure / โครงสร้างเอกสาร

This documentation is organized into several sections:

เอกสารนี้จัดแบ่งเป็นหลายส่วน:

- **Installation Guide** / **คู่มือการติดตั้ง**: How to install and set up the library
- **Quick Start** / **เริ่มต้นใช้งาน**: Basic usage examples and tutorials
- **API Reference** / **เอกสารอ้างอิง API**: Complete API documentation
- **Examples** / **ตัวอย่าง**: Real-world usage examples
- **Theory Manual** / **คู่มือทฤษฎี**: Theoretical background and formulations
- **Standards Guide** / **คู่มือมาตรฐาน**: Detailed standard implementations

## 🌍 Supported Standards / มาตรฐานที่รองรับ

| Standard | Version | Status | Coverage |
|----------|---------|--------|----------|
| ACI 318M | ACI 318M-25 | ✅ Complete | Concrete structures |
| Thai Ministry Reg. | B.E. 2566 (2023) | ✅ Complete | All structural types |
| Thai Wind Loads | TIS 1311-50 | ✅ Complete | Wind analysis |
| Thai Seismic | TIS 1301/1302-61 | ✅ Complete | Earthquake analysis |
| Eurocode 2 | EN 1992 | 🚧 Planned | Concrete structures |
| Japanese AIJ | Latest | 🚧 Planned | All structural types |

## 🤝 Contributing / การมีส่วนร่วม

We welcome contributions from the structural engineering community! Please see our [Contributing Guide](contributing) for details on how to get involved.

เรายินดีรับการมีส่วนร่วมจากชุมชนวิศวกรโครงสร้าง! โปรดดู [คู่มือการมีส่วนร่วม](contributing) สำหรับรายละเอียดการเข้าร่วม

## 📄 License / ใบอนุญาต

This project is licensed under the MIT License. See the [LICENSE](https://github.com/your-org/structural-design-standards/blob/main/LICENSE) file for details.

โปรเจกต์นี้อยู่ภายใต้ใบอนุญาต MIT ดูรายละเอียดในไฟล์ [LICENSE](https://github.com/your-org/structural-design-standards/blob/main/LICENSE)

## 🙏 Acknowledgments / กิตติกรรมประกาศ

- American Concrete Institute (ACI) for ACI 318M-25 standards
- Thai Industrial Standards Institute for TIS standards
- Ministry of Interior, Thailand for Ministry Regulation B.E. 2566
- All contributors and users of this library

---

**Made with ❤️ by Structural Engineers, for Structural Engineers**  
**สร้างด้วย ❤️ โดยวิศวกรโครงสร้าง เพื่อวิศวกรโครงสร้าง**