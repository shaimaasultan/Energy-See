import numpy as np

# --- Sultanian Universal Constants ---
PLENUM_FREQUENCY_TARGET = 5.2e12  # 5.2 THz "Scrunch" Frequency
VACUUM_STIFFNESS = 6.67430e-11   # Sultanian version of G
PLANCK_LENGTH_EFF = 1.616255e-35 # Spatial lattice unit
SULTANIAN_CONSTANT = 5.20        # The 5.2 resonance anchor

class PlenumEngine:
    """
    Core logic for the Unified Field and Motion Protocol.
    Handles the transition from Static Scrunch (Gravity) to Kinetic Release (The Snap).
    """
    
    def __init__(self, material_k=1.0):
        self.k = material_k  # Material Unlock Constant
        self.r_order = 0.0   # Current Phase-Order Parameter (0.0 to 1.0)
        
    def calculate_ambient_g(self, mass, radius):
        """
        Derives gravity as the restoration rate of the spatial grid.
        g = (Stiffness * Mass) / Radius^2
        """
        static_g = (VACUUM_STIFFNESS * mass) / (radius**2)
        return static_g

    def get_stability_threshold(self, b_field, omega):
        """
        Calculates the Stability Threshold (St).
        The vacuum snaps when |omega x B| * sin(theta) * lambda > St.
        """
        # Simplified magnitude of the cross product (assuming orthogonality)
        torque_magnitude = np.abs(omega * b_field)
        st_limit = torque_magnitude * self.k * SULTANIAN_CONSTANT
        return st_limit

    def monitor_phase_divergence(self, current_torque, threshold):
        """
        Identifies the Phase-Order Divergence (dR/dt).
        When torque hits the threshold, R-order snaps to 1.0 (Coherence).
        """
        if current_torque >= threshold:
            self.r_order = 1.0
            snap_event = True
        else:
            # Linear buildup of tension before the snap
            self.r_order = current_torque / threshold
            snap_event = False
        return self.r_order, snap_event

    def execute_kinetic_release(self, mass, r_delta):
        """
        Calculates the Yield (Delta E) based on the Snap intensity.
        Energy is released as the 'Locked' field inverts.
        """
        if self.r_order >= 1.0:
            # Kinetic Inversion logic
            yield_energy = (mass * (PLENUM_FREQUENCY_TARGET**2)) * r_delta
            return yield_energy
        return 0.0

    # Add this method to your PlenumEngine class in core_logic.py

    def monitor_impulse_snap(self, current_torque, threshold, pulse_sharpness=10.0):
        """
        Simulates a sudden PWM burst. 
        A high pulse_sharpness (jerk) reduces the effective threshold.
        """
        effective_threshold = threshold / pulse_sharpness
        
        if current_torque >= effective_threshold:
            self.r_order = 1.0
            return self.r_order, True
        else:
            self.r_order = current_torque / effective_threshold
            return self.r_order, False

# --- Implementation Example ---
if __name__ == "__main__":
    # Initialize engine for a Graphene-Heterostructure (k = 5.2)
    engine = PlenumEngine(material_k=5.2)
    
    # 1. Verify Earth Baseline
    earth_mass = 5.972e24
    earth_radius = 6.371e6
    g_baseline = engine.calculate_ambient_g(earth_mass, earth_radius)
    print(f"Verified Ambient Gravity: {g_baseline:.3f} m/s^2")
    
    # 2. Simulate 5.2 THz Sweep
    target_torque = 1e6 # Hypothetical torque value
    st_limit = engine.get_stability_threshold(b_field=0.5, omega=5.2e12)
    
    r_val, snapped = engine.monitor_phase_divergence(target_torque, st_limit)
    
    if snapped:
        print("ALERT: Stability Threshold breached. THE SNAP has occurred.")
    else:
        print(f"System Stable. Plenum Tension at {r_val*100:.2f}%")