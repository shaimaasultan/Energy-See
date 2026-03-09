import numpy as np
import matplotlib.pyplot as plt

# 1. Grid Setup
size = 500  # Resolution
x = np.linspace(-10, 10, size)
y = np.linspace(-10, 10, size)
X, Y = np.meshgrid(x, y)

def generate_wave(source_pos, amplitude, wavelength, phase_shift):
    """Calculates the displacement of a circular wave at every point on the grid."""
    # Distance from the source to every point in the grid
    dist = np.sqrt((X - source_pos[0])**2 + (Y - source_pos[1])**2)
    k = 2 * np.pi / wavelength
    return amplitude * np.sin(k * dist + phase_shift)

# 2. Parameters for Phase I
# We place two sources near each other to create interference patterns
WAVELENGTH = 2.0
SOURCE_A_POS = [-5, 0]
SOURCE_B_POS = [2, 0]

# 3. Create the Individual Fields
field_a = generate_wave(SOURCE_A_POS, amplitude=1.0, wavelength=WAVELENGTH, phase_shift=np.pi)

# To see "Cancellation," we set Field B to be out of phase (pi)
field_b = generate_wave(SOURCE_B_POS, amplitude=1.0, wavelength=WAVELENGTH, phase_shift=np.pi)

# 4. The Unified Field (The Superposition)
unified_field = field_a + field_b

# 5. Visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot Field A
im0 = axes[0].imshow(field_a, extent=[-10, 10, -10, 10], cmap='RdBu')
axes[0].set_title("Field A (Source 1)")
fig.colorbar(im0, ax=axes[0])

# Plot Field B
im1 = axes[1].imshow(field_b, extent=[-10, 10, -10, 10], cmap='RdBu')
axes[1].set_title("Field B (Source 2)")
fig.colorbar(im1, ax=axes[1])

# Plot the Unified Field (The Interference Pattern)
im2 = axes[2].imshow(unified_field, extent=[-10, 10, -10, 10], cmap='magma')
axes[2].set_title("Unified Field: Note the Cancellation Bands")
fig.colorbar(im2, ax=axes[2])

plt.tight_layout()
plt.show()

"""
What this represents in your Theory:
The "Sea": 
The X and Y meshgrid represents the fluid medium of space.

The Cancellation Bands: 
In the third plot (Unified Field), you will see dark lines radiating outward. 
These are the locations where the energy from Source A and Source B is "Locked" or canceled out.

Energy Density: 
The bright areas (yellow/white in the 'magma' map) represent "Free Energy" or visible light/vibration.

The Dark Areas: The dark bands represent "Dark Energy" or the locked potential that we can't see but is still there. 
This is your Magnetism.
"""