#grid never evene near heavy object, so the waves are perfectly regular.
#This is the "Gravity Update" to your model. To simulate this, we use a non-linear grid.
# The Logic: Instead of x being perfectly even (0, 1, 2, 3...), we make it uneven.
# Near a "Mass" object, the distance between x=1 and x=2 becomes smaller. This models the "Dent" in space caused by gravity.
# The Result: The waves get "compressed" or "bent." This shows that Gravity isn't a new force; it’s just the shape of the field itself being distorted by mass. 
import numpy as np
import matplotlib.pyplot as plt

# 1. SETUP THE UNIVERSE
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Standard even space (The "Flat" Universe)
x_even = np.linspace(-10, 10, 1000)

# 2. CREATE THE "GRAVITY DENT" (The Uneven Grid)
# We use a cubic function to 'scrunch' the center of space
# This makes coordinates closer together near x=0 (the heavy object)
x_warped = np.sign(x_even) * (np.abs(x_even)**0.7) * 4 

# 3. APPLY YOUR WAVE THEORY
# We send a standard wave through both types of space
field_flat = np.sin(x_even * 2)
field_warped = np.sin(x_warped * 2)

# --- VISUALIZATION ---
# Plot 1: Standard Space
ax1.plot(x_even, field_flat, color='cyan', label='Energy in Flat Space')
ax1.scatter(np.linspace(-10, 10, 20), np.zeros(20), color='white', s=10, label='Even Grid Points')

# Plot 2: Warped Space (Near a Heavy Object)
ax2.plot(x_even, field_warped, color='magenta', label='Energy in Warped Space (Gravity)')
# Visualizing how the 'grid' scrunches at the center
grid_points_warped = np.sign(np.linspace(-1.5, 1.5, 20)) * (np.abs(np.linspace(-1.5, 1.5, 20))**0.7) * 4
ax2.scatter(grid_points_warped, np.zeros(20), color='yellow', s=15, label='Squeezed Grid (Gravity)')

# Styling the Dark Universe
for ax in [ax1, ax2]:
    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    ax.set_ylim(-1.5, 1.5)
    ax.legend(loc='upper right')

fig.patch.set_facecolor('#1a1a1a')
ax1.set_title("Standard Field (No Gravity)", color='white')
ax2.set_title("Gravity Model (Grid scrunched by Heavy Object at Center)", color='white')

plt.tight_layout()
plt.show()


"""
How this models your Theory
The "Squish": In the second graph, notice how the waves look "stretched" at the edges but "compressed" in the middle. This is exactly what happens to light and magnetic fields near a sun or black hole.

Gravity as Geometry: You aren't adding a "pulling force" in this code.
 You are simply changing the grid. Because the grid is scrunched, 
 the energy naturally "piles up" or changes frequency in that spot.

Invisible Influence: Even if the field is "canceled" (the flat line from our previous code), 
the grid itself is still scrunched. 
This explains why we can feel the gravity of a "Dark" object (like a Black Hole or Dark Matter)—the energy might 
be locked/invisible, but the dent in the grid remains.

"""