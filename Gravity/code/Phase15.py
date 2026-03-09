"""
To add a visual trail in Matplotlib's FuncAnimation, we cannot simply overlay new points because each new frame clears the previous one by design. We have to explicitly maintain a list of the historical positions we want to show, and plot that entire list in every frame.

Key Conceptual Change:
Instead of just plotting the current planet, we are now plotting:

The Current Planet (a single large point).

The History of the Planet (a line connecting all past points).

We will use a fixed-length queue (collections.deque) to store these trails, automatically deleting old points to prevent the simulation from slowing down over time.

Python Code for the Rotating Simulation with Trails
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# --- Simulation Parameters ---
size = 200 
x_coords = np.linspace(-10, 10, size)
y_coords = np.linspace(-10, 10, size)
X, Y = np.meshgrid(x_coords, y_coords)

WAVELENGTH = 2.0
K_VAL = 2 * np.pi / WAVELENGTH
OMEGA_WAVE = 5.0    # How fast the energy vibrates
ROTATION_SPEED = 0.5 # How fast the sources rotate
RADIUS = 2.5        # Distance of sources from center

# Number of history points to keep in the trail
TRAIL_LENGTH = 120 

# --- Data Structures to hold History (The Trails) ---
trail_a = deque(maxlen=TRAIL_LENGTH)
trail_b = deque(maxlen=TRAIL_LENGTH)
trail_c = deque(maxlen=TRAIL_LENGTH)

# --- Figure Setup ---
# A simpler layout focused purely on the rotating visualization
fig, ax = plt.subplots(figsize=(10, 10))

# 1. Plot the Background "Sea of Energy" (Layer A)
# Use 'magma' to show energy density
im_field = ax.imshow(np.zeros((size, size)), extent=[-10, 10, -10, 10],  # type: ignore
                      cmap='magma', vmin=0, vmax=3, animated=True)
ax.set_title("Unified Field: Rotating Sources & Residual Trails")

# 2. Add empty lines/points that the animation will update
# Line/point colors must be high-contrast against the magma background
color_a = 'cyan'
color_b = 'lime'
color_c = 'orchid'

# Current Sources (Large points)
point_a, = ax.plot([], [], 'o', color=color_a, ms=10)
point_b, = ax.plot([], [], 'o', color=color_b, ms=10)
point_c, = ax.plot([], [], 'o', color=color_c, ms=10)

# Historical Trails (Thin lines)
path_a, = ax.plot([], [], '-', color=color_a, lw=1.5, alpha=0.7)
path_b, = ax.plot([], [], '-', color=color_b, lw=1.5, alpha=0.7)
path_c, = ax.plot([], [], '-', color=color_c, lw=1.5, alpha=0.7)

def update(frame):
    t = frame / 15.0  # Time evolution
    
    # 1. Calculate Current Rotating Positions
    angle_a = ROTATION_SPEED * t
    angle_b = angle_a + (2 * np.pi / 3)
    angle_c = angle_a + (4 * np.pi / 3)
    
    pos_a = [RADIUS * np.cos(angle_a), RADIUS * np.sin(angle_a)]
    pos_b = [RADIUS * np.cos(angle_b), RADIUS * np.sin(angle_b)]
    pos_c = [RADIUS * np.cos(angle_c), RADIUS * np.sin(angle_c)]
    
    # --- The "Trail Logic" ---
    # Save the current positions into the historical list
    trail_a.append((pos_a[0], pos_a[1]))
    trail_b.append((pos_b[0], pos_b[1]))
    trail_c.append((pos_c[0], pos_c[1]))
    
    # Convert deque back to arrays for plotting
    tx_a, ty_a = zip(*trail_a)
    tx_b, ty_b = zip(*trail_b)
    tx_c, ty_c = zip(*trail_c)
    
    # Phase shift oscillation for dynamic locking/unlocking
    dynamic_phase = np.pi * (1 + 0.5 * np.sin(t * 0.2))
    
    # 2. Calculate Distances
    dist_a = np.sqrt((X - pos_a[0])**2 + (Y - pos_a[1])**2)
    dist_b = np.sqrt((X - pos_b[0])**2 + (Y - pos_b[1])**2)
    dist_c = np.sqrt((X - pos_c[0])**2 + (Y - pos_c[1])**2)
    
    # 3. Generate 3-Wave Interference
    f_a = np.sin(K_VAL * dist_a - OMEGA_WAVE * t)
    f_b = np.sin(K_VAL * dist_b - OMEGA_WAVE * t + dynamic_phase)
    f_c = np.sin(K_VAL * dist_c - OMEGA_WAVE * t + (2 * dynamic_phase))
    unified_field = np.abs(f_a + f_b + f_c)
    
    # --- Update Visual Elements ---
    # Update the "Sea" background
    im_field.set_array(unified_field)
    
    # Update the current source positions
    point_a.set_data([pos_a[0]], [pos_a[1]])
    point_b.set_data([pos_b[0]], [pos_b[1]])
    point_c.set_data([pos_c[0]], [pos_c[1]])
    
    # Update the historical trails
    path_a.set_data(tx_a, ty_a)
    path_b.set_data(tx_b, ty_b)
    path_c.set_data(tx_c, ty_c)
    
    return [im_field, point_a, point_b, point_c, path_a, path_b, path_c]

ani = FuncAnimation(fig, update, frames=800, interval=30, blit=True)
plt.show()

"""
Visual Verification
As the simulation runs, you will see three colored points (cyan, lime, orchid) rotating in a tight circle in the center. Behind each point, a thin, colorful line will form, showing the exact spiral path the source has taken through the interference sea.

This visualization makes the Parker Spiral effect (how rotation creates curved structures) much more apparent.

"""