#!/usr/bin/env python3
"""
ACI 318M-25 Beam Design Example
==============================

This example demonstrates how to design a simply supported reinforced concrete beam
according to ACI 318M-25 Building Code Requirements for Structural Concrete.

Example Problem:
Design a simply supported beam for a residential building with the following requirements:
- Span length: 6.0 m
- Dead load: 5.0 kN/m (including self-weight)
- Live load: 8.0 kN/m
- Concrete: f'c = 28 MPa
- Steel: Grade 420 (fy = 420 MPa)
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from structural_standards.aci.aci318m25.materials.concrete import ACI318M25Concrete
from structural_standards.aci.aci318m25.materials.steel import ACI318M25ReinforcementSteel
from structural_standards.aci.aci318m25.members.beam_design import (
    ACI318M25BeamDesign, BeamGeometry, BeamLoads, BeamType
)
from structural_standards.base.design_base import DesignStatus


def main():
    """
    Main function demonstrating ACI 318M-25 beam design
    """
    print("=" * 60)
    print("ACI 318M-25 Beam Design Example")
    print("=" * 60)
    
    # Step 1: Define Materials
    print("\n1. Material Properties:")
    print("-" * 30)
    
    # Create concrete material (f'c = 28 MPa)
    concrete = ACI318M25Concrete(fc_prime=28.0)
    print(f"Concrete: f'c = {concrete.fc_prime} MPa")
    print(f"Elastic modulus: Ec = {concrete.elastic_modulus():.0f} MPa")
    print(f"Modulus of rupture: fr = {concrete.modulus_of_rupture():.2f} MPa")
    
    # Create steel material (Grade 420)
    steel = ACI318M25ReinforcementSteel(bar_designation='20M', grade='GRADE420')
    print(f"Steel: {steel.grade} (fy = {steel.fy} MPa)")
    print(f"Elastic modulus: Es = {steel.elastic_modulus():.0f} MPa")
    
    # Step 2: Define Geometry
    print("\n2. Beam Geometry:")
    print("-" * 30)
    
    geometry = BeamGeometry(
        width=300,           # mm
        height=600,          # mm
        effective_depth=550, # mm (assuming 40mm cover + 10mm stirrup + 10mm bar radius)
        span_length=6000     # mm
    )
    
    print(f"Width (b): {geometry.width} mm")
    print(f"Height (h): {geometry.height} mm")
    print(f"Effective depth (d): {geometry.effective_depth} mm")
    print(f"Span length (L): {geometry.span_length/1000:.1f} m")
    
    # Step 3: Define Loads
    print("\n3. Applied Loads:")
    print("-" * 30)
    
    loads = BeamLoads(
        dead_load=5.0,       # kN/m
        live_load=8.0        # kN/m
    )
    
    print(f"Dead load: {loads.dead_load} kN/m")
    print(f"Live load: {loads.live_load} kN/m")
    print(f"Total service load: {loads.dead_load + loads.live_load} kN/m")
    
    # Calculate factored loads (ACI 318M-25)
    wu = 1.4 * loads.dead_load + 1.7 * loads.live_load
    print(f"Factored load: wu = 1.4×{loads.dead_load} + 1.7×{loads.live_load} = {wu} kN/m")
    
    # Calculate maximum moment
    Mu = wu * (geometry.span_length/1000)**2 / 8  # kN⋅m
    print(f"Factored moment: Mu = {Mu:.1f} kN⋅m")
    
    # Step 4: Perform Design
    print("\n4. Design Calculation:")
    print("-" * 30)
    
    # Create beam designer
    beam_designer = ACI318M25BeamDesign(concrete, steel)
    
    print("Performing ACI 318M-25 beam design...")
    
    try:
        # Perform complete beam design
        result = beam_designer.design(geometry, loads, BeamType.SIMPLY_SUPPORTED)
        
        # Step 5: Display Results
        print("\n5. Design Results:")
        print("-" * 30)
        
        print(f"Design Status: {result.overall_status}")
        print(f"Design Method: {result.design_method}")
        print(f"Utilization Ratio: {result.utilization_ratio:.2f}")
        
        if result.overall_status == DesignStatus.PASS:
            print("✅ Design PASSED - Beam is adequate")
        elif result.overall_status == DesignStatus.FAIL:
            print("❌ Design FAILED - Beam needs revision")
        else:
            print("⚠️  Design has WARNINGS - Review required")
        
        # Display reinforcement requirements
        if hasattr(result, 'required_reinforcement'):
            print("\nReinforcement Requirements:")
            
            if 'required_steel_area' in result.required_reinforcement:
                As_req = result.required_reinforcement['required_steel_area']
                print(f"Required steel area: As = {As_req:.0f} mm²")
                
                # Suggest bar arrangement
                bar_area = steel.bar_area()  # Area of one 20M bar
                num_bars = max(2, int(As_req / bar_area) + 1)
                As_provided = num_bars * bar_area
                
                print(f"Suggested: {num_bars}×{steel.bar_designation} bars")
                print(f"Provided steel area: {As_provided:.0f} mm²")
                print(f"Steel ratio: ρ = {As_provided/(geometry.width * geometry.effective_depth):.4f}")
            
            if 'minimum_steel_area' in result.required_reinforcement:
                As_min = result.required_reinforcement['minimum_steel_area']
                print(f"Minimum steel area: As,min = {As_min:.0f} mm²")
        
        # Display design checks
        if hasattr(result, 'strength_checks') and result.strength_checks:
            print("\nStrength Design Checks:")
            for check in result.strength_checks:
                status = "✅ PASS" if check.status == "PASS" else "❌ FAIL"
                print(f"  {check.name}: {status}")
                if hasattr(check, 'utilization_ratio'):
                    print(f"    Utilization: {check.utilization_ratio:.2f}")
        
        if hasattr(result, 'serviceability_checks') and result.serviceability_checks:
            print("\nServiceability Checks:")
            for check in result.serviceability_checks:
                status = "✅ PASS" if check.status == "PASS" else "❌ FAIL"
                print(f"  {check.name}: {status}")
        
        # Step 6: Design Summary
        print("\n6. Design Summary:")
        print("-" * 30)
        print(f"Beam: {geometry.width}×{geometry.height} mm")
        print(f"Span: {geometry.span_length/1000:.1f} m")
        print(f"Concrete: f'c = {concrete.fc_prime} MPa")
        print(f"Steel: {steel.grade}")
        print(f"Final Status: {result.overall_status}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Design Error: {e}")
        print("Please check input parameters and try again.")
        return None


if __name__ == "__main__":
    # Run the example
    result = main()
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    
    if result and result.overall_status == DesignStatus.PASS:
        print("The beam design meets ACI 318M-25 requirements.")
    else:
        print("The beam design needs to be revised.")
    
    print("=" * 60)