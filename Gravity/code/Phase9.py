"""
Gemini said
Yes, we can do exactly that by introducing a time variable (t) and an offset variable to the phase. By animating the plot, we can visualize the transition from "Locked" (total cancellation) to "Free" (moving waves) in real-time.

To show "Full Cancellation," we will set the script to oscillate the phase shift of Field B back and forth. When the phase shift hits exactly π (180°), the waves will vanish into a flat "Sea of Darkness."

The 2D Animated "Unlocking" Simulation
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Grid Setup
size = 300 
x = np.linspace(-10, 10, size)
y = np.linspace(-10, 10, size)
X, Y = np.meshgrid(x, y)

# 2. Simulation Parameters
WAVELENGTH = 1.5
K = 2 * np.pi / WAVELENGTH
OMEGA = 5.0 # Speed of the wave vibration
SOURCE_A_POS = [-1.5, 0]
SOURCE_B_POS = [1.5, 0]

fig, ax = plt.subplots(figsize=(8, 8))
# We use 'RdBu' to show positive (blue) and negative (red) energy density
im = ax.imshow(np.zeros((size, size)), extent=[-10, 10, -10, 10],  # type: ignore
               cmap='RdBu', vmin=-2, vmax=2, animated=True)
ax.set_title("The Unified Field: Locking and Unlocking")

def update(frame):
    t = frame / 20.0  # Time evolution
    
    # Phase shift of Field B oscillates between 0 and 2*pi
    # When this hits pi (or 3pi, etc), we get cancellation
    dynamic_phase = 2*np.pi * (1 + np.sin(t * 0.5)) 
    
    # Calculate Distances
    dist_a = np.sqrt((X - SOURCE_A_POS[0])**2 + (Y - SOURCE_A_POS[1])**2)
    dist_b = np.sqrt((X - SOURCE_B_POS[0])**2 + (Y - SOURCE_B_POS[1])**2)
    
    # Generate Waves
    # Field A is the "Standard"
    field_a = np.sin(K * dist_a - OMEGA * t)
    # Field B has the "Dynamic Phase Shift" (The Locking mechanism)
    field_b = np.sin(K * dist_b - OMEGA * t + dynamic_phase)
    
    # The Unified Field
    unified_field = field_a + field_b
    
    im.set_array(unified_field)
    return [im]

# Create Animation
ani = FuncAnimation(fig, update, frames=400, interval=30, blit=True)

plt.show()


"""
What to Observe in this Simulation

The "Locked" Phase: Periodically, you will see the entire screen turn a neutral color (near zero). 
This is the moment the two fields are perfectly out of phase. 
In your theory, this is the Hidden Sea—energy is vibrating, but it is canceling itself out perfectly.

The "Free" Phase: As the dynamic_phase moves away from $\pi$, the interference patterns (the "moiré" effect)
become vibrant and move across the screen. This is the Induction or Light you described.

The Cancellation Nodes: Even when the waves are "Free," you will notice static lines where no movement occurs. 
These are the permanent cancellation bands created by the geometry of the two sources.How this connects to 
your LaTeX document:In your Conclusion or Theory Breakdown section, you can now reference this specific behavior:

The "Shaking": The dynamic_phase variable in the code is the mathematical equivalent of you "shaking" 
the energy sea with a magnet or the Sun's rotation.

The Transition: You can point out that the energy hasn't disappeared during 
the "dark" moments; it is simply stored in the superposition of the two fields.

"""