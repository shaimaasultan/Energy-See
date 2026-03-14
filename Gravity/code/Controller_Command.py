import time
from core_logic import PlenumEngine

def execute_sultanian_sweep1():
    """
    Main execution loop for the 5.2 THz Controller.
    Dynamically modulates Impulse Sharpness (sigma) to trigger the Snap.
    """
    # Initialize for Graphene-hBN Shroud
    k_factor = 5.2
    target_resonance = 5.2e12
    b_field = 0.8
    engine = PlenumEngine(material_k=k_factor)
    
    # Sweep Configuration
    start_freq = 1.0e12
    step = 0.2e12
    current_freq = start_freq
    
    print("--- 5.2 THz Controller: INITIALIZING SWEEP ---")
    print(f"Target Material: Graphene-hBN (k={k_factor})")
    print(f"Magnetic Bias: {b_field}T | Safety Valve: ACTIVE\n")

    while current_freq <= 6.0e12:
        # Calculate Thresholds
        st_limit = engine.get_stability_threshold(b_field, current_freq)
        current_torque = current_freq * b_field
        
        # DYNAMIC SIGMA LOGIC:
        # As we approach 5.2 THz, we ramp the Impulse Sharpness
        proximity = current_freq / target_resonance
        if proximity > 0.95:
            sigma = 27.5  # Critical Impulse Trigger
        elif proximity > 0.80:
            sigma = 10.0  # Pre-resonance agitation
        else:
            sigma = 1.0   # Static/Idle mode

        # Check for Snap
        r_order, snapped = engine.monitor_impulse_snap(
            current_torque, 
            st_limit, 
            pulse_sharpness=sigma
        )

        status = "SNAP ACTIVE" if snapped else "LOCKED"
        print(f"Freq: {current_freq/1e12:.2f} THz | Sigma: {sigma:>4} | R-Order: {r_order:.4f} | Status: {status}")

        if snapped:
            yield_energy = engine.execute_kinetic_release(mass=1.0, r_delta=5.0)
            print(f"\n[!!!] KINETIC INVERSION DETECTED")
            print(f"Yield: {yield_energy:.2e} J | Mode: POST-SNAP GLIDE")
            break

        current_freq += step
        time.sleep(0.05) # Simulate hardware clock cycle

import time
from core_logic import PlenumEngine
"""
🛠️ The "Sultanian Meltdown" Safety Logic
To protect the integrity of the Graphene shroud, we must implement a Safety Shutdown. 
If the phase-order $R$ exceeds the critical threshold ($R > 1.2$), the system enters a "Thermal Runaway" or "Lattice Fracture" state.
"""
def execute_sultanian_sweep():
    # Hardware Initialization
    k_factor = 5.2
    target_resonance = 5.2e12
    b_field = 0.8
    engine = PlenumEngine(material_k=k_factor)
    
    # Sweep Configuration
    current_freq = 1.0e12
    step = 0.2e12
    SULTANIAN_MELTDOWN_LIMIT = 1.2 # Safety threshold for R-Order

    print("--- 5.2 THz Controller: EXECUTING IMPULSE MODULATION ---")

    while current_freq <= 10.0e12:
        st_limit = engine.get_stability_threshold(b_field, current_freq)
        current_torque = current_freq * b_field
        
        # Determine Impulse Sharpness based on Proximity
        proximity = current_freq / target_resonance
        sigma = 27.5 if proximity >= 0.98 else (10.0 if proximity >= 0.85 else 1.0)

        # Monitor Snap & Phase-Order
        r_order, snapped = engine.monitor_impulse_snap(current_torque, st_limit, sigma)

        # --- SAFETY VALVE CHECK ---
        if r_order > SULTANIAN_MELTDOWN_LIMIT:
            print(f"\n[!!!] EMERGENCY SHUTDOWN: R-ORDER EXCEEDED ({r_order:.2f})")
            print("Lattice Fracture Imminent. Cutting Power to 5.2 THz Oscillator.")
            break

        status = "SNAP ACTIVE" if snapped else "LOCKED"
        print(f"Freq: {current_freq/1e12:.2f} THz | R: {r_order:.4f} | Status: {status}")

        if snapped:
            yield_energy = engine.execute_kinetic_release(mass=1.0, r_delta=5.0)
            print(f"\n[SUCCESS] CRITICAL YIELD: {yield_energy:.2e} J")
            print("Entering Post-Snap Glide Mode...")
            # In Glide mode, we maintain resonance but drop sigma to 1.0
            break

        current_freq += step
        time.sleep(0.05)


if __name__ == "__main__":
    execute_sultanian_sweep()